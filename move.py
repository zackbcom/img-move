#!/usr/bin/python
import os
import fnmatch
import exifread
import shutil
from datetime import datetime
import logging

# Logging
LOG_FILENAME = 'move_log.out'
logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s',
                    filename=LOG_FILENAME,
                    level=logging.DEBUG)

# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical error message')

# Config
deleteSrcFile = False
mediaPath = "./img"
dest_path = "./dest"
fileTypes = ["*.jpg", "*.cr2", "*.raw", "*.nef"]

# Variables
Images = []


class Image(object):

    def __init__(self, srcPath, fileName, shotDate='', destPath=''):
        self.srcPath = srcPath
        self.destPath = destPath
        self.fileName = fileName
        self.shotDate = shotDate

    def __str__(self):
        returnStr = 'Date:' + str(self.shotDate) + '\n'
        returnStr += 'src :' + str(self.srcPath) + '\n'
        returnStr += 'dest:' + str(self.destPath) + '\n'
        returnStr += 'file:' + str(self.fileName) + '\n'
        return returnStr


# Methods
def findImages():
    logging.info('This is an info message')
    for root, dirnames, filenames in os.walk(mediaPath):
        for filename in filenames:
            if matchesExtensions(filename):
                srcPath = root
                shotDate = getShotDate(os.path.join(root, filename))

            if isinstance(shotDate, exifread.classes.IfdTag):
                destPath = os.path.join(dest_path, datetime.strptime(str(shotDate), "%Y:%m:%d %H:%M:%S").strftime("%Y/%Y-%m-%d Rename Me"))
            else:
                destPath = os.path.join(dest_path, 'unsorted')
                Images.append(Image(srcPath, filename, shotDate, destPath))
    logging.info('Found ' + Images.length + ' Images')
    return


def matchesExtensions(name):
    for pattern in fileTypes:
        if fnmatch.fnmatch(name.lower(), pattern.lower()):
            return True
    return False


def moveImages():
    for Image in Images:
        transferFile(Image.srcPath, Image.destPath, Image.fileName)


def transferFile(src, dest, fileName):
    if not os.path.isdir(dest):
        os.makedirs(dest)
    # TODO: error handling

    if deleteSrcFile:
        shutil.move(os.path.join(src, fileName), os.path.join(dest, fileName))

    # TODO: Logging
    else:
        shutil.copy(os.path.join(src, fileName), os.path.join(dest, fileName))


def getShotDate(filePath):
    # Open image file for reading (binary mode)
    try:
        f = open(filePath, 'rb')

        try:
            # Return Exif tags
            tags = exifread.process_file(f, details=False,
                                         stop_tag="EXIF DateTimeOriginal")
            shotDate = tags["EXIF DateTimeOriginal"]
        except (KeyError):
            return
        finally:
            f.close()
        return shotDate

    except (IOError, OSError):
        logging.error('Could not open' + filePath)
    return


def main():
    findImages()
    moveImages()
    print(*Images, sep='\n\n')


if __name__ == "__main__":
    main()
