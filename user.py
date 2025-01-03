"""
Routes and cruds fonction of User entity
"""

from flask import (request, jsonify, redirect, url_for, render_template, Blueprint, flash, get_flashed_messages)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from lead_me.models.User import User
from .db import db

users_bp = Blueprint("users", __name__, url_prefix="/users")
class CSRFProtectForm(FlaskForm):
    pass

class CreateUserForm(FlaskForm):
    """
    Cette classe se charge de créer le formulaire et ses champs
    et de faire la validation des donnés
    """
    user_nom = StringField("Nom", validators=[DataRequired(message="Le champ ne doit pas être vide.")])
    user_prenom = StringField("Prenom", validators=[DataRequired(message="Le champ ne doit pas être vide.")])
    user_mail = StringField("Email", validators=[DataRequired(message="Le champ ne doit pas être vide.")])
    
    def validate_user_mail(self, field):
        if User.query.filter_by(email=field.data.strip()).first():
            raise ValidationError("Un utilisateur avec ce email existe déjà.")

    submit = SubmitField('Soumettre')
    
class EditUserForm(FlaskForm):
    user_nom = StringField("Nom", validators=[DataRequired(message="Le champ ne doit pas être vide.")])
    user_prenom = StringField("Prénom", validators=[DataRequired(message="Le champ ne doit pas être vide.")])
    user_mail = StringField("Email", validators=[DataRequired(message="Le champ ne doit pas être vide.")])

    def __init__(self, original_email, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_user_mail(self, field):
        if field.data.strip() != self.original_email and User.query.filter_by(email=field.data).first():
            raise ValidationError("Un utilisateur avec cet email existe déjà.")

    submit = SubmitField('Modifier')

class DeleteUserForm(FlaskForm):
    pass

@users_bp.route("/", methods=["GET"])
def list_users():
    users = User.query.all()
    form = CSRFProtectForm()
    return render_template("dashboard/users/index.html", users=users, form=form)

@users_bp.route("/create", methods=["GET", "POST"])
def create():
    """
    création des user
    """
    form = CreateUserForm()
    if form.validate_on_submit():
        user= User(
            prenom=form.user_prenom.data.strip(),
            nom=form.user_nom.data.strip(),
            matricule="ROOT",
            email= form.user_mail.data.strip(),
            role='Administrateur',
            serie=None,
            password='ROOT'
        )
        db.session.add(user)
        db.session.commit()
        flash('Utilisateur créé avec succès!', 'success')
        return redirect(url_for('users.list_users'))
    return render_template("dashboard/users/create.html", form=form)

@users_bp.route("/edit/<string:user_id>", methods=["GET", "POST"])
def edit(user_id):
    """Mis a jour d'un utilisateur"""
    user = User.query.get_or_404(user_id)
    form = EditUserForm(user.email, obj=user)
    if form.validate_on_submit():
        user.prenom = form.user_prenom.data.strip()
        user.nom = form.user_nom.data.strip()
        user.email = form.user_mail.data.strip()
        db.session.commit()
        flash('Utilisateur Modifié avec succès!', 'success')
        return redirect(url_for('users.list_users'))
    return render_template("dashboard/users/edit.html", form=form, user=user)

@users_bp.route("/delete/<string:user_id>", methods=["POST"])
def delete_role(user_id):
    form = DeleteUserForm()  
    if form.validate_on_submit():
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash('Utilisateur supprimé  avec succès!', 'success')
        return redirect(url_for('users.list_users'))
    return "Erreur CSRF", 400

