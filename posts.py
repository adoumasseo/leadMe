"""
Routes and CRUD functions of Post entity
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
from lead_me.models.User import User
from lead_me.models.Post import Post
from flask_login import current_user
from .db import db
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

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'png'}

@posts_bp.route('/', methods=["GET"])
def list_posts():
    posts = Post.query.all()
    form = CSRFProtectForm()
    return render_template("dashboard/posts/index.html", posts=posts, form=form)

@posts_bp.route('/create', methods=['GET', 'POST'])
def create():
    """Create Post"""
    form = CreatePostForm()
    current_user = User.query.filter_by(matricule='ROOT').first()
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
            user_id=current_user.id 
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Post créé avec succès!', 'success')
        return redirect(url_for('posts.list_posts'))
    return render_template('dashboard/posts/create.html', form=form)

@posts_bp.route('/edit/<string:post_id>', methods=['GET', 'POST'])
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
    return render_template('dashboard/posts/edit.html', form=form, post=post)

@posts_bp.route('/delete/<string:post_id>', methods=['POST'])
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
