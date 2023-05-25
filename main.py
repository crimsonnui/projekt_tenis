from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)
#db.init_app(app)

class Kort(db.Model):
    __tablename__ = 'kort'
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(255), nullable=False)
    wysokoscSiatki = db.Column(db.Integer(), nullable=False)
    wyposazenie = db.Column(db.String(255), nullable=False)
    odbicie = db.Column(db.String(255), nullable=False)

class Gracz(db.Model):
    __tablename__ = 'gracz'
    id = db.Column(db.Integer, primary_key=True)
    imieInazwisko = db.Column(db.String(255), nullable=False)
    adresEmail = db.Column(db.String(255), nullable=False)
    wiek = db.Column(db.Integer(), nullable=False)
    nrTelefonu = db.Column(db.Integer(), nullable=False)

class Trener(db.Model):
    __tablename__ = 'trener'
    id = db.Column(db.Integer, primary_key=True)
    imieInazwisko = db.Column(db.String(255), nullable=False)
    adresEmail = db.Column(db.String(255), nullable=False)
    wiek = db.Column(db.Integer(), nullable=False)
    nrTelefonu = db.Column(db.Integer(), nullable=False)
    specjalizacja = db.Column(db.String(255), nullable=False)

class Rezerwuj(db.Model):
    __tablename__ = 'rezerwuj'
    id = db.Column(db.Integer, primary_key=True)
    kortId = db.Column(db.Integer, nullable=False)
    graczId = db.Column(db.Integer, nullable=False)
    trenerId = db.Column(db.Integer, nullable=False)
    uwagi = db.Column(db.String(255), nullable=False)
    kodZnizkowy = db.Column(db.String, nullable=False)
    liczbaDni = db.Column(db.Integer, nullable=False)
    dataPoczatkowa = db.Column(db.Date, nullable=False, default=date.today())
    dataKoncowa = db.Column(db.Date, nullable=False, default=date.today())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/korty/")
def korty():
    korty = db.session.execute(db.select(Kort).order_by(Kort.id)).scalars()
    return render_template("korty.html", korty=korty)

@app.route("/gracze/")
def gracze():
    gracze = db.session.execute(db.select(Gracz).order_by(Gracz.id)).scalars()
    return render_template("gracze.html", gracze=gracze)

@app.route("/trenerzy/")
def trenerzy():
    trenerzy = db.session.execute(db.select(Trener).order_by(Trener.id)).scalars()
    return render_template("trenerzy.html", trenerzy=trenerzy)

@app.route("/korty/Rezerwacje/")
def rezerwacje():
    rezerwacje = [r for r in db.session.execute(db.select(Rezerwuj).order_by(Rezerwuj.id)).scalars()]
    korty = [k for k in db.session.execute(db.select(Kort).order_by(Kort.nazwa)).scalars()]
    gracze = [g for g in db.session.execute(db.select(Gracz).order_by(Gracz.imieInazwisko)).scalars()]
    trenerzy = [t for t in db.session.execute(db.select(Trener).order_by(Trener.imieInazwisko)).scalars()]
    return render_template("rezerwacje.html", rezerwacje=rezerwacje, korty=korty, gracze=gracze,trenerzy=trenerzy)

@app.route("/korty/Dodaj")
def dodajKort():
    return render_template("dodajKort.html")

@app.route("/korty/Rezerwuj")
def zarezerwujGre():
    korty = db.session.execute(db.select(Kort).order_by(Kort.nazwa)).scalars()
    gracze = db.session.execute(db.select(Gracz).order_by(Gracz.imieInazwisko)).scalars()
    trenerzy = db.session.execute(db.select(Trener).order_by(Trener.imieInazwisko)).scalars()
    return render_template("zarezerwujGre.html", korty=korty,gracze=gracze,trenerzy=trenerzy)

@app.route("/gracze/Dodaj")
def dodajGracza():
    return render_template("dodajGracza.html")

@app.route("/trenerzy/Dodaj")
def dodajTrenera():
    return render_template("dodajTrenera.html")

@app.route("/dodaj_kort", methods=["GET", "POST"])
def dodaj_kort():
    if request.method == "POST":
        nazwa = request.form['nazwa']
        wysokoscSiatki = request.form['wysokoscSiatki']
        wyposazenie = request.form['wyposazenie']
        odbicie = request.form['odbicie']
        kort = Kort(
            nazwa=nazwa,
            wysokoscSiatki=wysokoscSiatki,
            wyposazenie=wyposazenie,
            odbicie=odbicie,
        )
        db.session.add(kort)
        db.session.commit()
        return redirect("/korty")
    return redirect("/korty")

@app.route("/dodaj_gracza", methods=["GET", "POST"])
def dodaj_gracza():
    if request.method == "POST":
        imieInazwisko = request.form['imieInazwisko']
        adresEmail = request.form['adresEmail']
        wiek = request.form['wiek']
        nrTelefonu = request.form['nrTelefonu']
        gracz = Gracz(
            imieInazwisko=imieInazwisko,
            adresEmail=adresEmail,
            wiek=wiek,
            nrTelefonu=nrTelefonu,
        )
        db.session.add(gracz)
        db.session.commit()
        return redirect("/gracze")
    return redirect("/gracze")

@app.route("/dodaj_trenera", methods=["GET", "POST"])
def dodaj_trenera():
    if request.method == "POST":
        imieInazwisko = request.form['imieInazwisko']
        adresEmail = request.form['adresEmail']
        wiek = request.form['wiek']
        nrTelefonu = request.form['nrTelefonu']
        specjalizacja = request.form['specjalizacja']
        trener = Trener(
            imieInazwisko=imieInazwisko,
            adresEmail=adresEmail,
            wiek=wiek,
            nrTelefonu=nrTelefonu,
            specjalizacja=specjalizacja
        )
        db.session.add(trener)
        db.session.commit()
        return redirect("/trenerzy")
    return redirect("/trenerzy")

@app.route("/zarezerwuj_gre", methods=["GET", "POST"])
def zarezerwuj_gre():
    if request.method == "POST":
        kort_id = request.form.get('korty_select')
        gracz_id = request.form.get('gracze_select')
        trener_id = request.form.get('trenerzy_select')
        uwagi = request.form['uwagi']
        liczbaDni = request.form['liczbaDni']
        kodZnizkowy = request.form['kodZnizkowy']
        dataKoncowa = date.today() + timedelta(days=int(liczbaDni))
        rezerwuj = Rezerwuj(
            kortId=kort_id,
            graczId=gracz_id,
            trenerId=trener_id,
            liczbaDni=liczbaDni,
            uwagi=uwagi,
            kodZnizkowy=kodZnizkowy,
            dataKoncowa=dataKoncowa
        )
        db.session.add(rezerwuj)
        db.session.commit()
        return redirect('/korty')
    return redirect('/korty')

if __name__ == "__main__":
    app.run(debug=True, port=5005)