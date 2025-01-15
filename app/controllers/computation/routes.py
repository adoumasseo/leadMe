from app.controllers.computation import bp
from app.extensions import db
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms import StringField, SubmitField, HiddenField, SelectField
from app.database.models.user import User
from app.database.models.serie import Serie
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
def user_marks():
    return "User Marks"