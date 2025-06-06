from flask import Flask, render_template
from api.products import get_all_products
from api.inventory import get_all_inventory
from api.orders import get_all_orders

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/products')
def products():
    return render_template('products.html', products=get_all_products())

@app.route('/inventory')
def inventory():
    return render_template('inventory.html', inventory=get_all_inventory())

@app.route('/orders')
def orders():
    return render_template('orders.html', orders=get_all_orders())