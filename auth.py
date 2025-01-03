"""Define function views for login and register
"""
from flask import (
        Blueprint, url_for, redirect, request, render_template, flash
        )
from werkzeug.security import check_password_hash
from flask_login import login_user
from .models.User import User
from .models.Matiere import Matiere
from .db import db
from .FormValidator import RegistrationForm, LoginForm


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=("GET", "POST"))
def register():
    """Permet a l'utilisateur de s'enregistrer"""
    form = RegistrationForm(request.form)
    r_or_l = "register"
    if request.method == "POST":
        """if not form.validate():
            return render_template("auth/register_login.html",
                                    form=form, r_or_l=r_or_l)"""
        user = User(
            matricule=request.form.get("matricule"),
            prenom=request.form.get("prenom"),
            nom=request.form.get("nom"),
            email=request.form.get("email"),
            password=request.form.get("password"),
            serie=request.form.get("serie")
         )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        
        return redirect(url_for('notes.traiter'))
    return render_template("login.html", r_or_l=r_or_l)

@auth_bp.route("/login", methods=("GET", "POST"))
def login():
    """Permet a l'utilisateur de se connecter a l'application"""
    r_or_l = "login"
    if request.method == "POST":
        matricule = request.form.get('matricule')
        password = request.form.get('password')

        user = User.query.filter_by(matricule=matricule).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        
        return redirect(url_for('notes.traiter'))
    return render_template("login.html", r_or_l=r_or_l)
