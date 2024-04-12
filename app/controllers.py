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

class RegisterController(View):

    def dispatch_request(self):
        myform = RegisterForm()

        if request.method == 'POST' and myform.validate_on_submit():
            first_name = myform.first_name.data
            last_name = myform.last_name.data
            user_name = myform.user_name.data
            email = myform.email.data
            user_type = myform.user_type.data
            password = myform.password.data

            new_user = UserProfile(first_name=first_name,
                                   last_name=last_name,
                                   user_name=user_name,
                                   email=email,
                                   user_type=user_type,
                                   password=password)

            db.session.add(new_user)
            db.session.commit()

            flash('You have successfully registered!', 'success')
            return redirect(url_for('home'))

        # If the form is not valid, handle the form errors
        if request.method == 'POST':
            flash_errors(myform)  # Assumes flash_errors is a function that handles form errors

        return render_template('register.html', form=myform)

# Setup the route
app.add_url_rule('/register', view_func=RegisterController.as_view('register'), methods=['GET','POST'])

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


class DashboardController(View):
    decorators = [login_required]

    def dispatch_request(self):
        if current_user.user_type == 'seller':
            products = Product.query.filter_by(seller_id=current_user.id).all()
            # Update image URLs
            for prod in products:
                prod.image_url = url_for('send_image', filename=prod.image_filename)

            return render_template('dashboard.html', products=products)
        else:
            flash('Access denied! You are not authorized to view this page.', 'danger')
            return redirect(url_for('home'))

# Setup the route
app.add_url_rule('/dashboard', view_func=DashboardController.as_view('dashboard'))


class EditProductController(View):
    decorators = [login_required]

    def dispatch_request(self, product_id):
        product = Product.query.get_or_404(product_id)
        if current_user.user_type != 'seller' or product.seller_id != current_user.id:
            flash('Access denied! You are not authorized to edit this product.', 'danger')
            return redirect(url_for('dashboard'))

        form = ProductForm(obj=product)
        if request.method == 'POST' and form.validate_on_submit():
            # Update product details from form data
            product.name = form.name.data
            product.price = form.price.data
            product.description = form.description.data
            product.quantity = form.quantity.data
            product.category = form.category.data
            product.weight = form.weight.data
            image = form.image.data
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            product.image_filename = image_filename

            # Commit changes to the database
            db.session.commit()

            # Flash message and redirect to dashboard
            flash('Product updated successfully!', 'success')
            return redirect(url_for('dashboard'))

        return render_template('edit_product.html', form=form, product=product)

# Setup the route
app.add_url_rule('/dashboard/edit_product/<int:product_id>', view_func=EditProductController.as_view('edit_product'), methods=['GET','POST'])

class LoginController(View):

    def dispatch_request(self):
        form = LoginForm()

        if request.method == 'POST' and form.validate_on_submit():
            user_name = form.user_name.data
            password = form.password.data

            # Attempt to retrieve user by username
            user = db.session.execute(db.select(UserProfile).filter_by(user_name=user_name)).scalar()

            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('Logged in successfully.', 'success')
                return redirect(url_for('home'))  # Redirect to home or another specific route
            else:
                flash('Invalid username or password.', 'danger')

        return render_template("login.html", form=form)

# Setup the route
app.add_url_rule('/login', view_func=LoginController.as_view('login'), methods=['GET','POST'])


class LogoutController(View):

    def dispatch_request(self):
        logout_user()
        flash('You have been logged out successfully.', 'success')
        return redirect(url_for('home'))

# Setup the route
app.add_url_rule('/logout', view_func=LogoutController.as_view('logout'))



class AddProductController(View):
    decorators = [login_required]

    def dispatch_request(self):
        form = ProductForm()

        if request.method == 'POST' and form.validate_on_submit():
            name = form.name.data
            price = form.price.data
            description = form.description.data
            quantity = form.quantity.data
            category = form.category.data
            weight = form.weight.data
            seller_id = current_user.id
            
            # Handle image upload
            image = form.image.data
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

            # Create and add the new product to the database
            product = Product(name=name, price=price, description=description, quantity=quantity,
                              category=category, weight=weight, image_filename=image_filename, seller_id=seller_id)
            db.session.add(product)
            db.session.commit()

            flash('Product added successfully!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to the dashboard or product detail page

        if request.method == 'POST':
            flash_errors(form)  # Assumes flash_errors is a function that handles form errors
        
        return render_template('add_product.html', form=form)

# Setup the route
app.add_url_rule('/add_product', view_func=AddProductController.as_view('add_product'), methods=['GET','POST'])


class CartController(View):
    decorators = [login_required]

    def dispatch_request(self):
        # Retrieve the cart items for the current user
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()

        # Calculate the total price
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Assign image URLs to each product in the cart
        for item in cart_items:
            item.product.image_url = url_for('send_image', filename=item.product.image_filename)

        # Render the cart view
        return render_template('view_cart.html', cart_items=cart_items, total_price=total_price)

# Setup the route
app.add_url_rule('/cart', view_func=CartController.as_view('cart'))
    
