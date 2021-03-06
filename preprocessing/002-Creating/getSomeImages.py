"""
This is used for loading a few images from a created datafile with the name DATAFILE_NAME,
just to see if the creation of this dataset worked, for example. 
Just set the directory and file names here and run from terminal.
"""

import os
import numpy as np 
from PIL import Image
import h5py
import random

Dir = "/home/admin/Desktop/aerogel_preprocess"
datafile_name = "FOV100.hdf5"
SaveDir = "/home/admin/Desktop/aerogel_repo/fromHDF"

DF = h5py.File(os.path.join(Dir, datafile_name), "r")
TrainYes = DF["TrainYes"]
TrainNo = DF["TrainNo"]

if not os.path.exists(SaveDir):
	os.mkdir(SaveDir)

num_ims = 7 #Number of images (x2 for track and no track) to download
for_seed = 4673 
np.random.seed(for_seed)

numIms1 = TrainYes.shape[0]
numIms2 = TrainNo.shape[0]

yes_inds = np.random.randint(0, high = numIms1, size = num_ims)
no_inds = np.random.randint(0, high = numIms2, size = num_ims)

for j in range(num_ims):
	if not os.path.exists(os.path.join(SaveDir, "yes" + str(j))):
		os.mkdir(os.path.join(SaveDir, "yes" + str(j)))
	i = 0
	while True:
		try:
			im_slice = TrainYes[yes_inds[j], i, :, :, :]
			#print(im_slice.dtype)
			im = Image.fromarray(im_slice)
			im.save(os.path.join(SaveDir, "yes" + str(j), str(i) + ".png"))
			i += 1
		except ValueError:
			f = open(os.path.join(SaveDir, "yes" + str(j), "info.txt"), "w")
			f.write("j=" + str(j) + "\n")
			f.write("yes index: " + str(yes_inds[j]) + "\n")
			f.write("seed: " + str(for_seed) + "\n")
			f.write("Dir: " + Dir + "\n")
			f.write("datafile_name: " + datafile_name + "\n")
			f.write("SaveDir: " + SaveDir + "\n")
			f.close()
			break

for j in range(num_ims):
	if not os.path.exists(os.path.join(SaveDir, "no" + str(j))):
		os.mkdir(os.path.join(SaveDir, "no" + str(j)))
	i = 0
	while True:
		try:
			im_slice = TrainNo[no_inds[j], i, :, :, :]
			#print("no: ", im_slice.dtype)
			im = Image.fromarray(im_slice)
			im.save(os.path.join(SaveDir, "no" + str(j), str(i) + ".png"))
			i += 1
		except ValueError:
			f = open(os.path.join(SaveDir, "no" + str(j), "info.txt"), "w")
			f.write("j=" + str(j) + "\n")
			f.write("no index: " + str(no_inds[j]) + "\n")
			f.write("seed: " + str(for_seed) + "\n")
			f.write("Dir: " + Dir + "\n")
			f.write("datafile_name: " + datafile_name + "\n")
			f.write("SaveDir: " + SaveDir + "\n")
			f.close()
			break




