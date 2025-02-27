"""
Routes and cruds fonction of Universite entity
"""
from flask_login.utils import login_required, current_user
from app.middleware.auth import admin_required
from app.controllers.university import bp
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.extensions import db
from app.database.models.university import Universite
from flask import flash, render_template, redirect, url_for


class CSRFProtectForm(FlaskForm):
    pass

class CreateUniversiteForm(FlaskForm):
    """
    Cette classe se charge de créer le formulaire et ses champs
    et de faire la validation des donnés
    """
    universite_name = StringField("Name", validators=[DataRequired(message="Field must not be empty.")])
    universite_code = StringField("Code", validators=[DataRequired(message="Field must not be empty.")])

    def validate_universite_name(self, field):
        if Universite.query.filter_by(nom=field.data.strip()).first():
            raise ValidationError("A University with this name already exists.")
    def validate_universite_code(self, field):
        if Universite.query.filter_by(code=field.data.strip()).first():
            raise ValidationError("A University with this code already exists.")

    submit = SubmitField('Submit')
    
class EditUniversiteForm(FlaskForm):
    universite_name = StringField("Name of University", validators=[DataRequired(message="The field must not be empty.")])
    universite_code = StringField("Code of University", validators=[DataRequired(message="The field must not be empty.")])
    
    def __init__(self, original_name, original_code, *args, **kwargs):
        super(EditUniversiteForm, self).__init__(*args, **kwargs)
        self.original_name = original_name
        self.original_code = original_code

    def validate_universite_name(self, field):
        if field.data.strip() != self.original_name and Universite.query.filter_by(nom=field.data.strip()).first():
                raise ValidationError("A university of this name already exists")
        
    def validate_universite_code(self, field):
        if field.data.strip() != self.original_code and Universite.query.filter_by(code=field.data.strip()).first():
            raise ValidationError("A university of this name already exists")

    submit = SubmitField('Update')
    
class DeleteUniversiteForm(FlaskForm):
    pass

@bp.route("/", methods=["GET"])
@login_required
@admin_required
def list_universites():
    universites = Universite.query.all()
    form = CSRFProtectForm()
    userFullName = current_user.prenom + " " + current_user.nom
    userInitials = current_user.prenom[0] + current_user.nom[0]
    return render_template(
        "dashboard/university/index.html",
        universites=universites,
        form=form,
        userFullName=userFullName,
        userInitials=userInitials
    ) 

@bp.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def create():
    form = CreateUniversiteForm()
    if form.validate_on_submit():
        new_universite = Universite(nom=form.universite_name.data.strip(), code=form.universite_code.data.strip())
        db.session.add(new_universite)
        db.session.commit()
        flash('University successfully created!', 'success')
        return redirect(url_for('universites.list_universites'))
    return render_template('dashboard/university/create.html', form=form)

@bp.route("/edit<string:universite_id>", methods=("GET", "POST"))
@login_required
@admin_required
def edit(universite_id):
    universite = Universite.query.get_or_404(universite_id)
    form = EditUniversiteForm(universite.nom, universite.code, obj=universite)
    if form.validate_on_submit():
        universite.nom = form.universite_name.data.strip()
        universite.code = form.universite_code.data.strip()
        db.session.commit()
        flash('University successfully updated!', 'success')
        return redirect(url_for('universites.list_universites'))
    return render_template("dashboard/university/edit.html", form=form, universite=universite)

@bp.route("/delete/<string:universite_id>", methods=["POST"])
@login_required
@admin_required
def delete_universite(universite_id):
    form = DeleteUniversiteForm()  
    if form.validate_on_submit():
        universite = Universite.query.get_or_404(universite_id)
        db.session.delete(universite)
        db.session.commit()
        flash('University successfully deleted!', 'success')
        return redirect(url_for('universites.list_universites'))
    return "Erreur CSRF", 400