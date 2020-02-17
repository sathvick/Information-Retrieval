#https://joernhees.de/blog/2015/08/26/scipy-hierarchical-clustering-and-dendrogram-tutorial/
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from scipy.cluster.hierarchy import fcluster
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
    return ddata

df = pd.read_table('tweets/relevant_tweets.txt')
df.columns = ['tweet']
documents = df['tweet']

query = "love food hurricane harvey texas houston flood road drink water bottle"
tvec = TfidfVectorizer(vocabulary=query.split(' '))
tvec_tfidf = tvec.fit_transform(documents)
tvec_tfidf_as_nparray = tvec_tfidf.toarray()

good_documents = []
for d in tvec_tfidf_as_nparray:
    if sum(d) > 1:
        good_documents.append(d)
        # np.append(good_documents, d)

# generate the linkage matrix
# Z = linkage(good_documents, method='ward')
# Z = linkage(good_documents, method='single', metric='cosine')
# Z = linkage(good_documents, method='centroid',  metric='cosine')
# Z = linkage(X, 'centroid')
Z = linkage(good_documents, method='complete', metric='cosine')
# Z = linkage(good_documents, method='average', metric='cosine')
# Z = linkage(X, 'average')

print(Z)

# calculate full dendrogram
plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('tf-idf vector index')
plt.ylabel('distance')
# dendrogram(
#     Z,
#     leaf_rotation=90.,  # rotates the x axis labels
#     leaf_font_size=8.,  # font size for the x axis labels
# )
# dendrogram(
#     Z,
#     truncate_mode='lastp',  # show only the last p merged clusters
#     p=12,  # show only the last p merged clusters
#     show_leaf_counts=False,  # otherwise numbers in brackets are counts
#     leaf_rotation=90.,
#     leaf_font_size=12.,
#     show_contracted=True,  # to get a distribution impression in truncated branches
# )
# dendrogram(
#     Z,
#     truncate_mode='lastp',  # show only the last p merged clusters
#     p=20,  # show only the last p merged clusters
#     leaf_rotation=90.,
#     leaf_font_size=12.,
#     show_contracted=True,  # to get a distribution impression in truncated branches
# )

max_d = 21
fancy_dendrogram(
    Z,
    # orientation='right',
    truncate_mode='lastp',  # show only the last p merged clusters
    p=20,  # show only the last p merged clusters
    leaf_rotation=90.,
    leaf_font_size=12.,
    show_contracted=True,  # to get a distribution impression in truncated branches
    max_d=max_d,  # plot a horizontal cut-off line

)

plt.show()

####
# max_d = 50
# clusters = fcluster(Z, max_d, criterion='distance')
# clusters
#
# ## visualize the result clusters
# plt.figure(figsize=(10, 8))
# plt.scatter(X[:,0], X[:,1], c=clusters, cmap='prism')  # plot points with cluster dependent colors
# plt.show()