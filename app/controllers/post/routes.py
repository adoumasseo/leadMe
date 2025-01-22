from app.controllers.post import bp
from flask_login.utils import login_required, current_user
from app.middleware.auth import admin_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
from app.extensions import db
from app.database.models.post import Post
from flask import flash, render_template, redirect, url_for, current_app
from werkzeug.utils import secure_filename
import os

class CSRFProtectForm(FlaskForm):
    pass

class CreatePostForm(FlaskForm):
    titre = StringField('Titre de la Bourse', validators=[DataRequired(message="Le titre ne doit pas être vide.")])
    adresse = StringField('Adresse')
    contenu = TextAreaField('Contenu de la Bourse', validators=[DataRequired(message="Le contenu ne doit pas être vide.")])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'], 'Seules les images sont autorisées!')])
    submit = SubmitField('Soumettre')

class EditPostForm(FlaskForm):
    titre = StringField('Titre', validators=[DataRequired(message="Le titre ne doit pas être vide.")])
    adresse = StringField('Adresse')
    contenu = TextAreaField('Contenu', validators=[DataRequired(message="Le contenu ne doit pas être vide.")])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png'], 'Seules les images sont autorisées!')])
    submit = SubmitField('Modifier')

class DeletePostForm(FlaskForm):
    pass

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'png'}

@bp.route('/', methods=["GET"])
@login_required
@admin_required
def list_posts():
    posts = Post.query.all()
    form = CSRFProtectForm()
    userFullName = current_user.prenom + " " + current_user.nom
    userInitials = current_user.prenom[0] + current_user.nom[0]
    return render_template(
        "dashboard/post/index.html",
        posts=posts,
        form=form,
        userFullName=userFullName,
        userInitials=userInitials
    )

@bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    """Create Post"""
    form = CreatePostForm()
    if form.validate_on_submit():
        filename = None
        
        if form.image.data and allowed_file(form.image.data.filename):
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        
        new_post = Post(
            titre=form.titre.data.strip(),
            adresse=form.adresse.data.strip(),
            contenu=form.contenu.data.strip(),
            imagePath=filename,
            user_id=current_user.id_user
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Post créé avec succès!', 'success')
        return redirect(url_for('posts.list_posts'))
    return render_template('dashboard/post/create.html', form=form)

@bp.route('/edit/<string:post_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    form = EditPostForm(obj=post)
    if form.validate_on_submit():
        if form.image.data and allowed_file(form.image.data.filename):
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            post.imagePath = filename
        post.titre = form.titre.data.strip()
        post.adresse = form.adresse.data.strip()
        post.contenu = form.contenu.data.strip()
        db.session.commit()
        flash('Post modifié avec succès!', 'success')
        return redirect(url_for('posts.list_posts'))
    return render_template('dashboard/post/edit.html', form=form, post=post)

@bp.route('/delete/<string:post_id>', methods=['POST'])
@login_required
@admin_required
def delete(post_id):
    form = DeletePostForm()
    if form.validate_on_submit():
        post = Post.query.get_or_404(post_id)
        if post.imagePath:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], post.imagePath))
        db.session.delete(post)
        db.session.commit()
        flash('Post supprimé avec succès!', 'success')
        return redirect(url_for('posts.list_posts'))
    return "Erreur CSRF", 400

