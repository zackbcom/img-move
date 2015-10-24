#!/usr/bin/python
import os
import fnmatch
import exifread

relevant_path = "./img"
Images = []

class Image(object):
  def __init__(self, sdcardPath):
    self.sdcardPath = sdcardPath
    self.removePath = ''
    self.shotDate = ''
  def __str__(self):
    return self.shotDate


def findImages():
  for root, dirnames, filenames in os.walk(relevant_path):
    for filename in filenames:
      if matchesExtensions(filename):
        Images.append(Image(os.path.join(root, filename)))
  return

def matchesExtensions(name,extensions=["*.jpg", "*.cr2", "*.raw"]):
  for pattern in extensions:
    if fnmatch.fnmatch(name.lower(), pattern.lower()):
      return True
  return False

def getShotDate():
  # Open image file for reading (binary mode)
  try:
    f = open(relevant_path + '/' + img, 'rb')

    # Return Exif tags
    tags = exifread.process_file(f, details=False, stop_tag="EXIF DateTimeOriginal")
    dateTaken = tags["EXIF DateTimeOriginal"]
    f.close()
    return dateTaken
  else:
    return


def main():
  findImages()
  print(*Images, sep='\n')


if __name__ == "__main__":
  main()