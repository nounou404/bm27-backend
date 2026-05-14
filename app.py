import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import cloudinary
import cloudinary.uploader

app = Flask(__name__)
CORS(app, origins="*")

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:JSpbLoPXKodnxPTBVLiaEgEELcbzsHtn@yamabiko.proxy.rlwy.net:54887/railway')app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cloudinary.config(
    cloud_name='dxbbtf3lh',
    api_key='871243736664454',
    api_secret='0Otie6nOAle0l7vZzBWMs_KKg-I'
)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    document = db.Column(db.String(500))

@app.route('/inscription', methods=['POST'])
def inscription():
    nom = request.form.get('nom') or request.form.get('name', '')
    prenom = request.form.get('prenom', '')
    email = request.form.get('email', '')
    telephone = request.form.get('telephone', '')
    document_url = ''
    if 'file' in request.files:
        file = request.files['file']
        result = cloudinary.uploader.upload(file)
        document_url = result['secure_url']
    user = User(nom=nom, prenom=prenom, email=email, telephone=telephone, document=document_url)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'تم التسجيل بنجاح!'})

@app.route('/admin')
def admin():
    users = User.query.all()
    html = '<h1>قائمة المسجلين</h1><table border="1"><tr><th>ID</th><th>الاسم</th><th>الإيميل</th><th>الهاتف</th><th>الوثيقة</th></tr>'
    for u in users:
        doc = f'<a href="{u.document}">شوف الوثيقة</a>' if u.document else 'لا يوجد'
        html += f'<tr><td>{u.id}</td><td>{u.nom}</td><td>{u.email}</td><td>{u.telephone}</td><td>{doc}</td></tr>'
    html += '</table>'
    return html

with app.app_context():
    db.create_all()

if __name__ == '__main__':
   app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))