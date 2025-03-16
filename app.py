from flask import Flask, render_template, request, redirect,jsonify
import pandas as pd
import os

app = Flask(__name__)
FILENAME = "etudiants.csv"

def charger_donnees():
    if not os.path.exists(FILENAME):
        df = pd.DataFrame(columns=["ID", "Nom", "Prénom", "Email", "Matière", "Note"])
        df.to_csv(FILENAME, index=False)
    return pd.read_csv(FILENAME)

@app.route('/api/etudiants')
def api_etudiants():
    try:
        df = pd.read_csv(FILENAME)  # Always read the latest data from the CSV file
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)})

# Sauvegarder les données
def sauvegarder_donnees(df):
    df.to_csv(FILENAME, index=False)

@app.route('/')
def index():
    df = pd.read_csv(FILENAME)  # Always read the latest data from the CSV file
    return render_template("index.html", etudiants=df.to_dict(orient='records'))

@app.route('/ajouter', methods=["GET", "POST"])
def ajouter_etudiant():
    if request.method == "POST":
        df = charger_donnees()
        nouvel_id = df["ID"].max() + 1 if not df.empty else 1
        nouvel_etudiant = {
            "ID": int(nouvel_id),
            "Nom": request.form["nom"],
            "Prénom": request.form["prenom"],
            "Email": request.form["email"],
            "Matière": request.form["matiere"],
            "Note": float(request.form["note"])
        }
        df = pd.concat([df, pd.DataFrame([nouvel_etudiant])], ignore_index=True)
        sauvegarder_donnees(df)
        return redirect('/')
    return render_template("ajouter.html")

@app.route('/supprimer/<int:id>')
def supprimer_etudiant(id):
    df = charger_donnees()
    df = df[df["ID"] != id]
    sauvegarder_donnees(df)
    return redirect('/')

@app.route('/stats')
def stats():
    df = pd.read_csv(FILENAME)  # Always read the latest data from the CSV file
    if df.empty:
        moyennes = {}
    else:
        moyennes = df.groupby("Matière")["Note"].mean().to_dict()
    return render_template("stats.html", moyennes=moyennes)

@app.route('/table')
def table():
    df = pd.read_csv(FILENAME)  # Always read the latest data from the CSV file
    return render_template("table.html", etudiants=df.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)
