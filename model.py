import spacy
import gensim
import pandas as pd
import numpy as np
from math import pi 
import math
import matplotlib.pyplot as plt
#from wordcloud import WordCloud

nlp = spacy.load('en_core_web_sm')
#stopwords = nlp.Defaults.stop_words

#user_bio = pd.read_csv("./sample_data/encoded_user_final_dataset.csv")
org_bio = pd.read_csv("org_dataset_age_cat.csv")
org_bio.rename(columns = {'Organization/ City Agency/ Division Name': 'Organization Name'}, inplace=True)

#user_bio.rename(columns = {'Unnamed: 0': 'User Index'}, inplace=True)
#user_bio.head()
#print("____________")
#org_bio.head()

# user_bio.iloc[specific_user]["Age"] --> 0
#specific_user = 111
#user_bio

def get_recommendations(user_data):

    long_lat_user = {
    "Manhattan": [40.7831, -73.9712],
    "Brooklyn" : [40.6782, -73.9442],
    "Bronx" : [40.8448, -73.8648],
    "Queens" : [40.7282, -73.7949],
    "Staten Island" : [40.5795, -74.1502]
    }

    #ref_sentence = user_bio.loc[user_bio['User Index'] == specific_user, "Biography"].iloc[0]
    ref_sentence = user_data["Bio"]
    priority1 = user_data['Pri1']
    priority2 = user_data['Pri2']
    priority3 = user_data['Pri3']

    

    stripped_ref_sentence = ref_sentence.replace('[','').replace(']','').replace('"','')
    stripped_ref_sentence #reference sentence that is stripped of extra things

    stripped_ref_sentence_vec = nlp(stripped_ref_sentence) #vectorizing tokens
    stripped_ref_sentence_vec

    all_docs = [nlp(str(row)) for row in org_bio["Interest Areas"]]
    #all_docs

    sims = []
    doc_id = []
    for i in range(len(all_docs)):
        sim = all_docs[i].similarity(stripped_ref_sentence_vec) 
        sims.append(sim)
        doc_id.append(i)
        sims_docs = pd.DataFrame(list(zip(doc_id, sims)), columns = ['doc_id', 'sims'])

    sims_docs_sorted = sims_docs.sort_values(by = 'sims', ascending=False)
    #sims_docs_sorted

    top5_sim_docs = org_bio.iloc[sims_docs_sorted['doc_id'][1:]] #getting the top 1-__ from the org_bio --> we would have names and all info
    #top5_sim_docs

    #print(user_bio[user_bio['User Index']==111]['Biography'].values)
    #print(user_bio[user_bio['User Index']==111]['Interests'].values)

    top_sim_scores = pd.concat([top5_sim_docs, sims_docs_sorted['sims'][1:]], axis = 1) #get 1 to end all info of organization --> ordered from highest to lowet sim

    #borough = user_bio.iloc[specific_user]["Borough"].capitalize()
    borough = user_data["Location"].capitalize()
    #print(borough)
    closest = []
    lonA = long_lat_user[borough][1]
    latA = long_lat_user[borough][0]


    # for i in range(len(top_sim_scores)):
    #   radius = 6371
    #   p = (math.pi / 180)
    #   lonB = top5_sim_docs['Longitude']
    #   latB = top5_sim_docs['Latitude']
    #   dist = (2 * radius) * math.asin(math.sqrt(0.5 - math.cos((latA - latB) * p)/2 + math.cos(latB * p) * Cos(latA * p) * (1 - Cos((lonA - lonB) * p)) / 2))
    # closest.append(dist)

    def haversine_distance(lat1, lon1, lat2, lon2):
        r = 6371
        phi1 = np.radians(lat1)
        phi2 = np.radians(lat2)
        delta_phi = np.radians(float(lat2) - lat1)
        delta_lambda = np.radians(lon2 - lon1)
        a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
        res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
        return np.round(res, 2)

    distances_km = []
    for row in top_sim_scores.itertuples(index=False):
        #print(row.Latitude)
        #print(type(row.Latitude))
        distances_km.append(
            haversine_distance(latA, lonA, row.Latitude, row.Longitude)
        )

    #distances_km.sort()
    dist_score = [0]*len(distances_km)
    for i in range(len(distances_km)):
        #print(math.isnan(distances_km[i]))
        #if(math.(distances_km[i]) == False):
        dist_score[i] = distances_km[i] / 20.0
        dist_score[i] = 1 - dist_score[i]
        if distances_km[i]>20:
            dist_score[i] = 0
        
        

    #print(dist_score)

    top_sim_scores['Distance Org To User'] = dist_score

    total_score = [0]*len(top_sim_scores)
    for i in range(len(top_sim_scores)):
        total_score[i] = dist_score[i]* top_sim_scores.iloc[i]['sims']

    top_sim_scores['Matching Score'] = total_score

    age_applied_to_sim = []
    #age_of_user = user_bio.iloc[specific_user]["Age"]
    age_of_user = user_data["Age"]
    for i in range(len(top_sim_scores)):
        #print(top_sim_scores.iloc[i]["Age Category"]) #prints the different age groups according to the most similarity to least similar
        if (top_sim_scores.iloc[i]["Age Category"] != int(age_of_user)):
            age_applied_to_sim.append(0.8)
        else:
            age_applied_to_sim.append(1)
    top_sim_scores["Age Score"] = age_applied_to_sim

    a = 0.7
    b = 0.2
    c = 0.1
    final_filter_score = [0] * len(top_sim_scores)

    for i in range(len(top_sim_scores)):
        final_filter_score[i] = top_sim_scores.iloc[i][user_data["Pri1"]]* a + top_sim_scores.iloc[i][user_data["Pri2"]]* b + top_sim_scores.iloc[i][user_data["Pri3"]]* c

    top_sim_scores['finalScoreAfterFilter'] = final_filter_score

    top_sim_scores = top_sim_scores.sort_values(by = 'finalScoreAfterFilter', ascending=False)

    org_dict = {}
    top5Name =[]
    top5Score =[]
    for i in range(5):
        if (top_sim_scores.iloc[i]['finalScoreAfterFilter'] == 'nan'):
            match_percent_round = 0
        else:
            match_percent_round = int(float("{:.2f}".format(top_sim_scores.iloc[i]['finalScoreAfterFilter']))*100)
        #match_percent_round = int(match_percent_round)
            top5Name.append(top_sim_scores.iloc[i]['Organization Name'])
            top5Score.append(match_percent_round)
    org_dict["Explainability of AI"] = "Based on your bio description and choice of preferences, we deployed a Machine Learning model using NLP to recommend top organizations matching your preferences."
    org_dict["Organization's Name"] = top5Name
    org_dict["Similarity Score"] = top5Score


    return org_dict
    #Explainable AI
    #print("Based on your bio description and choice of preferences, we deployed a Machine Learning model using NLP to recommend top organizations matching your preferences. \n User Interests : ", user_data["Bio"], "\n")

    #df_first_5 = top_sim_scores.head(5)
    #for row in df_first_5.itertuples(index=False):
        #print(row['Organization Name'])



#user1 = {}

#print(user1['Age'])

#get_recommendations(user1)