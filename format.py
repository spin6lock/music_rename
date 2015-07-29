import untangle
import re

disc_track_to_filename = {}
disc_track_to_desc = {}
filename_pattern = re.compile("[A-Z0-9\-]+.wav")
track_index_pattern = re.compile("TRACK(\d+)-(\d+).wav")
disc_and_track_pattern = re.compile("([A-Z0-9]+-\d+)-TRACK(\d+).wav")

def extract_filename(line):
	match = filename_pattern.search(line)
	if not match:
		return
	start = match.start()
	end = match.end()
	filename = line[start:end]
	return filename

def extract_disc_and_track(line):
	match = disc_and_track_pattern.findall(line)[0]
	disc = match[0]
	track = match[1]
	return disc, track

def get_disc_and_track_key(disc, track):
	return "-".join([disc, track])

with open("source.xml", "r") as fh:
	xmlsource = fh.read()
with open("output.txt", "r") as fh:
	lines = fh.readlines()
	for line in lines:
		filename = extract_filename(line)
		if not filename:
			continue
		disc, track = extract_disc_and_track(line)
		disc_track_to_filename[get_disc_and_track_key(disc, track)] = filename
		

document = untangle.parse(xmlsource)
resultset = document.FMPXMLRESULT.RESULTSET
rows = resultset.ROW
disc_col = 0
track_col = 1
index_col = 2
description_col = 3

def get_text(data, col):
	result = data[col].DATA.cdata
	return result

for row in rows:
	cols = row.COL
	disc = get_text(cols, disc_col)
	track = get_text(cols, track_col)
	index = get_text(cols, index_col)
	description = get_text(cols, description_col)
	#print "%s_%s_%s_%s"%(disc, track, index, description)
	disc_track_to_desc[get_disc_and_track_key(disc, track)] = {
		"disc":disc,
		"track":track,
		"index":index,
		"desc":description,
	}

max_len = 0
for key, filename in disc_track_to_filename.iteritems():
	info = disc_track_to_desc[key]
	disc = info["disc"]
	track = info["track"]
	index = info["index"]
	description = info["desc"]
	new_filename = "%s_%s_%s.wav"%(disc, track, description)
	if len(new_filename) > max_len:
		max_len = len(new_filename)
	#print "%s|%s"%(filename, new_filename)
print max_len
