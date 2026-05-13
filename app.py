from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:JSpbLoPXKodnxPTBVLiaEgEELcbzsHtn@mysql.railway.internal:3306/railway'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telephone = db.Column(db.String(20))

@app.route('/inscription', methods=['POST'])
def inscription():
    data = request.json
    user = User(
        nom=data['nom'],
        prenom=data['prenom'],
        email=data['email'],
        telephone=data['telephone']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'تم التسجيل بنجاح!'})

with app.app_context():
    db.create_all()

@app.route('/admin')
def admin():
    users = User.query.all()
    html = '<h1>قائمة المسجلين</h1><table border="1"><tr><th>ID</th><th>الاسم</th><th>الإيميل</th><th>الهاتف</th></tr>'
    for u in users:
        html += f'<tr><td>{u.id}</td><td>{u.nom}</td><td>{u.email}</td><td>{u.telephone}</td></tr>'
    html += '</table>'
    return html

if __name__ == '__main__':
    app.run(debug=True)