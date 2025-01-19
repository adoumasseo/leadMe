from app.controllers.computation import bp
from app.extensions import db
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, ValidationError, NumberRange
from wtforms import StringField, SubmitField, SelectField, FieldList, FormField, FloatField
from app.database.models.user import User
from app.database.models.serie import Serie
from app.database.models.associations import Note
from flask_login import login_required, current_user, login_user
from flask import flash, redirect, url_for, render_template, request
from app.database.models.associations import MatiereFiliere, Moyenne, Coefficient, FiliereSerie
from flask_mail import Message
from weasyprint import HTML
from app.extensions import mail
from flask import current_app

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
        return redirect(url_for('computation.compute_average'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
    return render_template('computation/user-marks.html', form=form, matieres=matieres)

def compute_user_average(user):
    try:
        # Step 1: Get the user's Serie
        serie = Serie.query.get(user.id_serie)
        if not serie:
            raise ValueError("No associated serie found for the user.")

        # Step 2: Get related Filieres via FiliereSerie
        filiere_ids = [
            fs.id_filiere
            for fs in FiliereSerie.query.filter_by(id_serie=serie.id_serie).all()
        ]
        if not filiere_ids:
            raise ValueError("No filieres found for the user's serie.")

        # Step 3: Get Matieres related to those Filieres via MatiereFiliere
        matiere_ids = [
            mf.id_matiere
            for mf in MatiereFiliere.query.filter(MatiereFiliere.id_filiere.in_(filiere_ids)).all()
        ]
        # print(matiere_ids)
        if not matiere_ids:
            raise ValueError("No matieres found for the user's filieres.")

        # Step 4: Fetch Coefficients for the user's Serie and Matieres
        coefficients = Coefficient.query.filter(
            Coefficient.id_serie == serie.id_serie,
            Coefficient.id_matiere.in_(matiere_ids)
        ).all()
        
        if not coefficients:
            raise ValueError("No coefficients found for the user's matieres.")

        # Map coefficients by matiere_id for quick lookup
        coeff_map = {coef.id_matiere: coef.coe for coef in coefficients}
        
        # Step 5: Fetch Notes for the user and Matieres
        notes = Note.query.filter(
            Note.id_user == user.id_user,
            Note.id_matiere.in_(matiere_ids)
        ).all()
        
        if not notes:
            raise ValueError("No notes found for the user.")

        # Compute the weighted sum and total coefficients
        weighted_sum = 0
        total_coefficients = 0

        for note in notes:
            coe = coeff_map.get(note.id_matiere)
            if coe:
                weighted_sum += note.mark * coe
                total_coefficients += coe

        if total_coefficients == 0:
            raise ValueError("Total coefficients sum to zero, cannot compute average.")

        # Step 6: Calculate the average
        average = weighted_sum / total_coefficients

        # Step 7: Store the result in Moyenne for each Filiere
        for filiere_id in filiere_ids:
            moyenne = Moyenne.query.filter_by(
                id_user=user.id_user, id_filiere=filiere_id
            ).first()
            if not moyenne:
                moyenne = Moyenne()
                moyenne.id_user = user.id_user
                moyenne.id_filiere = filiere_id
                db.session.add(moyenne)

            moyenne.average = average
            # print(f"Computed average for user {user.id_user}: {average}")
            

        db.session.commit()

        # print(f"Computed average for user {user.id_user}: {average}")
        return average

    except Exception as e:
        print(f"Error computing average: {e}")
        db.session.rollback()
        raise


@bp.route('/user-result', methods=['GET', 'POST'])
@login_required
def compute_average():
    try:
        # Compute the user's average
        compute_user_average(current_user)

        # Get the user's Serie
        serie = Serie.query.get(current_user.id_serie)
        if not serie:
            raise ValueError("No associated serie found for the user.")

        # Get related Filieres via FiliereSerie
        filiere_series = FiliereSerie.query.filter_by(id_serie=serie.id_serie).all()
        if not filiere_series:
            raise ValueError("No filieres found for the user's serie.")

        # Build detailed data for the view
        filiere_data = []
        for filiere_serie in filiere_series:
            filiere = filiere_serie.filiere
            # Get Matieres related to this Filiere
            matiere_filiere = MatiereFiliere.query.filter_by(id_filiere=filiere.id_filiere).all()
            matieres = [mf.matiere for mf in matiere_filiere]

            # Get Notes for the user and those Matieres
            notes = Note.query.filter(
                Note.id_user == current_user.id_user,
                Note.id_matiere.in_([m.id_matiere for m in matieres])
            ).all()

            # Get Moyenne for this Filiere
            moyenne = Moyenne.query.filter_by(
                id_user=current_user.id_user, id_filiere=filiere.id_filiere
            ).first()

            # Build data for this filiere
            filiere_data.append({
                'filiere': filiere,
                'moyenne': moyenne.average if moyenne else None,
                'matieres': [
                    {
                        'matiere': matiere,
                        'note': next((note.mark for note in notes if note.id_matiere == matiere.id_matiere), None)
                    }
                    for matiere in matieres
                ]
            })

        # Sort filiere_data by moyenne in descending order
        filiere_data.sort(key=lambda x: x['moyenne'] if x['moyenne'] is not None else 0, reverse=True)

        # Render the result
        return render_template('computation/user-result.html', filieres=filiere_data)

    except Exception as e:
        flash(f"Error computing average: {e}", "error")
        return redirect(url_for('computation.compute_average'))


@bp.route('/generate-pdf', methods=['GET', 'POST'])
@login_required
def generate_pdf():
    try:

        serie = Serie.query.get(current_user.id_serie)
        if not serie:
            raise ValueError("No associated serie found for the user.")

        filiere_series = FiliereSerie.query.filter_by(id_serie=serie.id_serie).all()
        if not filiere_series:
            raise ValueError("No filieres found for the user's serie.")

        filiere_data = []
        for filiere_serie in filiere_series:
            filiere = filiere_serie.filiere
            matiere_filiere = MatiereFiliere.query.filter_by(id_filiere=filiere.id_filiere).all()
            matieres = [mf.matiere for mf in matiere_filiere]
            notes = Note.query.filter(
                Note.id_user == current_user.id_user,
                Note.id_matiere.in_([m.id_matiere for m in matieres])
            ).all()
            moyenne = Moyenne.query.filter_by(
                id_user=current_user.id_user, id_filiere=filiere.id_filiere
            ).first()
            filiere_data.append({
                'filiere': filiere,
                'moyenne': moyenne.average if moyenne else None,
                'matieres': [
                    {
                        'matiere': matiere,
                        'note': next((note.mark for note in notes if note.id_matiere == matiere.id_matiere), None)
                    }
                    for matiere in matieres
                ]
            })

        filiere_data.sort(key=lambda x: x['moyenne'] if x['moyenne'] is not None else 0, reverse=True)

        # Render HTML for PDF
        html = render_template('computation/user-result.html', filieres=filiere_data)
        pdf = HTML(string=html).write_pdf()

        # Email the PDF to the user
        subject = "Your Computation Results"
        recipient = current_user.email
        msg = Message(
            subject,
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[current_user.email]
        )
        msg.body = "Please find attached your computation results."
        msg.attach("computation_results.pdf", "application/pdf", pdf)
        mail.send(msg)

        return redirect(url_for('auth.logout'))
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return redirect(url_for('computation.compute_average'))