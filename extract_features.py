from format_imsdb import format_script
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from textstat.textstat import textstat
from httplib2 import Http
from urllib import urlencode
from xml.etree.ElementTree import fromstring
from nltk.corpus import sentiwordnet as swn
import csv
from operator import itemgetter
from collections import Counter
import re
import numpy as np
from sklearn.feature_extraction import DictVectorizer

"""
bad_action = "bad_action.txt"
bad_dialogue = "bad_dialogue.txt"

badA = open(bad_action, 'w')
badD = open(bad_dialogue, 'w') 

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
"""
#print genre_dict

# amount of dialogue to action


error_codes = ["'", 'E', 'T', 'D', 'Z']
http = Http()

def find_lex_d(text):
    data = {'input': text}
    response, content = http.request("http://lex-d.herokuapp.com", "POST", urlencode(data))
    if response['status'] != 200:
        if str(content)[2] in error_codes:
            print(content)                    # print error message if error
        else:
        	if content == "EMPTY STRING":
        		return 0
        	if content == "TOO SHORT":
        		return 90
        	return {'lexical_diversity': float(content)}  # print Lexical diversity score
    else:
        print('Error 200 thrown from server')

def extract_senti_wordnet(text):
	#pos_score = 0
	#neg_score = 0
	overall_score = 0
	for word in text:
		synsets = swn.senti_synsets(word.decode('utf-8', 'ignore'))
		for synonym in list(synsets):
			#print synonym.pos_score
			#pos_score += synonym.pos_score()
			#neg_score += synonym.neg_score()
			overall_score += (synonym.pos_score() - synonym.neg_score())
	overall_score /= len(text)
	#neg_score /= len(text)
	return {'senti_score': overall_score}



# tf-idf code
all_genres = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Drama", "Family", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Short", "Thriller", "War"]


# combine synonyms
def general_inquirer_to_dict():
	#feature_names = ["Positiv", "Negativ", "Active", "Passive", "Object"]
	inquirer_dict = {}
	count = 0
	with open("harvard_general_inquirer.txt", 'r') as f:
		reader = csv.reader(f, delimiter='\t')
		header = reader.next()
		#indices = [header.index(name) for name in feature_names]
		for row in reader:
			#inquirer_dict[row[0].lower()] = itemgetter(*indices)(row)
			#header.index("Defined") # remove definition
			key = row[0].split('#')[0].lower()
			# can have many of same feature per word (implicit weighting)
			if key in inquirer_dict:
				inquirer_dict[key].extend([elem for elem in row[2:185] if elem != ''])
			else:
				inquirer_dict[key] = [elem for elem in row[2:185] if elem != '']
	return inquirer_dict

opposites_features = [('Power', 'Weak'), ('Active', 'Passive'), ('Pleasur', 'Pain'), ('Virtue', 'Vice'), ('Ovrst', 'Undrst'), ('Female', 'MALE'), ('Increas', 'Decreas'), ('Positiv', 'Negativ'), ('PowGain', 'PowLoss')]
single_features = ['Relig', 'POLIT', 'SocRel', 'Causal', 'Object', 'Self', 'Our', 'You']
def general_inquirer_features(text):
	inquirer_dict = general_inquirer_to_dict()
	#word_list = text.split()
	word_list = re.findall(r"[\w']+", text.lower())
	word_counter = Counter(word_list)
	hgi_feature_dict = {}
	features_dict = dict((feature,0) for feature in single_features+ ['/'.join(tup) for tup in opposites_features])
	for word in word_counter:
		if word in inquirer_dict:
				for feature in single_features:
					if feature in inquirer_dict[word]:
						features_dict[feature] += word_counter[word]
				# accounts for synoynms of words having different meanings
				for tup in opposites_features:
					if tup[0] in inquirer_dict[word] and tup[1] not in inquirer_dict[word]:
						features_dict['/'.join(tup)] += word_counter[word]
					elif tup[0] not in inquirer_dict[word] and tup[1] in inquirer_dict[word]:
						features_dict['/'.join(tup)] -= word_counter[word]
					elif inquirer_dict[word].count(tup[0]) > inquirer_dict[word].count(tup[1]):
						features_dict['/'.join(tup)] += word_counter[word]
					elif inquirer_dict[word].count(tup[0]) < inquirer_dict[word].count(tup[1]):
						features_dict['/'.join(tup)] -= word_counter[word]
		for feature in features_dict:
			features_dict[feature] = float(features_dict[feature])/len(text)
	return features_dict
	#vectorizer = DictVectorizer()
	#return (list(vectorizer.fit_transform([features_dict]).toarray()[0]), vectorizer.get_feature_names())
	

# amount of dialogue, action, dialogue to action
def dialogue_action_length_features(dialogue_list, action_list):
	dialogue_to_action = len(dialogue_list)/float(len(action_list))
	dialogue_lens = [len(line.split()) for line in dialogue_list]
	action_lens = [len(line.split()) for line in action_list]
	dialogue_len_mean = np.mean(dialogue_lens)
	dialogue_len_std = np.std(dialogue_lens)
	action_len_mean = np.mean(action_lens)
	action_len_std = np.std(action_lens)
	return {'dialogue_to_action': dialogue_to_action, 'dialogue_len_mean': dialogue_len_mean, 'dialogue_len_std': dialogue_len_std, 'action_len_mean': action_len_mean, 'action_len_std': action_len_std}
	#return [dialogue_to_action,dialogue_len_mean,dialogue_len_std,action_len_mean,action_len_std]

# voice over and off screen
def get_dialogue_type_features(chunk):
	dialogue_list = [dialogue for dialogue in chunk if dialogue[1] == 'character name']
	dialogue_type = [''.join(e for e in dialogue[2] if e.isalnum()).lower() for dialogue in dialogue_list]
	proportion_vo = float(dialogue_type.count("vo"))/len(dialogue_type)
	proportion_os = float(dialogue_type.count("os"))/len(dialogue_type)
	#print proportion_vo
	#print proportion_os
	return {'proportion_vo': proportion_vo, 'proportion_os': proportion_os}

def extract_features(chunk, nth_chunk):
	if chunk is None:
		return None
	dialogue_list = [re.sub(r'\([^)]*\)', '', line[0]) for line in chunk if line[1] == 'dialogue']
	all_dialogue = ' '.join(dialogue_list)
	#print all_dialogue
	action_list = [line[0] for line in chunk if line[1] == 'action']
	all_action = ' '.join(action_list)
	if len(all_dialogue) == 0 or len(all_action) == 0:
		return []
	dialogue_features = extract_features_sub(all_dialogue.lower())
	action_features = extract_features_sub(all_action.lower())
	chunk_summary_features = dialogue_action_length_features(dialogue_list, action_list)
	dialogue_type_features = get_dialogue_type_features(chunk)
	final_features = {}
	final_features.update(dialogue_features)
	final_features.update(action_features)
	final_features.update(chunk_summary_features)
	final_features.update(dialogue_type_features)
	for feature in final_features:
		final_features[feature + str(nth_chunk)] = final_features.pop(feature)
	return final_features
	#return dialogue_features + action_features +  chunk_summary_features + dialogue_type_features
	#genre_features = [1 if x in genre_dict[movie_name] else 0 for x in all_genres]



# change input to scenes
def extract_features_sub(text):
	## aggregate all dialogue, action
	#scenes = format_script(file_name)
	if len(text) > 0:
		language_complexity = {'flesch_reading_ease': textstat.flesch_reading_ease(text), 'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text), 'automated_readability_index': textstat.automated_readability_index(text)}
	else:
		#badD.write(movie_name + "\n")
		language_complexity = {'flesch_reading_ease': 0, 'flesch_kincaid_grade': 0, 'automated_readability_index': 0}
	lexical_diversity = find_lex_d(text)
	sentiment = extract_senti_wordnet(text)
	#print sentiment
	inquirer_features = general_inquirer_features(text)
	final_features = {}
	final_features.update(language_complexity)
	final_features.update(lexical_diversity)
	final_features.update(sentiment)
	final_features.update(inquirer_features)
	#final_features = language_complexity + lexical_diversity + sentiment + inquirer_features
	return final_features

# for each group of features, we return a tup
#extract_features("Revenant, The")

#extract_features('')

#extract_features('imsdb_scripts/Revenant, The.txt', 'Revenant, The')









"""def split(a, n):
    k, m = len(a) / n, len(a) % n
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in xrange(n))

scenes = format_script()
count_vect = CountVectorizer()
all_scene_lists = []
# extract lines of dialogue 
for scene in scenes:
	full_dialogue_strings = [line[0] for line in scene if line[1] == 'dialogue']
	if len(full_dialogue_strings) > 0:
		all_scene_lists.append(full_dialogue_strings)

split_script = list(split(all_scene_lists, 10))
split_script = [' '.join(elem) for elem in split_script]
print split_script"""

