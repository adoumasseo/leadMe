"""
Routes and cruds fonction of Ecole entity
"""

from flask import (request, jsonify, redirect, url_for, render_template, Blueprint, flash, get_flashed_messages)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from lead_me.models.Ecole import Ecole
from lead_me.models.Universites import Universite
from .db import db

ecoles_bp = Blueprint('ecoles', __name__, url_prefix="/ecoles")

class CSRFProtectForm(FlaskForm):
    pass

class CreateEcoleForm(FlaskForm):
    """
    Cette classe se charge de créer le formulaire et ses champs
    et de faire la validation des donnés
    """
    ecole_name = StringField("Nom", validators=[DataRequired(message="Le champ ne doit pas être vide.")])
    ecole_code = StringField("Code", validators=[DataRequired(message="Le champ ne doit pas être vide.")])
    universite_id = SelectField("Université", choices=[], validators=[DataRequired(message="Veuillez sélectionner une université.")])

    def validate_ecole_name(self, field):
        if Ecole.query.filter_by(nom=field.data.strip()).first():
            raise ValidationError("Un rôle avec ce nom existe déjà.")
    def validate_ecole_code(self, field):
        if Ecole.query.filter_by(code=field.data.strip()).first():
            raise ValidationError("Une Université avec ce code existe déjà.")

    submit = SubmitField('Soumettre')
    def __init__(self, *args, **kwargs):
        super(CreateEcoleForm, self).__init__(*args, **kwargs)
        self.universite_id.choices = [(u.id_universite, u.nom) for u in Universite.query.all()]

class EditEcoleForm(FlaskForm):
    ecole_name = StringField("Nom de l'école", validators=[DataRequired(message="Le champ ne doit pas être vide.")])
    ecole_code = StringField("Code de l'école", validators=[DataRequired(message="Le champ ne doit pas être vide.")])
    universite_id = SelectField("Université", choices=[], validators=[DataRequired(message="Veuillez sélectionner une université.")])
    submit = SubmitField('Modifier')

    def __init__(self, original_name, original_code, *args, **kwargs):
        super(EditEcoleForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
        self.original_code = original_code
        self.universite_id.choices = [(u.id_universite, u.nom) for u in Universite.query.all()]

    def validate_ecole_name(self, field):
        if field.data.strip() != self.original_name and Ecole.query.filter_by(nom=field.data.strip()).first():
            raise ValidationError("Une école de ce nom existe déjà.")
        
    def validate_ecole_code(self, field):
        if field.data.strip() != self.original_code and Ecole.query.filter_by(code=field.data.strip()).first():
            raise ValidationError("Une école de ce code existe déjà.")

class DeleteEcoleForm(FlaskForm):
    pass

@ecoles_bp.route("/", methods=["GET"])
def list_ecoles():
    universites = Universite.query.all()
    form = CSRFProtectForm()
    return render_template("dashboard/ecoles/index.html", universites=universites, form=form)

@ecoles_bp.route("/create", methods=["GET", "POST"])
def create():
    form = CreateEcoleForm()
    if form.validate_on_submit():
        nom = form.ecole_name.data.strip()
        code = form.ecole_code.data.strip()
        id_universite = form.universite_id.data

        new_ecole = Ecole(nom=nom, code=code)
        new_ecole.id_universite = id_universite

        db.session.add(new_ecole)
        db.session.commit()
        flash('Ecole créé avec succès!', 'success')
        return redirect(url_for('ecoles.list_ecoles'))

    return render_template('dashboard/ecoles/create.html', form=form)

@ecoles_bp.route("/edit<string:ecole_id>", methods=("GET", "POST"))
def edit(ecole_id):
    ecole = Ecole.query.get_or_404(ecole_id)
    form = EditEcoleForm(original_name=ecole.nom, original_code=ecole.code)
    
    if form.validate_on_submit():
        ecole.nom = form.ecole_name.data.strip()
        ecole.code = form.ecole_code.data.strip()
        ecole.id_universite = form.universite_id.data
        db.session.commit()
        flash('Ecole modifié avec succès!', 'success')
        return redirect(url_for('ecoles.list_ecoles'))

    form.ecole_name.data = ecole.nom
    form.ecole_code.data = ecole.code
    form.universite_id.data = ecole.id_universite
    return render_template('dashboard/ecoles/edit.html', form=form, ecole=ecole)

@ecoles_bp.route("/delete/<string:ecole_id>", methods=["POST"])
def delete(ecole_id):
    ecole = Ecole.query.get_or_404(ecole_id)
    db.session.delete(ecole)
    db.session.commit()
    flash('Ecole supprimé avec succès!', 'success')
    
    return redirect(url_for('ecoles.list_ecoles'))  