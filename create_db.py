import sqlite3
def create_db():
    con=sqlite3.connect(database=r's_mart.db') 
    cur=con.cursor()
    
    cur.execute("CREATE TABLE IF NOT EXISTS customer(Cust_id INTEGER PRIMARY KEY AUTOINCREMENT ,name text,contact text,address text,dob text,email text)")    
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS Supplier(Sup_id INTEGER PRIMARY KEY AUTOINCREMENT ,name text,contact text,address text,description text,email text)")    
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS Category(cat_id INTEGER PRIMARY KEY AUTOINCREMENT ,name text)")    
    con.commit()
    
    #    ("P_Id","Name","Category","Supplier_Id","Price","Description","Quantity","Availability")
    cur.execute("CREATE TABLE IF NOT EXISTS Product(P_Id INTEGER PRIMARY KEY AUTOINCREMENT ,Name text,Category text,Supplier text,Price text,Description text,Quantity text,Availability text)")    
    con.commit()
    
    
create_db()    
 
 
 