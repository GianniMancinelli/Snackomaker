from flask import Flask, flash
from flask import render_template
from flask import url_for
from flask import request
from flask import json
import plotly.express as px
import json





app = Flask(__name__)
# Quelle Flash Messages:
# https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/
# Quelle für Secret Key:
# https://stackoverflow.com/questions/30223379/trying-to-flash-a-message-raises-an-exception
app.config["SECRET_KEY"] = "2A69DB69695KWL8XP1LZ69KJF0"

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
            flash("Besten Dank für deine Eingabe, deine Daten wurden ordnungsgemäss gespeichert.", "success")
            return render_template("index.html")
    else:
        return render_template("index.html")

#Ausgabe der Daten jsonfile wenn man auf "deine Ernährung" klickt & Verknüpfung zu html Seite deine Ernährung
@app.route("/menu")
def menu():
    with open("ernährung_zusammengefasst.json", encoding="utf-8") as open_file:
        inhalt = json.load(open_file)
        return render_template("menu.html", inhalt=inhalt)

#Plotly grafic, berechnung von /statistc nochmals verwendet um die aktuellen Zahlen auch auf dem Chart ersichtlich zu haben.

@app.route("/grafik")
def grafik():
    with open("ernährung_zusammengefasst.json", encoding="utf-8") as open_file:
        inhalt = json.load(open_file)
        count = len(inhalt)
    summe = 0
    for el in inhalt:
        summe += int(float(el["Preis CHF"]))
    summe1 = 0
    for el in inhalt:
        summe1 += int(float(el["Kalorien"]))

    data = dict(
        number=[summe1, summe, count],
        zusammenfassung=["eingenommene Kalorien", "Ausgaben", "verspeiste Menus/Snacks"])

    fig = px.funnel(data, x='number', y='zusammenfassung')
    fig.show()
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True, port=5000)


