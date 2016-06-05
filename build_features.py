from format_imsdb import format_script
import math
from extract_features import extract_features
import csv
from sklearn import naive_bayes
from sklearn.metrics import confusion_matrix
import numpy as np

from sklearn import preprocessing
from sklearn.feature_extraction import DictVectorizer

file_base = "imsdb_scripts/"

flagUseBinary = False
flagUseTomatoes = True
flagUseMetascore = False

tomatoesBad = 5
tomatoesGood = 8
metascoreBad = 50
metascoreGood = 80

film_file = "films.txt"
feat_file = "feats.txt"
qual_file = "qual.txt"

film_list_file = open(film_file, 'w')
feat_list_file = open(feat_file, 'w')
qual_list_file = open(qual_file, 'w')

film_list = []
feat_list = [] 
qual_list = []


file_name = '{}{}'.format(file_base,"American Hustle.txt")


#scenes = format_script(file_name)


# parameter to be tuned - segment length in number of minutes/pages


# divide film into 30 minute chunks

# Divide film by page numbers; page number first, if no page number then acts
def script_to_n_chunks(scenes, num_segments = 4):
	def get_script_by_page(scenes):
		disaggregated_script = [event for events in scenes for event in events]
		script_by_page = []
		curr_events = []
		for event in disaggregated_script:
			if event[1] == 'page number':
				script_by_page.append(curr_events)
				curr_events = [] # don't include page number as event
			else:
				curr_events.append(event)
		return script_by_page
	# divide film into four chunks
	# Returns generator
	def get_n_chunks(l, n):
		return [l[i:i+n] for i in xrange(0, len(l), n)]
	def get_num_chunks(l, num_segments):
		return math.ceil(len(l)/float(num_segments))
	script_by_page = get_script_by_page(scenes)
	print "Num pages: " + str(len(script_by_page))
	if len(script_by_page) > 1:
		num_chunks = get_num_chunks(script_by_page, num_segments)
		temp = get_n_chunks(script_by_page, int(num_chunks))
	else:
		print "Page numbers not available"
		num_chunks = get_num_chunks(scenes, num_segments)
		temp = get_n_chunks(scenes, int(num_chunks))
	chunks = []
	# temp has four elements each with 38 elements
	for chunk in temp:
		chunks.append([event for page in chunk for event in page])
	return chunks

# Process data and build features. Scale features is next step
def get_status(row):
	#3 metascored
	#4 rottentomatoes
	if flagUseTomatoes:
		if row[4] > tomatoesGood:
			return "Good"
		elif row[4] < tomatoesBad:
			return "Bad"
		else:
			return "Neutral"
	if flagUseMetascore:
		if row[3] > metascoreGood:
			return "Good"
		elif row[3] < metascoreBad:
			return "Bad"
		else:
			return "Neutral"

def get_genre_dict():
	genre_dict = {}
	with open('imsdb_ratings.csv', 'rb') as csvfile:
		spamreader = csv.reader(csvfile)
		for row in spamreader:
			if "," in row[1]:
				row[1] = row[1].replace("\"","")
				row_list = row[1].split(", ")
			else:
				row_list = [row[1]]
			genre_dict[row[0]] = row_list
	return genre_dict


# amount of dialogue, action, dialogue to action

def get_summary_features(scenes, movie_name):
	#summary_features = []
	genre_dict = get_genre_dict()
	all_genres = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Drama", "Family", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Short", "Thriller", "War"]
	genre_features = [1 if x in genre_dict[movie_name] else 0 for x in all_genres]
	genre_features_dict = dict(zip(all_genres, genre_features))
	#summary_features.extend(genre_features)
	num_scenes = {'num_scenes': len(scenes)}
	summary_features = {}
	summary_features.update(genre_features_dict)
	summary_features.update(num_scenes)
	return summary_features

"""
features = {}
for idx, chunk in enumerate(chunks):
# change input parameter to scenes for extract features
	chunk_features = extract_features(chunk, idx + 1)
	features.update(chunk_features)
"""
# scaling data
# 25th hour?

def build_features(scale_features = False):
	film_list = []
	feat_list = [] 
	qual_list = []
	count = 0
	with open('imsdb_ratings_processed.csv', 'rb') as csvfile:
		__ = csvfile.readline()
		reader = csv.reader(csvfile)
		for row in reader:
			count += 1
			print "Film No.: " + str(count)
			#if count == 10:
			#	break
			#if get_status(row) == "Good" or get_status(row) == "Bad":
			file_name = file_base + row[0] + ".txt"
			print file_name
			scenes = format_script(file_name)
			if scenes is None:
				print "No file or formatting error"
				continue
			print "Num scenes: " + str(len(scenes))
			# Segment level features
			chunks = script_to_n_chunks(scenes)
			features = {}
			for idx, chunk in enumerate(chunks):
			# change input parameter to scenes for extract features
				chunk_features = extract_features(chunk, idx + 1)
				features.update(chunk_features)
			# Full script features
			script_summary_features = get_summary_features(scenes, row[0])
			final_features = {}
			final_features.update(features)
			final_features.update(script_summary_features)
			feat_list.append(final_features)
			#if get_status(row) == "Good":
			qual_list.append(row[4])
			#else:
			#qual_list.append(0)
			film_list.append(row[0])
	return film_list, feat_list, qual_list

#chunks = script_to_n_chunks(scenes)
#features = []
#for chunk in chunks:
# change input parameter to scenes for extract features
#	chunk_features = extract_features(file_name, "American Hustle")
#	features = features + chunk_features

