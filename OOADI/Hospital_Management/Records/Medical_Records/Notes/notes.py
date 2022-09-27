from ..medical_records import Medical_Record
class Note(Medical_Record):
    def __init__(self, text, author):
        self.test = test
        self.author = self.ID

    # Setter and getter for the text in the Note
    def setText(self, text):
        self.text = text
    def getText(self):
        return self.text

    # Getter for author - no setter for this one.
    def getAuthor(self):
        return self.author

    
