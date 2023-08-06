#!/bin/bash

# THIS STARTS AN ANONYMOUS FUNCTION TO REDIRECT ALL OUTPUT TO FILE
{
# ----------------------------------------------------------------

# expand empty glob to empty string, not original pattern
shopt -s nullglob

UTILS_FILE='/boot/boot-utils.sh'
. $UTILS_FILE
echo ". $UTILS_FILE" >> /etc/profile.d/firstboot.sh


# if we've already finished, exit.

if [ "$(status.list done)" ]; then
    [ -f /boot/firstboot.sh ] && mv /boot/firstboot.sh /boot/firstboot.sh.done
    exit 0;
fi

########################################
# Setup
########################################

# create a general workspace
mkdir -p /etc/firstboot
cd /etc/firstboot

status.update start ip=$(localip)


# make sure the date is right

if [ -z "$(status.list correct-time)" ]; then
    date -s "$(wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-8)Z"
    status.update correct-time
fi


# run custom setup

if [ -z "$(status.list setup-before)" ]; then
    exec.maybe /boot/resources/setup-before.sh
    status.update setup-before
fi

for f in /boot/resources/.internal/pre-scripts/*.sh; do
    _id=$(basename "${f%.*}")
    if [ -z "$(status.list addon-pre-$_id)" ]; then
        exec.maybe "$f"
        status.update addon-pre-$_id
    fi
done


# create user

if [ -z "$(status.list update-user)" ]; then
    echo.section "Setting user to $USERNAME:$PASSWORD ..."
    if [ ! -z "$USERNAME" ] && [ ! -d "/home/$USERNAME" ]; then
        adduser --disabled-password --gecos '' $USERNAME
        usermod -aG "$(id -Gn pi | sed -e 's/ /,/g')" $USERNAME
        passwd --lock pi
        echo "Current user: $USER"
    fi

    export HOME="/home/${USERNAME:-pi}"

    if [ ! -z "$PASSWORD" ]; then
        yes "$PASSWORD" | passwd "${USERNAME:-pi}"
        bootvars.remove PASSWORD
    fi

    status.update update-user
fi


# set hostname

if [ -z "$(status.list hostname)" ]; then

    FIRSTBOOT_HOSTNAME=${FIRSTBOOT_HOSTNAME:-firstboot_hostname}  # deprecate old
    if [ -z "$FIRSTBOOT_HOSTNAME" ]; then
        MAC=$(cat /sys/class/net/eth0/address | sed 's/://g')
        HOSTNAME_PREFIX="${HOSTNAME_PREFIX:-${APP_NAME}node}"
        FIRSTBOOT_HOSTNAME="${HOSTNAME_PREFIX}-${MAC}"
    fi

    echo.section "Setting hostname to $FIRSTBOOT_HOSTNAME ..."

    CURRENT_HOSTNAME=$(hostname)
    echo "$FIRSTBOOT_HOSTNAME" > /etc/hostname
    sed -i "s/$CURRENT_HOSTNAME/$FIRSTBOOT_HOSTNAME/g" /etc/hosts
    hostname "$FIRSTBOOT_HOSTNAME"

    status.update hostname
fi


# set raspi-config defaults (0=yes, 1=no ??idk why)

#define CHANGE_PASSWD   "(echo \"%s\" ; echo \"%s\" ; echo \"%s\") | passwd"
if [ -z "$(status.list system-config)" ]; then
    # set country - TODO will country/keyboard be the same ???
    COUNTRY=${COUNTRY:-US}
    KEYBOARD=$(echo ${KEYBOARD:-$COUNTRY} | awk '{print tolower($0)}')
    raspi-config nonint do_wifi_country $COUNTRY
    raspi-config nonint do_configure_keyboard $KEYBOARD

    echo "ClientAliveInterval 30" >> /etc/ssh/sshd_config

    # set network interfaces
    cp.backup /boot/resources/network_interfaces /etc/network/interfaces
    # set fstab
    cp.backup /boot/resources/fstab /etc/fstab

    status.update system-config
fi


# installs

if [ -z "$(status.list installs)" ]; then
    echo.section "Installing core packages..."
    apt-get update

    # # set timezone
    apt-get install -y jq && \
        timedatectl set-timezone "$(curl -s http://ip-api.com/json/$(curl -s ifconfig.me) | jq -r .timezone 2>&1)"

    apt-get install -y git htop wavemon

    # github
    if [ ! -z "$GIT_USERNAME" ]; then
        git config --global user.name "$GIT_USERNAME"
    fi
    if [ ! -z "$GIT_PASSWORD" ]; then
        git config --global user.password "$GIT_PASSWORD"
        bootvars.remove GIT_PASSWORD
    fi

    status.update installs
fi


# openvpn

if [ -z "$(status.list vpn)" ]; then

    VPNDIR=/boot/resources/vpn
    exec.maybe "$VPNDIR/setup.sh"

    if [ ! -z $(find.matching $VPNDIR'/*.conf') ]; then
        echo.section "Installing openvpn client..."

        apt-get install -y openvpn
        sudo systemctl daemon-reload

        lineinfile.match '^\s*AUTOSTART=' 'AUTOSTART="all"' /etc/default/openvpn

        for f in $VPNDIR"/*.conf"; do
            _id=$(basename "${f%.*}")  # get file base stem
            mv "$f" /etc/openvpn/${_id}.conf
            sudo systemctl restart openvpn@${_id} && systemctl enable openvpn@${_id}
        done
        status.update vpn
    fi
fi


# install python 3 and make it the default

if [ -z "$(status.list install-python)" ]; then
    echo.section "Installing Python 3..."

    apt-get install -y python3 python3-pip
    update-alternatives --install /usr/bin/python python /usr/bin/python3 4
    update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 4
    pip install -U pip setuptools

    status.update install-python
fi

# raspi-config

if [ -z "$(status.list raspi-config)" ]; then
    raspi-config nonint do_boot_wait 1
    raspi-config nonint do_i2c 0
    raspi-config nonint do_serial 0
    if [ -f /boot/i2smic ]; then
        pip install --upgrade adafruit-python-shell
        curl -sSL https://raw.githubusercontent.com/beasteers/Raspberry-Pi-Installer-Scripts/i2smic-nonint-patch-1/i2smic.py -o i2smic.py
        python i2smic.py -autoload -noreboot
    fi
    status.update raspi-config
fi


# set splash image

if [ -f /boot/resources/splash.png ]; then
    if [ -z "$(status.list splash)" ]; then
        echo.section "Installing splash image..."
        apt-get install -y fbi
        # cp.backup /boot/resources/splash.png /usr/share/plymouth/themes/pix/splash.png
        cp.backup /boot/resources/.internal/splashscreen.service /etc/systemd/system/splashscreen.service
        systemctl enable splashscreen
        # systemctl start splashscreen
        raspi-config nonint do_boot_splash 0
        status.update splash
    fi
fi


# upgrade wifi device

if [ -z "$(status.list wifi-drivers)" ]; then
    # # available: 8188eu|8188fu|8192eu|8192su|8812au|8821cu|8822bu|mt7610|mt7612
    # DEFAULT_INSTALL_WIFI=("8188eu" "8192eu" "8812au")
    # INSTALL_WIFI=("${INSTALL_WIFI[@]:-${DEFAULT_INSTALL_WIFI[@]}}")

    if [ ! -z $INSTALL_WIFI ]; then
        echo.section "Installing wifi devices..."
        apt-get install -y firmware-ralink

        wget http://downloads.fars-robotics.net/wifi-drivers/install-wifi -O /usr/bin/install-wifi
        chmod +x /usr/bin/install-wifi
        for wifiid in "${INSTALL_WIFI[@]}"; do
            install-wifi -u "$wifiid"
        done

        status.update wifi-drivers
    fi
fi


# install docker, docker-compose

if [ -z "$(status.list docker)" ]; then
    echo.section "Installing docker..."

    if [ $BALENA_ENGINE -eq 1 ]; then
        _balen_url='https://gist.githubusercontent.com/beasteers/5a2b69e0b486d57039a52f5ee205cea8/raw/balena-engine-install.sh'
        curl -sSL $_balen_url | sh
    else
        curl -sSL https://get.docker.com | sh
    fi

    # install docker-compose
    [ ! -z $USERNAME ] && usermod -aG docker $USERNAME
    /usr/bin/python3 -m pip install docker-compose
    systemctl restart docker

    status.update docker
fi


# install systemctl services

if [ -z "$(status.list systemctl-services)" ]; then
    echo.section "Installing any systemctl services..."

    CWD=$(pwd)
    for svc_dir in /boot/resources/services/*; do
        [ -d "$svc_dir" ] && cd "$svc_dir" || continue
        [ -f "./setup.sh" ] && (./setup.sh || continue)

        # start
        svc_name=$(basename "$svc_dir")
        f=${svc_name}.service
        [ -f "$f" ] && (cp "$f" "/etc/systemd/system/$f" || continue)

        echo "starting service "$svc_name" and setting to run on boot..."
        systemctl start "$svc_name" && systemctl enable "$svc_name"
        echo 'done.'
        sleep 1
        systemctl status "$svc_name"
    done
    cd "$CWD"

    status.update systemctl-services
fi


# install docker containers

if [ -z "$(status.list docker-compose)" ]; then
    echo.section "Installing any docker containers..."

    CWD=$(pwd)
    for svc_dir in /boot/resources/docker/*; do
        [ -d "$svc_dir" ] && cd "$svc_dir" || continue
        [ -f "./setup.sh" ] && (./setup.sh || continue)
        docker-compose up -d
    done
    cd "$CWD"

    status.update docker-compose
fi


# run custom setup

for f in /boot/resources/.internal/scripts/*.sh; do
    _id=$(basename "${f%.*}")
    if [ -z "$(status.list addon-$_id)" ]; then
        exec.maybe "$f"
        status.update addon-$_id
    fi
done

if [ -z "$(status.list custom-setup)" ]; then
    exec.maybe /boot/resources/setup.sh
    status.update custom-setup
fi


# close up

echo.section "Done! Enjoy!! Don't be evil. **Do** topple capitalism. :D"
status.update "done"

# sleep 5
# reboot


# THIS CREATES AN ANONYMOUS FUNCTION TO REDIRECT ALL OUTPUT TO FILE
} &> /var/log/firstboot.log
# -----------------------------------------------------------------
