from flask import Flask, render_template, request, redirect, url_for
from models import db, Activity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///activities.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    activities = Activity.query.all()
    return render_template('index.html', activities=activities)

@app.route('/add', methods=['GET', 'POST'])
def add_activity():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        duration = int(request.form['duration'])
        new_act = Activity(name=name, category=category, duration=duration)
        db.session.add(new_act)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_activity.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Skapar databasen första gången
    app.run(debug=True)




