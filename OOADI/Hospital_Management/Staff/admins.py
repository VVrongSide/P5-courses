class Admin(object):
    """
    Admin class created with the following:
    ID              [int],
    Password        [string],
    Access_level    [int],
    patient         [list] (ID, Age, Gender, Name, Medical, Financial)
    """

    def __init__(self, ID, Password, Access_level):
        self.ID = ID
        self.Password = Password
        self.Access_level = Access_level

    def run(self):
        return

    def newPatient(self, patient):
        patient = Patient(patient[0], patient[1], patient[2], patient[3], patient[4], patient[5])
        return patient