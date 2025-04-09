from flask import Blueprint, render_template, request, redirect, url_for, flash
from backend.models import db, Product

products_bp = Blueprint('products', __name__)

@products_bp.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        new_product = Product(name=name, price=price, stock=stock)
        db.session.add(new_product)
        db.session.commit()
        flash('Producto agregado exitosamente.')
        return redirect(url_for('products.list_products'))
    return render_template('add_product.html')

@products_bp.route('/list')
def list_products():
    products = Product.query.all()
    return render_template('list_products.html', products=products)