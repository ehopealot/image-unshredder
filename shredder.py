from PIL import Image
from random import shuffle
import argparse
import os.path


parser = argparse.ArgumentParser(description='Shred an image')
parser.add_argument('--shreds', default=20, type=int)
parser.add_argument('-f', default='sample.png')
args = parser.parse_args()

SHREDS = args.shreds
filename = args.f


image = Image.open(filename)
shredded = Image.new('RGBA', image.size)
width, height = image.size
shred_width = width/SHREDS
sequence = range(0, SHREDS)
shuffle(sequence)

for i, shred_index in enumerate(sequence):
    shred_x1, shred_y1 = shred_width * shred_index, 0
    shred_x2, shred_y2 = shred_x1 + shred_width, height
    region =image.crop((shred_x1, shred_y1, shred_x2, shred_y2))
    shredded.paste(region, (shred_width * i, 0))

split_filename = os.path.splitext(filename)
print split_filename
shredded.save('{0}_shredded{1}'.format(*split_filename))
