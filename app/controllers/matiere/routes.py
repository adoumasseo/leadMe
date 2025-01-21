"""
Routes and cruds fonction of Matiere entity
"""
from flask import render_template, redirect, url_for
from app.controllers.matiere import bp
from flask_wtf import FlaskForm
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
    



@bp.route("/delete/<string:matiere_id>", methods=["POST"])
@login_required
@admin_required
def delete(matiere_id):
    form = DeleteMatiereForm()  
    if form.validate_on_submit():
        matiere = Matiere.query.get_or_404(matiere_id)
        db.session.delete(matiere)
        db.session.commit()
        return redirect(url_for('matieres.list_matieres'))
    return "Erreur CSRF", 400