# Audio File Splitter
Divide single track audio file (with associated ".cue" file), into separate per-track files. 

This is a simple python script that makes use of third part libraries to split single track audio album files into separate per-track files, while keeping the ID3 tags consistent, and track names as well. It basically uses the .cue file to split and name each of the created tracks.

Created this to help me organize my audio library, and get rid of those annoying single track albums, which are not very suitable to phones and dumb players in general.

I have intentions to grow up this application as the necessity for other feature come. May include an user interface as well. Let's see when. 

Run amd tested on Ubuntu 16.04.03 using Python 3.5

##### Installing dependencies on Ubuntu 16.04.03
```
sudo apt install libtag1-dev
sudo pip3 install pytaglib pydub
```

##### How to use it

To conver a single files, simply type in the terminal
```
python3 songfilespliter.py TARGET_CUE_FILE_HERE.cue
```

To convert many, I use this command:
```
find -iname '*.cue' -execdir python3 songfilespliter.py {} \;
```


#### Please use carefully, at you own risk. I don't want to be blamed for accidentally deleted files. 

