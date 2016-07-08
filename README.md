# textclusteringDBSCAN

Document clustering using DBSCAN. In this mini project, we clustered documents based on topic similarity. We have used the *DBSCAN clustering algorithm* for doing so. We also have used *TFIDF* for weighting of words inside documents.

The steps involved in document clustering implemented in this project are:
1. Remove punctuations from all the source text files.
2. Score each word inside documents using TF-IDF.
3. Find the distance between documents using Euclidean distance.
4. Perform clustering of documents using DBSCAN based on inter document distances found in the previous step.
5. Evaluate the performance of clustering.   

The corresponding files for all these steps are available in this repository.

Folders: 

SOURCE
- Contains 60 text files from 60 topics belonging to 6 different categories.
- i.e. 10 documents from each category.
