FROM python

# Install nltk
RUN pip install nltk

# Download stopwords
RUN python -c "import nltk; nltk.download('stopwords')"

RUN git clone https://github.com/arnab64/textclusteringDBSCAN.git

# To build it 
# docker build -t my_image .

# To start in bash
# docker run -it my_image /bin/bash