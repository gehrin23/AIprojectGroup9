```python
def calculate_total_sales(sales_data):
    """
    Calculates the total sales from a list of sales records.

    Args:
        sales_data (list of dict): A list where each dictionary represents a sale with at least a 'price' key.

    Returns:
        float: The total sum of all sales prices.
    """
    total = 0.0
    for sale in sales_data:
        # Add the price of each sale to the total
        total += sale.get('price', 0)
    return total

def get_top_selling_products(sales_data, top_n=5):
    """
    Retrieves the top N products based on their total sales.

    Args:
        sales_data (list of dict): A list where each dictionary represents a sale with at least 'product' and 'price' keys.
        top_n (int): The number of top selling products to retrieve.

    Returns:
        list of tuple: A list of tuples containing the product name and total sales amount, sorted by highest sales first.
    """
    from collections import defaultdict

    # Dictionary to accumulate total sales per product
    product_sales = defaultdict(float)
    for sale in sales_data:
        product_sales[sale['product']] += sale.get('price', 0)

    # Sort products by total sales in descending order and get top N
    return sorted(product_sales.items(), key=lambda item: item[1], reverse=True)[:top_n]

def process_sales_report(sales_file_path):
    """
    Processes a CSV file containing sales data and generates summary reports.

    Args:
        sales_file_path (str): The path to the CSV file containing sales data with columns 'product' and 'price'.

    Returns:
        dict: A dictionary containing the total sales and top selling products.
    """
    import csv

    # Read sales data from a CSV file
    with open(sales_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        sales_data = list(reader)

    # Calculate total sales
    total_sales = calculate_total_sales(sales_data)

    # Get top selling products
    top_products = get_top_selling_products(sales_data)

    return {
        'total_sales': total_sales,
        'top_products': top_products
    }
```

**Onboarding PDF Summary:**

1. **Overall file purpose:**
   - This Python script processes sales data from a CSV file, calculates the total sales, and identifies the top selling products.

2. **Key functions/methods and their responsibilities:**
   - `calculate_total_sales(sales_data)`: Calculates the total sum of all sales prices.
   - `get_top_selling_products(sales_data, top_n=5)`: Retrieves the top N products based on their total sales.
   - `process_sales_report(sales_file_path)`: Processes a CSV file containing sales data and generates summary reports.

3. **Inputs/outputs/side effects:**
   - `calculate_total_sales(sales_data)`:
     - Input: A list of dictionaries where each dictionary represents a sale with at least a 'price' key.
     - Output: The total sum of all sales prices as a float.
     - Side effect: None.
   
   - `get_top_selling_products(sales_data, top_n=5)`:
     - Input: A list of dictionaries where each dictionary represents a sale with at least 'product' and 'price' keys; an integer specifying the number of top products to retrieve.
     - Output: A list of tuples containing the product name and total sales amount, sorted by highest sales first.
     - Side effect: None.

   - `process_sales_report(sales_file_path)`:
     - Input: The path to a CSV file containing sales data with columns 'product' and 'price'.
     - Output: A dictionary containing the total sales and top selling products.
     - Side effect: Reads from a CSV file.

4. **Design patterns, dependencies:**
   - The script uses the `defaultdict` from the `collections` module to accumulate total sales per product.
   - It reads data from a CSV file using Python's built-in `csv` module.

5. **Point out cohesion and coupling:**
   - High Cohesion: Each function has a clear, focused responsibility related to processing sales data.
   - Low Coupling: Functions are designed to work independently of each other, with minimal dependencies between them. The `process_sales_report` function coordinates the use of `calculate_total_sales` and `get_top_selling_products`, but does not rely on their internal workings directly.