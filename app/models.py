from . import db
from werkzeug.security import generate_password_hash


class UserProfile(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    user_name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(200), unique=True)
    user_type = db.Column(db.String(80))
    password = db.Column(db.String(128))

    # User Can Have Many reviews 
    review = db.relationship('Review', backref='user')
    # products = db.relationship('Product', backref='seller', foreign_keys='Product.seller_id')
    # products = db.relationship('Product', backref='user')
    # products = db.relationship('Product', backref='seller')
    products = db.relationship('Product', backref='seller')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
    
    
    def __init__(self, first_name, last_name, user_name, email, user_type, password):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.email = email
        self.user_type = user_type
        self.password = generate_password_hash(password, method='pbkdf2:sha256')


        
# class Product(db.Model):
#     __tablename__ = 'products'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     description = db.Column(db.Text)
#     quantity = db.Column(db.Integer, nullable=False, default=0)
#     category = db.Column(db.String(100))
#     weight = db.Column(db.Float)
#     image_filename = db.Column(db.String(255))
#     reviews = db.relationship('Review', backref='product')

#     # Foreign Key To Link Users (refer to primary key of the user)
#     # seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     # Define a relationship with the UserProfile model to access the seller's username
#     # seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     # # seller = db.relationship('UserProfile', backref='products_selling', foreign_keys='Product.seller_id')
#     # seller = db.relationship('UserProfile', backref='products_selling')
#     seller = db.relationship('UserProfile', backref='seller_products')


#     def get_id(self):
#         return str(self.id)

#     def __repr__(self):
#         return f'<Product {self.name}>'
    
#     def __init__(self, name, price, description, quantity, category, weight,image_filename, seller_id):
#         self.name = name
#         self.price = price
#         self.description = description
#         self.quantity = quantity
#         self.category = category
#         self.weight = weight
#         self.image_filename = image_filename
#         self.seller_id = seller_id
#         # self.seller_name = seller_name
        

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    category = db.Column(db.String(100))
    weight = db.Column(db.Float)
    image_filename = db.Column(db.String(255))
    reviews = db.relationship('Review', backref='product')

    # Foreign Key To Link Users (refer to primary key of the user)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<Product {self.name}>'
    
    def __init__(self, name, price, description, quantity, category, weight, image_filename, seller_id):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity
        self.category = category
        self.weight = weight
        self.image_filename = image_filename
        self.seller_id = seller_id



    
class CartItem(db.Model):

    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    user = db.relationship('UserProfile', backref=db.backref('cart_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<Cart {self.user.user_name}>'

    def __init__(self, user_id, product_id, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

        
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))


    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f'<Review {self.user}>'

    def __init__(self, user_id, product_id, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
 