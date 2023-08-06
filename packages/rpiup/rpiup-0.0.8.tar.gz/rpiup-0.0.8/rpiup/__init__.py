''''''
# generate certificate
# generate wifi
import os as os_
from . import util
from . import os
from . import sd
from . import varsfile
from . import wifi
from .util import DEFAULT_SRC


DEFAULT_PATH = '.'

def init(name=None, path=None, ssid=None, psk=None, user=None, password=None,
         git_user=None, git_password=None, src=None, ssh=True, boot_script='full-docker'):
    '''Copy over files. Interactive setup?'''
    path = path or name or DEFAULT_PATH
    print('''
****************
rpiup: Initializing Project.

Copying sd boot files to: {path}

After the initial setup, (this command), you can edit the files inside "{path}".

 - setup.sh: this is a script to run arbitrary setup. This is run after the system is setup (Docker is available)
 - vars.sh: this is used to store arbitrary variables that are needed during setup. this can include any
            certificates or passwords.
 - aps.yml: this contains the wpa supplicant information for any wifi networks you want to connect to.
 - services/: where you can store arbitrary services that you want to be installed on first boot.
    - servicename/: each service is stored in its own subdirectory
        - install.sh: used to do any installs, wget, apt-get, cp, mkdir, etc. that you need.
        - servicename.service: this is a systemctl service. ** installation of this file will be handled for you. **
 - docker/: any docker containers that you want to start
    - servicename:
        - docker-compose.yml: the docker-compose file that describes your container.

Now that you've finished the general setup, insert your SD card and flash it using Balena Etcher.


When that's finished run:
```
rpiup sd setup {maybe_path}
```

And then eject the SD card and put it in your pi!
****************

    '''.format(path=path, maybe_path=path if path != DEFAULT_PATH else ''))

    try:
        util.copytree(DEFAULT_SRC, path, overwrite=False)
        if src:
            util.copytree(src, path, overwrite=True)

        # set app name
        name = name or os_.path.basename(os_.path.abspath(path)) or ''
        var = varsfile.Vars(os_.path.join(path, 'resources'))
        if len(var.config):
            print('current variables:', set(var.config), '\n')
        var.prompt('APP_NAME', 'What is the app name?', name)
        var.prompt('USERNAME', 'What should the device username be?', name, user)
        var.prompt('PASSWORD', 'What should the device password be?', '', password, secret=True)

        var.prompt('GIT_USERNAME', 'Do you want to set a git username?', '', git_user)
        var.prompt('GIT_PASSWORD', 'Do you want to set a git password?', '', git_password, secret=True)

        ip = util.localip()
        if ip:
            host = '{}:{}'.format(ip, 8056)
            # if set(util.check_json_response('http://{}'.format(host)) or ()) == {'message'}:
            var.update(MONITOR_HOST=host)

        # set device flags
        sd.flag_file(path, 'ssh', ssh)
        # sd.flag_file(path, 'i2c', var.prompt('Would you like to enable i2c?'))
        # sd.flag_file(path, 'serial', var.prompt('Would you like to enable serial?'))
        # sd.flag_file(path, 'i2s', var.prompt('Would you like to install i2s software?'))
        # sd.flag_file(path, 'vnc', var.prompt('Would you like to enable vnc for remote GUI?'))

        # add default wifi
        wifi.add(ssid, psk, path=path, default=True, remember=None)

        ap_path = var.prompt(
            'AP_PATH', 'Do you have a set of alternate wifi credentials you would like to add?\n  (Read more at https://github.com/beasteers/netswitch) \nWhat is their path?', '', update=False)
        if ap_path:
            util.copytree(ap_path, os_.path.join(path, 'resources/aps/'))

        var.prompt('LIFELINE_SSID', 'Do you have a wifi lifeline?\nNOTE: This is a wifi network that your device will always connect to with the highest priority. This is useful for engineers debugging a sensor in the field.\nWhat is the SSID?', '')

    except KeyboardInterrupt:
        print('Interrupted')


def describe(path=None):
    path = os_.path.abspath(path or DEFAULT_PATH)
    print('**', path, '**')
    util.file_tree(path, ignore={'.DS_Store'})
    print('*'*10, '\n')
    _file_summary(os_.path.join(path, 'resources/vars.sh'))
    _file_summary(os_.path.join(path, 'wpa_supplicant.conf'))


def _file_summary(path):
    print('**', path, '**')
    print(util.file_content(path).strip())
    print('*'*10)
    print()




def cli():
    import fire
    fire.Fire({
        'init': init, 'os': os, 'sd': sd, 'vars': varsfile.Vars,
        'wifi': wifi, 'copydiff': util.copydiff, 'util': util,
        'describe': describe
    })
