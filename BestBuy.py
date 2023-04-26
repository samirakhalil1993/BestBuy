import mysql.connector as mysql

MYSQL_USER = 'USER-NAME'  # replace with your user name.
MYSQL_PASS = 'MYSQL_PASS'  # replace with your MySQL server password
MYSQL_DATABASE = 'DATABASE_NAME'  # replace with your database name

# Function to establish a connection to the MySQL database
def get_connection():
    return mysql.connect(
        user=MYSQL_USER,
        passwd=MYSQL_PASS,
        database=MYSQL_DATABASE,
        host='127.0.0.1'
    )

# Use a context manager to handle the connection and cursor
with get_connection() as connection:
    with connection.cursor(dictionary=True) as cnx:
        # Drop table if it exists
        cnx.execute('DROP TABLE IF EXISTS Names')
        
        # Create table
        cnx.execute('CREATE TABLE Names (name varchar(20))')
        
        # Insert data into table
        cnx.execute("INSERT INTO Names VALUES ('test')")
        cnx.execute("INSERT INTO Names VALUES ('test_1')")
        
        # Select data from table
        cnx.execute('SELECT * FROM Names')

        # Print the result
        for row in cnx:
            print(row)

# Connection is closed automatically when leaving the 'with' block

def get_products_filtered(categories=None):
    connection = get_connection()
    cursor = connection.cursor()
    
    if categories:
        categories_str = "','".join(categories)
        query = f"SELECT * FROM Products WHERE Type IN ('{categories_str}')"
    else:
        query = "SELECT * FROM Products"
        
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return result


def get_products_search(values):
    connection = get_connection()
    cursor = connection.cursor()
    
    values_str = "','".join(values)
    query = f"SELECT * FROM Products WHERE ProductID IN ('{values_str}')"
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return result


def get_products_ids(ids):
    return get_products_search(ids)


def get_categories():
    connection = get_connection()
    cursor = connection.cursor()
    
    query = "SELECT DISTINCT Type FROM Products"
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return result


def get_subcategories(gender, category):
    connection = get_connection()
    cursor = connection.cursor()
    
    query = f"SELECT DISTINCT Subtype FROM Products WHERE Gender = '{gender}' AND Type = '{category}'"
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return result


def write_order(order):
    connection = get_connection()
    cursor = connection.cursor()
    
    # Insert customer information
    query = f"INSERT INTO Customers (FirstName, LastName, PostalAddress) VALUES ('{order['first_name']}', '{order['last_name']}', '{order['address']}')"
    cursor.execute(query)
    connection.commit()
    customer_id = cursor.lastrowid
    
    # Insert order information
    query = f"INSERT INTO Orders (CustomerID, OrderDate, TotalPrice) VALUES ({customer_id}, NOW(), {order['total']})"
    cursor.execute(query)
    connection.commit()
    order_id = cursor.lastrowid
    
    # Insert order details
    for item in order['items']:
        query = f"INSERT INTO OrderDetails (OrderID, ProductID, Quantity, Size, Color, SubtotalPrice) VALUES ({order_id}, {item['id']}, {item['quantity']}, '{item['size']}', '{item['color']}', {item['subtotal']})"
        cursor.execute(query)
        connection.commit()

    cursor.close()
    connection.close()


def get_20_most_popular():
    connection = get_connection()
    cursor = connection.cursor()
    
    query = """
        SELECT p.ProductID, p.Type, p.Subtype, p.Brand, p.Color, p.Gender, p.Price, p.Size, SUM(od.Quantity) as total_quantity
        FROM Products p
        JOIN OrderDetails od ON p.ProductID = od.ProductID
        GROUP BY p.ProductID
        ORDER BY total_quantity DESC
        LIMIT 20
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return result
