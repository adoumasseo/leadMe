"""
Routes and cruds fonction of Serie entity
"""

from flask_login.utils import login_required, current_user
from app.middleware.auth import admin_required
from app.controllers.serie import bp
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.extensions import db
from app.database.models.serie import Serie
from flask import flash, render_template, redirect, url_for


class CSRFProtectForm(FlaskForm):
    pass

class CreateSerieForm(FlaskForm):
    """
    Cette classe se charge de créer le formulaire et ses champs
    et de faire la validation des donnés
    """
    serie_name = StringField('Nom de la serie', validators=[DataRequired(message="Le champ ne doit pas être vide.")])
    def validate_serie_name(self, field):
        if Serie.query.filter_by(nom=field.data.strip()).first():
            raise ValidationError("Une série de ce nom existe déjà.")

    submit = SubmitField('Soumettre')
    
class EditSerieForm(FlaskForm):
    serie_name = StringField('Nom de la Serie', validators=[DataRequired(message="Le champ ne doit pas être vide.")])

    def __init__(self, original_name, *args, **kwargs):
        super(EditSerieForm, self).__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_serie_name(self, field):
        if field.data.strip() != self.original_name and Serie.query.filter_by(nom=field.data.strip()).first():
            raise ValidationError("Une série de ce nom existe déjà.")

    submit = SubmitField('Modifier')
    
class DeleteSerieForm(FlaskForm):
    pass

@bp.route("/", methods=["GET"])
@login_required
@admin_required
def list_series():
    series = Serie.query.all()
    form = CSRFProtectForm()
    userFullName = current_user.prenom + " " + current_user.nom
    userInitials = current_user.prenom[0] + current_user.nom[0]
    return render_template(
        "dashboard/serie/index.html",
        series=series,
        form=form,
        userFullName=userFullName,
        userInitials=userInitials
    )

@bp.route("/create", methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    form = CreateSerieForm()
    if form.validate_on_submit():
        new_serie = Serie(nom=form.serie_name.data)
        db.session.add(new_serie)
        db.session.commit()
        flash('Série créé avec succès!', 'success')
        return redirect(url_for('series.list_series'))
    return render_template('dashboard/serie/create.html', form=form)

@bp.route("/edit<string:serie_id>", methods=("GET", "POST"))
@login_required
@admin_required
def edit(serie_id):
    serie = Serie.query.get_or_404(serie_id)
    form = EditSerieForm(serie.nom, obj=serie)
    if form.validate_on_submit():
        serie.nom = form.serie_name.data
        db.session.commit()
        flash('Série modifié avec succès!', 'success')
        return redirect(url_for('series.list_series'))
    return render_template("dashboard/serie/edit.html", form=form, serie=serie)

@bp.route("/delete/<string:serie_id>", methods=["POST"])
@login_required
@admin_required
def delete(serie_id):
    form = DeleteSerieForm()  
    if form.validate_on_submit():
        serie = Serie.query.get_or_404(serie_id)
        db.session.delete(serie)
        db.session.commit()
        flash('Ecole supprimé avec succès!', 'success')
        return redirect(url_for('series.list_series'))
    return "Erreur CSRF", 400