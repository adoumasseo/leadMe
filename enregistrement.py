"""Defini les fonctions pour l'enregistrement et le traitement des notes
"""
from flask import (
        Blueprint, url_for, redirect, request, render_template
        )
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from .db import db
from flask_login import login_user
from .models.Matiere import Matiere
from .models.User import User
from .models.Serie import Serie
from .models.Moyenne import Moyenne
from .models.Filiere import Filiere
notes_bp = Blueprint("notes", __name__, url_prefix="/notes")

class CreateSerieForm(FlaskForm):
    """
    Cette classe se charge de créer le formulaire et ses champs
    et de faire la validation des donnés
    """
    serie = SelectField("Série", choices=[], validators=[DataRequired(message="Veuillez sélectionner une Série.")])
    submit = SubmitField('Soumettre')
    def __init__(self, *args, **kwargs):
        super(CreateSerieForm, self).__init__(*args, **kwargs)
        self.serie.choices = [(u.id_serie, u.nom) for u in Serie.query.all()]

@notes_bp.route("/traiter", methods=("GET", "POST"))
@login_required
def traiter():
    serie = Serie.query.filter_by(nom=current_user.serie).first()
    matieres = serie.matiere
    return render_template("enregistrement.html", matieres=matieres)

@notes_bp.route("/traitrement", methods=("GET", "POST"))
def traiter_anonyme():
    form = CreateSerieForm()
    if form.validate_on_submit():
        user = User (
            nom = 'anonyme',
            prenom= 'anonyme',
            email = 'anonyme@gmail.com',
            serie = form.serie.data,
            matricule = 'ANONYME'
        )
        login_user(user)
        serie = Serie.query.filter_by(nom=form.serie.data).first()
        matieres = serie.matiere
        return render_template("enregistrement.html", matieres=matieres)
    return render_template("/frontend/form/create_anonyme_user.html", form=form)
     
@notes_bp.route("/resultat", methods=["POST"])
def resultat():
    serie = Serie.query.filter_by(nom=current_user.serie).first()
    filieres = serie.filiere
    avg, total_coeff = 0, 0
    moyennes = Moyenne.query.filter_by(id_user=current_user.id).order_by(Moyenne.moyennecalc.desc()).all()
    if len(moyennes) == 0:
        for filiere in filieres:
            matieres = filiere.matiere
            for matiere in filiere.matiere:
                total_coeff += int(matiere.coefficient)
                avg += matiere.coefficient * int(request.form.get(str(matiere.nom)))
            avg = avg / total_coeff
            moyenne = Moyenne(id_filiere=filiere.id_filiere, id_user=current_user.id, moyennecalc=avg)
            """la moyenne ne doit pas etre recalculer ou enregister pour un utilisateur qui as deja ses resultats"""
            db.session.add(moyenne)
            db.session.commit()
            avg, total_coeff = 0, 0
    
    filieres = []
    noms = []
    for f in moyennes:
            fill = Filiere.query.filter_by(id_filiere=f.id_filiere).first()
            if fill.nom not in noms:
                noms.append(fill.nom)
                filieres.append(fill)
    nbr = len(filieres)

    return render_template("result.html", moyennes=moyennes, filieres=filieres, nbr=nbr)
