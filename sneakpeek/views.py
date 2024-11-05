

from flask import Blueprint, render_template, url_for, request, session, flash, redirect, abort
from .models import Product, Order, OrderDetail
from datetime import datetime
from .forms import CheckoutForm
from . import db

main_bp = Blueprint('main', __name__)

# Home page that displays products
@main_bp.route('/')
def index():
    featured_products = db.session.query(Product).order_by(Product.id).limit(8)  
    return render_template('index.html', products=featured_products)

# Product detail page
@main_bp.route('/item/<int:product_id>')
def item_detail(product_id):
    product = db.session.scalar(db.select(Product).where(Product.id == product_id))
    if product is None:
        abort(404, description="Product not found")
    return render_template('item_detail.html', product=product)



@main_bp.route('/cart', methods=['GET', 'POST'])
def cart():
    if 'order_id' not in session:
        # Creating a new order if one doesn't exist
        new_order = Order(status=False, total_cost=0, date=datetime.now())
        db.session.add(new_order)
        db.session.commit()
        session['order_id'] = new_order.id
        order = new_order
    else:
        order = db.session.get(Order, session['order_id'])

    if request.method == 'POST':
        product_id = request.form.get('product_id', type=int)
        if product_id:
            product = db.session.get(Product, product_id)
            if product:
                # Checking if the product is already in the cart
                existing_detail = OrderDetail.query.filter_by(order_id=order.id, product_id=product.id).first()
                if existing_detail:
                    existing_detail.quantity += 1
                else:
                    new_detail = OrderDetail(order_id=order.id, product_id=product.id, quantity=1)
                    db.session.add(new_detail)
                db.session.commit()
                flash('Product added to cart successfully!', category='success')
            else:
                flash('Product not found', category='error')

    order_details = OrderDetail.query.filter_by(order_id=order.id).all()
    total = sum(detail.product.price * detail.quantity for detail in order_details)
    order.total_cost = total
    db.session.commit()

    return render_template('cart.html', order_details=order_details, total=total)


@main_bp.route('/remove-from-cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'order_id' in session:
        order = Order.query.get(session['order_id'])
        if order:
            order_detail = OrderDetail.query.filter_by(order_id=order.id, product_id=product_id).first()
            if order_detail:
                db.session.delete(order_detail)
                db.session.commit()
                flash('Product removed from cart', category='success')
            else:
                flash('Product not found in cart', category='error')
        else:
            flash('No active order', category='error')
    else:
        flash('No active session', category='error')

    return redirect(url_for('main.cart'))

@main_bp.route('/empty-cart')
def empty_cart():
    # Your logic to empty the cart
    session.pop('cart', None)  # Clear the cart from the session
    return redirect(url_for('main.cart'))  # Redirect to the cart page or another appropriate page


# Checkout page
@main_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()  # Make sure this form is appropriately defined to handle the fields

    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        if not order.order_details:  # Ensure there are products in the cart
            flash('No products in cart to checkout.', 'error')
            return redirect(url_for('main.cart'))
        
        if form.validate_on_submit():
            order.status = True
            order.first_name = form.first_name.data  # Make sure the form field is 'first_name' if that's how it's defined
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            total_cost = 0

            # Calculate total cost based on the products in the order
            for detail in order.order_details:
                total_cost += detail.product.price * detail.quantity
            
            order.total_cost = total_cost
            order.date = datetime.now()

            try:
                db.session.commit()
                session.pop('order_id', None)  # Clear the order session after checkout
                flash('Checkout successful! Thank you for your order.', 'success')
                return redirect(url_for('main.index'))
            except:
                db.session.rollback()
                flash('There was an issue completing your order', 'error')
                return redirect(url_for('main.checkout'))
    
    else:
        flash('No active order to checkout', 'error')
        return redirect(url_for('main.cart'))
    
    return render_template('checkout.html', form=form)

@main_bp.route('/men')
def men():
    products = Product.query.filter(Product.category == 'Men Shoes').all()
    return render_template('men.html', products=products)

#Womens page
@main_bp.route('/women')
def women():
    products = Product.query.filter(Product.category == 'Women Shoes').all()
    return render_template('women.html', products=products)

# Brands Page
@main_bp.route('/brand/<brand_name>')
def brand_products(brand_name):
    products = Product.query.filter_by(brand=brand_name).all()
    return render_template('brand.html', products=products, title=f'{brand_name} Sneakers')



# Search functionality
@main_bp.route("/search")
def search():
    query = f'%{request.args.get('search', '')}%'
    products = db.session.scalars(db.select(Product).where(Product.name.like(query)))
    return render_template('index.html', products=products)





