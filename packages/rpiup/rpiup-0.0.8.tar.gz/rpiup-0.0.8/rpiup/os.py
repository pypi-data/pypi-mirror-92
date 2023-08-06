import os
import re
import yaml
from . import util


def url(version=None, official=False, repo='nmcclain/raspberian-firstboot'):
    if official:
        if version:
            # https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2020-12-04/2020-12-02-raspios-buster-armhf-lite.zip
            download_url = 'https://downloads.raspberrypi.org/raspios_lite_armhf/images/{}.zip'.format(version)
        else:
            download_url = 'https://downloads.raspberrypi.org/raspios_lite_armhf_latest'
            version = get_file_download_name(url)
    else:
        import urllib.request
        if version:
            download_url = 'https://s3.amazonaws.com/devicecfg.newmoon.io/images/raspbian-lite-firstboot/{}.zip'.format(version)
        else:
            url = 'https://api.github.com/repos/{}/releases/latest'.format(repo)
            with urllib.request.urlopen(url) as response:
                pkg_info = yaml.safe_load(response)
            print('*** Found latest: ***')
            print(pkg_info['body'])
            print('*' * 20, '\n')

            matches = re.search(r'\[\w*\s*([^\]]+)\.img]\(([^\)]+)\)', pkg_info['body'])
            version, download_url = matches.groups()
    return download_url, version

def download(output_path='.', *a, **kw):
    '''Download the latest version.'''
    # get download url
    download_url, version = url(*a, **kw)
    print('Downloading Release from {}'.format(download_url))
    util.download_file(download_url, output_path, name='{}.zip'.format(version))


# def flash(img_fname):
#     pass
