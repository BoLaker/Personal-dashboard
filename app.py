from flask import Flask, render_template, request, redirect, url_for
from models import db, Activity
from utils import generate_activity_plot


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

@app.route('/stats')
def stats():
    plot_url=generate_activity_plot()
    return render_template('stats.html', plot_url=plot_url)

@app.route('/delete/<int:id>')
def delete_activity(id):
    activity = Activity.query.get_or_404(id)
    db.session.delete(activity)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_activity(id):
    activity = Activity.query.get_or_404(id)

    if request.method == 'POST':
        activity.name = request.form['name']
        activity.category = request.form['category']
        activity.duration = int(request.form['duration'])

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_activity.html', activity=activity)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Skapar databasen första gången
    app.run(debug=True)




