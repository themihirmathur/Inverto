
# IMPORTING ESSENTIAL LIBRARIES
from snowballstemmer import EnglishStemmer as es  # FOR STEMMING
from nltk.corpus import stopwords as Stopwords  # FOR GATHERING STOPWORDS
import re  # FOR EXPRESSION HANDLING
from pymongo import MongoClient  # FOR STORING InvertedIndex INTO MongoDB DATABASE

# STARTING MongoDB CLIENT
Client = MongoClient()
# NAMING THE CLIENT
DB = Client.Inverted_Index

# ELIMINATING STOPWORDS
StopWords = Stopwords.words('english')
p = re.compile('\w+')


def Clean(Data):
    # STORING DATA AS A SINGLE STRING
    Words = [Word for Word in ' '.join(Data).split(' ')]

    # SEARCHING FOR EVERY WORD
    Words = p.findall(' '.join(Words))

    # LOWERCASING
    Words = [Word.lower() for Word in Words]

    # STEMMING WORDS
    Words = [es().stemWord(Word) for Word in Words]

    # REMOVING STOPWORDS
    Words = [Word for Word in Words if Word not in StopWords]

    # RETURNING THE PROCESSED WORDS
    return Words


def Index(File, Words, Index):
    for position in range(len(Words)):
        Word = Words[position]

        # IF THE WORD IS NOT ADDED AS A KEY
        if Words[position] not in Index:
            Index[Word] = {'Term Frequency': 1,
                           'Document Frequency': 1,
                           'Document(s)': {File: {'Frequency': 1,
                                                  'Position(s)': [position]
                                                  }
                                           }
                           }

        # IF THE WORD IS ALREADY PRESENT AS A KEY
        else:
            Index[Word]['Term Frequency'] += 1

            # IF THE WORD IS NOT IN THE DOCUMENT
            if File not in Index[Word]['Document(s)']:
                Index[Word]['Document Frequency'] += 1
                Index[Word]['Document(s)'][File] = {'Frequency': 1,
                                                    'Position(s)': [position]}

            # IF THE WORD IS FOUND
            else:
                Index[Word]['Document(s)'][File]['Frequency'] += 1
                Index[Word]['Document(s)'][File]['Position(s)'].append(
                    position)

    # RETURNING THE INDEX
    return Index


# STORING THE INDEX INTO THE MongoDB DATBASE
def Store(Index, Folder):
    Collection = DB[Folder]
    for Word in Index:
        Collection.save({'_ID': Word, 'INFO': Index[Word]})
