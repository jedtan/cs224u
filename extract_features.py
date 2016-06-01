from format_imsdb import format_script
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from textstat.textstat import textstat
from httplib2 import Http
from urllib import urlencode
from xml.etree.ElementTree import fromstring
import csv
from operator import itemgetter
from collections import Counter
import re

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
			inquirer_dict[row[0].lower()] = [elem for elem in row[2:185] if elem != '']
	return inquirer_dict

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

#print genre_dict

error_codes = ["'", 'E', 'T', 'D', 'Z']
http = Http()

def find_lex_d(text):
    data = {'input': text}
    response, content = http.request("http://lex-d.herokuapp.com", "POST", urlencode(data))
    if response['status'] != 200:
        if str(content)[2] in error_codes:
            print(content)                    # print error message if error
        else:
            return float(content)  # print Lexical diversity score
    else:
        print('Error 200 thrown from server')


# tf-idf code
all_genres = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Drama", "Family", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Short", "Thriller", "War"]

def extract_features(file_name, movie_name):
	print "hi"
	## aggregate all dialogue, action
	scenes = format_script(file_name)

	if scenes is None:
		return None

	all_lines = [re.sub(r'\([^)]*\)', '', line[0]) for scene in scenes for line in scene if line[1] == 'dialogue']
	all_text = ' '.join(all_lines)

	all_action = [line[0]  for scene in scenes for line in scene if line[1] == 'action']
	all_action_text = ' '.join(all_action)

	if len(all_text) > 0:
		dialogue_scores = (textstat.flesch_reading_ease(all_text), textstat.flesch_kincaid_grade(all_text), textstat.automated_readability_index(all_text))
	else:
		badD.write(movie_name + "\n")
		dialogue_scores = (0,0,0)

	if len(all_action_text) > 0:
		action_scores = (textstat.flesch_reading_ease(all_action_text), textstat.flesch_kincaid_grade(all_action_text), textstat.automated_readability_index(all_action_text))
	else:
		badA.write(movie_name + "\n")
		action_scores = (0,0,0)
	## reading scores for dialogue/action
	print dialogue_scores
	print action_scores

	genre_features = [1 if x in genre_dict[movie_name] else 0 for x in all_genres]

	lexical_diversity = [find_lex_d(all_text)]
	# Harvard General Inquirer
	inquirer_dict = general_inquirer_to_dict()
	word_list = all_text.split()
	word_counter = Counter(word_list)
	hgi_feature_dict = {}
	for word in word_counter:
		if word in inquirer_dict:
			for feature in inquirer_dict[word]:
				if feature not in hgi_feature_dict:
					hgi_feature_dict[feature] = word_counter[word]
				else:
					hgi_feature_dict[feature] += word_counter[word]
	for feature in hgi_feature_dict:
		hgi_feature_dict[feature] = float(hgi_feature_dict[feature])/len(word_list)

	final_features = dialogue_scores + action_scores + tuple(genre_features) + lexical_diversity
	return final_features, hgi_feature_dict

#extract_features("Revenant, The")

#extract_features('')

extract_features('imsdb_scripts/Revenant, The.txt', 'Revenant, The')









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

