from app.extensions import db
from app.controllers.filiere import bp
from flask import render_template, redirect, url_for, flash, request
from app.middleware.auth import admin_required
from flask_login.utils import login_required, current_user
from app.database.models.filiere import Filiere
from app.database.models.associations import MatiereFiliere, FiliereSerie
from app.database.models.serie import Serie
from flask_wtf import FlaskForm

class CSRFProtectForm(FlaskForm):
    pass

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