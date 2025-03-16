import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qt_material import apply_stylesheet
from data_manager import DataManager 
from modals import StudentForm, StatsWindow
from PyQt5.QtCore import QTimer
import pandas as pd

class FenPrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Étudiants")
        self.setFixedSize(900, 600)
        self.data_manager = DataManager()
        self.uit()
        self.load_table_data()
         # ⏳ Rafraîchir toutes les 7 secondes
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_table_data)
        self.timer.start(5000)

    def uit(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.form_layout = QVBoxLayout()
        self.layout.addLayout(self.form_layout, 1)

        self.recherche = QLineEdit()
        self.recherche.setPlaceholderText("Rechercher un étudiant")
        self.form_layout.addWidget(self.recherche)

        self.btn_rechercher = QPushButton("🔍 Rechercher")
        self.btn_rechercher.clicked.connect(self.rechercher_etudiant)
        self.form_layout.addWidget(self.btn_rechercher)

        self.btn_ajouter = QPushButton("➕ Ajouter/Modifier")
        self.btn_ajouter.clicked.connect(self.ouvrir_formulaire_etudiant)
        self.form_layout.addWidget(self.btn_ajouter)

        self.btn_supprimer = QPushButton("🗑️ Supprimer")
        self.btn_supprimer.clicked.connect(self.supprimer_etudiant)
        self.form_layout.addWidget(self.btn_supprimer)


        self.btn_moyenne = QPushButton("📊 Statistiques")
        self.btn_moyenne.clicked.connect(self.ouvrir_statistiques)
        self.form_layout.addWidget(self.btn_moyenne)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Email", "Matière", "Note"])
        self.layout.addWidget(self.table, 3)

    def load_table_data(self):
        self.table.setRowCount(0)
        self.data_manager.df = pd.read_csv("etudiants.csv")  # Recharger les données du CSV

        for _, row in self.data_manager.df.iterrows():
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for col, value in enumerate(row):
                self.table.setItem(row_position, col, QTableWidgetItem(str(value)))

    def supprimer_etudiant(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            student_id = int(self.table.item(selected_row, 0).text())
            self.data_manager.supprimer_etudiant(student_id)
            self.data_manager.df.to_csv("etudiants.csv", index=False)  # Save changes to CSV
            self.load_table_data()

    def rechercher_etudiant(self):
        nom = self.recherche.text()
        if nom:
            results = self.data_manager.rechercher_etudiant(nom)
            self.table.setRowCount(0)
            for _, row in results.iterrows():
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                for col, value in enumerate(row):
                    self.table.setItem(row_position, col, QTableWidgetItem(str(value)))

    def ouvrir_formulaire_etudiant(self):
        selected_row = self.table.currentRow()
        
        if selected_row != -1:  
            student_data = {
                "Nom": self.table.item(selected_row, 1).text(),
                "Prénom": self.table.item(selected_row, 2).text(),
                "Email": self.table.item(selected_row, 3).text(),
                "Matière": self.table.item(selected_row, 4).text(),
                "Note": self.table.item(selected_row, 5).text(),
            }
        else:
            student_data = None  

        form = StudentForm(self, student_data)

        if form.exec_():
            data = form.get_data()

            if selected_row != -1:
                student_id = int(self.table.item(selected_row, 0).text())
                self.data_manager.modifier_etudiant(student_id, data["Nom"], data["Prénom"], data["Email"], data["Matière"], data["Note"])
            else:
                self.data_manager.ajouter_etudiant(data["Nom"], data["Prénom"], data["Email"], data["Matière"], data["Note"])
            
            self.data_manager.df.to_csv("etudiants.csv", index=False)  # Save changes to CSV
            self.load_table_data()

    def ouvrir_statistiques(self):
        stats_window = StatsWindow(self)
        stats_window.exec_()

def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    fen = FenPrincipale()
    fen.show()
    app.exec_()

if __name__ == "__main__":
    main()
