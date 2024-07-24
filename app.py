from flask import Flask, render_template, request, redirect, url_for, flash
import matplotlib
matplotlib.use('Agg')  # Using the Agg backend for non-GUI environments
import matplotlib.pyplot as plt
from sqlalchemy import func
from models import User, db, Manager, Product, Category, Order, OrderItem, CartItem
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '123qwe123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_db.db'
login_manager = LoginManager(app)
db.init_app(app)
login_manager.init_app(app)

#--------------------------------------------------------- Home ---------------------------------------------------#
@app.route('/')
def home():
    return render_template("home.html")

#--------------------------------------------------------- About ---------------------------------------------------#
@app.route('/about')
def about():
    return render_template("about.html")

#--------------------------------------------------------- Contact -------------------------------------------------#
@app.route('/contact')
def contact():
    return render_template("contact.html")


#--------------------------------------------------- Register New User ---------------------------------------------#

@app.route('/user_register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        # Store all data into user table
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User(username=username,email=email, password=password )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_login'))
    return render_template('user_register.html')

#------------------------------------------------------- Login New User --------------------------------------------#
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Query the User model to find the user by username
        user = User.query.filter_by(username=username).first()

        # Check the valid password
        if user and user.password == password:
            flash("Invalid username or password", "error")
            login_user(user)
            return redirect(url_for('user_dashboard'))    
        else:
            flash("Invalid username or password", "error")

    return render_template('user_login.html')


#--------------------------------------------------- Log Out ------------------------------------------------------#

@app.route('/user_logout')
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('home'))


#------------------------------------------------------------- Manager Log In ---------------------------------------#


@app.route('/manager_login', methods=['GET', 'POST'])
def manager_login():
    if request.method == 'POST':
        m_name = request.form.get('m_name')
        m_password = request.form.get('m_password')

        # Query the Manager model to find the manager by username
        manager = Manager.query.first()
        # Check the valid password
        if manager and manager.m_password == m_password:
            return redirect(url_for('manager_dashboard'))
        else:
            flash("Invalid manager username or password", "error")

    return render_template('manager_login.html')


#--------------------------------------------------- Manager Log Out ----------------------------------------------#
@app.route('/manager_logout')
@login_required
def manager_logout():
    logout_user()
    return redirect(url_for('home'))



#------------------------------------------------- User Dashboard --------------------------------------------------#

@app.route('/user_dashboard', methods=['GET', 'POST'])
def user_dashboard():


    search_term = request.args.get('category_search')
    category_filter = request.args.get('category')
    
    # Fetch all categories from the Category table
    categories = Category.query.all()
    
    # Initialize products_by_category as an empty dictionary for filtering the products.
    products_by_category = {}

    if search_term:
        # If clicked on search, it will filter products by category.
        products = Product.query.filter(
            Product.category.ilike(f"%{search_term}%")
        ).all()
    elif category_filter:
        # If a category is selected from the dropdown, then filter products of that category.
        products = Product.query.filter_by(category=category_filter).all()
    else:
        # If no category is selected, show all products.
        products = Product.query.all()

    # Get the current user's name (if logged in)
    current_user_name = current_user.username if current_user.is_authenticated else None

    for product in products:
        if product.category not in products_by_category:
            products_by_category[product.category] = []
        products_by_category[product.category].append(product)

    return render_template('user_dashboard.html', products_by_category=products_by_category, search_term=search_term, categories=categories, current_user_name=current_user_name)

#--------------------------------------------------- Add to Cart --------------------------------------------------#

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if product:
        quantity = int(request.form.get('quantity', 1))
        existing_cart_item = CartItem.query.filter_by(product_id=product_id).first()

        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.total_price = existing_cart_item.quantity * product.price_per_unit
        else:
            cart_item = CartItem(product_id=product_id, quantity=quantity)
            cart_item.total_price = cart_item.quantity * product.price_per_unit
            db.session.add(cart_item)

            # Reduce the product quantity in stock
            product.quantity -= quantity

            # Mark the product as out of stock if quantity becomes zero
            if product.quantity == 0:
                product.out_of_stock = True
            elif product.quantity < 0:
                product.out_of_stock = True
        db.session.commit()

    return redirect(url_for('user_dashboard'))


#--------------------------------------------------- Cart --------------------------------------------------------#

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    cart_items = CartItem.query.all()
    overall_total = sum(cart_item.total_price for cart_item in cart_items)
    return render_template('cart.html', cart_items=cart_items, overall_total=overall_total)


#--------------------------------------------------- Delete from Cart ----------------------------------------------#

@app.route('/delete_from_cart/<int:cart_item_id>', methods=['GET'])
def delete_from_cart(cart_item_id):

    cart_item = CartItem.query.get(cart_item_id)
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
    
    # Redirect back to the cart page after deletion
    return redirect(url_for('cart'))

#---------------------------------------------------- Checkout Items ----------------------------------------------------------#

@app.route('/checkout')
@login_required
def checkout():
    cart_items = CartItem.query.all()
    overall_total = sum(cart_item.total_price for cart_item in cart_items)

    # Here we are creating an order and associate it with the current user.
    order = Order(user_id=current_user.id, overall_total=overall_total)
    db.session.add(order)
    db.session.commit()

    # Add indivisual oreder items in order table.
    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            total_price=cart_item.total_price
        )
        
        db.session.add(order_item)


    # Clear the cart after saving all items into order_item table
    db.session.query(CartItem).delete()

    db.session.commit()


    return redirect(url_for('order_confirmation'))

#--------------------------------------------------- Order Confirmation --------------------------------------------#

@app.route('/order_confirmation')
def order_confirmation():
    return render_template('order_confirmation.html')


#---------------------------------------------- Display Only User's Order --------------------------------------------------------------#

@app.route('/orders')
@login_required
def orders():
    # Fetch only current user's orders.
    user_orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template('orders.html', orders=user_orders)

#-------------------------------------------------- Selected Order Detail --------------------------------------------#

@app.route('/order/<int:order_id>')
@login_required
def order_details(order_id):
    order = Order.query.get(order_id)
    if order:
        # Show all order items related to selected order_id.
        order_items = OrderItem.query.filter_by(order_id=order.id).all()
        return render_template('order_details.html', order=order, order_items=order_items)
    else:
        return "Order not found"
    

#---------------------------------------------------- Manager Dashboard -------------------------------------------#

@app.route('/manager_dashboard')
def manager_dashboard():
    managers = Manager.query.all()
    categories = Category.query.all()
    
    return render_template('manager_dashboard.html',managers=managers, categories=categories)


#------------------------------------------------- Add New Category --------------------------------------------------#

@app.route('/new_category', methods=['GET', 'POST'])
def new_category():
    if request.method == 'POST':
        category_name = request.form['category_name']
        print(f'name = {category_name}')
        category = Category(category_name=category_name)
        db.session.add(category)
        db.session.commit()

        return redirect(url_for('manager_dashboard'))

    return render_template('new_category.html')
    

#---------------------------------------------- add new product ---------------------------------------------------#

@app.route('/new_product', methods=['GET', 'POST'])
def new_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        category = request.form['category']
        unit = request.form['unit']
        quantity = request.form['quantity']
        price_per_unit = request.form['price_per_unit']

        new_product = Product(product_name=product_name, category=category, unit=unit, quantity=quantity, price_per_unit=price_per_unit)
        db.session.add(new_product)
        db.session.commit()
        

        return redirect(url_for('product_list'))

    return render_template('new_product.html')


#-------------------------------------------------------- Product List ---------------------------------------------#

@app.route('/product_list', methods=['GET'])
def product_list():
    products = Product.query.all()
    return render_template('product_list.html',products=products)

#--------------------------------------------------- User Data -----------------------------------------------------#

@app.route('/user_data', methods=['GET'])
def user_data():
    users = User.query.all()
    return render_template('user_data.html',users=users)


#-------------------------------------------------------- Delete Product ----------------------------------------------#
@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('product_list'))



#-------------------------------------------------------- Edit Product -----------------------------------------------------#

class ProductForm:
    def __init__(self, product_name='', category='', unit='', price_per_unit=''):
        self.product_name = product_name
        self.category = category
        self.unit = unit
        self.price_per_unit = price_per_unit


@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)
    form = ProductForm(
        product_name=product.product_name,
        category=product.category,

        unit=product.unit,
        price_per_unit=product.price_per_unit
    )

    if request.method == 'POST':
        product.product_name = request.form['product_name']
        product.category = request.form['category']
        product.unit = request.form['unit']
        quantity_to_add = int(request.form.get('quantity'))
        product.price_per_unit = float(request.form['price_per_unit'])
        # Add the specified quantity to the previous quantity
        product.quantity += quantity_to_add
        
        if product.quantity > 0:
            # If the updated quantity is greater than 0, unmark the product as out of stock
            product.out_of_stock = False
        else:
            product.out_of_stock = True

        
        db.session.commit()
        return redirect(url_for('product_list'))

    return render_template('edit_product.html', form=form)


#-------------------------------------------------------- Edit Category --------------------------------------------#
class CategoryForm:
    def __init__(self, category_name=''):

        self.category = category_name



@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    category = Category.query.get(category_id)
    form = CategoryForm(
        category_name=category.category_name
    )

    if request.method == 'POST':
        category.category_name = request.form['category']
        db.session.commit()
        return redirect(url_for('manager_dashboard'))

    return render_template('edit_category.html', form=form, category_id=category_id)


#-------------------------------------------------------- Delete Category ----------------------------------------------#
@app.route('/<int:category_id>/delete', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get(category_id)

    if category:
        # Delete the category from the database
        db.session.delete(category)
        db.session.commit()

    return redirect(url_for('manager_dashboard'))

#-------------------------------------------------------- Summary --------------------------------------------------#

@app.route('/summary')
def summary():
    # Find the product which have heighest sale
    total_sales = db.session.query(db.func.sum(Order.overall_total)).scalar()
    total_products = db.session.query(db.func.sum(OrderItem.quantity)).scalar()
    total_users = db.session.query(db.func.max(User.id)).scalar()


    # Query the database to get item names and purchase quantities for the current user
    query = (
        db.session.query(Product.product_name, func.sum(OrderItem.quantity).label('total_quantity'))
        .join(OrderItem, OrderItem.product_id == Product.product_id)
        .join(Order, OrderItem.order_id == Order.id)
        .group_by(Product.product_name)
        .all()
    )


    # Unpack it and create two lists for item names and quantities
    item_names, quantities = zip(*query)

    most_purchased_index = quantities.index(max(quantities))
    most_purchased_item_name = item_names[most_purchased_index]

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(item_names, quantities, color='skyblue')
    plt.xlabel('Quantity Purchased')
    plt.ylabel('Item Name')
    plt.title('Item Purchase by Quantity')

    # Save the chart as an image file into static folder
    chart_image_path = 'static/item_purchase_chart.png'
    plt.savefig(chart_image_path, bbox_inches='tight')
    plt.close()   # Close the figure to free up memory


    user_data = {
        'most_purchased_item_name': most_purchased_item_name,

    }

    return render_template('summary.html', total_sales=total_sales, user_data=user_data, chart_image_path=chart_image_path, total_user=total_users, most_purchased_item_name=most_purchased_item_name, total_products=total_products)

#--------------------------------------------------- User Summary --------------------------------------------------------#


@app.route('/user_summary')
@login_required
def user_summary():

    if current_user.is_authenticated:
        user_id = current_user.id  # Get the current user's ID
        
        # Calculate total number of orders by the current user
        total_orders = Order.query.filter_by(user_id=user_id).count()
        
        # Calculate the total purchase amount by the current user
        total_purchase_amount = db.session.query(func.sum(Order.overall_total)).filter_by(user_id=user_id).scalar()
            
    # Query the database to get product names and purchase quantities for the current user
    query = (
        db.session.query(Product.product_name, func.sum(OrderItem.quantity).label('total_quantity'))
        .join(OrderItem, OrderItem.product_id == Product.product_id)
        .join(Order, OrderItem.order_id == Order.id)
        .filter(Order.user_id == current_user.id)
        .group_by(Product.product_name)
        .all()
    )

    #  Unpack it and create two lists for product names and quantities
    product_names, quantities = zip(*query)

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(product_names, quantities, color='skyblue')
    plt.xlabel('Quantity Purchased')
    plt.ylabel('Product Name')
    plt.title('Product Purchase by Quantity')

    # Save the chart as an image file into static folder
    chart_image_path = 'static/bar_chart.png'
    plt.savefig(chart_image_path, bbox_inches='tight')
    plt.close()  # Close the figure to free up memory

    # Find the product with the maximum sales (favorite product)
    favorite_product_index = quantities.index(max(quantities))
    favorite_product_name = product_names[favorite_product_index]

    # All information we want to display on user_summary page
    user_data = {
        'username': current_user.username,
        'email': current_user.email,
        'total_orders': total_orders,
        'total_purchase_amount': total_purchase_amount,
        'favorite_product_name': favorite_product_name,
    }

    return render_template('user_summary.html', user_data=user_data, chart_image_path=chart_image_path, favorite_product_name=favorite_product_name)





#----------------------------------------------- End -----------------------------------------------#

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)