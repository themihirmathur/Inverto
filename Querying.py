
# IMPORTING ESSENTIAL LIBRARIES
from math import log
from snowballstemmer import EnglishStemmer as es # FOR STEMMING
from nltk.corpus import stopwords as Stopwords # GETTING A COLLECTION OF STOPWORDS
import re # REGULAR EXPRESSION

# PREPROCESSING THE QUERY TERM
def CleanQuery(String):
    # ACCEESSING STOPWORDS
    StopWords = Stopwords.words('english')
    
    # EXPRESSION EDITING
    p = re.compile('\w+')

    # GOING THROUGH ALL THE WORDS
    Words = p.findall(String)

    # LOWERCASING THE QUERY
    Words = [Word.lower() for Word in Words]

    # STEMMING
    Words = [es().stemWord(word) for word in Words]
    
    # REMOVING STOPWORDS
    Words = [Word for Word in Words if Word not in StopWords]
    
    # RETURNING PROCESSED QUERY
    return Words

# RANKING DOCUMENTS
def RankDocuments(Index, Words):
    Rankings = {}
    
    for Word in Words:
        for Document in Index[Word]['Document(s)'].keys():
            
            # TF-IDF ALGORITHM
            TF = Index[Word]['Document(s)'][Document]['Frequency']
            
            if TF > 0:
                TF = 1 + log(TF)
            else:
                TF = 0
            
            # STORING THE RANKINGS
            if Document not in Rankings:
                Rankings[Document] = TF
            else:
                Rankings[Document] += TF

    # SORTING THE RESULTS
    Rankings = list(reversed(sorted(Rankings.items(), key=lambda x: x[1])))

    # RETURNING THE RANKING
    return Rankings

    
