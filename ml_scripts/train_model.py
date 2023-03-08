import pandas as pd
import pickle
import os
from bertopic import BERTopic
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import IncrementalPCA
from bertopic.vectorizers import OnlineCountVectorizer

name_folder = "model_01"
os.mkdir(name_folder)
dialogs = pd.read_pickle('./data/all_docs_clean.pkl')
dialogs = dialogs.iloc[0:50]

#Slice corpus in smaller documents
all_docs = dialogs['msg'].values.tolist()
doc_chunks = [all_docs[i:i+100000] for i in range(0, len(all_docs), 100000)]

#Prepare sub-models for online learning
umap_model = IncrementalPCA(n_components=30)
cluster_model = MiniBatchKMeans(n_clusters=30, random_state=0)
vectorizer_model = OnlineCountVectorizer(stop_words="english", decay=.01, delete_min_df=10)

# Initiate BERTopic
topic_model = BERTopic(
    umap_model=umap_model,
    hdbscan_model=cluster_model,
    vectorizer_model=vectorizer_model,
    nr_topics="auto"
    )

#Start model training
alltopics = []
#counter = 0
for docs in doc_chunks:
    #counter = counter+1
    topic_model.partial_fit(docs)
    alltopics.extend(topic_model.topics_)
    #fig = topic_model.visualize_barchart(top_n_topics = 30)
    #fig.write_html("./"+ name_folder +"/barchart_"+ str(counter) + ".html")
    #top_hier = topic_model.visualize_hierarchy()
    #top_hier.write_html("./"+ name_folder +"/top_hierarchy_" + str(counter) + ".html")

topic_model.topics_ = alltopics

#Save model
topic_model.save("./"+ name_folder +"/BERT_model")
topics, pred = topic_model.transform(docs)
pickle.dump(topics, open( "./"+ name_folder +"/topics.pickle", "wb" ) )

print("done")

