#download all the images associated with the movie into a directory that has its name as the amazon code.

from PIL import Image 
import numpy as np 
import urllib.request
import h5py
import requests
from io import BytesIO
# import matplotlib.pyplot as plt
import os
import glob2 as glob
import argparse

def verify_previous_download(MovieName):
    # There must be a directory with the movie name...
    if not os.path.exists(os.path.join(args.SaveDirName, MovieName)):
        return False

    # There should be at least 15 files in the directory...
    FileNames = glob.glob(os.path.join(args.SaveDirName, MovieName, "*"))
    if len(FileNames) < 15:
        return False
    # and each file in the directory needs to be more than zero bytes.
    for FileName in FileNames:
        if os.stat(FileName).st_size == 0:
            return False

    return True

#Get a single movie from the amazon server and store it locally.
def make_one(MovieName):
    frame = 1
    # Make a directory for the movie.
    direc = os.path.join(args.SaveDirName, MovieName)
    if not os.path.exists(direc):
        os.mkdir(direc)
    # Download up to 100 frames from the movie.
    while frame < 100:
        #print(frame)
        if frame < 10:
                fnumber = "0" + str(frame)
        else:
                fnumber = str(frame)
        url = "http://s3.amazonaws.com/stardustathome.testbucket/real/{x}/{x}-0{y}.jpg".format(x = MovieName, y = fnumber)
        r = requests.get(url)
        if r.status_code != 200: # Keep going until we run out of files or hit the max of 100.
            return
        OutputFileName = os.path.join(direc, str(frame)+".jpg")
        with open(OutputFileName, 'wb') as f:
            f.write(r.content)
        #try:
        #        img = Image.open(BytesIO(r.content))
        #        img = np.array(img)
        #except OSError:
        #        #print("got error from URL")
        #        break
        #plt.imsave(direc + "/" + str(frame) + ".png", img)
        frame += 1


if __name__ == "__main__":

    # Example command to run this with many instances in parallel using gnu parallel -- i.e. 100 downloads in parallel
    # parallel python download_movie.py --Shuffle True ; echo {} ::: {1..100}

    parser = argparse.ArgumentParser()
    parser.add_argument('--AmazonFileName', default=os.path.join('aerogel_codes.txt'))
    parser.add_argument('--SaveDirName', default=os.path.join("..", "..", "..", "Data", "blanks"))
    parser.add_argument('--MaxImages', default=None)
    parser.add_argument('--Shuffle', default=False)
    args = parser.parse_args()

    # Make the output directory for saving images to disk.
    if not os.path.exists(args.SaveDirName):
        os.mkdir(args.SaveDirName)

    MovieNames = np.genfromtxt(args.AmazonFileName, dtype=str)

    # Shuffling can be used to have multiple of these processes downloading at once.
    if bool(args.Shuffle) == True:
        from random import shuffle
        shuffle(MovieNames)

    # MaxImages is used to do small runs if you only need some images.
    if args.MaxImages is None:
        MaxImages = len(MovieNames)
    else:
        MaxImages = int(args.MaxImages)

    print(f'Downloading {MaxImages} files from Amazon.')
    for MovieName in MovieNames[:MaxImages]:

        # Check if this movie was previously downloaded and if the download completed successfully.
        MoviePreviouslyDownloaded = verify_previous_download(MovieName)
        if MoviePreviouslyDownloaded == True:
            print('x', end='', flush=True) # x means we are not downloading it.
            continue

        # The movie has not been downloaded so do so now.
        # time.sleep(0.5)
        print('.', end='', flush=True) # . means we are downloading it.
        make_one(MovieName)
    print()
    print('Done!')

