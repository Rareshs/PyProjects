from flask import Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
import os

app = Flask(__name__)

# Set up configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback_secret_key')  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Initialize database
db = SQLAlchemy(app)

# Set up LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, default=1)

# Forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CheckoutForm(FlaskForm):
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Checkout')
# Load user function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home Route
@app.route("/")
def home():
    products = Product.query.all()  # Get all products to display on homepage
    return render_template('home.html', products=products)

# Registration Route
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)  
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# Login Route
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            print("User found:", user.username)  # Debugging
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                print("Password incorrect")  # Debugging
        else:
            print("User not found")  # Debugging
        flash('Login unsuccessful. Check email and password.', 'danger')
    return render_template('login.html', form=form)


# Logout Route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', 'info')
    return redirect(url_for('home'))

# Add to Cart Route
@app.route("/add_to_cart/<int:product_id>")
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    existing_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()
    if existing_item:
        existing_item.quantity += 1
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product.id, quantity=1)
        db.session.add(cart_item)
    db.session.commit()
    flash(f'Added {product.name} to cart.', 'success')
    return redirect(url_for('home'))

# Remove from Cart Route
# Cart Route

@app.route("/cart")
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    # Fetch products for each cart item
    products = Product.query.filter(Product.id.in_([item.product_id for item in cart_items])).all()
    product_dict = {product.id: product for product in products}
    
    total_price = sum(product_dict[item.product_id].price * item.quantity for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, product_dict=product_dict, total_price=total_price)


# Simulated Checkout Route
@app.route("/checkout", methods=['GET', 'POST'])
@login_required
def checkout():
    form = CheckoutForm()
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash('Your cart is empty! Add items before checking out.', 'warning')
        return redirect(url_for('home'))
    
    if form.validate_on_submit():
        # Fetch products for the cart items
        product_ids = [item.product_id for item in cart_items]
        products = Product.query.filter(Product.id.in_(product_ids)).all()
        product_dict = {product.id: product for product in products}

        total_price = sum(product_dict[item.product_id].price * item.quantity for item in cart_items)

        # Simulate a successful checkout by clearing the cart
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash(f'Checkout successful! You have been charged ${total_price:.2f}.', 'success')
        return redirect(url_for('home'))

    return render_template('checkout.html', form=form)


# Remove from Cart Route
@app.route("/remove_from_cart/<int:product_id>")
@login_required
def remove_from_cart(product_id):
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from your cart.', 'success')
    else:
        flash('Item not found in your cart.', 'warning')
    return redirect(url_for('cart'))


# def add_sample_products():
#     if Product.query.count() == 0:  # Check if products already exist
#         product1 = Product(name='Sneaker 1', price=79.99, description='A comfortable sneaker.', image_url='https://via.placeholder.com/150')
#         product2 = Product(name='Sneaker 2', price=89.99, description='A stylish sneaker.', image_url='https://via.placeholder.com/150')
#         db.session.add(product1)
#         db.session.add(product2)
#         db.session.commit()
#         print("Sample products added.")



with app.app_context():
    db.create_all()
# Run the app
if __name__ == "__main__":
    app.run(debug=True)
