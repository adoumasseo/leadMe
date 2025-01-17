from app.controllers.computation import bp
from app.extensions import db
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, ValidationError, NumberRange
from wtforms import StringField, SubmitField, SelectField, FieldList, FormField, FloatField, HiddenField
from app.database.models.user import User
from app.database.models.serie import Serie
from app.database.models.associations import Note
from flask_login import login_required, current_user, login_user, logout_user
from flask import flash, redirect, url_for, render_template, request
from app.utils.debug import dd

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
    matiere_id = StringField("Matiere ID", validators=[])
    matiere_nom = StringField("Matiere Name", validators=[])
    mark = FloatField("Mark", validators=[
        DataRequired("Please provide a valid number"),
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
    """
        For real i don't know how this function is working.
        Not feel good to investigate :(, i will surely come later on it
    """
    user = current_user
    serie = Serie.query.get(user.id_serie)
    print("In controller")
    if not serie:
        print("not serie")
        flash("No associated serie found for this user.", "error")
        return redirect(url_for('computation.user_information'))
    
    matieres = serie.matieres

    # Prepare initial data for the form
    marks_data = [
        {"matiere_id": matiere.id_matiere, "matiere_nom": matiere.nom}
        for matiere in matieres
    ]
    print(marks_data)
    form = UserMarksForm()
    
    # Populate form's FieldList with matieres if GET request
    if request.method == 'GET':
        form.marks.entries = []
        for mark_data in marks_data:
            entry = form.marks.append_entry()
            entry.matiere_id.data = mark_data['matiere_id']
            entry.matiere_nom.data = mark_data['matiere_nom']
           
    # Handle form submission
    if form.validate_on_submit():
        print("Form validation errors:", form.errors)
        for mark_entry in form.marks.entries:
            matiere_id = mark_entry.data.get("matiere_id")
            mark_value = mark_entry.data.get("mark")
            if not matiere_id or not mark_value:
                print("Missing matiere_id or mark_value:", mark_entry.data)
                continue
            user_mark = Note()
            user_mark.id_user = user.id_user
            user_mark.id_matiere = matiere_id
            user_mark.mark = mark_value
            db.session.add(user_mark)
        
        try:
            db.session.commit()
            flash("Marks saved successfully!", "success")
        except Exception as e:
            db.session.rollback()
            print(f"Database error: {e}")
            flash("An error occurred while saving marks.", "error")
        flash("Marks saved successfully!", "success")
        return redirect(url_for('computation.user_result'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
    return render_template('computation/user-marks.html', form=form, matieres=matieres)

    
@bp.route('/user-result', methods=['GET', 'POST'])
@login_required
def user_result():
    return 'User Result'