"""
Routes and cruds fonction of Role entity
"""

from flask import (request, jsonify, redirect, url_for, render_template, Blueprint, flash, get_flashed_messages)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from lead_me.models.Role import Role
from .db import db

roles_bp = Blueprint("roles", __name__, url_prefix="/roles")
class CSRFProtectForm(FlaskForm):
    pass

class CreateRoleForm(FlaskForm):
    """
    Cette classe se charge de créer le formulaire et ses champs
    et de faire la validation des donnés
    """
    role_name = StringField('Nom du Rôle', validators=[DataRequired(message="Le champ ne doit pas être vide.")])

    def validate_role_name(self, field):
        if Role.query.filter_by(nom=field.data.strip()).first():
            raise ValidationError("Un rôle avec ce nom existe déjà.")

    submit = SubmitField('Soumettre')

class EditRoleForm(FlaskForm):
    role_name = StringField('Nom du Rôle', validators=[DataRequired(message="Le champ ne doit pas être vide.")])

    def __init__(self, original_name, *args, **kwargs):
        super(EditRoleForm, self).__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_role_name(self, field):
        if field.data.strip() != self.original_name and Role.query.filter_by(nom=field.data.strip()).first():
            raise ValidationError("Un rôle avec ce nom existe déjà.")

    submit = SubmitField('Modifier')
    
class DeleteRoleForm(FlaskForm):
    pass

@roles_bp.route("/", methods=["GET"])
def list_roles():
    roles = Role.query.all()
    form = CSRFProtectForm()
    return render_template("dashboard/roles/index.html", roles=roles, form=form) 

@roles_bp.route("/create", methods=("GET", "POST"))
def create():
    form = CreateRoleForm()
    if form.validate_on_submit():
        new_role = Role(nom=form.role_name.data.strip())
        db.session.add(new_role)
        db.session.commit()
        flash('Role créé avec succès!', 'success')
        return redirect(url_for('roles.list_roles'))
    return render_template('dashboard/roles/create.html', form=form)

@roles_bp.route("/edit/<string:role_id>", methods=("GET", "POST"))
def edit(role_id):
    role = Role.query.get_or_404(role_id)
    form = EditRoleForm(role.nom, obj=role)
    if form.validate_on_submit():
        role.nom = form.role_name.data.strip()
        db.session.commit()
        flash('Role modifié avec succès!', 'success')
        return redirect(url_for('roles.list_roles'))
    return render_template("dashboard/roles/edit.html", form=form, role=role)


@roles_bp.route("/delete/<string:role_id>", methods=["POST"])
def delete_role(role_id):
    form = DeleteRoleForm()  
    if form.validate_on_submit():
        role = Role.query.get_or_404(role_id)
        db.session.delete(role)
        db.session.commit()
        flash('Role supprimé avec succès!', 'success')
        return redirect(url_for('roles.list_roles'))
    return "Erreur CSRF", 400