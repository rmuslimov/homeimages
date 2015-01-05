# coding:utf-8

import os

# Path on disk where all images and videos live
DATABASE_PHOTOS_PATH = os.path.expanduser('~/Google Drive/Photos')
DATABASE_VIDEOS_PATH = os.path.expanduser('~/Google Drive/Videos')

# Directory name where SD usually is added
POSSIBLE_STORAGE_PATHS = ('CANON_DC', 'EOS_DIGITAL')

# system path to sd directories
SYSTEM_PREPATH = '/Volumes/{0}/'
