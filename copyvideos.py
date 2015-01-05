# coding:utf-8

import os
import subprocess

from hachoir_core.error import HachoirError
from hachoir_core.stream import InputIOStream
from hachoir_metadata import extractMetadata
from hachoir_parser import guessParser

from .constants import (
    DATABASE_VIDEOS_PATH,
    POSSIBLE_STORAGE_PATHS,
    SYSTEM_PREPATH
)


PATH = None

for each in POSSIBLE_STORAGE_PATHS:
    if os.path.exists(SYSTEM_PREPATH.format(each)):
        PATH = SYSTEM_PREPATH.format(each)
        break

if not PATH:
    raise ValueError('Video source path not found')


def metadata_for_filelike(filelike):
    try:
        filelike.seek(0)
    except (AttributeError, IOError):
        return None

    stream = InputIOStream(filelike, None, tags=[])
    parser = guessParser(stream)

    if not parser:
        return None

    try:
        metadata = extractMetadata(parser)
    except HachoirError:
        return None

    return metadata


CMD = 'ffmpeg -i "{}" -vcodec h264 -acodec aac -strict -2 "{}"'

if __name__ == '__main__':

    copied, total = 0, 0
    for r, dirs, files in os.walk(PATH):
        videos = filter(lambda x: x.upper().endswith('MOV'), files)

        for video in videos:
            total += 1
            with open(os.path.join(PATH, r, video), 'rb') as f:
                metadata = metadata_for_filelike(f)
                if not metadata:
                    print 'No metadata for', video
                    continue
                d = metadata.get('creation_date')

                targetpath = os.path.join(
                    DATABASE_VIDEOS_PATH,
                    '{:02}'.format(d.month), '{:02}'.format(d.day))
                target = os.path.join(
                    targetpath, video.lower().replace('.mov', '.mp4'))

                if not os.path.exists(target):
                    try:
                        os.makedirs(targetpath)
                    except:
                        pass
                    copied += 1

                    print CMD.format(
                        os.path.join(PATH, r, video), target)
                    p = subprocess.Popen(CMD.format(
                        os.path.join(PATH, r, video), target), shell=True)
                    p.wait()
