"""
Routes and cruds fonction of Universite entity
"""

from flask import (request, jsonify, redirect, url_for, render_template, Blueprint, Blueprint, flash, get_flashed_messages)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from lead_me.models.Universites import Universite
from .db import db

universites_bp =  Blueprint("universites", __name__, url_prefix="/universites")
class CSRFProtectForm(FlaskForm):
    pass

class CreateUniversiteForm(FlaskForm):
    """
    Cette classe se charge de créer le formulaire et ses champs
    et de faire la validation des donnés
    """
    universite_name = StringField("Nom", validators=[DataRequired(message="Le champ ne doit pas être vide.")])
    universite_code = StringField("Code", validators=[DataRequired(message="Le champ ne doit pas être vide.")])

    def validate_universite_name(self, field):
        if Universite.query.filter_by(nom=field.data.strip()).first():
            raise ValidationError("Un rôle avec ce nom existe déjà.")
    def validate_universite_code(self, field):
        if Universite.query.filter_by(code=field.data.strip()).first():
            raise ValidationError("Une Université avec ce code existe déjà.")

    submit = SubmitField('Soumettre')
    
class EditUniversiteForm(FlaskForm):
    universite_name = StringField("Nom de l'université", validators=[DataRequired(message="Le champ ne doit pas être vide.")])
    universite_code = StringField("Code de l'université", validators=[DataRequired(message="Le champ ne doit pas être vide.")])
    
    def __init__(self, original_name, original_code, *args, **kwargs):
        super(EditUniversiteForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
        self.original_code = original_code

    def validate_universite_name(self, field):
        if field.data.strip() != self.original_name and Universite.query.filter_by(nom=field.data.strip()).first():
            raise ValidationError("Une université de ce nom existe déjà")
        
    def validate_universite_code(self, field):
        if field.data.strip() != self.original_code and Universite.query.filter_by(code=field.data.strip()).first():
            raise ValidationError("Une université de ce nom existe déjà")

    submit = SubmitField('Modifier')
    
class DeleteUniversiteForm(FlaskForm):
    pass

@universites_bp.route("/", methods=["GET"])
def list_universites():
    universites = Universite.query.all()
    form = CSRFProtectForm()
    return render_template("dashboard/universites/index.html", universites=universites, form=form) 

@universites_bp.route("/create", methods=["GET", "POST"])
def create():
    form = CreateUniversiteForm()
    if form.validate_on_submit():
        new_universite = Universite(nom=form.universite_name.data.strip(), code=form.universite_code.data.strip())
        db.session.add(new_universite)
        db.session.commit()
        flash('Université créé avec succès!', 'success')
        return redirect(url_for('universites.list_universites'))
    return render_template('dashboard/universites/create.html', form=form)

@universites_bp.route("/edit<string:universite_id>", methods=("GET", "POST"))
def edit(universite_id):
    universite = Universite.query.get_or_404(universite_id)
    form = EditUniversiteForm(universite.nom, universite.code, obj=universite)
    if form.validate_on_submit():
        universite.nom = form.universite_name.data.strip()
        universite.code = form.universite_code.data.strip()
        db.session.commit()
        flash('Université modifié avec succès!', 'success')
        return redirect(url_for('universites.list_universites'))
    return render_template("dashboard/universites/edit.html", form=form, universite=universite)

@universites_bp.route("/delete/<string:universite_id>", methods=["POST"])
def delete_role(universite_id):
    form = DeleteUniversiteForm()  
    if form.validate_on_submit():
        universite = Universite.query.get_or_404(universite_id)
        db.session.delete(universite)
        db.session.commit()
        flash('Université supprimée avec succès!', 'success')
        return redirect(url_for('universites.list_universites'))
    return "Erreur CSRF", 400