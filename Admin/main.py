from flask import Flask, render_template, request, redirect
from api.products import get_all_products
from api.inventory import get_all_inventory
from api.orders import get_all_orders, update_order_status

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
    status = request.args.get('status')
    orders = get_all_orders(status)
    return render_template('orders.html', orders=orders, current_filter=status)

@app.route('/update_status', methods=['POST'])
def update_status():
    update_order_status(request.form['order_id'], request.form['new_status'])
    return redirect('/orders')
