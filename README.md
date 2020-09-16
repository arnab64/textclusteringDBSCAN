# textClusteringDBSCAN : Clustering text using Density Based Spatial Clustering (DBSCAN) using TF-IDF, FastText word vectors and other combined approaches

## NOTE: This is an improved library for clustering text. For original repository, please pull to the 'original' branch of this code. All further changes will be default, as a part of the change plan. 

### The following functionalities are being added to this code (estimated completion by 10/01/2020):
- Add support for performing clustering on csv files. 
- Ability to save cluster characteristic file for real time cluster inference boosting.
- Add TFIDF support for large datasets.
- Train FastText word vectors on categorical information from data, and use it to enhance real-time clustering.
- Use pre-trained GloVe word vectors, for real-time clustering enhancement
- Available as a Python repository and installable via pip

Introduction
-------------
This is a library for performing unsupervised lingustic functionalities based on textual fields on your data. An API will also be released for real-time inference. This is a small part of project fling, which is an opensource linguistic library designed for easy integration to applications. 

Primary functionalities:
- Add tf-idf as a new column, for a dataset.
- Train word vectors on full training dataset, and categorical word vectors on categorical documents. 
- Apply DBSCAN based on (tf-idf, tf-idf with GloVe vectors enhanced, trained FastText word vectors)

*fastboardAI/fling*
https://github.com/fastboardAI/fling.git

Latest Developments tracked in
*arnab64/fling*
https://github.com/arnab64/fling.git

Usage
-------
Basic usage instructions. As the code is in development, it might not be stable.  More details will be added by 09/30/2020 for proper usage of the library.

*Reading data*
```python
from textclustering import utilities as ut
from textclustering import tfidfModule as tfm
```
For now, operations are performed in Pandas dataframes, and the file format we read is csv.
```python
#change operating folder      
os.chdir("/Users/arnabborah/Documents/repositories/textclusteringDBSCAN/scripts/")

#read the .csv data file using the dataProcessor class
rp = tfm.dataProcessor("../datasets/DataAnalyst.csv")
```

### using the generic TF-IDF module (unsupervised)
```python
#create a flingTFIDF object around the pre-processed daa
ftf = tfm.flingTFIDF(rp.dataInitialSmall,'Job Description')

# tokenization, customizable
ftf.smartTokenizeColumn()

# get Term Frequency of each document, and store add it as an object, in a new column
ftf.getTF()

# compute Inverse Document Frequencies across the entire vocabulary
ftf.computeIDFmatrix()

# get TFIDF, and store it as a new column in data, tf-idf
ftf.getTFIDF()

# compute sum of all tf-idf values and add it as a new column
ftf.createDistanceMetadata()
ftf.writeToFile()
```

### using the categeorical TF-IDF module (semi-supervised)
```python
from textclustering import categoricalCharacteristicModule as ccm

rp = dataProcessor("../datasets/DataAnalyst.csv")

# performing custom categorical operations on the data-frame
rp.customProcessData()

fcat = flingCategoricalTFIDF()
allfnames = ft.getallfilenames("/Users/arnabborah/Documents/repositories/textclusteringDBSCAN/processFiles/trainCatFiles")
ft.computeTFIDFallfiles(allfnames)
```

### adding pre-trained GloVe vectors
```python
from textclustering import flingPretrained as pre

dataProcessed = pd.read_pickle('../processFiles/data_tfidf_processed.pkl')
fdb = pre.flingPretrained(dataProcessed)
fdb.loadPretrainedWordVectors('glove')
fdb.addDocumentGloveVector()

# to get a sample of the distance distribution, where the first param is number of random documents 
db.getDistanceDistribution(200,'glove')
db.getDistanceDistribution(500,'glove')
```
