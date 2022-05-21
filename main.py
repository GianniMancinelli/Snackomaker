from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import json
import json





app = Flask(__name__)


@app.route("/")
def index():
    about_link = url_for("index")
    return render_template("index.html", link=about_link)

@app.route("/menu")
def menu():
    about_link = url_for("menu")
    return render_template("menu.html", link=about_link)

@app.route("/statistic")
def statistic():
    about_link = url_for("statistic")
    return render_template("statistik.html", link=about_link)

#kann mann löschen
#@app.route('/menu', methods=["GET", "POST"]) #formular erstellt bzw. verknüfung, mit get und post wird entgegengenommen und wiedergegeben
#def formularmenu():
    #if request.method == "POST":
        #mahlzeit = request.form['snack']
        #kalorien = request.form['klr']
        #kosten = request.form['preis']
        #datum = request.form['date']


        #return render_template("menu.html", snack1 = mahlzeit, kcal = kalorien,  price = kosten, date = datum)

    #return render_template("menu.html")

@app.route("/menu", methods=["GET", "POST"])
def eingabe():
    if request.method == "POST":
        data = request.form
        menu = data["snack"]
        kalorien = data["klr"]
        kosten = data["preis"]
        datum = data["date"]
        try:
            with open("ernährung_zusammengefasst.json", "r") as open_file:
                datei_inhalt = json.load(open_file)
        except FileNotFoundError:
            datei_inhalt = []

        my_dict = {"Menu/Snack": menu, "Kalorien": kalorien, "Preis CHF": kosten, "Datum": datum}
        datei_inhalt.append(my_dict)

        with open("ernährung_zusammengefasst.json", "w") as open_file:
            json.dump(datei_inhalt, open_file, indent=4)
        return str("Besten Dank, deine Daten wurden gespeichert")
    else:
        return render_template("menu.html")








@app.route("/about")
def about():
    return "Bitte gib "

@app.route('/hello/<name2>')
def begruessung(name2):
    return "Hallo " + name2 + "!"

@app.route('/formular', methods=["get", "post"]) #formular erstellt bzw. verknüfung, mit get und post wird entgegengenommen und wiedergegeben
def formular():
    if request.method.lower() == "get":
        return render_template('formular.html')
    if request.method.lower() == "post":
        name = request.form['vorname']
        return(name)

@app.route("/list")
def auflistung():
    elemente = ["Money boy", "yolo", "swag", "dreh den swag auf"]
    return render_template("liste.html", html_elemente=elemente)

@app.route("/table")
def tabelle():

    biere = [
        {
            "name": "Panix Perle",
            "herkunft": "Glarus",
            "vol": "4.6",
            "brauerei": "Adler",
            "preis": 2.40
        },
        {
            "name": "Retro",
            "herkunft": "Luzern",
            "vol": "4.9",
            "brauerei": "Eichhof",
            "preis" : 1.80
        },
        {
            "name": "Quöllfrisch",
            "herkunft": "Appenzell",
            "vol": "4.8",
            "brauerei": "Locher",
            "preis" : 2.50
        }
    ]
    for bier in biere:
        preis = bier["preis"]
        tax = berechnen(preis)
        bier["steuern"] = tax


    table_header = ["Name", "Herkunft", "Vol%", "Brauerei", "Preis", "Steuern"]
    return render_template("beer.html", beers=biere, header=table_header)


@app.route("/abgaben")
def yo(preis):
    abgaben_betrag = abgaben(preis)
    return render_template("preis.html", abgabe=abgaben_betrag)


if __name__ == "__main__":
    app.run(debug=True, port=5000)