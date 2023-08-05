# READFILE.PY
# Used to read mkmusic file and convert to a class
# By Hyperhydrochloric Acid

from mkmusic.mclass import *
from mkmusic.instrument import *
from mkmusic.table import *
import re
import copy


def read_file(name, hz) -> Music:
    music = Music()
    tracks, ins = {}, {}

    def get_instrument(base_i, deep=False):
        if base_i in ins:
            if deep:
                base_t = copy.deepcopy(ins[base_i])
            else:
                base_t = ins[base_i]
        elif base_i == 'sin':
            if deep:
                base_t = copy.deepcopy(Fourier(1))
            else:
                base_t = Fourier(1)
        elif re.match(r'^f(\d[13579])', base_i):
            mth = re.match(r'^f(\d[13579])', base_i).group(1)
            if deep:
                base_t = copy.deepcopy(Fourier(int(mth)))
            else:
                base_t = Fourier(int(mth))
        elif re.match(r'^p(\d\d)', base_i):
            mth = re.match(r'^p(\d\d)', base_i).group(1)
            if deep:
                base_t = copy.deepcopy(Pulse(int(mth)))
            else:
                base_t = Pulse(int(mth))
        elif base_i == 'tri':
            if deep:
                base_t = copy.deepcopy(Triangle())
            else:
                base_t = Triangle()
        else:
            raise ValueError('Invalid instrument.')
        return base_t

    with open(name) as file:
        lines = file.readlines()
        mode = ''
        for line in lines:
            line = line[:-1]
            if not line or line.startswith('#'):
                continue
            match = re.match(r'^\[(.+?)]$', line)
            if match:
                mode = match.group(1)
                continue
            if not mode:
                line = line.replace(' ', '')
                match = re.match(r'^(.+?)\((.+?)\):(.+)', line)
                if match is None:
                    raise ValueError('Invalid instrument.')
                name = match.group(1)
                base = match.group(2)
                pro = match.group(3)
                base_track = get_instrument(base, True)
                pro = pro.split(';')
                for obj in pro:
                    match = re.match(r'^(.+?)=(.+)', obj)
                    variable = match.group(1)
                    value = match.group(2)
                    if variable == 'vol':
                        match = re.match(r'^\((.+?)\)(.*?)\[(.+?)](.*)', value)
                        if match:
                            left = match.group(2)
                            mid = match.group(3)
                            right = match.group(4)
                            base_track.vol_loop = [len(left), len(left) + len(mid)]
                            base_track.vol_time = eval(match.group(1)) * hz / 1000
                            tmp = left + mid + right
                            base_track.vol = []
                            for ch in tmp:
                                base_track.vol.append(vol[ch])
                        else:
                            match = re.match(r'^([^()]+)', value)
                            if not match:
                                raise ValueError('Unknown volume value')
                            tmp = match.group(1)
                            base_track.vol = []
                            for ch in tmp:
                                base_track.vol.append(vol[ch])
                    if variable == 'pit':
                        match = re.match(r'^\((.+?)\)(.*?)\[(.+?)](.*?)\((.+?)\)', value)
                        if match:
                            left = match.group(2)
                            mid = match.group(3)
                            right = match.group(4)
                            base_track.pit_loop = [len(left), len(left) + len(mid)]
                            base_track.pit_time = eval(match.group(1)) * hz / 1000
                            base_track.pit_val = eval(match.group(5))
                            tmp = left + mid + right
                            base_track.pit = []
                            for ch in tmp:
                                base_track.pit.append(vol[ch])
                        else:
                            match = re.match(r'^([^()]+?)\((.+?)\)', value)
                            if not match:
                                raise ValueError('Unknown pitch value')
                            tmp = match.group(1)
                            base_track.pit_val = eval(match.group(2))
                            base_track.pit = []
                            for ch in tmp:
                                base_track.pit.append(vol[ch])
                ins[name] = base_track
            else:
                match = re.match(r'^(.+?):(.+)', line)
                if match is None:
                    raise ValueError('Invalid instrument.')
                mode = match.group(1)
                mode = mode.replace(' ', '')
                value = match.group(2)
                if '.' in mode:
                    match = re.match(r'^(.+?)\.(.+)', mode)
                    if not match:
                        raise ValueError('Unknown track')
                    track = match.group(1).replace(' ', '')
                    pro = match.group(2).replace(' ', '')
                    if track == 'meta':
                        tr = music.metaTrack
                    else:
                        tr = tracks[track]
                    if not tr:
                        raise ValueError('Unknown track')
                    i, pos = 0, 0
                    while i < len(value):
                        if value[i] == ' ':
                            i += 1
                            pos += 1
                            continue
                        s = ""
                        now_pos = pos
                        i += 1
                        pos += 1
                        if pro == 'lyr':
                            while i < len(value) and value[i] != ' ':
                                s += value[i]
                                i += 1
                                if ord(value[i]) < 11904:
                                    pos += 1
                                else:
                                    pos += 2
                        elif pro == 'vol' or pro == 'pit':
                            s = value[now_pos]
                            s = vol[s]
                        else:
                            while i < len(value) and value[i] != ' ':
                                s += value[i]
                                i += 1
                                pos += 1
                            s = eval(s)
                        tr.add_meta_event(now_pos, pro, s)
                else:
                    match = re.match(r'^(.+?)\((.+)\)', mode)
                    if not match:
                        raise ValueError('Unknown track')
                    track = match.group(1)
                    base = match.group(2)
                    tr = copy.deepcopy(Track())
                    tr.notes = list()
                    tr.properties = list()
                    tr.inst = get_instrument(base)
                    tracks[track] = tr
                    i = 0
                    while i < len(value):
                        if value[i] == ' ':
                            i += 1
                            continue
                        no = note[value[i]]
                        bg = i
                        i += 1
                        while i < len(value) and value[i] == '-':
                            i += 1
                        tr.add_note_event(no, bg, i)
    for track in tracks.values():
        music.tracks.append(track)
    return music
