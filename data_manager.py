import pandas as pd

class DataManager:
    def __init__(self, file="etudiants.csv"):
        self.file = file
        self.load_data()
    
    def load_data(self):
        try:
            self.df = pd.read_csv(self.file)
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=["ID", "Nom", "Prénom", "Email", "Matière", "Note"])
            self.sauvegarder()

    def sauvegarder(self):
        self.df.to_csv(self.file, index=False)

    
    def modifier_etudiant(self, id, nom, prenom, email, matiere, note):
    # Convertir la note en float pour éviter l'erreur
        note = float(note)  # Assure-toi que note est bien un float
        self.df.loc[self.df["ID"] == id, ["Nom", "Prénom", "Email", "Matière", "Note"]] = [nom, prenom, email, matiere, note]
        self.sauvegarder()

                
         
    def ajouter_etudiant(self, nom, prenom, email, matiere, note):
        if not self.df.empty:
            last_id = self.df["ID"].max()  
        else:
            last_id = 0  

        new_id = last_id + 1  

        new_student = pd.DataFrame([[new_id, nom, prenom, email, matiere, note]], 
                                columns=self.df.columns)
        
        self.df = pd.concat([self.df, new_student], ignore_index=True)
        self.sauvegarder()

    def supprimer_etudiant(self, id):
        self.df = self.df[self.df["ID"] != id]
        self.sauvegarder()

    def rechercher_etudiant(self, nom):
        return self.df[self.df["Nom"].str.contains(nom, case=False, na=False)]     

    def calculer_moyenne(self, matiere):
        notes = self.df[self.df["Matière"] == matiere]["Note"].astype(float)
        return notes.mean() if not notes.empty else 0
      


