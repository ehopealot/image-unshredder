Image Unshredder
================

From the challenge posted here on the instagram engineering blog: http://instagram-engineering.tumblr.com/post/12651721845/instagram-engineering-challenge-the-unshredder
-----------------

Make sure you have PIL installed

to shred an image, run:

`python shredder.py -f <filename> --shreds <number of shreds (default 20)>`

to unshred an image, run:

`python unshredder.py -f <filename>`

which outputs the unshredded image to unshredded.jpg

if the unshredder is having a hard time discovering the correct shred width, the -s option allows you to tell it how many shreds there are:

`python unshredder.py -f <filename> -s <shred_count>`