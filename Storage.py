
# IMPORTING ESSENTIAL LIBRARIES
import sys
import os
import Parsing
import re
import time

# GETTING THE CURRENT PATH
ProjectPath = os.path.dirname(os.path.realpath('Storage.py'))
print(ProjectPath)

# DEFINING THE LIBRARY PATH
LibPath = ProjectPath + '/lib'
print(LibPath)

# ADDING PATH TO BE SEARCHED
sys.path.append(LibPath)

# CHANGING THE CURRENT WORKING DIRECTORY TO THE ProjectPath
os.chdir(ProjectPath)

# -----------------------------------------------------------------------
# INDEXING

# TO MEASURE THE INDEX FORMATION TIME
startTime = time.time()

# SPECIFYING THE COLLECTION TO INDEX
Collection = 'New Testament'

# USING A DICTIONARY FOR STORING POSTINGS LIST
Index = {}

# GOING TO THE COLLECTED DOCUMENTS DIRECTORY
print(ProjectPath + '/data/' + Collection)
os.chdir(ProjectPath + '/data/' + Collection)

# LIST OF THE FILES IN THE COLLECTION
Files = [File for File in os.listdir('.') if os.path.isfile(File)]

# READING AND PROCESSING THE DATA OF EVERY FILE
for File in Files:
    # SPLITING THE FILE IN LINES
    Data = open(File).read().splitlines()

    # CLEANING THE DATA
    Words = Parsing.Clean(Data)

    # REMOVING THE EXTENSION FROM THE FILE FOR STORAGE
    Name = re.match('(^[^.]*)', File).group(0)

    # ADDING WORDS TO THE INDEX
    Parsing.Index(Name, Words, Index)
print("\nINDEXING - TOTAL TIME TAKEN = " +
      str(time.time() - startTime) + " SEC.\n")


# -----------------------------------------------------------------------
# STORING THE INVERTED INDEX INTO THE DATABASE

# FOR MEASURING STORAGE TIME
startTime = time.time()

Parsing.Store(Index, Collection)

# PRINTING THE INVERTED INDEX
# ITERATING THROUGH THE DICTIONARY
for A in Index:
    print("[", A, " -> ", Index[A], "]")


print("\nSTORAGE - TOTAL TIME TAKEN = " +
      str(time.time() - startTime) + " SEC.\n")
