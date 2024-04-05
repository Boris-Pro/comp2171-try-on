import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.models import UserProfile
from app.models import Product, Cart, Review
from app.forms import LoginForm
from app.forms import RegisterForm, ReviewForm
from werkzeug.security import check_password_hash
from app.helper import get_uploaded_images
from flask import send_from_directory
from app.forms import ProductForm
from flask.views import View
from app.views import flash_errors


# class HomeController(View):
#     def dispatch_request(self):
#         products = Product.query.all()
#         for prod in products:
#             prod.image_url = url_for('send_image', filename=prod.image_filename)
#         return render_template('home2.html', products=products)

# app.add_url_rule('/', view_func=HomeController.as_view('home'))

class HomeController(View):
    def dispatch_request(self):
        # Logic to fetch products from the database
        products = Product.query.all()
        for prod in products:
            prod.image_url = url_for('send_image', filename=prod.image_filename)
        # Render the template and pass the products to it
        return render_template('home.html', products=products)

# Registering the HomeController class with the 'home' endpoint
app.add_url_rule('/', view_func=HomeController.as_view('home'))


class AboutController(View):
    def dispatch_request(self):
        return render_template('about.html', name="Mary Jane")
    
app.add_url_rule('/about/', view_func=AboutController.as_view('about'))

class RegisterController(View):
    def get(self):
        myform = RegisterForm()
        return render_template('register.html', form=myform)

    def post(self):
        myform = RegisterForm()
        if request.method == 'POST' and myform.validate_on_submit():
            # Your registration logic here
            flash('You have successfully filled out the form', 'success')
            return redirect(url_for('home'))
        flash_errors(myform)
        return render_template('register.html', form=myform)

class DashboardController(View):
    decorators = [login_required]

    def get(self):
        if current_user.user_type == 'seller':
            products = Product.query.filter_by(seller_id=current_user.id).all()
            return render_template('dashboard.html', products=products)
        else:
            flash('Access denied! You are not authorized to view this page.', 'danger')
            return redirect(url_for('home'))

class ProductEditController(View):
    decorators = [login_required]

    def get(self, product_id):
        product = Product.query.get_or_404(product_id)
        if current_user.user_type == 'seller' and product.seller_id == current_user.id:
            form = ProductForm(obj=product)
            return render_template('edit_product.html', form=form, product=product)
        else:
            flash('Access denied! You are not authorized to edit this product.', 'danger')
            return redirect(url_for('dashboard'))

    def post(self, product_id):
        product = Product.query.get_or_404(product_id)
        if current_user.user_type == 'seller' and product.seller_id == current_user.id:
            form = ProductForm(obj=product)
            if form.validate_on_submit():
                # Update product logic here
                flash('Product updated successfully!', 'success')
                return redirect(url_for('dashboard'))
            return render_template('edit_product.html', form=form, product=product)
        else:
            flash('Access denied! You are not authorized to edit this product.', 'danger')
            return redirect(url_for('dashboard'))

class ProductDeleteController(View):
    decorators = [login_required]

    def post(self, product_id):
        product = Product.query.get_or_404(product_id)
        if current_user.user_type == 'seller' and product.seller_id == current_user.id:
            # Delete product logic here
            flash('Product deleted successfully!', 'success')
        else:
            flash('Access denied! You are not authorized to delete this product.', 'danger')
        return redirect(url_for('dashboard'))

class LoginController(View):
    def get(self):
        form = LoginForm()
        return render_template("login.html", form=form)

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            # Login logic here
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home'))
        flash('Invalid username or password.', 'danger')
        return render_template("login.html", form=form)
    
# def flash_errors(form):
#     for field, errors in form.errors.items():
#         for error in errors:
#             flash(u"Error in the %s field - %s" % (
#                 getattr(form, field).label.text,
#                 error
# ), 'danger')

# Add URL rules for the controller classes


# app.add_url_rule('/register', view_func=RegisterController.as_view('register'))
# app.add_url_rule('/dashboard', view_func=DashboardController.as_view('dashboard'))
# app.add_url_rule('/product/edit/<int:product_id>', view_func=ProductEditController.as_view('edit_product'))
# app.add_url_rule('/product/delete/<int:product_id>', view_func=ProductDeleteController.as_view('delete_product'))
# app.add_url_rule('/login', view_func=LoginController.as_view('login'))
