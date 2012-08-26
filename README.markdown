Image Unshredder
================

From the challenge posted here on the instagram engineering blog: http://instagram-engineering.tumblr.com/post/12651721845/instagram-engineering-challenge-the-unshredder
-----------------

Make sure you have PIL installed

To see a demonstration, running 

`python unshredder.py` 

will unshred the TokyoPanoramaShredded.png image file included in the repo and save the output to a file called unshredded.jpg

to shred your own image, run:

`python shredder.py -f <filename> --shreds <number of shreds (default 20)>`

This definitely works best if the number of shreds is a divisor of the width of the images in pixels

and to unshred that image, run:

`python unshredder.py -f <filename>`

which outputs the unshredded image to unshredded.jpg. If you don't specify a filename then the script looks for a file called TokyoPanoramaUnshredded.png

if the unshredder is having a hard time discovering the correct shred width, the -s option allows you to tell it how many shreds there are:

`python unshredder.py -f <filename> -s <shred_count>`