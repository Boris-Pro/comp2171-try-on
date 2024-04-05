import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.models import UserProfile
from app.models import Product, CartItem, Review
from app.forms import LoginForm
from app.forms import RegisterForm, ReviewForm
from werkzeug.security import check_password_hash
from app.helper import get_uploaded_images
from flask import send_from_directory
from app.forms import ProductForm
from sqlalchemy import or_


###
# Routing for your application.
###

# @app.route('/')
# def home():
#     """Render website's home page."""
#     products = Product.query.all()  # Fetch all products from the database
#     for prod in products:
#         prod.image_url = url_for('send_image', filename=prod.image_filename)
#     return render_template('home.html', products=products)


# @app.route('/about/')
# def about():
#     """Render the website's about page."""
#     return render_template('about.html', name="Mary Jane")


@app.route('/register', methods=['GET', 'POST'])
def register():
    myform = RegisterForm()
    if request.method == 'POST':
    
        if myform.validate_on_submit():
            first_name = myform.first_name.data
            last_name = myform.last_name.data
            user_name = myform.user_name.data
            email = myform.email.data
            user_type = myform.user_type.data
            password = myform.password.data
    
            flash('You have successfully filled out the form', 'success')
            new_user = UserProfile(first_name=first_name,
                                    last_name=last_name,
                                    user_name=user_name,
                                    email=email,
                                    user_type=user_type,
                                    password=password)
            
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('home'))
        flash_errors(myform)
    return render_template('register.html', form=myform)

# @app.route('/dashboard')
# @login_required
# def dashboard():
#     if current_user.user_type == 'seller':
#         products = Product.query.filter_by(seller_id=current_user.id).all()
#         # products = Product.query.all()  # Fetch all products from the database
#         for prod in products:
#             prod.image_url = url_for('send_image', filename=prod.image_filename)
#             return render_template('dashboard.html', products=products)
#     else:
#         flash('Access denied! You are not authorized to view this page.', 'danger')
#         return redirect(url_for('home'))
    

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type == 'seller':
        products = Product.query.filter_by(seller_id=current_user.id).all()
        # products = Product.query.all()  # Fetch all products from the database

        for prod in products:
            prod.image_url = url_for('send_image', filename=prod.image_filename)

        return render_template('dashboard.html', products=products)
    else:
        flash('Access denied! You are not authorized to view this page.', 'danger')
        return redirect(url_for('home'))

# @app.route('/product/add', methods=['GET', 'POST'])
# @login_required
# def add_product():
#     if current_user.user_type == 'seller':
#         form = ProductForm()
#         if form.validate_on_submit():
#             product = Product(
#                 name=form.name.data,
#                 price=form.price.data,
#                 description=form.description.data,
#                 quantity=form.quantity.data,
#                 category=form.category.data,
#                 weight=form.weight.data,
#                 image_filename=form.image_filename.data,
#                 seller=current_user
#             )
#             db.session.add(product)
#             db.session.commit()
#             flash('Product added successfully!', 'success')
#             return redirect(url_for('dashboard'))
#         return render_template('add_product.html', form=form)
#     else:
#         flash('Access denied! You are not authorized to add products.', 'danger')
#         return redirect(url_for('dashboard'))

# app.route('/dashboard/edit_product/<int:product_id>', methods=['GET', 'POST'])
# @login_required
# def edit_product(product_id):
#     product = Product.query.get_or_404(product_id)
#     if current_user.user_type == 'seller' and product.seller_id == current_user.id:
#         form = ProductForm(obj=product)
#         if form.validate_on_submit():
#             product.name = form.name.data
#             product.price = form.price.data
#             product.description = form.description.data
#             product.quantity = form.quantity.data
#             product.category = form.category.data
#             product.weight = form.weight.data
#             product.image_filename = form.image_filename.data
#             db.session.commit()
#             flash('Product updated successfully!', 'success')
#             return redirect(url_for('dashboard'))
#         return render_template('edit_product.html', form=form, product=product)
#     else:
#         flash('Access denied! You are not authorized to edit this product.', 'danger')
#         return redirect(url_for('dashboard'))
    
@app.route('/dashboard/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if current_user.user_type == 'seller' and product.seller_id == current_user.id:
        form = ProductForm(obj=product)
        if form.validate_on_submit():
            # Update product details from form data
            product.name = form.name.data
            product.price = form.price.data
            product.description = form.description.data
            product.quantity = form.quantity.data
            product.category = form.category.data
            product.weight = form.weight.data
            image = form.image.data
            image_filename = secure_filename(form.image.data.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            product.image_filename = image_filename
            
            # Commit changes to the database
            db.session.commit()
            
            # Flash message and redirect to dashboard
            flash('Product updated successfully!', 'success')
            return redirect(url_for('dashboard'))  # Corrected redirect
        return render_template('edit_product.html', form=form, product=product)
    else:
        flash('Access denied! You are not authorized to edit this product.', 'danger')
        return redirect(url_for('dashboard'))


@app.route('/dashboard/delete/<int:product_id>', methods=['POST', 'GET'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if current_user.user_type == 'seller' and product.seller_id == current_user.id:
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
    else:
        flash('Access denied! You are not authorized to delete this product.', 'danger')
    return redirect(url_for('dashboard'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user_name = form.user_name.data
        password = form.password.data

        #user = UserProfile.query.filter_by(username=username).first()
        user = db.session.execute(db.select(UserProfile).filter_by(user_name=user_name)).scalar()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home'))  # Redirect to the upload route or any other route
        else:
            flash('Invalid username or password.', 'danger')

    return render_template("login.html", form=form)    

@staticmethod
def create_product(name, price, description, quantity, category, weight, image, seller):
    product = Product(name=name, price=price, description=description, quantity=quantity,category=category, weight=weight, image=image, seller=seller)
    db.session.add(product)
    db.session.commit()

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            price = form.price.data
            description = form.description.data
            quantity = form.quantity.data
            category = form.category.data
            weight = form.weight.data
            seller_id=current_user.id
            # Handle image upload if needed
            image = form.image.data
            image_filename = secure_filename(form.image.data.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            flash('Product added successfully!', 'success')

            # Create the product
            product = Product(name=name, price=price, description=description, quantity=quantity,
                            category=category, weight=weight,image_filename=image_filename, seller_id=seller_id)
            db.session.add(product)
            db.session.commit()
            # Redirect to the product detail page or any other page
            return redirect(url_for('dashboard'))
            #return redirect(url_for('product_detail', product_id=product.id))
        flash_errors(form)
    return render_template('add_product.html', form=form)


@app.route('/uploads/<filename>')
def send_image(filename):
    # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    uploads_dir = os.path.join(os.getcwd(), 'uploads')
    return send_from_directory(uploads_dir, filename)


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user_id' in session:
        user_id = session['user_id']
        cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = CartItem(user_id=user_id, product_id=product_id)
            db.session.add(cart_item)
        db.session.commit()
    return redirect(url_for('view_cart'))


@app.route('/product/<int:product_id>/add_review', methods=['GET', 'POST'])
@login_required
def add_review(product_id):
    form = ReviewForm()
    product = Product.query.get_or_404(product_id)

    if form.validate_on_submit():
        rating = form.rating.data
        comment = form.comment.data

        review = Review(rating=rating, comment=comment, user_id=current_user.id, product_id=product_id)
        db.session.add(review)
        db.session.commit()

        flash('Your review has been added successfully.', 'success')
        return redirect(url_for('product_details', product_id=product_id))

    return render_template('add_review.html', form=form, product=product)

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(UserProfile).filter_by(id=id)).scalar()

###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        # Perform search logic by filtering products whose names contain the query
        products = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
        for prod in products:
            prod.image_url = url_for('send_image', filename=prod.image_filename)
    else:
        # If no query is provided, return all products
        products = Product.query.all()
        for prod in products:
            prod.image_url = url_for('send_image', filename=prod.image_filename)
    return render_template('home.html', products=products)
