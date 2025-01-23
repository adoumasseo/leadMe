"""
Routes and cruds fonction of Ecole entity
"""

from flask_login.utils import login_required, current_user
from app.middleware.auth import admin_required
from app.controllers.ecole import bp
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.extensions import db
from app.database.models.university import Universite
from app.database.models.ecole import Ecole
from flask import flash, render_template, redirect, url_for

class CSRFProtectForm(FlaskForm):
    pass

class CreateEcoleForm(FlaskForm):
    """
    Cette classe se charge de créer le formulaire et ses champs
    et de faire la validation des donnés
    """
    ecole_name = StringField("Name", validators=[DataRequired(message="The field must not be empty.")])
    ecole_code = StringField("Code", validators=[DataRequired(message="The field must not be empty.")])
    universite_id = SelectField("University", choices=[], validators=[DataRequired(message="Please select a university.")])

    def validate_ecole_name(self, field):
        if Ecole.query.filter_by(nom=field.data.strip()).first():
            raise ValidationError("A school with that name already exists.")
    def validate_ecole_code(self, field):
        if Ecole.query.filter_by(code=field.data.strip()).first():
            raise ValidationError("A school with that code already exists.")

    submit = SubmitField('Submit')
    def __init__(self, *args, **kwargs):
        super(CreateEcoleForm, self).__init__(*args, **kwargs)
        self.universite_id.choices = [(u.id_universite, u.nom) for u in Universite.query.all()]

class EditEcoleForm(FlaskForm):
    ecole_name = StringField("School Name", validators=[DataRequired(message="The field must not be empty.")])
    ecole_code = StringField("School Code", validators=[DataRequired(message="The field must not be empty.")])
    universite_id = SelectField("University", choices=[], validators=[DataRequired(message="Please select a university.")])
    submit = SubmitField('Update')

    def __init__(self, original_name, original_code, *args, **kwargs):
        super(EditEcoleForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
        self.original_code = original_code
        self.universite_id.choices = [(u.id_universite, u.nom) for u in Universite.query.all()]

    def validate_ecole_name(self, field):
        if field.data.strip() != self.original_name and Ecole.query.filter_by(nom=field.data.strip()).first():
            raise ValidationError("A school with that name already exists.")
        
    def validate_ecole_code(self, field):
        if field.data.strip() != self.original_code and Ecole.query.filter_by(code=field.data.strip()).first():
            raise ValidationError("A school with that code already exists.")

class DeleteEcoleForm(FlaskForm):
    pass

@bp.route("/", methods=["GET"])
@login_required
@admin_required
def list_ecoles():
    universites = Universite.query.all()
    form = CSRFProtectForm()
    userFullName = current_user.prenom + " " + current_user.nom
    userInitials = current_user.prenom[0] + current_user.nom[0]
    return render_template(
        "dashboard/ecole/index.html",
        universites=universites,
        form=form,
        userFullName=userFullName,
        userInitials=userInitials
    )

@bp.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def create():
    form = CreateEcoleForm()
    if form.validate_on_submit():
        nom = form.ecole_name.data.strip()
        code = form.ecole_code.data.strip()
        id_universite = form.universite_id.data

        new_ecole = Ecole(nom=nom, code=code, id_universite=id_universite)

        db.session.add(new_ecole)
        db.session.commit()
        flash('School successfully created!', 'success')
        return redirect(url_for('ecoles.list_ecoles'))

    return render_template('dashboard/ecole/create.html', form=form)

@bp.route("/edit<string:ecole_id>", methods=("GET", "POST"))
@login_required
@admin_required
def edit(ecole_id):
    ecole = Ecole.query.get_or_404(ecole_id)
    form = EditEcoleForm(original_name=ecole.nom, original_code=ecole.code)
    
    if form.validate_on_submit():
        ecole.nom = form.ecole_name.data.strip()
        ecole.code = form.ecole_code.data.strip()
        ecole.id_universite = form.universite_id.data
        db.session.commit()
        flash('School successfully updated', 'success')
        return redirect(url_for('ecoles.list_ecoles'))

    form.ecole_name.data = ecole.nom
    form.ecole_code.data = ecole.code
    form.universite_id.data = ecole.id_universite
    return render_template('dashboard/ecole/edit.html', form=form, ecole=ecole)

@bp.route("/delete/<string:ecole_id>", methods=["POST"])
@login_required
@admin_required
def delete(ecole_id):
    ecole = Ecole.query.get_or_404(ecole_id)
    db.session.delete(ecole)
    db.session.commit()
    flash('School successfully deleted!', 'success')
    
    return redirect(url_for('ecoles.list_ecoles'))  