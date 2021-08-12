from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)


# MAIL_SERVER: 'smtp.gmail.com'
# MAIL_PORT: 465
# MAIL_USERNAME: 'mts.emailnotifications@gmail.com'
# MAIL_PASSWORD: 'Testinggg3'
# MAIL_USE_TLS: False
# MAIL_USE_SSL: True
# MAIL_DEFAULT_SENDER: 'mts.emailnotifications@gmail.com'

# mail = Mail()
# mail.init_app(app)


# @app.route('/')
# def index():
#     msg = Message('Hello from the coso', recipients=['ankar_aguirre@live.com'])
#     mail.send(msg)

#     return '<h1>Sent!</h1>'


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_first_name = db.Column(db.String(100), nullable=False)
    user_last_name = db.Column(db.String(100), nullable=False)
    user_password = db.Column(db.String(40), nullable=False)
    user_email = db.Column(db.String(100), nullable=False, unique=True)
    user_confirmation = db.Column(db.String(6), unique=True)
    user_address = db.relationship('Address', backref='user')
    user_payment = db.relationship('Payment', backref='user')
    user_is_active = db.Column(db.Boolean, default='False')

    def __init__(self, user_first_name, user_last_name, user_email, user_password, user_confirmation, user_is_active):
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name
        self.user_password = user_password
        self.user_email = user_email
        self.user_confirmation = user_confirmation
        self.user_is_active = user_is_active


class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'user_first_name', 'user_last_name',
                  'user_password', 'user_email', 'user_confirmation', 'user_is_active')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Address(db.Model):
    __tablename__ = 'address'
    address_id = db.Column(db.Integer, primary_key=True)
    address_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    address_street = db.Column(db.String(20), nullable=False)
    address_number = db.Column(db.String(10))
    address_city = db.Column(db.String(20))
    address_state = db.Column(db.String(10))
    address_zip = db.Column(db.Integer)
    address_receiver = db.Column(db.String(30))

    def __init__(self, address_user_id, address_street, address_number, address_city, address_state, address_zip, address_receiver):

        self.address_user_id = address_user_id
        self.address_street = address_street
        self.address_number = address_number
        self.address_city = address_city
        self.address_state = address_state
        self.address_zip = address_zip
        self.address_receiver = address_receiver


class AddressSchema(ma.Schema):
    class Meta:
        fields = ('address_id', 'address_user_id', 'address_street', 'address_number',
                  'address_city', 'address_state', 'address_zip', 'address_receiver')


address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)


class Payment(db.Model):
    __tablename__ = 'payment'
    payment_id = db.Column(db.Integer, primary_key=True)
    payment_card = db.Column(db.Integer)
    payment_cardholder_name = db.Column(db.String)
    payment_exp_month = db.Column(db.Integer)
    payment_exp_year = db.Column(db.Integer)
    payment_cv = db.Column(db.Integer)
    payment_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __init__(self, payment_card, payment_cardholder_name, payment_exp_month, payment_exp_year, payment_cv, payment_user_id):
        self.payment_card = payment_card
        self.payment_cardholder_name = payment_cardholder_name
        self.payment_exp_month = payment_exp_month
        self.payment_exp_year = payment_exp_year
        self.payment_cv = payment_cv
        self.payment_user_id = payment_user_id


class PaymentSchema(ma.Schema):
    class Meta:
        fields = ('payment_id', 'payment_card', 'payment_cardholder_name', 'payment_exp_month',
                  'payment_exp_year', 'payment_cv', 'payment_user_id')


payment_schema = PaymentSchema()
payments_schema = PaymentSchema(many=True)


class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String)
    product_brand = db.Column(db.String)
    product_category_name = db.Column(db.String)
    product_subcategory_name = db.Column(db.String)
    product_description = db.Column(db.String)
    product_variation = db.relationship('Variation', backref='product')

    def __init__(self, product_name, product_brand, product_category_name, product_subcategory_name, product_description):
        self.product_name = product_name
        self.product_brand = product_brand
        self.product_category_name = product_category_name
        self.product_subcategory_name = product_subcategory_name
        self.product_description = product_description


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('product_id', 'product_name', 'product_brand',
                  'product_category_name', 'product_subcategory_name', 'product_description')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


class Variation(db.Model):
    __tablename__ = 'variation'
    variation_id = db.Column(db.Integer, primary_key=True)
    variation_product_id = db.Column(
        db.Integer, db.ForeignKey('product.product_id'))
    variation_name = db.Column(db.String)
    variation_price = db.Column(db.Float)
    variation_stock = db.Column(db.Integer)
    variation_size = db.Column(db.String)
    variation_color = db.Column(db.String)

    def __init__(self, variation_product_id, variation_name, variation_price, variation_stock, variation_size, variation_color):
        self.variation_product_id = variation_product_id
        self.variation_name = variation_name
        self.variation_price = variation_price
        self.variation_stock = variation_stock
        self.variation_size = variation_size
        self.variation_color = variation_color


class VariationSchema(ma.Schema):
    class Meta:
        fields = ('variation_id', 'variation_product_id', 'variation_name',
                  'variation_price', 'variation_stock', 'variation_size', 'variation_color')


variation_schema = VariationSchema()
variations_schema = VariationSchema(many=True)


# APP ROUTES FOR POSTING


@app.route('/user', methods=["POST"])
def add_user():
    user_first_name = request.json['user_first_name']
    user_last_name = request.json['user_last_name']
    user_password = request.json['user_password']
    user_email = request.json['user_email']
    user_confirmation = request.json['user_confirmation']
    user_is_active = request.json['user_is_active']

    new_user = User(user_first_name, user_last_name, user_email,
                    user_password, user_confirmation, user_is_active)

    db.session.add(new_user)
    db.session.commit()

    user = User.query.get(new_user.user_id)

    return user_schema.jsonify(user)


@app.route('/user/address', methods=["POST"])
def add_address():

    address_user_id = request.json['address_user_id']
    address_street = request.json['address_street']
    address_number = request.json['address_number']
    address_city = request.json['address_city']
    address_state = request.json['address_state']
    address_zip = request.json['address_zip']
    address_receiver = request.json['address_receiver']

    new_address = Address(address_user_id, address_street, address_number,
                          address_city, address_state, address_zip, address_receiver)

    db.session.add(new_address)
    db.session.commit()

    address = Address.query.get(new_address.address_id)

    return address_schema.jsonify(address)


@app.route('/user/payment', methods=["POST"])
def add_payment():

    payment_card = request.json['payment_card']
    payment_cardholder_name = request.json['payment_cardholder_name']
    payment_exp_month = request.json['payment_exp_month']
    payment_exp_year = request.json['payment_exp_year']
    payment_cv = request.json['payment_cv']
    payment_user_id = request.json['payment_user_id']

    new_payment = Payment(payment_card, payment_cardholder_name,
                          payment_exp_month, payment_exp_year, payment_cv, payment_user_id)

    db.session.add(new_payment)
    db.session.commit()

    payment = Payment.query.get(new_payment.payment_id)

    return payment_schema.jsonify(payment)


@app.route('/product', methods=['POST'])
def add_product():

    product_name = request.json['product_name']
    product_brand = request.json['product_brand']
    product_category_name = request.json['product_category_name']
    product_subcategory_name = request.json['product_subcategory_name']
    product_description = request.json['product_description']

    new_product = Product(product_name, product_brand,
                          product_category_name, product_subcategory_name, product_description)

    db.session.add(new_product)
    db.session.commit()

    product = Product.query.get(new_product.product_id)

    return product_schema.jsonify(product)


@app.route('/product/variation', methods=['POST'])
def new_variation():
    variation_product_id = request.json['variation_product_id']
    variation_name = request.json['variation_name']
    variation_price = request.json['variation_price']
    variation_stock = request.json['variation_stock']
    variation_size = request.json['variation_size']
    variation_color = request.json['variation_color']

    new_variation = Variation(variation_product_id,
                              variation_name, variation_price, variation_stock, variation_size, variation_color)

    db.session.add(new_variation)
    db.session.commit()

    variation = Variation.query.get(new_variation.variation_id)

    return variation_schema.jsonify(variation)


# APP ROUTES FOR GETTING


@app.route('/users', methods=["GET"])
def get_users():
    all_users = User.query.all()

    result = users_schema.dump(all_users)
    return jsonify(result)


@app.route('/user/<id>', methods=["GET"])
def get_user(id):
    user = User.query.get(id)

    return user_schema.jsonify(user)


@app.route('/user/addresses', methods=["GET"])
def get_users_addresses():
    all_users_addresses = Address.query.all()

    result = addresses_schema.dump(all_users_addresses)
    return jsonify(result)


@app.route('/user/address/<id>', methods=["GET"])
def get_user_address(id):
    user_address = Address.query.get(id)

    return address_schema.jsonify(user_address)


@app.route('/user/payments', methods=["GET"])
def get_users_payments():
    all_users_payments = Payment.query.all()

    result = payments_schema.dump(all_users_payments)
    return jsonify(result)


@app.route('/user/payment/<id>', methods=["GET"])
def get_user_payment(id):
    user_payment = Payment.query.get(id)

    return payment_schema.jsonify(user_payment)


@app.route('/product/<id>', methods=["GET"])
def get_product(id):
    product = Product.query.get(id)

    return product_schema.jsonify(product)


@app.route('/products', methods=["GET"])
def get_products():
    products = Product.query.all()

    result = products_schema.dump(products)
    return jsonify(result)


@app.route('/product/variation/<id>', methods=["GET"])
def get_variation(id):
    variation = Variation.query.get(id)

    return variation_schema.jsonify(variation)


@app.route('/product/variations', methods=["GET"])
def get_variations():
    variation = Variation.query.all()

    result = variations_schema.dump(variation)
    return jsonify(result)

# APP ROUTES FOR PUTTING


@app.route('/user/<id>', methods=["PUT"])
def user_update(id):
    user = User.query.get(id)

    first_name = request.json['user_first_name']
    last_name = request.json['user_last_name']
    password = request.json['user_password']
    email = request.json['user_email']
    confirmation = request.json['user_confirmation']
    is_active = request.json['user_is_active']

    user.user_first_name = first_name
    user.user_last_name = last_name
    user.user_email = email
    user.user_password = password
    user.confirmation = confirmation
    user.is_active = is_active

    db.session.commit()
    return user_schema.jsonify(user)


@app.route('/user/address/<id>', methods=["PUT"])
def address_update(id):
    address = Address.query.get(id)

    address_street = request.json['address_street']
    address_number = request.json['address_number']
    address_city = request.json['address_city']
    address_state = request.json['address_state']
    address_zip = request.json['address_zip']
    address_receiver = request.json['address_receiver']

    address.address_street = address_street
    address.address_number = address_number
    address.address_city = address_city
    address.address_state = address_state
    address.address_zip = address_zip
    address.address_receiver = address_receiver

    db.session.commit()
    return address_schema.jsonify(address)


@app.route('/user/payment/<id>', methods=["PUT"])
def payment_update(id):
    payment = Payment.query.get(id)

    card = request.json['payment_card']
    cardholder_name = request.json['payment_cardholder_name']
    exp_month = request.json['payment_exp_month']
    exp_year = request.json['payment_exp_year']
    cv = request.json['payment_cv']

    payment.payment_card = card
    payment.payment_cardholder_name = cardholder_name
    payment.payment_exp_month = exp_month
    payment.payment_exp_year = exp_year
    payment.payment_cv = cv

    db.session.commit()
    return payment_schema.jsonify(payment)


@app.route('/product/<id>', methods=["PUT"])
def product_update(id):
    product = Product.query.get(id)

    name = request.json['product_name']
    brand = request.json['product_brand']
    category_name = request.json['product_category_name']
    subcategory_name = request.json['product_subcategory_name']
    description = request.json['product_description']

    product.product_name = name
    product.product_brand = brand
    product.product_category_name = category_name
    product.product_subcategory_name = subcategory_name
    product.product_description = description

    db.session.commit()
    return product_schema.jsonify(product)


@app.route('/product/variation/<id>', methods=["PUT"])
def variation_update(id):
    variation = Variation.query.get(id)

    name = request.json['variation_name']
    price = request.json['variation_price']
    stock = request.json['variation_stock']
    size = request.json['variation_size']
    color = request.json['variation_color']

    variation.variation_name = name
    variation.variation_price = price
    variation.variation_stock = stock
    variation.variation_size = size
    variation.variation_color = color

    db.session.commit()
    return variation_schema.jsonify(variation)


# APP ROUTES FOR DELETING

@app.route('/user/<id>', methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user.user_id)


@app.route('/user/address/<id>', methods=["DELETE"])
def address_delete(id):
    address = Address.query.get(id)
    db.session.delete(address)
    db.session.commit()

    return address_schema.jsonify(address.address_id)


@app.route('/user/payment/<id>', methods=["DELETE"])
def payment_delete(id):
    payment = Payment.query.get(id)
    db.session.delete(payment)
    db.session.commit()

    return payment_schema.jsonify(payment.payment_id)


@app.route('/product/<id>', methods=["DELETE"])
def product_delete(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product.product_id)


@app.route('/product/variation/<id>', methods=["DELETE"])
def variation_delete(id):
    variation = Variation.query.get(id)
    db.session.delete(variation)
    db.session.commit()

    return 'Variation successfully deleted'


if __name__ == '__main__':
    app.run(debug=True)
