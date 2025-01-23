from app.extensions import db
from app.controllers.filiere import bp
from flask import render_template, redirect, url_for, flash, request
from app.middleware.auth import admin_required
from flask_login.utils import login_required, current_user
from app.database.models.filiere import Filiere
from app.database.models.matiere import Matiere
from app.database.models.associations import MatiereFiliere, FiliereSerie
from app.database.models.serie import Serie
from app.database.models.ecole import Ecole
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange, ValidationError, InputRequired, Optional, Length

class CSRFProtectForm(FlaskForm):
    pass

class FiliereForm(FlaskForm):
    nom = StringField("Nom", validators=[DataRequired(), Length(max=255)])
    debouches = TextAreaField("Débouchés")
    bourses = IntegerField("Nombre de bourses", validators=[Optional(), NumberRange(min=0)])
    semi_bourses = IntegerField("Nombre de semi-bourses", validators=[Optional(), NumberRange(min=0)])
    ecole_id = SelectField("École", coerce=str, validators=[DataRequired()])
    series = SelectMultipleField("Séries", coerce=str, validators=[DataRequired()])
    matieres = SelectMultipleField("Matières", coerce=str, validators=[DataRequired()])
    submit = SubmitField("Soumettre")
    
    def __init__(self, edit=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.edit = edit
    
    def validate_nom(self, field):
        filiere = Filiere.query.filter_by(nom=field.data.strip()).first()
        if filiere and self.edit:
            raise ValidationError("Une Filiere avec ce nom existe déjà")


class DeleteFiliereForm(FlaskForm):
    pass

@bp.route('/', methods=['GET'])
@login_required
@admin_required
def list_filieres():
    filieres = Filiere.query.all()
    form = CSRFProtectForm()
    userFullName = current_user.prenom + " " + current_user.nom
    userInitials = current_user.prenom[0] + current_user.nom[0]
    return render_template(
        "dashboard/filiere/index.html",
        filieres=filieres,
        form=form,
        userFullName=userFullName,
        userInitials=userInitials
    )


@bp.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def create():
    form = FiliereForm()
    
    # Pre-fill the dropdowns with available options
    form.ecole_id.choices = [(ecole.id_ecole, ecole.nom) for ecole in Ecole.query.all()]
    form.series.choices = [(serie.id_serie, serie.nom) for serie in Serie.query.all()]
    form.matieres.choices = [(matiere.id_matiere, matiere.nom) for matiere in Matiere.query.all()]
    
    if form.validate_on_submit():
        # Create the Filiere
        filiere = Filiere(
            nom=form.nom.data.strip(),
            debouches=form.debouches.data,
            bourses=form.bourses.data,
            semi_bourses=form.semi_bourses.data,
            ecole_id=form.ecole_id.data
        )
        db.session.add(filiere)
        db.session.flush()  # Get the ID of the new Filiere
        
        # Link the Filiere to the selected Series
        for serie_id in form.series.data:
            filiere_series = FiliereSerie()
            filiere_series.id_filiere = filiere.id_filiere
            filiere_series.id_serie = serie_id
            db.session.add(filiere_series)
        
        # Link the Filiere to the selected Matieres
        for matiere_id in form.matieres.data:
            filiere_matiere = MatiereFiliere()
            filiere_matiere.id_filiere = filiere.id_filiere
            filiere_matiere.id_matiere = matiere_id
            db.session.add(filiere_matiere)
        
        db.session.commit()
        flash("Filière créée avec succès.", "success")
        return redirect(url_for("filieres.list_filieres"))
    
    return render_template("dashboard/filiere/create.html", form=form)


@bp.route("/edit/<string:filiere_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit(filiere_id):
    filiere = Filiere.query.get_or_404(filiere_id)
    form = FiliereForm(False)
    
    # Pre-fill the dropdowns with available options
    form.ecole_id.choices = [(ecole.id_ecole, ecole.nom) for ecole in Ecole.query.all()]
    form.series.choices = [(serie.id_serie, serie.nom) for serie in Serie.query.all()]
    form.matieres.choices = [(matiere.id_matiere, matiere.nom) for matiere in Matiere.query.all()]
    
    if request.method == "GET":
        # Pre-fill the form with the existing Filiere data
        form.nom.data = filiere.nom
        form.debouches.data = filiere.debouches
        form.bourses.data = filiere.bourses
        form.semi_bourses.data = filiere.semi_bourses
        form.ecole_id.data = filiere.id_ecole
        form.series.data = [serie.id_serie for serie in filiere.series]
        form.matieres.data = [matiere.id_matiere for matiere in filiere.matieres]
    
    if form.validate_on_submit():
        # Update the Filiere attributes
        filiere.nom = form.nom.data.strip()
        filiere.debouches = form.debouches.data
        filiere.bourses = form.bourses.data
        filiere.semi_bourses = form.semi_bourses.data
        filiere.id_ecole = form.ecole_id.data
        
        # Update Series relationships
        current_series_ids = {fs.id_serie for fs in filiere.filiereserie}
        new_series_ids = set(form.series.data)
        
        # Add new Series
        for serie_id in new_series_ids - current_series_ids:
            filiereserie_new = FiliereSerie()
            filiereserie_new.id_filiere = filiere.id_filiere
            filiereserie_new.id_serie = serie_id
            db.session.add(filiereserie_new)
        
        # Remove unselected Series
        for serie_id in current_series_ids - new_series_ids:
            FiliereSerie.query.filter_by(id_filiere=filiere.id_filiere, id_serie=serie_id).delete()
        
        # Update Matiere relationships
        current_matiere_ids = {mf.id_matiere for mf in filiere.matierefiliere}
        new_matiere_ids = set(form.matieres.data)
        
        # Add new Matieres
        for matiere_id in new_matiere_ids - current_matiere_ids:
            matierefiliere_new = MatiereFiliere()
            matierefiliere_new.id_filiere = filiere.id_filiere
            matierefiliere_new.id_matiere = matiere_id
            db.session.add(matierefiliere_new)
        
        # Remove unselected Matieres
        for matiere_id in current_matiere_ids - new_matiere_ids:
            MatiereFiliere.query.filter_by(id_filiere=filiere.id_filiere, id_matiere=matiere_id).delete()
        
        db.session.commit()
        flash("Filière mise à jour avec succès.", "success")
        return redirect(url_for("filieres.list_filieres"))
    
    return render_template("dashboard/filiere/edit.html", form=form, filiere=filiere)


@bp.route("/delete/<string:filiere_id>", methods=["POST"])
@login_required
@admin_required
def delete_filiere(filiere_id):
    form = DeleteFiliereForm()  
    if form.validate_on_submit():
        filiere = Filiere.query.get_or_404(filiere_id)
        db.session.delete(filiere)
        db.session.commit()
        flash('Filiere Supprimé avec success!', 'success')
        return redirect(url_for('filieres.list_filieres'))
    return "Erreur CSRF", 400
