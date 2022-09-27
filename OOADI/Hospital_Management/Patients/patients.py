from ..Medical_Records.medical_records import Medical_Record
from ..Financial_Records.financial_records.py import Financial_Record

class Patient(object):
    """
    Patient class created with the following:
    ID          [int], 
    Age         [int], 
    Gender      [int], 
    Name        [string], 
    Medical     [tuple] (Card_Info, Balance),
    Financial   [tuple] (Prescription, Notes)
    """
    def __init__(self, ID, Age, Gender, Name, Medical, Financial):
            self.ID = ID
            self.Age = Age
            self.Gender = Gender
            self.Name = Name
            self.Medical = Medical_Record(Medical[0], Medical[1])
            self.Financial = Financial_Record(Financial[0], Financial[1])

    def run(self):
        return