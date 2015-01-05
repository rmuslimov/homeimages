# coding:utf-8

import os
import shutil
import sys

from datetime import datetime

import exifread

from constants import (
    DATABASE_PHOTOS_PATH,
    POSSIBLE_STORAGE_PATHS,
    SYSTEM_PREPATH
)


def import_images(source_path):
    """ Find attached storage and run importing all existing images """
    copied, total = 0, 0
    for r, d, files in os.walk(source_path):
        images = filter(lambda x: x.upper().endswith('JPG'), files)

        for image in images:
            total += 1
            with open(os.path.join(source_path, r, image), 'rb') as f:
                try:
                    created = str(exifread.process_file(f)['Image DateTime'])
                except:
                    continue

                d = datetime.strptime(created.split()[0], '%Y:%m:%d')

                targetpath = os.path.join(
                    DATABASE_PHOTOS_PATH, '{:02}'.format(d.month),
                    '{:02}'.format(d.day))
                target = os.path.join(targetpath, image)

                if not os.path.exists(target):
                    try:
                        os.makedirs(targetpath)
                    except:
                        pass
                    shutil.copyfile(os.path.join(source_path, r, image), target)
                    copied += 1

                sys.stdout.write('.')

if __name__ == '__main__':

    source_path = None
    for each in POSSIBLE_STORAGE_PATHS:
        if os.path.exists(SYSTEM_PREPATH.format(each)):
            source_path = SYSTEM_PREPATH.format(each)
            break

    if not source_path:
        raise ValueError('Photos source path not found')

    import_images(source_path)
