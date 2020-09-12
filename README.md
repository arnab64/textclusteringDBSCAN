# Text Clustering using Density Based Spatial Clustering (DBSCAN)

The following functionalities are being added to this code (estimated completion by 10/01/2020):
- Cluster files into a new folder structure with cluster labelled folders
- Add support for performing clustering on external datasets
- Add TFIDF support for large datasets
- Add visualization for clusters in plotly


Introduction
-------------
This is a project done by me in 2015 for NLP class, while I was in undergrad. It's been more than 5 years, and now I am trying to bring this project a bit upto the latest standards in NLP, while still keeping it simple as a NLP class project.

2015: This project, I performed document clustering using the DBSCAN clustering algorithm. I clustered documents based on topic similarity. The basic idea is simple, we first find the scores of each word in each document using *TFIDF* and then we compute the distance between two documents using a distance measure to find the difference between the scores of words of the documents.

Steps
---------
The steps involved in document clustering implemented in this project are:
- Remove punctuations from all the source text files.
- Score each word inside documents using TF-IDF.
- Find the distance between documents using Euclidean distance.
- Perform clustering of documents using DBSCAN based on inter document distances found in the previous step.
- Evaluate the performance of clustering.   

The corresponding files for all these steps are available in this repository.

Dataset
--------- 
The *source* folder
- Contains 60 text files from 60 topics belonging to 6 different categories.
- i.e. 10 documents from each category.

Usage
-------
All of the input files of all known categories are inside the *source* folder. After that, the first thing we need to do is to remove punctuations using the code *1_rempunct.py*. The processed files after this step are available in the *stops_removed* folder.
```
python 1_rempunct.py
```

After the removal of punctuations and stopwords, the weights of all terms in each document need to be found out. We apply *term-frequency inverse document frequency (TFIDF)* on all the files inside the folder *stops_removed*. The processed files are stored in the folder *dest*.
```
python 2_alltfidf.py
```

After the weights of all the words in each document is computed, we then find the Euclidean distance between each of the documents, using their respective weights. The distance between all the documents are stored in the file *scores.txt*. 
```
python 3_distance.py
```

After the distance between files are found, we perform the clustering using DBSCAN, which is performed by the code *4_cluster.py*. After which the results of the clustering is evaluated, by comparing with the real known clusters. The clustering performance is evaluated using **Adjusted Rand Index**, and it is d`one by the code *5_result_evaluation.py*. These two tasks are done by the code *6_main_module.py*. This code also finds out which is the best threshold for performing the clustering, as DBSCAN takes the *threshold* as input from the user.
```
python 6_main_module.py
```
