import os
import shlex
from . import util

VARS_FNAME = 'vars.sh'

def get_fname(path):
    return path if os.path.isfile(path) else os.path.join(path, VARS_FNAME)

RESERVED_NAMES = {
    'hostname': 'firstboot_hostname'
}


class Vars:
    DEFAULT_PATH = '.'
    def __init__(self, path='./resources', autosave=True, overwrite=False):
        self.fname = get_fname(path)
        self.config = {}
        self.current_config = {}
        self.autosave = autosave
        if not overwrite:
            self.load()

    def __str__(self):
        import yaml
        return '--- Variables in {}: \n{}---'.format(self.fname, yaml.dump(self.config))

    def load(self):
        '''Load existing variables from a string'''
        if os.path.isfile(self.fname):
            with open(self.fname, 'r') as f:
                self.current_config = self.parse(f.read())
                self.update(self.current_config, save_=False)
        return self

    def update(self, dct=(), save_=None, **kw):
        self.config.update(dct)
        self.config.update(kw)
        if self.autosave if save_ is None else save_:
            self.save()
        return self

    def pop(self, name, *a, **kw):
        return self.config.pop(name, *a, **kw)

    def save(self):
        changed_vars = [
            '{}={}'.format(k, v) for k, v in self.config.items()
            if self.current_config.get(k, ...) != v
        ]
        if not changed_vars:
            return
        print('*** Setting Variables ({}). ***'.format(', '.join(changed_vars)))
        util.touch(self.fname, '\n'.join([
            'export {}={}'.format(RESERVED_NAMES.get(k.lower(), k), shlex.quote(v)) for k, v in self.config.items() if v
        ]) + '\n')
        print()
        self.current_config = dict(self.config)
        return self

    def get(self, name, *a, **kw):
        return self.config.get(name, *a, **kw)

    def set(self, *args, **kw):
        return self.parse_string(*args, **kw) if args else self.prompt_any(**kw)

    def prompt(self, name, desc='', default=None, value=None, secret=False, update=True, ask=True):
        '''Prompt user for a specific variable.'''
        if value is None and ask:
            print('*'*20)
            default = self.config.get(name) or default
            while True:
                value = util.getinput('{} [{}] {}='.format(desc, default, name), secret=secret)
                if value or default is not None:
                    break
                print('{} is required.'.format(name))
            print()
        if update:
            self.update(**{name: value or default})
        return value or default

    def prompt_any(self, n=None, ask=True, **kw):
        '''Prompt user for arbitrary KEY=VALUE pairs to store on the sd card.'''
        if ask:
            print('*** Enter variables to store (KEY=VALUE): ***')
            for i in util.count(n):
                inp = input('... ')
                if not inp:
                    break
                parts = inp.split('=', 1)
                if len(parts) != 2:
                    print('*** ERROR - Input {} must be of the format KEY=VALUE ***'.format(inp))
                    continue
                kw[parts[0]] = parts[1]
        return self.update(kw)

    def parse_string(self, *args, **kw):
        '''Parse from a string in the form of KEYA=1,KEYB=2,KEY3=...'''
        return self.update(dict(
            kw, (l.split('=') for ls in args if ls for l in ls.split(','))))

    @staticmethod
    def parse(text, comments=False, **kw):
        cfg, cmts = {}, []
        for l in text.strip().splitlines():
            if l.strip().startswith('#'):
                cmts.append(l)
            else:
                k, v = l.split('=')
                cfg[k.split(' ')[-1]] = strip_quotes(v)
        cfg.update(kw)
        return (cfg, comments) if comments else cfg


def strip_quotes(x):
    if isinstance(x, str) and len(x) >= 2 and x[0] == x[1] and x[0] in '"\'':
        return x[1:-1]
    return x
