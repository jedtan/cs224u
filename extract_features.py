from format_imsdb import format_script
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from textstat.textstat import textstat
import csv

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

print genre_dict


# tf-idf code
all_genres = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Drama", "Family", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Short", "Thriller", "War"]

def extract_features(movie_name, file_name):
	## aggregate all dialogue, action
	scenes = format_script(file_name)

	all_lines = [line[0]  for scene in scenes for line in scene if line[1] == 'dialogue']
	all_text = ' '.join(all_lines)

	all_action = [line[0]  for scene in scenes for line in scene if line[1] == 'action']
	all_action_text = ' '.join(all_action)

	dialogue_scores = (textstat.flesch_reading_ease(all_text), textstat.flesch_kincaid_grade(all_text), textstat.automated_readability_index(all_text))
	action_scores = (textstat.flesch_reading_ease(all_action_text), textstat.flesch_kincaid_grade(all_action_text), textstat.automated_readability_index(all_action_text))

	## reading scores for dialogue/action
	print dialogue_scores
	print action_scores

	print genre_dict[movie_name]
	genre_features = [1 if x in genre_dict[movie_name] else 0 for x in all_genres]
	print genre_features

extract_features("Revenant, The")

#extract_features('')






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

