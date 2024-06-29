from extensions import app, db
from flask_login import UserMixin
from extensions import login_manager
from werkzeug.security import generate_password_hash, check_password_hash

class Product(db.Model):
    name = db.Column(db.String)
    file = db.Column(db.String)
    price = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key = True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    ingredients = db.Column(db.Text) 

    def __str__(self):

        return f"{self.name}"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    product_id = db.relationship('Product', backref='category', lazy=True)
    
    def __str__(self):

        return f"{self.name}"
    

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    user = db.relationship('User', back_populates='cart')
    product = db.relationship('Product')
    
class User(db.Model, UserMixin):
    username = db.Column(db.String)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)
    cart = db.relationship('Cart', back_populates='user')
       
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __init__(self, username, password, role="guest"):
        self.username = username
        self.set_password(password)
        self.role = role


    def __str__(self):
        return f"{self.username}"

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        if not Category.query.filter_by(name="user add").first():
            products_category = Category(name="user add")
            db.session.add(products_category)
            db.session.commit()

        products = Category(name="Products")
        

        admin = User(username="admin", password="password123", role="admin")
        user = User(username="test1", password="pass123")

        db.session.add_all([products, user, admin])
        db.session.commit()

        products = [
        Product(name='lemon ice cream', file='../static/images/lemon.jpg', price=4, category=products, ingredients="Lemons, Heavy cream, Milk, Sugar, Egg yolks"),
        Product(name='berry ice cream', file='../static/images/berry.jpg', price=4, category=products, ingredients="Mixed berries, Heavy cream, Milk, Sugar, Lemon juice, Egg yolks"),
        Product(name='strawberry ice cream', file='../static/images/strawberry.jpg', price=4, category=products, ingredients="Fresh Strawberries, Sugar, Heavy Cream, Whole Milk, Vanilla Extract, Lemon Juice"),
        Product(name='orange ice cream', file='../static/images/orange.jpg', price=4, category=products, ingredients="Oranges, Heavy cream, Milk, Sugar, Egg yolks"),
        Product(name='chocolate ice cream', file='../static/images/chocolate.jpg', price=3, category=products, ingredients="Cocoa powder, Heavy cream, Milk, Sugar, Egg yolks, Vanilla extract"),
        Product(name='vanilla ice cream', file='../static/images/vanilla.jpg', price=2, category=products, ingredients="Vanilla beans, Heavy cream, Milk, Sugar, Egg yolks")
        ]

        db.session.add_all(products)
        db.session.commit()