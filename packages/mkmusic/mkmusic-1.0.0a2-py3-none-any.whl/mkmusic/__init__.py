# __INIT__.PY
# This is the main code of the project.
# By Hyperhydrochloric Acid

import mkmusic.version
from mkmusic.readfile import *
import argparse
import wave
import numpy as np


def start_program(args=None):
    parser = argparse.ArgumentParser(prog='mkmusic', description=f'Mkmusic Compiler Version {mkmusic.version.ver}')
    parser.add_argument('-o', '--output', help='the output wave file, default is [file].wav')
    parser.add_argument('-r', '--rate', help='specify the sample rate of the output file, default is 44100')
    parser.add_argument('-v', '--version', help='show the version of this program and exit', action="store_true")
    parser.add_argument('file', help='the source code file', nargs='?', default='')
    args = parser.parse_args(args)
    if args.version:
        print(version.ver)
        exit()
    if args.file == '':
        parser.print_help()
        print('-' * 50)
        args.file = input("Input file name: ").strip()
    if args.output:
        out_file = args.output
    else:
        out_file = args.file + '.wav'
    if not args.rate:
        hz = 44100
    else:
        hz = int(args.rate)
    file = read_file(args.file, hz)
    file.convert_time_to_second()
    file.convert_time_to_frame(hz)
    wav = file.make_wav(hz)
    out = wave.open(out_file, 'wb')
    out.setnchannels(1)
    out.setsampwidth(2)
    out.setframerate(hz)
    out.setcomptype('NONE', 'not compressed')
    out.writeframes(np.array(wav).astype(np.int16).tobytes())
    out.close()


if __name__ == '__main__':
    start_program()
