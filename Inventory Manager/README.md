# Inventory Manager

A simple, lightweight web-based application to manage inventory, built with Python (Flask) and standard HTML/CSS. This was built strictly following the Software Requirements Specification (SRS) for the mini project. Data is persistently stored in a local `inventory.json` file to avoid complex database configurations.

## Features

- **Add Product:** Register new products easily with a Name, SKU, Description, Initial Quantity, and Low Stock Threshold.
- **Stock Movement:** Increment (Stock In) or decrement (Stock Out) stock quantities directly from the product list.
- **Search Products:** Filter products dynamically by Name or SKU using the top search bar.
- **Low Stock Alerts:** Automatically flags items when their current quantity reaches or falls below the designated threshold level.
- **JSON Data Storage:** Safely stores all data in a local JSON format. No need for internet connection or external SQL database.
- **Error Handling:** Gracefully handles missing information, duplicate SKUs, negative quantities during stock-out, or missing inventory files without crashing.

## Prerequisites

- Python 3.x
- Flask (`pip install Flask`)

## Setup & Running

1. **Install Flask (if not already installed):**
   ```bash
   pip install Flask
   ```

2. **Run the Application:**
   Navigate to the project directory and run the application script:
   ```bash
   python app.py
   ```

3. **Access the Application:**
   Open a modern web browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

## Project Architecture

- **Backend:** `app.py` handles the Python/Flask server logic (routing, form processing, JSON file I/O).
- **Frontend Views:** `templates/index.html` (Task/Product list and dashboard) and `templates/add.html` (Form to add products).
- **Styling:** `static/style.css` provides a simple, clear, and easy-to-navigate user interface.
- **Storage:** `inventory.json` saves data locally after every add or stock movement operation.
