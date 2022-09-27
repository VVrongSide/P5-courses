from ..medical_records import Medical_Record

class Prescription(Medical_Record,Doctor):
    def __init__(self,medicin_name, dosage, prescriber, price):
        self.medicin_name = medicin_name
        self.dosage = dosage
        self.prescriber = Doctor.getID()
        self.price = price
    
    # Getter functions for attributes
    def getMedicinName(self):
        return self.medicin_name

    def getDosage(self):
        return self.dosage
    
    def getPrescriber(self):
        return self.prescriber

    def getPrice(self):
        return self.price

    # Setter function for attributes
    def setMedicinName(self, name):
        self.medicin_name = medicin_name

    def setDosage(self, dosage):
        self.dosage = dosage
    
    def setPrescriber(self, prescriber):
        self.prescriber = prescriber

    def setPrice(self):
        self.price = price
