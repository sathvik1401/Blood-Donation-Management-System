from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    blood_group = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    location = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    blood_group = request.form['blood_group']
    phone = request.form['phone']
    location = request.form['location']

    if not name or not blood_group or not phone or not location:
        return render_template('index.html', error="All fields are required!")

    new_donor = Donor(name=name, blood_group=blood_group, phone=phone, location=location)
    db.session.add(new_donor)
    db.session.commit()
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/donors', methods=['GET'])
def donor_list():
    search = request.args.get('search', '')
    if search:
        donors = Donor.query.filter(Donor.blood_group == search).all()
    else:
        donors = Donor.query.all()
    return render_template('donors.html', donors=donors)



@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_donor(id):
    donor = Donor.query.get_or_404(id)
    if request.method == 'POST':
        donor.name = request.form['name']
        donor.blood_group = request.form['blood_group']
        donor.phone = request.form['phone']
        donor.location = request.form['location']
        db.session.commit()
        return redirect(url_for('donor_list'))
    return render_template('edit.html', donor=donor)

@app.route('/delete/<int:id>')
def delete_donor(id):
    donor = Donor.query.get_or_404(id)
    db.session.delete(donor)
    db.session.commit()
    return redirect(url_for('donor_list'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
