class Nurse(object):
    """
    Creates a nurse class containing:
    ID              [int],
    Password        [String],
    Access_level    [int]
    """
    def __init__(self, ID, Password, Access_level):
        self.ID = ID
        self.Password = Password
        self.Access_level = Access_level
    
    def run(self):
        return

    def ViewPresciption(self, patient):
        """Prints persciptoins."""
        # print("Dosage", patient.Medical.notes.Dosage) #Not finalized yet
        # print("Type", patient.Medical.notes.Type)
        # print("Creator", patient.Medical.notes.Creator)
    
    def ViewNotes(self, patient):
        """Prints notes."""
        # print("Notes: ", patient.Medical.notes.getText())
        # print("Author: ", patient.Medical.notes.getAuthor())

    def 