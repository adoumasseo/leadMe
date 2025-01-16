from app.controllers.computation import bp
from app.extensions import db
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, ValidationError, NumberRange
from wtforms import StringField, SubmitField, SelectField, FieldList, FormField
from app.database.models.user import User
from app.database.models.serie import Serie
from app.database.models.associations import Note
from flask_login import login_required, current_user, login_user, logout_user
from flask import flash, redirect, url_for, render_template, request

class CSRFProtectForm(FlaskForm):
    """For CSRF protection"""
    pass

class UserInformations(FlaskForm):
    """This class will be use to create a form for retriving user information"""
    nom = StringField("Nom", validators=[DataRequired("Your LastName is require")])
    prenom = StringField("Nom", validators=[DataRequired("Your FirstName is require")])
    email = StringField('Email', validators=[DataRequired(message="The Email is require"), Email()])
    matricule = StringField("Matricule", validators=[DataRequired("Your Matricule is require")])
    serie = SelectField("Université", choices=[], validators=[DataRequired(message="Choose your serie")])
    submit = SubmitField('Next')
    
    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Email already used for an record')

    def __init__(self, *args, **kwargs):
        super(UserInformations, self).__init__(*args, **kwargs)
        self.serie.choices = [(s.id_serie, s.nom) for s in Serie.query.all()]
    

class MarkForm(FlaskForm):
    matiere_id = StringField("Matiere ID", validators=[DataRequired()], render_kw={"readonly": True})
    matiere_nom = StringField("Matiere Name", validators=[DataRequired()], render_kw={"readonly": True})
    mark = StringField("Mark", validators=[
        DataRequired("Please provide a mark"),
        NumberRange(min=0, max=20, message="Mark must be between 0 and 20")
    ])

# Define the main form to contain multiple MarkForm instances
class UserMarksForm(FlaskForm):
    marks = FieldList(FormField(MarkForm), min_entries=1)
    submit = SubmitField('Save Marks')


@bp.route('/user-informations', methods=['GET', 'POST'])
def user_information():
    form = UserInformations()
    if form.validate_on_submit():
        user = User(
            nom=form.nom.data,
            prenom=form.prenom.data,
            email=form.email.data,
            matricule=form.matricule.data,
            serie_id = form.serie.data
        )
        db.session.add(user)
        db.session.commit()
        user_log = User.query.filter_by(email=form.email.data).first()
        login_user(user_log)
        return redirect(url_for('computation.user_marks'))
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
    return render_template('computation/user-informations.html', form=form)
    
@bp.route('/user-marks', methods=['GET', 'POST'])
@login_required
def user_marks():
    user = current_user
    serie = Serie.query.get(user.id_serie)
    if not serie:
        flash("No associated serie found for this user.", "error")
        return redirect(url_for('computation.user_information'))
    
    matieres = serie.matieres

    # Prepare initial data for the form
    marks_data = [
        {"matiere_id": matiere.id_matiere, "matiere_nom": matiere.nom}
        for matiere in matieres
    ]

    form = UserMarksForm()
    
    # Populate form's FieldList with matieres if GET request
    if request.method == 'GET':
        form.marks.entries = []
        for mark_data in marks_data:
            form.marks.append_entry(mark_data)

    # Handle form submission
    if form.validate_on_submit():
        for mark_entry in form.marks.entries:
            matiere_id = mark_entry.data["matiere_id"]
            mark_value = float(mark_entry.data["mark"])
            
            # Save each mark in the database
            user_mark = Note(
                id_user=user.id_user,
                id_matiere=matiere_id,
                mark=mark_value
            )
            db.session.add(user_mark)
        
        db.session.commit()
        flash("Marks saved successfully!", "success")
        return redirect(url_for('computation.user_result'))

    return render_template('computation/user-marks.html', form=form, matieres=matieres)

    
@bp.route('/user-result', methods=['GET', 'POST'])
@login_required
def user_result():
    return 'User Result'