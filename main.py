#Import der benötigten Module
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
app.config["SECRET_KEY"] = "2A69DB69695KWL8XP1LZ69KJF0" #wird für flashnachrichten benötigt


"""
verknüfung zu html Startseite aka index, so dass wenn man auf 
Home klickt, auf die Startseite gelagt, wo das Formular zur Eingabe steht
"""
@app.route("/")
def index():
    about_link = url_for("index")
    return render_template("index.html", link=about_link)

#verknüfung zu html Seite Statistic, so dass wenn man auf "Statistik" klickt auch wirklich auf diese Seite gelangt.
@app.route("/statistic")
def statistic():
    with open("ernährung_zusammengefasst.json", encoding="utf-8") as open_file:
        inhalt = json.load(open_file)
        #damit menues gezählt werden vom Inhalt bzw. jsonfile
        count = len(inhalt)
    about_link = url_for("statistic")
    # damit alle Preise CHF summiert werden, summe muss zuerst definiert werden
    summe = 0
    for el in inhalt:
        summe += int(float(el["Preis CHF"]))
        # wenn die Ausgaben höher als CHF 500.00 sind, macht das System mittels flashmessage auf statistik.html darauf aufmerksam, dass man die Ausgaben im Überblick behalten soll.
    if summe > 500:
        flash("Bitte behalte deine Ausgaben im Überblick!")
        # wenn die Ausgaben höher als CHF 1000.00 sind, macht das System mittels flashmessage auf statistik.html darauf aufmerksam, dass man bezüglich Ausgaben bremsen soll.
    if summe > 1000:
        flash("Du hast viel zu viele Ausgaben für Essen bzw. Snacks!!")
    # damit alle Kalorien summiert werden, summe muss zuerst definiert werden.
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
#json file wird erstellt
# falls das nicht klappt, wird eine leere Liste eröffnet
        try:
            with open("ernährung_zusammengefasst.json", "r") as open_file:
                datei_inhalt = json.load(open_file)
        except FileNotFoundError:
            datei_inhalt = []
#so wie untenstehend, werden die Daten mittels formular erfasst.
        my_dict = {"Menu/Snack": menu, "Kalorien": kalorien, "Preis CHF": kosten, "Datum": datum}
        datei_inhalt.append(my_dict)
#sobald die Daten eingegeben werden und gespeichert (im json file ernährung_zusammengefasst, erscheint die Flashnachricht, dass die daten gespeichert sind
        with open("ernährung_zusammengefasst.json", "w") as open_file:
            json.dump(datei_inhalt, open_file, indent=4)
            flash("Besten Dank für deine Eingabe, deine Daten wurden ordnungsgemäss gespeichert.", "success") #flash nachricht
            return render_template("index.html") #index soll wiedergegeben werden.
    else:
        flash("Etwas ist schiefgelaufen", "danger")
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
#folgender unterer Teil ist für das Plotly relevant, oberhalb einfach die berrechnung
    data = dict(
        number=[summe1, summe, count],
        zusammenfassung=["eingenommene Kalorien", "Ausgaben", "verspeiste Menus/Snacks"])

    fig = px.funnel(data, x='number', y='zusammenfassung')
    fig.show()
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True, port=5000)


