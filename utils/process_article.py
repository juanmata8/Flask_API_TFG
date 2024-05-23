import pickle
from sklearn import metrics


from sklearn.feature_extraction.text import CountVectorizer

model_pkl_file = "news_naive_bayes_mod.pkl" 

with open(model_pkl_file, 'rb') as file: 
   vect, clf = pickle.load(file)




def process_article(string_to_classify):
    X_to_classify = vect.transform([string_to_classify])
    predicted_class = clf.predict(X_to_classify)
    return predicted_class

