from build_features import *
from sklearn import linear_model
from random import sample

total_size = 20
test_size = 5

random_values = sample(range( total_size), test_size)

film_list, qual_list, feat_list = build_features(total_size)
print film_list
print qual_list
print feat_list

film_test_set = [film_list[i] for i in random_values]
film_train_Set = [elem for elem in film_list if elem not in film_test_set]
qual_test_set = [qual_list[i] for i in random_values]
qual_train_Set = [elem for elem in qual_list if elem not in film_test_set]
feat_test_set = [feat_list[i] for i in random_values]
feat_train_Set = [elem for elem in feat_list if elem not in film_test_set]



"""
from sklearn.linear_model import LogisticRegression
def fit_maxent_classifier(X, y):    
    mod = LogisticRegression(fit_intercept=True)
    mod.fit(X, y)
    return mod

fit_maxent_classifier(feat_list, qual_list)

#sample linear sgd classifier
X = np.array(feat_list)
Y = np.array(qual_list)
clf = linear_model.SGDClassifier()
clf.fit(X, Y)
print clf.coef_

#sample classifier
for i, item in enumerate(film_list):
		film_list_file.write("%s\n" % item)
		feat_list_file.write("%s\n" % ', '.join([str(feature) for feature in feat_list[i]]))
		qual_list_file.write("%s\n" % qual_list[i])


classifier = naive_bayes.GaussianNB()
model = classifier.fit(feat_list, qual_list)
prediction = model.predict(feat_list)

print confusion_matrix(qual_list, prediction)"""