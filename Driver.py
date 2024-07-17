
# IMPORTING LIBRARIES
import sys, os
from PyQt5 import QtWidgets
from Browser import Ui_MainWindow
from Querying import CleanQuery, RankDocuments
from pymongo import MongoClient

# GETTING THE CURRENT PATH
ProjectPath = os.path.dirname(os.path.realpath('Driver.py'))

# DEFINING THE LIBRARY PATH
LibPath = ProjectPath + '/lib'

# ADDING PATH TO BE SEARCHED
sys.path.append(LibPath)

# CHANGING THE CURRENT WORKING DIRECTORY TO THE ProjectPath
os.chdir(ProjectPath)


# CONNECTING TO DATABASE FOR ACCESSING THE INVERTED INDEX
Client = MongoClient()
DB = Client.Inverted_Index

# Choose a folder containing documents
Folder = 'New Testament'
Collection = DB[Folder]

# --------------------------------------------------------------------
class Browser(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        
        # GETTING COMMANDS FROM UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # LINKING QUERY FUNCTION TO SEARCH BUTTON
        self.ui.pushButton.clicked.connect(self.Query)

    def Query(self):
        # CLEARING THE LIST
        self.ui.listWidget.clear()

        # GETTING WORDS FROM QUERY
        Words = CleanQuery(self.ui.lineEdit.text())
        
        # FOR INFO COLLECTION OF QUERY
        Index = {}
        
        for Word in Words:
            Index[Word] = Collection.find({'_ID' : Word})[0]['INFO']

        # RANKING THE DOCs
        Results = RankDocuments(Index, Words)
        
        # DISPLAYING THE RESULT
        for Result in Results:
            self.ui.listWidget.addItem(Result[0]+' : '+str(round(Result[1], 2)))
            
if __name__ == "__main__":
    App = QtWidgets.QApplication(sys.argv)
    MyApp = Browser()
    MyApp.show()
    sys.exit(App.exec_())
