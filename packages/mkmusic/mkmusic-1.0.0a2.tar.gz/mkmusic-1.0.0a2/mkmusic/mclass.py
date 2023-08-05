# MCLASS.PY
# The music class
# By Hyperhydrochloric Acid

from tqdm import tqdm


class Meta:
    events = []  # 0 is time, 1 is name, 2 is value
    maxTime = 0

    def add_meta_event(self, time: int, name: str, val):
        self.events.append([time, name, val])
        self.maxTime = max(self.maxTime, time)


class Track:
    inst = None
    notes = []  # 0 is begin time, 1 is end time, 2 is note
    properties = []  # 0 is time, 1 is name, 2 is value
    maxTime = 0

    def add_note_event(self, note: int, begin: int, end: int):
        self.notes.append([begin, end, note])
        self.maxTime = max(self.maxTime, end)

    def add_meta_event(self, time: int, name: str, val):
        self.properties.append([time, name, val])
        self.maxTime = max(self.maxTime, time)

    def convert(self, wave, hz):
        pro = 0
        vol = 1
        self.notes.sort()
        for note in tqdm(self.notes):
            while pro < len(self.properties) and self.properties[pro][0] <= note[0]:
                if self.properties[pro][1] == 'vol':
                    vol = self.properties[pro][2]
                pro += 1
            self.inst.write_sound(wave, [note[0], note[1]], note[2], vol, hz)


class Music:
    metaTrack = Meta()
    tracks = []
    time = 0

    def convert_time_to_second(self):
        self.metaTrack.events.sort()
        full = self.metaTrack.maxTime
        for track in self.tracks:
            full = max(full, track.maxTime)
        stamp = [0] * (full + 1)
        bpm = 240
        pointer = 0
        time = 0
        for t in range(full + 1):
            stamp[t] = time
            while pointer < len(self.metaTrack.events) and self.metaTrack.events[pointer][0] <= t:
                if self.metaTrack.events[pointer][1] in ["bpm"]:
                    bpm = self.metaTrack.events[pointer][2]
                    if type(bpm) != float and type(bpm) != int:
                        raise TypeError(f"float bpm expected, found {type(bpm).__name__}")
                pointer += 1
            time += 60 / bpm
        self.time = time
        for track in self.tracks:
            track.notes.sort()
            pointer, pit = 0, 0
            for note in track.notes:
                while pointer < len(self.metaTrack.events) and self.metaTrack.events[pointer][0] <= note[0]:
                    if self.metaTrack.events[pointer][1] in ["pit"]:
                        pit = self.metaTrack.events[pointer][2]
                    pointer += 1
                note[0] = stamp[note[0]]
                note[1] = stamp[note[1]]
                note[2] += pit
            for prop in track.properties:
                prop[0] = stamp[prop[0]]
        for ev in self.metaTrack.events:
            ev[0] = stamp[ev[0]]

    def convert_time_to_frame(self, hz):
        for track in self.tracks:
            for note in track.notes:
                note[0] = int(note[0] * hz)
                note[1] = int(note[1] * hz)
            for prop in track.properties:
                prop[0] = int(prop[0] * hz)
        for ev in self.metaTrack.events:
            ev[0] = int(ev[0] * hz)
        self.time = int(self.time * hz)

    def make_wav(self, hz):
        wave = [0] * self.time
        for track in self.tracks:
            track.convert(wave, hz)
        for i in range(len(wave)):
            wave[i] *= 32768
            wave[i] = min(wave[i], 32767)
            wave[i] = max(wave[i], -32767)
        return wave
