# tutorial  http://madhugnadig.com/articles/machine-learning/2017/03/04/implementing-k-means-clustering-from-scratch-in-python.html
# repository: https://github.com/madhug-nadig/Machine-Learning-Algorithms-from-Scratch/blob/master/K%20Means%20Clustering.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt, mpld3
from matplotlib import style
style.use('ggplot')
from sklearn.decomposition import PCA

class K_Means:
    def __init__(self, k=3, tolerance=0.0001, max_iterations=500):
        self.k = k
        self.tolerance = tolerance
        self.max_iterations = max_iterations

    def fit(self, data):
        self.centroids = {}
        # initialize the centroids, the first 'k' elements in the dataset will be our initial centroids
        for i in range(self.k):
            self.centroids[i] = data[i]
        # begin iterations
        for i in range(self.max_iterations):
            self.classes = {}
            for i in range(self.k):
                self.classes[i] = []

            # find the similarity distance between the point and cluster; choose the nearest centroid
            for features in data:
            #    print(features)
              #distances = [np.linalg.norm((features - self.centroids[centroid])) for centroid in self.centroids]
              distances = [self.calculate_consine_similarity(features , self.centroids[centroid]) for centroid in self.centroids]
              print(distances)
              classification = distances.index(max(distances))
              print(classification)
              self.classes[classification].append(features)
              previous = dict(self.centroids)
            #print(previous)
            # average the cluster datapoints to re-calculate the centroids
            for classification in self.classes:
                self.centroids[classification] = np.average(self.classes[classification], axis=0)
            isOptimal = True

            for centroid in self.centroids:
                original_centroid = previous[centroid]
                curr = self.centroids[centroid]

                #if np.sum((curr - original_centroid) / original_centroid * 100.0) > self.tolerance:
                 #   isOptimal = False

            # break out of the main loop if the results are optimal, ie. the centroids don't change their positions much(more than our tolerance)
            if isOptimal:
                break

    def calculate_consine_similarity(self, vec1, vec2):
       # form vector for similarity
       sim = cosine_similarity([vec1], [vec2])
       sim1 = sim[0]
        #print(sim1)
       return sim1[0]

    def pred(self, data):
	    distances = [self.calculate_consine_similarity(data ,self.centroids[centroid]) for centroid in self.centroids]
	    classification = distances.index(max(distances))
	    return classification

def main():
    df = pd.read_table('tweets/relevant_tweets.txt')
    df.columns = ['tweet']
    documents = df['tweet']
    #print(df)
    # print(documents)
    query = "love food hurricane harvey texas houston flood road drink water bottle"
    tvec = TfidfVectorizer(vocabulary=query.split(' '))
    tvec_tfidf = tvec.fit_transform(documents)
    tvec_tfidf_as_array = np.array(tvec_tfidf.toarray())
    #print(tvec_tfidf_as_array[10111])
    good_documents = []
    for d in tvec_tfidf_as_array:
        if sum(d) >= 0.5:
            good_documents.append(d)
    #print(good_documents)
    X = np.array(good_documents)
    # print(X)
    # km = K_Means(3)  #
    # km.fit(X)
    # ###PCA
    # from sklearn.decomposition import PCA
    # pca = PCA(n_components=2).fit(X)
    # pca_2d = pca.transform(X)

    # Visualize the results on PCA-reduced data
    reduced_data = PCA(n_components=2).fit_transform(X)
    km = K_Means(3)  #
    km.fit(reduced_data)

    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = .02  # point in the mesh [x_min, x_max]x[y_min, y_max].
    # Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    # Obtain labels for each point in mesh. Use last trained model.
    Z = km.pred(np.c_[xx.ravel(), yy.ravel()])
    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1)
    plt.clf()
    plt.imshow(Z, interpolation='nearest',extent=(xx.min(), xx.max(), yy.min(), yy.max()),cmap=plt.cm.Paired,aspect='auto', origin='lower')
    plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
    # Plot the centroids as a white X
    centroids = km.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1],marker='x', s=169, linewidths=3,color='w', zorder=10)
    plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n''Centroids are marked with white cross')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())
    plt.show()




if __name__ == "__main__":
     main()