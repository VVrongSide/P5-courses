from ..medical_records import Medical_Record
class Note(Medical_Record):
    def __init__(self, author, text):
        self.author = author
        self.test = test
        
    # Setter functions for Note class
    def setText(self, text):
        self.text = text
    
    # Getter functions for Note class
    def getAuthor(self):
        return self.author
    def getText(self):
        return self.text

    
