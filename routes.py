from extensions import app, db
from flask import render_template, request, redirect, flash, send_from_directory
from forms import AddProduct, RegisterForm, LoginForm
import os
from models import Product, Category, User, Cart
from flask_login import logout_user, login_user, login_required, current_user



@app.route("/")
def index():
    user_add_category = Category.query.filter_by(name="User Add").first()
    if user_add_category:
        products = Product.query.filter(Product.category_id != user_add_category.id).all()
    else:
        products = Product.query.all()

    categories = Category.query.all()

    return render_template("index.html", products=products, categories=categories)


@app.route('/detail/<int:id>')
def detail(id):
    current = Product.query.get(id)

    return render_template("details.html", product=current)


@app.route("/uploadfile", methods=["GET", "POST"])
@login_required
def upload_file():
    if current_user.role == "admin":
        form = AddProduct()
        if form.validate_on_submit():
            file = request.files['file']
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                category = Category.query.filter_by(name="Products").first()
                obj = Product(name=form.name.data,
                            file=filename,
                            price = form.price.data,
                            category_id=category.id,
                            ingredients = form.ingredients.data)
                db.session.add(obj)
                db.session.commit()
                flash("You successfully added the product", category="success")
        
            return redirect("/category/2")
        if form.errors:
            print(form.errors)
            for error in form.errors:
                print(error)
            flash("You didn't add the product properly", category="danger")
        return render_template("addproduct.html", form=form)
        
    else:
        
        form = AddProduct()
        if form.validate_on_submit():
            file = request.files['file']
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user_add_category = Category.query.filter_by(name="user add").first()
                
                obj = Product(
                name=form.name.data,
                file=filename,
                price=form.price.data,
                category_id=user_add_category.id,
                ingredients = form.ingredients.data
                )
                db.session.add(obj)
                db.session.commit()
                flash("You successfully added the product", category="success")
            return redirect("/category/2")
        if form.errors:
            print(form.errors)
            for error in form.errors:
                print(error)
            flash("You didn't add the product properly", category="danger")
        return render_template("addproduct.html", form=form)
    

@app.route("/delete/<int:id>")
@login_required
def delete_product(id):

    if current_user.role == "admin":
        current = Product.query.get(id)
        db.session.delete(current)
        db.session.commit()
    else:
        return "You are not admin for this method", 404

    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_product(id):
    if current_user.role == "admin":
        current = Product.query.get(id)
        print(current)
        form = AddProduct(name=current.name,
                        price=current.price,
                        file = current.file,
                        ingredients = current.ingredients
                        )
        if form.validate_on_submit():
            file = request.files['file']
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            current.name = form.name.data
            print("name", current.name)
            current.file = filename
            current.price = form.price.data
            current.ingredients = form.ingredients.data

            db.session.commit()
            flash("You successfully adit the product", category="success")
            
            return redirect("/category/2")
        
        if form.errors:
            print(form.errors)
            for error in form.errors:
                print(error)

            flash("You didn't adit the product properly", category="danger")
        return render_template("addproduct.html", form=form)
    else:
        return "You are not admin", 404

    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/category/<int:category_id>")
def category_select(category_id):
    current_category = Category.query.get(category_id)
    if not current_category:
        flash("Category not found.", category="danger")
        return redirect("/category/2")

    products = Product.query.filter_by(category_id=category_id).all()
    return render_template("index.html", category=current_category, products=products)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You successgfully registered", category="success")
        login_user(user)
        return redirect("/category/2")


    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully.", category="success")
            return redirect("/category/2")
        else:
            flash("Invalid username or password.", category="danger")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/category/2")

@app.route("/add_to_cart/<int:product_id>")
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if product:
        cart_item = Cart(user_id=current_user.id, product_id=product.id)
        db.session.add(cart_item)
        db.session.commit()
        flash("Product added to cart", category="success")
    else:
        flash("Product not found", category="danger")
    return redirect("/cart")

@app.route("/remove_from_cart/<int:product_id>")
@login_required
def remove_from_cart(product_id):
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash("Product removed from cart", "success")
    else:
        flash("Product not found in cart", "danger")
    
    return redirect("/cart")

@app.route("/cart")
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    products = [item.product for item in cart_items]
    return render_template("cart.html", products=products)

@app.route("/detail/<int:id>")
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template("detail.html", product=product)