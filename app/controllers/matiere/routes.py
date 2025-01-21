"""
Routes and cruds fonction of Matiere entity
"""
from flask import render_template, redirect, url_for, flash, request
from app.controllers.matiere import bp
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, FieldList, FormField
from wtforms.validators import DataRequired, NumberRange, ValidationError, InputRequired
from app.database.models.associations import Coefficient
from app.middleware.auth import admin_required
from flask_login.utils import login_required, current_user
from app.database.models.serie import Serie
from app.database.models.matiere import Matiere
from app.extensions import db

class CSRFProtectForm(FlaskForm):
    pass

class DeleteMatiereForm(FlaskForm):
    pass

class CoefficientForm(FlaskForm):
    serie_id = StringField("Serie ID", validators=[DataRequired()])
    serie_nom = StringField("Serie Name", validators=[])
    coe = FloatField("Coefficient", validators=[
        InputRequired("Please provide a valid number"),
        NumberRange(min=0, max=10, message="Mark must be between 0 and 10")
    ])

# Define the main form to contain multiple MarkForm instances
class MatiereCoefficientForm(FlaskForm):
    matiereNom = StringField("NOM matiere", validators=[DataRequired()])
    coefficients = FieldList(FormField(CoefficientForm), min_entries=1)
    submit = SubmitField('Soumettre')
    
    def validate_matiereNom(self, field):
        matiere = Matiere.query.filter_by(nom=field.data.strip()).first()
        if matiere:
            raise ValidationError("Une matière avec ce nom existe déjà")


@bp.route('/', methods=["GET"])
@login_required
@admin_required
def list_matieres():
    # Query all series with their related matières and coefficients
    series = Serie.query.all()
    
    # Transform data into a JSON-friendly format
    form = CSRFProtectForm()
    userFullName = current_user.prenom + " " + current_user.nom
    userInitials = current_user.prenom[0] + current_user.nom[0]
    results = []
    for serie in series:
        serie_data = {
            "id": serie.id_serie,
            "name": serie.nom,
            "matieres": [
                {
                    "id": ms.id_matiere,
                    "name": ms.nom,
                    "coefficient": Coefficient.query.filter_by(id_serie=serie.id_serie, id_matiere=ms.id_matiere).first().coe,
                    "created_at": ms.created_at,
                    "updated_at": ms.updated_at
                }
                for ms in serie.matieres
            ]
        }
        results.append(serie_data)
    return render_template(
        "dashboard/matiere/index.html",
        results=results,
        form=form,
        userFullName=userFullName,
        userInitials=userInitials
    )
    

@bp.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
def create():
    form = MatiereCoefficientForm()
    
    # Pre-fill the coefficients for all series
    if request.method == 'GET':
        form.coefficients.entries = []
        series = Serie.query.all()
        for serie in series:
            entry = form.coefficients.append_entry()
            entry.serie_id.data = serie.id_serie
            entry.serie_nom.data = serie.nom
            entry.coe.data = 0
    
    
    if form.validate_on_submit():
        
        # Create the Matiere
        matiere = Matiere(nom=form.matiereNom.data.strip())
        db.session.add(matiere)
        db.session.flush()  # Flush to get the matiere ID

        # Add coefficients for the matiere
        for entry in form.coefficients.entries:
            serie_id = entry.data.get("serie_id")
            coefficient = float(entry.data.get("coe"))
            
            if coefficient > 0:  # Only add if coefficient > 0
                coeff = Coefficient()
                coeff.id_matiere = matiere.id_matiere
                coeff.id_serie = serie_id
                coeff.coe = coefficient
                db.session.add(coeff)
        
        db.session.commit()
        flash("Matière créée avec succès.", "success")
        return redirect(url_for("matieres.list_matieres"))
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
    return render_template("dashboard/matiere/create.html", form=form)


@bp.route("/delete/<string:matiere_id>", methods=["POST"])
@login_required
@admin_required
def delete(matiere_id):
    form = DeleteMatiereForm()  
    if form.validate_on_submit():
        matiere = Matiere.query.get_or_404(matiere_id)
        db.session.delete(matiere)
        db.session.commit()
        flash('Ecole supprimé avec succès!', 'success')
        return redirect(url_for('matieres.list_matieres'))
    return "Erreur CSRF", 400