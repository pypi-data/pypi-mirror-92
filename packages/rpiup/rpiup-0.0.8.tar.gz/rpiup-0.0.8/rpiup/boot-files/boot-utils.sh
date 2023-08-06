# setup, load variables
export BOOT_VARS_FILE='/boot/resources/vars.sh'
. $BOOT_VARS_FILE


# Add a variable to /boot/resources/vars.sh
# $ bootvars.add NAME bea
bootvars.add() {
    lineinfile.match "^export $1" "export $1=$2" "$BOOT_VARS_FILE"
}


# Remove a variable from /boot/resources/vars.sh
# $ bootvars.remove NAME
bootvars.remove() {
    sed -i '/^export '"$1"'=/d' "$BOOT_VARS_FILE"
}



# print section header
# echo.section this is my header
echo.section() {
    echo
    echo '****************************'
    echo ${@}
    echo '****************************'
    echo
}


# copy a file, but make a backup of an existing file
# $ cp.backup values.conf /etc/app/values.conf
cp.backup() {
    if [ -f "$1" ]; then
        [ -f "$2" ] && mv "$2" "${2}.old"
        DIR=$(dirname $(readlink -m "$2"))
        [ ! -z $DIR ] && mkdir -p "$DIR"
        cp "$1" "$2"
    fi
}


# run a file if it exists
# $ exec.maybe ./myscript.sh
exec.maybe() {
    if [ -f $1 ]; then chmod +x $1; $@;fi
}

exec.maybe.flag() {
    [ -f "$1" ] && rm "$1" && ${@:2}
}


# get a list of files matching
find.matching() {
    false; for f in $1; do [[ -e "$f" ]] && echo "$f"; done
}


# Make sure that a line is in a file
# $ lineinfile.match '^export BLAH=' 'export BLAH=123' ~/.bashrc
lineinfile.match() {
    [ ! -f "$3" ] && mkdir -p "$(dirname $3)" touch "$3"
    sed -i -n -e '/'"$1"'/!p' -e '$a'"$2" "$3"
}


# Make sure that a line is in a file
# $ lineinfile 'export BLAH=123' ~/.bashrc
lineinfile() {
    lineinfile.match "$1" "$1" "$2"
}






STATUSDIR=/boot/.firstboot-status
mkdir -p "$STATUSDIR"

# touch a file to show how far we got
# $ status.update step1
# $ status.update step2
status.update() {
    for i in {000..100}; do
        FNAME="$STATUSDIR/$i-$1"
        if [ -f $FNAME ] || [ -z "$(status.list '*' "$i")" ]; then
            # echo $FNAME
            touch $FNAME
            echo "$FNAME $(date)" >> "$STATUSDIR/times"
            status.upload "$1" "$2"
            break
        fi
    done
}

# get any status files matching that name
# $ [[ $(status.list step1) ]] && echo y || echo n
status.list() {
    name=${2:-*}-${1:-*}
    [ -d "$STATUSDIR" ] && find.matching "$STATUSDIR/$name"
}


# clear any status files matching that name
# $ status.clear step1
status.clear() {
    [ $(status.list) ] && rm "$STATUSDIR/*" || true
}


# clear any status files matching that name
# $ status.clear step1
status.upload() {
    if [ ! -z "$MONITOR_HOST" ] && [ ! -z "$UUID" ]; then
        URL="http://$MONITOR_HOST/update/$UUID/$1?$2"
        echo "$URL" && curl "$URL" || (echo "calling monitor server failed: $URL" && false)
    fi
}




# get your local IP address (e.g. 192.168.1.54)
# $ localip
localip() {
    _localip wlan1 || _localip wlan0 || _localip eth0
}
_localip() {
    regex="inet ([0-9.]+)" && [[ $(ifconfig ${1:-wlan0}) =~ $regex ]] && echo ${BASH_REMATCH[1]}
}



# raspi-config

# raspi-config nonint do_hostname %s
# raspi-config nonint do_boot_behaviour B1 (or: B2 B3 B4)
# raspi-config nonint do_boot_wait %d
# raspi-config nonint do_boot_splash %d

# raspi-config nonint do_camera %d
# raspi-config nonint do_ssh %d
# raspi-config nonint do_vnc %d
# raspi-config nonint do_spi %d
# raspi-config nonint do_i2c %d
# raspi-config nonint do_serial %d
# raspi-config nonint do_onewire %d
# raspi-config nonint do_rgpio %d

# raspi-config nonint do_overscan %d
# raspi-config nonint do_overclock %s
# raspi-config nonint do_expand_rootfs
# raspi-config nonint do_memory_split %d
# raspi-config nonint do_resolution %d %d
# raspi-config nonint do_wifi_country %s

# raspi-config nonint get_can_expand
# raspi-config nonint get_hostname
# raspi-config nonint get_boot_cli
# raspi-config nonint get_autologin
# raspi-config nonint get_boot_wait
# raspi-config nonint get_boot_splash
# raspi-config nonint get_overscan
# raspi-config nonint get_camera
# raspi-config nonint get_ssh
# raspi-config nonint get_vnc
# raspi-config nonint get_spi
# raspi-config nonint get_i2c
# raspi-config nonint get_serial
# raspi-config nonint get_serial_hw
# raspi-config nonint get_onewire
# raspi-config nonint get_rgpio
# raspi-config nonint get_pi_type
# raspi-config nonint get_wifi_country
# raspi-config nonint get_config_var arm_freq /boot/config.txt
# raspi-config nonint get_config_var gpu_mem /boot/config.txt
# raspi-config nonint get_config_var gpu_mem_256 /boot/config.txt
# raspi-config nonint get_config_var gpu_mem_512 /boot/config.txt
# raspi-config nonint get_config_var gpu_mem_1024 /boot/config.txt
# raspi-config nonint get_config_var hdmi_group /boot/config.txt
# raspi-config nonint get_config_var hdmi_mode /boot/config.txt
