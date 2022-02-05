from app import db, create_app
from models import File
from flask import Flask, Blueprint, render_template, request, redirect, send_file
from sqlalchemy import desc
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from werkzeug import filesystem
import os

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
def index():
    return render_template("index.html")


@main.route('/profile')
@login_required
def profile():
    return render_template("profile.html", username=current_user.username)


@main.route('/user-files/<string:name>')
@login_required
def user_info(name):
    return render_template("user.html")


@main.route('/files')
def files():
    files = File.query.order_by(desc(File.downloads)).all()
    return render_template("files.html", files=files)


@main.route('/myfiles')
def my_files():
    my_files = File.query.order_by(desc(File.downloads)).get(current_user.username)
    return render_template("myfiles.html", files=my_files)


@main.route('/allfiles')
def all_files():
    all_files = File.query.order_by(desc(File.downloads)).all()
    return render_template("allfiles.html", files=all_files)


@main.route('/files/<int:id>')
def download_file(id):
    file = File.query.get_or_404(id)
    file.downloads += 1
    db.session.commit()
    return send_file(os.path.join('files', file.filename), as_attachment=True)


@main.route('/delete-file/<int:id>')
@login_required
def delete_file(id):
    file = File.query.get_or_404(id)
    fpath = os.path.join('files', file.filename)
    try:
        if os.path.exists(fpath):
            os.remove(fpath)
        db.session.delete(file)
        db.session.commit()
        return redirect('/files')
    except:
        return 'Error'


@main.route('/create-file', methods=['POST', 'GET'])
@login_required
def create_file():
    if request.method == "POST":
        filepath = request.files['filepath']
        filename = filepath.filename
        private = request.form['private']
        if private == 'True':
            private = True
        else:
            private = False
        created_by = current_user.username
        if not os.path.exists('files'):
            os.mkdir(os.path.join('files'))
        filepath.save(os.path.join('files', filepath.filename))
        file = File(filename=filename, filepath=filepath.filename, created_by=created_by, private=private)

        db.session.add(file)

        db.session.commit()
        try:
            return redirect('/files')
        except:
            return "Error"
    else:
        return render_template("create-file.html")


if __name__ == "__main__":
    create_app().run(debug=True)
