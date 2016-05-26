from extract_features import extract_features
from sklearn import naive_bayes
from sklearn.metrics import confusion_matrix
import csv
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

film_list = []
feat_list = [] 
qual_list = []

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

list_of_hgi_features_dicts = []
counter = 0
with open('imsdb_ratings.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile)
	for row in spamreader:
		if get_status(row) == "Good" or get_status(row) == "Bad":
			
			file_name = file_base + row[0] + ".txt"
			print file_name
			features, hgi_features = extract_features(file_name, row[0])
			list_of_hgi_features_dicts.append(hgi_features)
			if features is not None:
				feat_list.append(features)
				film_list.append(row[0])
				qual_list.append(get_status(row))
		counter += 1
		if counter == 10:
			break

vectorizer = DictVectorizer()
hgi_feat_list = vectorizer.fit_transform(list_of_hgi_features_dicts).toarray()
hgi_feat_list = preprocessing.scale(hgi_feat_list)

for idx, row in enumerate(hgi_feat_list):
	feat_list[idx] = feat_list[idx] + tuple(row)

# get list
'''
hgi_feature_dicts_summary = {}
features = list(set([key for key in keys for keys in [keys for keys in [hgi_feature_dict.keys() for hgi_feature_dict in list_of_hgi_features_dicts]]]))
for feature in features:
	hgi_feature_dicts_summary[feature] = [hgi_feature_dict[feature] for hgi_feature_dict in list_of_hgi_features_dicts if feature in hgi_feature_dict]

list_of_hgi_features_dicts_standardized = []
for hgi_features_dict in list_of_hgi_features_dicts:
	curr_hgi_features_dict = {}
	for feature in hgi_features_dict:
		feature_mean = np.mean(hgi_feature_dicts_summary[feature])
		feature_std = np.std(hgi_feature_dicts_summary[feature])
		curr_hgi_features_dict[feature] = (hgi_features_dict[feature] - feature_mean)/feature_std
	list_of_hgi_features_dicts_standardized.append(curr_hgi_features_dict)
'''
#sample classifier

	classifier = naive_bayes.GaussianNB()
	model = classifier.fit(feat_list, qual_list)
	prediction = model.predict(feat_list)
	print confusion_matrix(qual_list, prediction)