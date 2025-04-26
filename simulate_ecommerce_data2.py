import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
random.seed(42)
np.random.seed(42)

# ---------- 1. Customers Table ----------
num_customers = 100
customer_ids = [f"CUST{i:04d}" for i in range(1, num_customers + 1)]

customers = pd.DataFrame({
    'Customer ID': customer_ids,
    'Customer Name': [f'Customer_{i}' for i in range(1, num_customers + 1)],
    'Gender': np.random.choice(['Male', 'Female', 'Other'], size=num_customers),
    'Age': np.random.randint(18, 60, size=num_customers),
    'City': np.random.choice(['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata'], size=num_customers),
    'Customer Segment': np.random.choice(['New', 'Returning', 'Loyal'], size=num_customers),
    'Registration Date': pd.to_datetime(np.random.choice(pd.date_range('2022-01-01', '2024-01-01'), num_customers)),
    'Login Type': np.random.choice(['Guest', 'Registered'], size=num_customers)
})

# ---------- 2. Products Table ----------
num_products = 50
product_ids = [f"PROD{i:04d}" for i in range(1, num_products + 1)]
categories = ['Electronics', 'Clothing', 'Home Decor', 'Beauty', 'Toys']

products = pd.DataFrame({
    'Product ID': product_ids,
    'Product Name': [f'Product_{i}' for i in range(1, num_products + 1)],
    'Product Category': np.random.choice(categories, size=num_products),
    'Brand': np.random.choice(['BrandA', 'BrandB', 'BrandC', 'BrandD'], size=num_products),
    'Price': np.random.randint(200, 10000, size=num_products)
})

products['Cost'] = (products['Price'] * np.random.uniform(0.6, 0.9, size=num_products)).round(2)

# ---------- 3. Transactions Table ----------
num_orders = 1000
order_ids = [f"ORD{i:05d}" for i in range(1, num_orders + 1)]

transactions = pd.DataFrame({
    'Order ID': order_ids,
    'Customer ID': np.random.choice(customer_ids, size=num_orders),
    'Product ID': np.random.choice(product_ids, size=num_orders),
    'Order Date': pd.to_datetime(np.random.choice(pd.date_range('2022-01-01', '2024-12-31'), num_orders)),
    'Quantity': np.random.randint(1, 5, size=num_orders),
    'Discount': np.random.choice([0, 5, 10, 15, 20], size=num_orders),
    'Payment Mode': np.random.choice(['Credit Card', 'Debit Card', 'Net Banking', 'UPI', 'COD'], size=num_orders),
    'Order Status': np.random.choice(['Delivered', 'Cancelled', 'Returned'], size=num_orders, p=[0.8, 0.1, 0.1])
})

# Join product prices and cost
transactions = transactions.merge(products[['Product ID', 'Price', 'Cost']], on='Product ID', how='left')

# Calculate Total Sales and Profit
transactions['Total Sales'] = transactions['Quantity'] * transactions['Price'] * (1 - transactions['Discount']/100)
transactions['Profit'] = transactions['Total Sales'] - (transactions['Quantity'] * transactions['Cost'])

# ---------- 4. Date Table ----------
date_range = pd.date_range(start='2022-01-01', end='2024-12-31')
date_dim = pd.DataFrame({
    'Date': date_range,
    'Day': date_range.day,
    'Month': date_range.month,
    'Month Name': date_range.strftime('%B'),
    'Quarter': date_range.quarter,
    'Year': date_range.year,
    'Week Number': date_range.isocalendar().week,
    'Day of Week': date_range.strftime('%A')
})

# ---------- 5. Delivery Table ----------
delivery = transactions[['Order ID', 'Order Date']].copy()
delivery['Shipping Method'] = np.random.choice(['Standard', 'Express', 'Same-Day'], size=num_orders)
delivery['Delivery Days'] = np.random.randint(1, 10, size=num_orders)
delivery['Delivery Date'] = delivery['Order Date'] + pd.to_timedelta(delivery['Delivery Days'], unit='D')
delivery['Delivery Status'] = np.random.choice(['Delivered', 'Cancelled', 'Delayed'], size=num_orders)

# ---------- 6. Returns Table ----------
returned_orders = transactions[transactions['Order Status'] == 'Returned'].copy()
returns = pd.DataFrame({
    'Return ID': [f'RET{i:04d}' for i in range(1, len(returned_orders) + 1)],
    'Order ID': returned_orders['Order ID'].values,
    'Product ID': returned_orders['Product ID'].values,
    'Return Reason': np.random.choice(['Damaged', 'Wrong Item', 'No longer needed', 'Other'], size=len(returned_orders)),
    'Return Date': returned_orders['Order Date'] + pd.to_timedelta(np.random.randint(1, 15, size=len(returned_orders)), unit='D'),
    'Refund Amount': returned_orders['Total Sales'].values
})

# ---------- 7. Device/Session Table ----------
num_sessions = 500
session_data = pd.DataFrame({
    'Session ID': [f'SSN{i:04d}' for i in range(1, num_sessions + 1)],
    'Customer ID': np.random.choice(customer_ids, size=num_sessions),
    'Device Type': np.random.choice(['Mobile', 'Desktop', 'Tablet'], size=num_sessions),
    'Browser': np.random.choice(['Chrome', 'Firefox', 'Safari', 'Edge'], size=num_sessions),
    'Session Duration (min)': np.random.randint(1, 60, size=num_sessions),
    'Login Type': np.random.choice(['Guest', 'Registered'], size=num_sessions)
})

# ---------- Show Sample ----------
print("Customers Table:\n", customers.head(), "\n")
print("Products Table:\n", products.head(), "\n")
print("Transactions Table:\n", transactions.head(), "\n")
print("Date Dimension Table:\n", date_dim.head(), "\n")
print("Delivery Table:\n", delivery.head(), "\n")
print("Returns Table:\n", returns.head(), "\n")
print("Device/Session Table:\n", session_data.head(), "\n")

# Optional: Save to CSVs
customers.to_csv("customers.csv", index=False)
products.to_csv("products.csv", index=False)
transactions.to_csv("transactions.csv", index=False)
date_dim.to_csv("date_dim.csv", index=False)
delivery.to_csv("delivery.csv", index=False)
returns.to_csv("returns.csv", index=False)
session_data.to_csv("session_data.csv", index=False)
