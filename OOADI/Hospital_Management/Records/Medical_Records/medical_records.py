from Notes.notes import Note
from Prescriptions.prescriptions import Prescription 

class Medical_Record():
    """Medical Record contains a list of patients prescriptions and notes.
    """
    def __init__(self, prescriptionList, note):
        self.prescriptionList = prescriptionList
        self.noteList = noteList

    def createNote(self, author, text):
        note = Note(author, text)
        self.noteList.append(note)

    def createPrescription(self, medicin_name, dosage, prescriber, price):
        recept = Prescription(medicin_name, dosage, prescriber, price)
        self.prescriptionList.append(recept)


    def list_prescriptions(self):
        for prescript in self.prescriptionList:
            print(prescript)

    def list_notes(self):
        pass
