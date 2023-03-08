import pandas as pd
from bertopic import BERTopic
from scipy.cluster import hierarchy as sch

name_folder = "model_01"

# load trained model and data
bertopic_model = BERTopic.load('./' + name_folder + '/BERT_model')
corpus = pd.read_pickle('./data/all_docs_clean.pkl')
corpus = corpus['msg'].values.tolist()

# Hierarchical topics
linkage_function = lambda x: sch.linkage(x, 'centroid', optimal_ordering=True)
hierarchical_topics = bertopic_model.hierarchical_topics(corpus, linkage_function=linkage_function)

fig_cluster = bertopic_model.visualize_hierarchy(hierarchical_topics=hierarchical_topics)
fig_cluster.write_html("./"+ name_folder +"/hierarchicalTopics.html")

#barchart topics visualize the most frequent topics
fig_barchart = bertopic_model.visualize_barchart(top_n_topics = 15)
fig_barchart.write_html("./"+ name_folder +"/BarChart.html")

## Change representation of the topics 
topic_labels = bertopic_model.generate_topic_labels(nr_words=10,
                                                    topic_prefix=False,
                                                    word_length=10,
                                                    separator=", "
                                                    )

bertopic_model.set_topic_labels(topic_labels)
bertopic_model.save("./"+ name_folder +"/BERT_model_rep")

print("done")