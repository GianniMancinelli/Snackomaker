from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import json
import json



# wie berrechnung in Statistik?

# wie Grafisch darstellen?




app = Flask(__name__)


#verknüfung zu html Startseite aka index
@app.route("/")
def index():
    about_link = url_for("index")
    return render_template("index.html", link=about_link)

#verknüfung zu html Seite Statistic
@app.route("/statistic")
def statistic():
    with open("ernährung_zusammengefasst.json", encoding="utf-8") as open_file:
        inhalt = json.load(open_file)
        #damit menues gezählt werden
        count = len(inhalt)
    about_link = url_for("statistic")
    # damit alle Preise CHF summiert werden
    summe = 0
    for el in inhalt:
        summe += int(float(el["Preis CHF"]))
    # damit alle Kalorien summiert werden
    summe1 = 0
    for el in inhalt:
        summe1 += int(float(el["Kalorien"]))
    return render_template("statistik.html", link=about_link, count=count,ausgaben=summe, kalorien=summe1 )




#Verknüpfung mit Formular, sodass json file entsteht, und die eingaben abspeichert.
@app.route("/form", methods=["GET", "POST"])
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
        return str("Besten Dank für deine Eingabe, deine Daten wurden ordnungsgemäss gespeichert.")
    else:
        return render_template("index.html")

#Ausgabe der Daten jsonfile wenn man auf "deine Ernährung" klickt & Verknüpfung zu html Seite deine Ernährung
@app.route("/menu")
def menu():
    with open("ernährung_zusammengefasst.json", encoding="utf-8") as open_file:
        inhalt = json.load(open_file)
        return render_template("menu.html", inhalt=inhalt)



if __name__ == "__main__":
    app.run(debug=True, port=5000)


