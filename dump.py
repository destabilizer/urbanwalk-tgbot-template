import config
import json
import time
from datetime import datetime
import os

datadir = os.path.join(os.path.expanduser('~'), 'data', config.name.lower().replace(' ', '_'))
if not os.path.exists(datadir): os.makedirs(datadir)

def fnpath(username, ts, ft, fmt):
    return os.path.join(datadir, '{0}_{1}_{2}.{3}'.format(username, ts, ft, fmt))

def data_with_location(filetype, data, username, location):
    print('going to save data', filetype, data, username, location)
    ts = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
    if filetype == 'photo':
        data.download(fnpath(username, ts, filetype, 'jpg'))
    elif filetype == 'voice':
        data.download(fnpath(username, ts, filetype, 'ogg'))
    elif filetype == 'text':
        with open(fnpath(username, ts, filetype, 'txt')) as textf:
            textf.write(data)
    else:
        raise TypeError('wrong filetype')
    with open(fnpath(username, ts, filetype, 'json'), 'w') as locf:
        locf.write(json.dumps({'longitude': location.longitude,
                               'latitude': location.latitude}, indent=2))
