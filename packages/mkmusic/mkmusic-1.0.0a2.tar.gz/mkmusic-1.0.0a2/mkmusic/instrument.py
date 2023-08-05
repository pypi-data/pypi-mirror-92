# INSTRUMENT.PY
# Base instruments class
# By Hyperhydrochloric Acid

import math


def make_array(vol, vol_loop, vol_time, area):
    arr = []
    if vol_loop[0] != -1:
        remain = (area[1] - area[0]) - (vol_loop[0] + len(vol) - vol_loop[1]) * vol_time
        for i in range(vol_loop[0]):
            arr.append([vol[i], i * vol_time])
        tim, tin, ni = 0, vol_loop[0] * vol_time, 0
        while tim < remain:
            arr.append([vol[ni % (vol_loop[1] - vol_loop[0]) + vol_loop[0]], tim + tin])
            tim += vol_time
        tim = remain + tin
        for i in range(vol_loop[1], len(vol)):
            arr.append([vol[i], tim + (i - vol_loop[1]) * vol_time])
    else:
        for i in range(len(vol)):
            arr.append([vol[i], (area[1] - area[0]) * i // len(vol)])
    return arr


class Fourier:
    t = 1
    vol = [1]
    vol_loop = [-1, -1]
    vol_time = -1
    pit = [0]
    pit_loop = [-1, -1]
    pit_time = -1
    pit_val = 0

    def __init__(self, tt):
        self.t = tt

    def write_sound(self, wave, area, note, loud, sample):
        varr = make_array(self.vol, self.vol_loop, self.vol_time, area)
        parr = make_array(self.pit, self.pit_loop, self.pit_time, area)
        vptr, pptr = 0, 0
        div = 0
        for i in range(1, self.t + 1, 2):
            div += 1 / i
        for t in range(area[0], area[1]):
            while vptr < len(varr) - 1 and varr[vptr + 1][1] <= t - area[0]:
                vptr += 1
            while pptr < len(parr) - 1 and parr[pptr + 1][1] <= t - area[0]:
                pptr += 1
            freq = sample / (440 * 2**((parr[pptr][0] * self.pit_val + note - 69) / 12))
            val = 0
            for i in range(1, self.t + 1, 2):
                val += math.sin(2 * math.pi * i / freq * (t - area[0])) / i
            wave[t] += val / div * loud * varr[vptr][0] / 8


class Pulse:
    t = 50
    vol = [1]
    vol_loop = [-1, -1]
    vol_time = -1
    pit = [0]
    pit_loop = [-1, -1]
    pit_time = -1
    pit_val = 0

    def __init__(self, tt):
        self.t = tt

    def write_sound(self, wave, area, note, loud, sample):
        varr = make_array(self.vol, self.vol_loop, self.vol_time, area)
        parr = make_array(self.pit, self.pit_loop, self.pit_time, area)
        vptr, pptr = 0, 0
        for t in range(area[0], area[1]):
            while vptr < len(varr) - 1 and varr[vptr + 1][1] <= t - area[0]:
                vptr += 1
            while pptr < len(parr) - 1 and parr[pptr + 1][1] <= t - area[0]:
                pptr += 1
            freq = sample / (440 * 2 ** ((parr[pptr][0] * self.pit_val + note - 69) / 12))
            if (t - area[0]) % freq <= self.t / 100 * freq:
                val = 1
            else:
                val = -1
            wave[t] += val * loud * varr[vptr][0] / 8


class Triangle:
    vol = [1]
    vol_loop = [-1, -1]
    vol_time = -1
    pit = [0]
    pit_loop = [-1, -1]
    pit_time = -1
    pit_val = 0

    def write_sound(self, wave, area, note, loud, sample):
        varr = make_array(self.vol, self.vol_loop, self.vol_time, area)
        parr = make_array(self.pit, self.pit_loop, self.pit_time, area)
        vptr, pptr = 0, 0
        for t in range(area[0], area[1]):
            while vptr < len(varr) - 1 and varr[vptr + 1][1] <= t - area[0]:
                vptr += 1
            while pptr < len(parr) - 1 and parr[pptr + 1][1] <= t - area[0]:
                pptr += 1
            freq = sample / (440 * 2 ** ((parr[pptr][0] * self.pit_val + note - 69) / 12))
            if (t - area[0]) % freq <= freq / 4:
                val = 4 / freq * ((t - area[0]) % freq)
            elif (t - area[0]) % freq >= freq * 3 / 4:
                val = 4 / freq * ((t - area[0]) % freq - freq)
            else:
                val = 4 / freq * (freq / 2 - (t - area[0]) % freq)
            wave[t] += val * loud * varr[vptr][0] / 8
