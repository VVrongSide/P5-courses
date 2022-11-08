class Doctor:
    def __init__(self, ID: str, Password: str, Access_level: int):
        # Assert dominance to hide weakness
        assert Access_level > 0, f" Access_level {Access_level} needs to be greater than 0"
        assert Access_level <= 5, f" Access level {Access_level} needs to be less than 6" 

        # Attributes initialised
        self.ID = ID
        self.Password = Password
        self.Access_level = Access_level
        

    def Prescribe(self, prescriptionID, Type, dosage):
        prescriptionID = Prescription(Type, dosage, self.ID)
        return prescriptionID

    def view_prescription(self, prescriptionID):

        print(prescriptionID.Type)
        print(prescriptionID.dosage)
        print(prescriptionID.creator)        

        return 

    def edit_prescription(prescriptionID, Type, dosage):
        prescriptionID.Type = Type
        prescriptionID.dosage = dosage        

        return

    def get_ID():
        return self.ID

    def get_Access_level():
        return self.Access_level


doctor1 = Doctor("numselæge", "1234", 5)

recept1 = doctor1.Prescribe(1, "peramol", 20)
