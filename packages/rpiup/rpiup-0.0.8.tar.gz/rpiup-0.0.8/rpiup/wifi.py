import os
import glob
import shutil


WIFI_CACHE = os.path.expanduser('~/.rpiup/wifi')


def add(ssid=None, password=None, path='.', default=False, country='US', remember=False):
    print('*** Setting up Wifi Credentials: ***')

    # check for saved wifi

    if not ssid and remember is not False and os.path.isfile(WIFI_CACHE):
        try:  # TODO: protect this file better
            with open(WIFI_CACHE, 'r') as f:
                ssid_cache = f.readline().strip()
                password_cache = f.readline().strip()

            use = input((
                'Would you like to use your previously saved credentials?'
                '\n  ssid: "{}" password: {}'
                '? ([y]/n) '
            ).format(ssid_cache, "*"*len(password_cache))).lower()  in {'y', ''}
            print()
            if use:
                remember, ssid, password = True, ssid_cache, password_cache
        except Exception as e:
            print(f'Error reading cached password. ({type(e).__name__}) {e}')

    # get ssid and password

    if not ssid:
        ssid = input('Enter the wifi ssid: ')
    if not ssid:
        print('No ssid specified.')
        return

    if ssid and not password:
        import getpass
        password = getpass.getpass('Enter the wifi password: ')

    # setup wifi file
    fname = os.path.join(path, 'resources/aps/{}.conf'.format(ssid))
    default_fname = os.path.join(path, 'wpa_supplicant.conf')

    if password:
        # custom ssid and password
        print('Creating wpa_supplicant file for ssid:', ssid)
        write_cfg(fname, ssid=ssid, psk=password, country=country)
    # elif os.path.isfile(fname):
    #     print('ssid exists:', fname)
    else:
        print('Creating unsecured network configuration for ssid:', ssid)
        write_cfg(fname, ssid=ssid, key_mgmt='NONE', country=country)

    if default or not os.path.isfile(default_fname):
        shutil.copyfile(fname, default_fname)

    # maybe save wifi

    if remember is None:
        remember = input(
            'Would you like to save the password for next time? ([y]/n) '
        ).lower() in {'y', ''}
        print()

    if remember is not False:
        os.makedirs(os.path.dirname(WIFI_CACHE), exist_ok=True)
        with open(WIFI_CACHE, 'w') as f:
            f.write(f'{ssid}\n')
            f.write(f'{password}\n')
        print(f'Credentials cached to {WIFI_CACHE}.')
    print()

    print('*** Done! :) ***')
    print()

    print('To check that your wifi credentials look correct, run:', '\n  ',
          f'less {fname}')


def aps_from(dir, app_path='.'):
    for f in glob.glob(os.path.join(dir, '*')):
        shutil.copyfile(f, os.path.join(app_path, 'resources', os.path.basename(f)))


def clear_cache():
    if os.path.isfile(WIFI_CACHE):
        os.remove(WIFI_CACHE)
    print('{} removed ({}).'.format(WIFI_CACHE, not os.path.isfile(WIFI_CACHE)))


def touch(fname, text=None, time=None):
    with open(fname, 'w') as f:
        os.utime(fname, time)
        if text:
            f.write(str(text))


def format_cfg(country='US', **kw):
    return WPA_SUPPLICANT_TPL.format(country=country, params='\n'.join([
        '\t{}="{}"'.format(k, v) for k, v in kw.items()
    ]))

def write_cfg(fname, **kw):
    with open(fname, 'w') as f:
        f.write(format_cfg(**kw))


WPA_SUPPLICANT_TPL = '''
ctrl_interface=/var/run/wpa_supplicant
update_config=1
country={country}

network={{
{params}
}}
'''.strip()

if __name__ == '__main__':
    import fire
    fire.Fire(add)
