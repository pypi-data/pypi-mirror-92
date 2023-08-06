import os
import re
import subprocess


DEFAULT_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), 'boot-files'))


def count(start=0, end=None, step=1):
    i = start or 0
    while True:
        yield i
        i += step
        if end and i >= end:
            break

def touch(fname, text=None, time=None):
    with open(fname, 'w') as f:
        os.utime(fname, time)
        if text:
            f.write(str(text))


def getinput(msg='', secret=False):
    if secret:
        import getpass
        return getpass.getpass(msg)
    return input(msg)


def download_file(url, output_path='.', name=None, overwrite=False):
    import urllib.request

    filename = None
    if output_path:
        output_path = os.path.expanduser(output_path)
        os.makedirs(output_path, exist_ok=True)
        filename = os.path.join(output_path, name or get_file_download_name(url))

        # check if the file already exists
        if not overwrite and os.path.isfile(filename):
            redownload = input(
                'It looks like this image is already downloaded at {}.'
                'Do you wish to redownload? y[N]  '.format(filename)
            ).lower().startswith('y')
            if not redownload:
                print('Okie! Not re-downloading. Have a nice day!')
                return
        print('Writing to {}'.format(filename))

    import tqdm
    class DownloadProgressBar(tqdm.tqdm):
        def update_to(self, b=1, bsize=1, tsize=None):
            if tsize is not None:
                self.total = tsize
            self.update(b * bsize - self.n)

    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1,
                             desc=filename or url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=filename, reporthook=t.update_to)


def get_file_download_name(url):
    import urllib.request
    import cgi
    header = urllib.request.urlopen(url).info()['Content-Disposition']
    return cgi.parse_header(header)[0]["filename"]



def check_json_response(url):
    import json
    import urllib.request
    try:
        with urllib.request.urlopen(url) as response:
            return json.loads(response.read())
    except urllib.error.URLError:
        pass
    return


def localip(n=1):
    out = subprocess.check_output('ifconfig').decode()
    match = set(re.findall(r'inet ([\d.]+)', out))
    return max((
        (i, ip) for i, ip in
        ((max_common_prefix('192.168.1'.split('.'), ip.split('.')), ip)
         for ip in match)
        if i >= n
    ))[1]


def max_common_prefix(*strs):
    return next(
        (i for i, chs in enumerate(zip(*strs)) if len(set(chs)) > 1),
        min(len(s) for s in strs))



def copytree(src, dst, symlinks=False, ignore=None, overwrite=None):
    '''Copies, but won't overwrite if a newer file exists.'''
    import shutil
    if not os.path.exists(dst):
        os.makedirs(dst)
        shutil.copystat(src, dst)
    for item in listdir(src, ignore=ignore):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if symlinks and os.path.islink(s):
            _copyslink(s, d)
        elif os.path.isdir(s):
            copytree(s, d, symlinks, ignore, overwrite=overwrite)
        elif (overwrite is True or not os.path.exists(d) or
              not overwrite is False and os.stat(s).st_mtime - os.stat(d).st_mtime > 1):
            shutil.copy(s, d)

def _copyslink(s, d):
    import stat
    if os.path.lexists(d):
        os.remove(d)
    os.symlink(os.readlink(s), d)
    try:
        os.lchmod(d, stat.S_IMODE(os.lstat(s).st_mode))
    except Exception:
        pass # lchmod not available

def listdir(src, ignore=None):
    lst = os.listdir(src)
    if ignore:
        excl = set(ignore(src, lst))
        lst = [x for x in lst if x not in excl]
    return lst

def file_tree(path, ignore=None):
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        print('{}{}/'.format(' ' * 4 * (level), os.path.basename(root)))
        for f in files:
            if ignore and f in ignore:
                continue
            print('{}{}'.format(' ' * 4 * (level + 1), f))

def file_content(path):
    with open(path, 'r') as f:
        return f.read()


def copydiff(output_path='./diff', path='.', ref=DEFAULT_SRC, test=False):
    '''Copy only files that are different.'''
    import shutil
    import filecmp
    filecmp.DEFAULT_IGNORES.append('.DS_Store')

    class dircmp2(filecmp.dircmp):
        def phase3(self): # Find out differences between common files
            self.same_files, self.diff_files, self.funny_files = filecmp.cmpfiles(
                self.left, self.right, self.common_files, shallow=False)

    def get_diff_files(dcmp):
        for name in dcmp.diff_files:
            print("diff_file %s found in %s and %s" % (name, dcmp.left, dcmp.right))
            yield os.path.join(dcmp.left, name)

        for name in dcmp.left_only:
            print("left_only %s found in %s but not %s" % (name, dcmp.left, dcmp.right))
            yield os.path.join(dcmp.left, name)

        for sub_dcmp in dcmp.subdirs.values():
            yield from get_diff_files(sub_dcmp)

    # move files
    ignore = filecmp.DEFAULT_IGNORES + [os.path.abspath(p) for p in (output_path, path, ref)] + ['ssh', 'wpa_supplicant.conf']
    for f in get_diff_files(dircmp2(path, ref, ignore=ignore)):
        if not os.path.isdir(f):
            outf = os.path.join(output_path, os.path.relpath(f, path))
            print('copying', f, 'to', outf)
            if not test:
                os.makedirs(os.path.dirname(outf), exist_ok=True)
                shutil.copy2(f, outf)
        print()
