FROM python

# Install nltk
RUN pip install nltk

# Download stopwords
RUN python -c "import nltk; nltk.download('stopwords')"