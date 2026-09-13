import json
import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "super_secret_inventory_key"

DATA_FILE = "inventory.json"

def load_inventory():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # Handle missing or corrupted inventory.json file
        return []

def save_inventory(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    inventory = load_inventory()
    search_query = request.args.get("search", "").lower()
    
    if search_query:
        inventory = [
            item for item in inventory 
            if search_query in item.get("name", "").lower() or search_query in item.get("sku", "").lower()
        ]
        
    return render_template("index.html", inventory=inventory, search_query=search_query)

@app.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        sku = request.form.get("sku", "").strip()
        description = request.form.get("description", "").strip()
        
        try:
            quantity = int(request.form.get("quantity", 0))
            threshold = int(request.form.get("threshold", 0))
        except ValueError:
            flash("Quantity and Threshold must be numbers.", "error")
            return redirect(url_for("add_product"))

        # Error Handling: Missing Name or SKU
        if not name or not sku:
            flash("Name and SKU are required.", "error")
            return redirect(url_for("add_product"))
            
        inventory = load_inventory()
        
        # Error Handling: Adding a product with a duplicate SKU
        if any(item.get("sku") == sku for item in inventory):
            flash(f"Product with SKU '{sku}' already exists.", "error")
            return redirect(url_for("add_product"))
            
        new_product = {
            "id": str(uuid.uuid4()),
            "sku": sku,
            "name": name,
            "description": description,
            "quantity": quantity,
            "threshold": threshold
        }
        
        inventory.append(new_product)
        save_inventory(inventory)
        flash("Product added successfully.", "success")
        return redirect(url_for("index"))
        
    return render_template("add.html")

@app.route("/stock/<item_id>", methods=["POST"])
def stock_movement(item_id):
    action = request.form.get("action") # "in" or "out"
    try:
        amount = int(request.form.get("amount", 0))
    except ValueError:
        flash("Amount must be a valid number.", "error")
        return redirect(url_for("index"))
        
    if amount <= 0:
        flash("Amount must be greater than zero.", "error")
        return redirect(url_for("index"))

    inventory = load_inventory()
    item_found = False
    
    for item in inventory:
        if item.get("id") == item_id:
            item_found = True
            if action == "in":
                item["quantity"] += amount
                flash(f"Added {amount} stock to '{item['name']}'.", "success")
            elif action == "out":
                # Error Handling: Negative stock quantities during stock out operations
                if item["quantity"] - amount < 0:
                    flash(f"Cannot remove {amount}. '{item['name']}' only has {item['quantity']} in stock.", "error")
                else:
                    item["quantity"] -= amount
                    flash(f"Removed {amount} stock from '{item['name']}'.", "success")
            else:
                flash("Invalid action.", "error")
            break
            
    if item_found:
        save_inventory(inventory)
    else:
        flash("Item not found.", "error")
        
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
