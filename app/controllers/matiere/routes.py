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
    submit = SubmitField('Submit')
    
    def __init__(self, edit=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.edit = edit
    
    def validate_matiereNom(self, field):
        matiere = Matiere.query.filter_by(nom=field.data.strip()).first()
        if matiere and self.edit:
            raise ValidationError("A subject with that name alredy exist")


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
        flash("Subject successfully created.", "success")
        return redirect(url_for("matieres.list_matieres"))
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
    return render_template("dashboard/matiere/create.html", form=form)

@bp.route("/edit/<string:matiere_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit(matiere_id):
    # Fetch the Matiere by ID
    matiere = Matiere.query.get_or_404(matiere_id)
    
    # Initialize the form
    form = MatiereCoefficientForm(False)
    
    # Pre-fill the form with existing data on GET
    if request.method == "GET":
        form.matiereNom.data = matiere.nom  # Set the current name of the Matiere
        
        # Pre-fill coefficients for all series
        form.coefficients.entries = []
        series = Serie.query.all()
        
        # Fetch existing coefficients for the Matiere
        existing_coefficients = {c.id_serie: c.coe for c in matiere.coefficient}
        
        for serie in series:
            entry = form.coefficients.append_entry()
            entry.serie_id.data = serie.id_serie
            entry.serie_nom.data = serie.nom
            entry.coe.data = existing_coefficients.get(serie.id_serie, 0)  # Default to 0 if no coefficient
    
    # Handle form submission
    if form.validate_on_submit():
        # Update the Matiere name
        matiere.nom = form.matiereNom.data.strip()
        
        # Update coefficients
        for entry in form.coefficients.entries:
            serie_id = entry.data.get("serie_id")
            coefficient = float(entry.data.get("coe"))
            
            # Find the existing coefficient or create a new one
            existing_coeff = next(
                (c for c in matiere.coefficient if c.id_serie == serie_id),
                None
            )
            
            if coefficient > 0:
                if existing_coeff:
                    existing_coeff.coe = coefficient  # Update the coefficient
                else:
                    # Add a new coefficient
                    new_coeff = Coefficient()
                    new_coeff.id_matiere = matiere.id_matiere
                    new_coeff.id_serie = serie_id
                    new_coeff.coe = coefficient
                    db.session.add(new_coeff)
            elif existing_coeff:
                # Remove the coefficient if it's now 0
                db.session.delete(existing_coeff)
        
        db.session.commit()
        flash("Subject successfully updated.", "success")
        return redirect(url_for("matieres.list_matieres"))
    
    # Display errors if validation fails
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
    
    return render_template("dashboard/matiere/edit.html", form=form, matiere=matiere)


@bp.route("/delete/<string:matiere_id>", methods=["POST"])
@login_required
@admin_required
def delete(matiere_id):
    form = DeleteMatiereForm()  
    if form.validate_on_submit():
        matiere = Matiere.query.get_or_404(matiere_id)
        db.session.delete(matiere)
        db.session.commit()
        flash('Subject successfully deleted/', 'success')
        return redirect(url_for('matieres.list_matieres'))
    return "Erreur CSRF", 400