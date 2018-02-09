from pydub import AudioSegment as audios
import taglib
import argparse
import re
import os

#Script thast splits songfiles according to playlist files
parser = argparse.ArgumentParser()
parser.add_argument('filename', help='CUE file containing the playlist')
args = parser.parse_args()

if args.filename is not None:
    file_playlist = args.filename
else:
    print('Invalid input file. Terminanting script.')
    exit(-1)


# file_playlist = '/mnt/hd/joao/Musicas/Colecao/Coldplay/2015 A Head Full Of Dreams/Coldplay - A Head Full Of Dreams.cue'


playlist = open(file_playlist).readlines()

last = file_playlist.rfind('/')
dir = file_playlist[0:last+1]

for line in playlist:
    v = line.find("FILE")
    if (v != -1):
        file_song = dir + re.search('"(.+?)"', line).group().replace('"', '')
        file_type = file_song.split('.')[-1]
        break
if v == -1:
    print('Filename not found on the playlist. Quiting now.')
    exit(-1)

try:
    song = audios.from_file(file_song)
    song_duration_millis = round(song.duration_seconds*1000,0)
    song_size = len(song)
    song_metadata = taglib.File(file_song)
except:
    print('Error opening song file {}. Quiting now.'.format(file_song))
    exit(-1)

tracks = []

for i, line in enumerate(playlist):
    #Parse the CUE file to identify the timing of the tracks
    track = line.find("TRACK")
    if (track != -1):
        track_num = re.search('\d+', playlist[i]).group()
        r = re.search('"(.+?)"', playlist[i+1])

        if r is not None:
            track_name = r.group().replace('"', "")
        else:
            print('Error detecting song name at the playlist. Quiting now.')
            exit(-1)

        if track_name.find('/') != -1:
            track_name_new = track_name.replace('/', ' - ')
            print('Invalid file name: {}. Changed it to: {}'.format(track_name, track_name_new))
            track_name = track_name_new

        output_filename = '{}{} - {}.{}'.format(dir, track_num, track_name, file_type)

        # j = 0
        for j in range(i+1, i+6):
            ts = playlist[j].find("INDEX 01")
            if ts != -1:
                break

        if ts == -1:
            print('Error: could not find tracks timing. Quiting now.')
            exit(-1)

        min = int(re.search('\d+:', playlist[j]).group().replace(':', ''))
        seg = int(re.search(':\d+:', playlist[j]).group().replace(':', ''))
        millis = int(re.search(':\d+', playlist[j]).group().replace(':', ''))

        track_start_millis = (min * 60 * 1000) + (seg * 1000) + millis

        tracks.append( {'filename' : output_filename, 'start' : track_start_millis, 'title': track_name, 'tracknumber': track_num} )


for i, track in enumerate(tracks):

    #Split and save the song
    a = round((track['start'] / song_duration_millis) * song_size, 0)

    if i < len(tracks)-1:
        b = round((tracks[i+1]['start'] / song_duration_millis) * song_size, 0)
    else:
        b = song_size

    song_split = song[a:b]
    r = song_split.export(track['filename'], format=file_type)

    #Add songs metadata
    song_split_metadata = taglib.File(track['filename'])

    song_split_metadata.tags = song_metadata.tags
    song_split_metadata.tags["TRACKNUMBER"] = track['tracknumber']
    song_split_metadata.tags["TITLE"] = track['title']

    song_split_metadata.save()

    print('Exported file: {}'.format(track['filename']))

# r1 = os.remove(file_playlist)
# r2 = os.remove(file_song)
print('Originals not removed!')


