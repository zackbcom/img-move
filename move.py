#!/usr/bin/python
import os
import fnmatch
import exifread

relevant_path = "./img"
Images = []

class Image(object):
  def __init__(self, sdcardPath, shotDate=''):
    self.sdcardPath = sdcardPath
    self.removePath = ''
    self.shotDate = shotDate
  def __str__(self):
    return str(self.shotDate) + ' ' +  self.sdcardPath


def findImages():
  for root, dirnames, filenames in os.walk(relevant_path):
    for filename in filenames:
      if matchesExtensions(filename):
        filePath = os.path.join(root, filename)
        shotDate = getShotDate(filePath)
        Images.append(Image(filePath, shotDate))
  return

def matchesExtensions(name,extensions=["*.jpg", "*.cr2", "*.raw"]):
  for pattern in extensions:
    if fnmatch.fnmatch(name.lower(), pattern.lower()):
      return True
  return False

def getShotDate(filePath):
  # Open image file for reading (binary mode)
  try:
    f = open(filePath, 'rb')

    try:
      # Return Exif tags
      tags = exifread.process_file(f, details=False, stop_tag="EXIF DateTimeOriginal")
      shotDate = tags["EXIF DateTimeOriginal"]
    except (KeyError) as e:
      return
    finally:
      f.close()
    return shotDate

  except (IOError, OSError) as e:
    return 

def main():
  findImages()
  print('DateTime            Folder' )
  print(*Images, sep='\n')


if __name__ == "__main__":
  main()