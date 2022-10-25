from ..Medical_Records.medical_records import Medical_Record
from ..Financial_Records.financial_records.py import Financial_Record

class Patient(object):
    """
    Patient class created with the following:
    ID          [int], 
    Age         [int], 
    Gender      [int], 
    Name        [string], 
    Medical     [tuple] (Prescription, Notes),
    Financial   [tuple] (Card_Info, Balance)
    """
    def __init__(self, ID, Age, Gender, Name, Medical, Financial):

            # Argument check
            assert type(ID)==str, f"ID has to be a string"
            assert type(Age)==int and Age>0, f"Age has to be an int higher than 0" 
            assert type(Gender)==int and Gender<=1 and Gender>=0, f"Gender has to be 0-1 (0 female and 1 male)"
            assert type(Name)==str, f"Name has to be a string(unless it is Elon Musk's child)"
            assert type(Medical)==tuple and len(Medical)==2, f"Medical has to be a tuple with (Prescription, Notes)"
            assert type(Financial)==tuple and len(Financial)==2, f"Financial has to be a tuple with (Card_Info, Balance)"

            # Set attributes
            self.ID = ID
            self.Age = Age
            self.Gender = Gender
            self.Name = Name
            self.Medical = Medical_Record(Medical[0], Medical[1])
            self.Financial = Financial_Record(Financial[0], Financial[1])


    def run(self):
        return