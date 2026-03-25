from flask import Flask, render_template, request, redirect, url_for
from scraper import get_price
from models import (
    add_product,
    get_all_products,
    get_product_by_id,
    update_product,
    delete_product
)
import threading
from tracker import run_tracker

app = Flask(__name__)


# 🔹 Home page
@app.route('/')
def home():
    return render_template('index.html')


# 🔹 Add product
@app.route('/track', methods=['POST'])
def track():
    name = request.form.get('name')
    url = request.form.get('url')
    target_price = float(request.form.get('target_price'))
    email = request.form.get('email')

    price_str = get_price(url)

    try:
        price = float(price_str.replace(",", ""))
    except:
        price = None

    add_product(name, url, target_price, email, price)

    return render_template('result.html',
                           name=name,
                           price=price_str,
                           target=target_price)


# 🔹 Dashboard (READ)
@app.route('/dashboard')
def dashboard():
    products = get_all_products()

    # Add status logic
    for p in products:
        if p['current_price'] is not None and p['current_price'] <= p['target_price']:
            p['status'] = "Target Reached"
        elif p['alert_sent']:
            p['status'] = "Alert Sent"
        else:
            p['status'] = "Tracking"

    return render_template('dashboard.html', products=products)


# 🔹 Update page (GET + POST)
@app.route('/update/<int:product_id>', methods=['GET', 'POST'])
def update(product_id):
    product = get_product_by_id(product_id)

    if request.method == 'POST':
        new_price = float(request.form.get('target_price'))
        new_email = request.form.get('email')

        update_product(product_id, new_price, new_email)

        return redirect(url_for('dashboard'))

    return render_template('update.html', product=product)


# 🔹 Delete product
@app.route('/delete/<int:product_id>')
def delete(product_id):
    delete_product(product_id)
    return redirect(url_for('dashboard'))


# 🔹 Start tracker safely
if __name__ == '__main__':
    import os

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Thread(target=run_tracker, daemon=True).start()

    app.run(debug=True)