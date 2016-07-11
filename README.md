# Text Clustering using Density Based Spatial Clustering (DBSCAN)

Introduction
-------------
In this project, I performed document clustering using the DBSCAN clustering algorithm. I clustered documents based on topic similarity. The basic idea is simple, we first find the scores of each word in each document using *TFIDF* and then we compute the distance between two documents using a distance measure to find the difference between the scores of words of the documents.

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

After the weights of all the words in each document is computed, we then find the Euclidean distance between each of the documents, using their respective weights.
```
python 3_distance.py
```


