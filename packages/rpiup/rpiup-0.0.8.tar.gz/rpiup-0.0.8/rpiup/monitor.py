import os
import flask
import yaml
import datetime
# import filelock
import sqlitedict


PORT = 8056


app = flask.Flask(__name__, template_folder='templates')#os.path.join(os.path.dirname(__file__), )


DEVICES = sqlitedict.SqliteDict('devices.db', autocommit=True)


'''

Accounting

'''


@app.route('/update/<device>/<status>')
def update(device, status=None):
    # use flask oidc and check for provisioner role
    d = DEVICES.get(device) or {'steps': [], 'last_updated': None, 'attrs':{},}
    args = dict(flask.request.args)

    t_now = datetime.datetime.now()
    statuses = []
    if status and status not in set(s['name'] for s in d['steps']):
        status, = statuses = [{'name': status, 'time': t_now}]
        err = args.pop('error', None)
        if err:
            status['error'] = err

    DEVICES[device] = {
        'steps': d['steps'] + statuses,
        'last_updated': t_now,
        'attrs': dict(d['attrs'], **flask.request.args),
    }
    if flask.request.args.get('ip'):
        refresh_inventory()
    # print(DEVICES[device])
    return flask.jsonify({'message': 'success'})


@app.route('/remove/<device>')
def remove(device):
    d = DEVICES[device].pop(device, None)
    refresh_inventory()
    return flask.jsonify({'message': 'success'})


@app.route('/clear')
def clear():
    DEVICES.clear()
    refresh_inventory()
    return flask.jsonify({'message': 'success'})

# export

@app.route('/inventory')
def inventory():
    with open('./inventory', 'r') as f:
        return '<pre>{}</pre>'.format(f.read())


@app.route('/inventory/refresh')
def inventoryrefresh():
    refresh_inventory()
    return flask.redirect(flask.url_for('inventory'))



'''

Status

'''



@app.route('/status')
def status():
    return flask.jsonify({'devices': dict(DEVICES)})


@app.route('/status/yaml')
def statusyaml():
    return flask.jsonify({'body': '<pre>{}</pre>'.format(yaml.dump(dict(DEVICES)))})


@app.route('/status/text')
def statustext():
    done, running = split_cond(DEVICES.items(), lambda x: any(x.endswith('done') for x in x[1]['steps']))

    return flask.jsonify({'body': '''{}'''.format(
        '\n'.join(
            [devicehtml(name, **d) for name, d in sorted(running)] +
            [tag('h4', 'Done ({})'.format(len(done))) if done else ''] +
            [devicehtml(name, done=True, **d) for name, d in sorted(done)]
        ).strip() or tag('h4', 'No Devices')
    )})


_ATTR_ALTS = {'c': 'class'}
_as_listitems = lambda xs: ' '.join(str(x) for x in xs if x) if isinstance(xs, (list, tuple)) else xs
tag = lambda _tag, *content, **kw: '<{tag} {attrs}>{content}</{tag}>'.format(
    tag=_tag, content=''.join(str(c) for c in content if c),
    attrs=' '.join(
        '{}="{}"'.format(_ATTR_ALTS.get(k, k), _as_listitems(v))
        for k, v in kw.items() if v is not None
    ))

tagmap = lambda _tag, *content, **kw: ''.join(tag(_tag, c, **kw) for c in content if c)
pill = lambda x, name=None: tag('span', name, name and ':', x) if x else ''


def devicehtml(name, steps, last_updated=None, done=False, attrs=None):
    return '<div class="device {}">{}</div>'.format(
        'done' if done else '',
        ''.join(tag('div', l) for l in [
            tag('span', name) + pill(attrs.get('ip'), 'ip'),
            tag('span', last_updated),
            ' | '.join(tag('span', s) for s in steps[::-1]),
            ''.join(pill(v, k) for k, v in attrs.items() if k != 'ip'),
        ]))


def split_cond(xs, cond):
    groups = {}
    for x in xs:
        groups.setdefault(cond(x), []).append(x)
    return [groups.get(k, []) for k in (True, False)] if not set(groups) - set((True, False)) else groups



'''

Pages

'''



@app.route('/watch')
def watch():
    # the most basic we can get
    return flask.render_template('index.html')

@app.route('/')
def index():
    return flask.jsonify({'message': "Welcome! Let's set up some devices!"})


import traceback
@app.errorhandler(Exception)
def handle_exception(e):
    return flask.jsonify({
        'error': True,
        'message': '''
{err}<pre><h3>Traceback (most recent call last):</h3><div>{tb}</div><h3>{typename}: {err}</h3></pre>
        '''.strip().format(
            err=e, tb='<hr/>'.join(traceback.format_tb(e.__traceback__)).strip('\n'),
            typename=type(e).__name__)
    }), 500


'''

Utils

'''

def refresh_inventory(fname='./inventory'):
    # with filelock.FileLock(fname + ".lock"):
    with open(fname, "w") as f:
        f.write(os.linesep.join(ip for ip in (
            d['attrs'].get('ip') for d in DEVICES.values()
        ) if ip))


if __name__=='__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
