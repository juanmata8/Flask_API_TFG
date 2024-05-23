import pickle



from sklearn.feature_extraction.text import CountVectorizer
# save the iris classification model as a pickle file
model_pkl_file = "title_classifier_model.pkl" 

with open(model_pkl_file, 'rb') as file: 
   vect, clf = pickle.load(file)


def process_title(string_to_classify):
    X_to_classify = vect.transform([string_to_classify])
    predicted_class = clf.predict(X_to_classify)
    if(predicted_class[0] == 1):
        return "NO CLICKBAIT"
    elif(predicted_class[0] == 0):
        return "CLICKBAIT"
    else:
        return "UNKNOWN"
    

