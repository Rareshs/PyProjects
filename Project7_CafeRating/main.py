from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, URL, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Needed for form validation with CSRF protection
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class AddCafeForm(FlaskForm):
    name = StringField("Cafe's Name", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[URL()])
    img_url = StringField("Image URL", validators=[URL()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = BooleanField("Has Sockets?")
    has_toilet = BooleanField("Has Toilet?")
    has_wifi = BooleanField("Has WiFi?")
    can_take_calls = BooleanField("Can Take Calls?")
    seats = IntegerField("Number of Seats", validators=[DataRequired(), NumberRange(min=1)])
    coffee_price = FloatField("Coffee Price", validators=[DataRequired(), NumberRange(min=0)])

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    map_url = db.Column(db.String(200))
    img_url = db.Column(db.String(200))
    location = db.Column(db.String(100))
    has_sockets = db.Column(db.Boolean, default=False)
    has_toilet = db.Column(db.Boolean, default=False)
    has_wifi = db.Column(db.Boolean, default=False)
    can_take_calls = db.Column(db.Boolean, default=False)
    seats = db.Column(db.Integer)
    coffee_price = db.Column(db.Float)

@app.route('/')
def home():
    cafes = Cafe.query.all()  
    return render_template('coffee_list.html', cafes=cafes)

@app.route('/add', methods=["GET", "POST"])
def add():
    form = AddCafeForm()
    if form.validate_on_submit():
        new_cafe = Cafe(
            name=form.name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=form.has_sockets.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        flash("New cafe added successfully!", "success")
        return redirect(url_for('home'))
    return render_template('add_cafe.html', form=form)

@app.route('/delete/<int:cafe_id>', methods=["POST"])
def delete_cafe(cafe_id):
    cafe_to_delete = Cafe.query.get_or_404(cafe_id)
    
    db.session.delete(cafe_to_delete)
    db.session.commit()
    
    flash(f"The cafe '{cafe_to_delete.name}' has been deleted.", "success")
    return redirect(url_for('home'))

@app.route('/edit/<int:cafe_id>', methods=["GET", "POST"])
def edit_cafe(cafe_id):
    cafe = Cafe.query.get_or_404(cafe_id)
    form = AddCafeForm(
        name=cafe.name,
        map_url=cafe.map_url,
        img_url=cafe.img_url,
        location=cafe.location,
        has_sockets=cafe.has_sockets,
        has_toilet=cafe.has_toilet,
        has_wifi=cafe.has_wifi,
        can_take_calls=cafe.can_take_calls,
        seats=cafe.seats,
        coffee_price=cafe.coffee_price
    )

    if form.validate_on_submit():
        cafe.name = form.name.data
        cafe.map_url = form.map_url.data
        cafe.img_url = form.img_url.data
        cafe.location = form.location.data
        cafe.has_sockets = form.has_sockets.data
        cafe.has_toilet = form.has_toilet.data
        cafe.has_wifi = form.has_wifi.data
        cafe.can_take_calls = form.can_take_calls.data
        cafe.seats = form.seats.data
        cafe.coffee_price = form.coffee_price.data
        
        db.session.commit()
        flash(f"The cafe '{cafe.name}' has been updated successfully!", "success")
        return redirect(url_for('home'))
    
    return render_template('edit_cafe.html', form=form, cafe=cafe)

if __name__ == "__main__":
    app.run(debug=True)
