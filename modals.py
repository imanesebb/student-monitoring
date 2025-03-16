from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from data_manager import DataManager

class StudentForm(QDialog):
    def __init__(self, parent=None, student_data=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter/Modifier Étudiant")
        self.setFixedSize(300, 250)

        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        self.nom = QLineEdit()
        self.prenom = QLineEdit()
        self.email = QLineEdit()
        self.matiere = QLineEdit()
        self.note = QLineEdit()
        
        self.form_layout.addRow("Nom:", self.nom)
        self.form_layout.addRow("Prénom:", self.prenom)
        self.form_layout.addRow("Email:", self.email)
        self.form_layout.addRow("Matière:", self.matiere)
        self.form_layout.addRow("Note:", self.note)

        self.layout.addLayout(self.form_layout)

        self.btn_save = QPushButton("Enregistrer")
        self.btn_save.clicked.connect(self.accept)  
        self.layout.addWidget(self.btn_save)
        if student_data:
            self.nom.setText(student_data.get("Nom", ""))
            self.prenom.setText(student_data.get("Prénom", ""))
            self.email.setText(student_data.get("Email", ""))
            self.matiere.setText(student_data.get("Matière", ""))
            self.note.setText(str(student_data.get("Note", "")))
        
    def get_data(self):
        return {
            "Nom": self.nom.text(),
            "Prénom": self.prenom.text(),
            "Email": self.email.text(),
            "Matière": self.matiere.text(),
            "Note": self.note.text(),
        }


class StatsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Statistiques des Notes")
        self.setFixedSize(400, 300)

        self.layout = QVBoxLayout(self)
        self.data_manager = DataManager()

        # Get the unique subjects (matieres)
        matieres = self.data_manager.df["Matière"].unique()

        # Create the table widget
        self.table = QTableWidget(len(matieres), 2)  # 2 columns: Matière and Moyenne
        self.table.setHorizontalHeaderLabels(["Matière", "Moyenne"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Disable editing

        # Populate the table with data
        for row, matiere in enumerate(matieres):
            moyenne = self.data_manager.calculer_moyenne(matiere)
            self.table.setItem(row, 0, QTableWidgetItem(matiere))  # Matière column
            self.table.setItem(row, 1, QTableWidgetItem(f"{moyenne:.2f}"))  # Moyenne column

        # Add the table to the layout
        self.layout.addWidget(self.table)
