import pytz
import os
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session, send_file, make_response
from flask import session as flask_session
from flask_bcrypt import Bcrypt
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from datetime import datetime, timedelta
import cloudinary
import cloudinary.uploader
import tempfile
from weasyprint import HTML, CSS
import pymysql
from werkzeug.utils import secure_filename


from sqlalchemy import text

created_at = datetime.now()

def check_session_timeout():
    if 'username' in session:
        if 'last_activity' in session:
            last_activity = datetime.fromisoformat(session['last_activity'])
            if datetime.now() - last_activity > timedelta(minutes=60):
                session.clear()
                return False
        session['last_activity'] = datetime.now().isoformat()
        return True
    return False

"""
cloudinary.config( 
  cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME"), 
  api_key = os.environ.get("CLOUDINARY_API_KEY"), 
  api_secret = os.environ.get("CLOUDINARY_API_SECRET")
)
"""
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")
app.permanent_session_lifetime = timedelta(minutes=60)


@app.route("/")
def hello_pm1():
        if not check_session_timeout():
            #flash('Su sesión ha expirado. Por favor, inicie sesión nuevamente.', 'danger')
            return redirect(url_for('login'))

        pg = load_pg_from_db2()

        es_profesor = flask_session.get('es_profesor', False)
        username = flask_session.get('username', 'Invitado')


        return render_template('home.html', es_profesor=es_profesor , pg=pg, username=username)