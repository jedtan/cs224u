from extract_features import extract_features
from sklearn import naive_bayes
from sklearn.metrics import confusion_matrix
import csv

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


with open('imsdb_ratings.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile)
	for row in spamreader:
		if get_status(row) == "Good" or get_status(row) == "Bad":
			
			file_name = file_base + row[0] + ".txt"
			print file_name
			features = extract_features(file_name, row[0])
			if features is not None:
				feat_list.append(features)
				film_list.append(row[0])
				qual_list.append(get_status(row))


#sample classifier
	for i, item in enumerate(film_list):
  		film_list_file.write("%s\n" % item)
  		feat_list_file.write("%s\n" % ', '.join([str(feature) for feature in feat_list[i]]))
  		qual_list_file.write("%s\n" % qual_list[i])


	classifier = naive_bayes.GaussianNB()
	model = classifier.fit(feat_list, qual_list)
	prediction = model.predict(feat_list)
	print confusion_matrix(qual_list, prediction)