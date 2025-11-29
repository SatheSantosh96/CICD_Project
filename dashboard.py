from tkinter import *
from datetime import datetime
from PIL import Image,ImageTk
from customer import CustomerClass
from supplier import SupplierClass
from category import CategoryClass
from product  import ProductClass
from sales import SalesClass
from billing import BillClass
from tkinter import messagebox
import time
import os
import sqlite3
class S_MART:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="lightgray")
        self.root.title("S_MART- The Supermarket Billing System   |  by Santosh & Dheeraj")
        
        # ----------- title -------
        self.icon_title=PhotoImage(file="images/logo.png")
        title=Label(self.root,text="S-MART Billing System",image=self.icon_title,compound=LEFT, font=("times new roman",40,"bold"),bg="#A3E958",fg="#3D5D1B",anchor='w',padx=50).place(x=0,y=0,relwidth=1,height=80)
        
        
        # ---------logout button------
        btn_logout=Button(self.root,text="LOGOUT",font=("times new roman",15,"bold"),bd=5,bg="lightyellow",cursor="hand2", anchor='w',padx=20 ).place(x=1150 ,y=15,height=50,width=150)
        
        # ---------clock-------
        self.lbl_clock=Label(self.root,text="Welcome to Supermarket Billing System\t\t Date:  DD-MM-YYYY\t\t Time: HH:MM:SS ",font=("times new roman",15,),bg="#1FB2F7",fg="white",anchor='w')
        self.lbl_clock.place(x=0,y=80,relwidth=1,height=30)
        # self.time()
        # -----------left menu---------
        self.MenuLogo=Image.open("images/bg.jpg")
        self.MenuLogo=self.MenuLogo.resize((300,170),Image.LANCZOS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)
        
        LeftMenu=Frame(self.root,bd=5,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=110,width=250,height=540)
        lbl_menulogo=Label(LeftMenu,image=self.MenuLogo,bg="lightyellow")
        lbl_menulogo.pack(side=TOP,fill=X)
        
        # self.icon_product=PhotoImage(file="images/product.png")
        lbl_menu=Label(LeftMenu,text="MENU",font=("times new roman",25,"bold"),bg="#1FB2F7", fg="white",cursor="hand2").pack(side=TOP,fill=X)  
        btn_product=Button(LeftMenu,text="PRODUCT",command=self.product,font=("times new roman",18,"bold"),bd=5,bg="#A3E958",cursor="hand2").pack(side=TOP,fill=X)
        btn_supplier=Button(LeftMenu,command=self.supplier,text="SUPPLIER",font=("times new roman",18,"bold"),bd=5,bg="#A3E958",cursor="hand2").pack(side=TOP,fill=X)
        btn_category=Button(LeftMenu,command=self.category,text="CATEGORY",font=("times new roman",18,"bold"),bd=5,bg="#A3E958",cursor="hand2").pack(side=TOP,fill=X)
        btn_customer=Button(LeftMenu,text="CUSTOMER",command=self.Customer,font=("times new roman",18,"bold"),bd=5,bg="#A3E958",cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(LeftMenu,command=self.sales,text="SALES",font=("times new roman",18,"bold"),bd=5,bg="#A3E958",cursor="hand2").pack(side=TOP,fill=X)
        btn_bill=Button(LeftMenu,command=self.bill,text="BILL",font=("times new roman",18,"bold"),bd=5,bg="#A3E958",cursor="hand2").pack(side=TOP,fill=X)
        
       
        
        # --------
        self.lbl_product=Label(self.root,text="total products\n[0]",bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"),bd=5,relief=RIDGE)
        self.lbl_product.place(x=400,y=170,height=125,width=250)
        
        self.lbl_supplier=Label(self.root,text="total Suppliers\n[0]",bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"),bd=5,relief=RIDGE)
        self.lbl_supplier.place(x=700,y=170,height=125,width=250)
         
        self.lbl_customers=Label(self.root,text="total customers\n[0]",bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"),bd=5,relief=RIDGE)
        self.lbl_customers.place(x=1000,y=170,height=125,width=250)
        
        self.lbl_categories=Label(self.root,text="today categories\n[0]",bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"),bd=5,relief=RIDGE)
        self.lbl_categories.place(x=400,y=400,height=125,width=250)
        
        self.lbl_sales=Label(self.root,text="total Sales\n[0]",bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"),bd=5,relief=RIDGE)
        self.lbl_sales.place(x=700,y=400,height=125,width=250)
        
        
        
        # ---------------  right frame ----------------
        # Rightframe=Frame(self.root,bd=5,relief=RIDGE,bg="lightgray")
        # Rightframe.place(x=300,y=140,width=1050,height=500)
        
        # --------------- footer ------------
        footer=Label(self.root,text="Supermarket Billing System | Developed By Santosh & Dheeraj\n for any enquiry, Contact: 8975228215",font=("times new roman",15,),bg="#1FB2F7",fg="black",anchor='center')
        footer.place(x=0,y=650,relwidth=1,height=60)
        
        
        self.update_content()
        # self.update_date_time()
        # ====================================================
        
    def Customer(self):
        self.new_window=Toplevel(self.root)
        self.new_obj=CustomerClass(self.new_window)
        
    def supplier(self):
        self.new_window=Toplevel(self.root)
        self.new_obj=SupplierClass(self.new_window)
        
    def category(self):
        self.new_window=Toplevel(self.root)
        self.new_obj=CategoryClass(self.new_window)        
    
    def product(self):
        self.new_window=Toplevel(self.root)
        self.new_obj=ProductClass(self.new_window)
        
    def sales(self):
        self.new_window=Toplevel(self.root)
        self.new_obj=SalesClass(self.new_window)    
        
    def bill(self):
        self.new_window=Toplevel(self.root)
        self.new_obj=BillClass(self.new_window)            
    
    # def time(self):

        # string = strftime("")
        # self.lbl_clock.config(text = string)
        # self.lbl_clock.after(1000, self)
                         
        
    def update_content(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_product.config(text=f'Total Products\n{str(len(product))}')
            
            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f'Total Suppliers\n{str(len(supplier))}')
            
            cur.execute("select * from customer")
            customer=cur.fetchall()
            self.lbl_customers.config(text=f'Total Customers\n{str(len(customer))}')
            
            cur.execute("select * from Category")
            product=cur.fetchall()
            self.lbl_categories.config(text=f'Total Categories\n{str(len(product))}')
            
            bill=len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Total Sales\n{str(bill)}')
            
            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
        
            self.lbl_clock.config(text=f"Welcome to Supermarket Billing System\t\t Date:{str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)
         
            
            
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root) 
        
    # def update_date_time(self):
        # time_=time.strftime("%I:%M:%S")
        # date_=time.strftime("%d-%m-%Y")
        
        # self.lbl_clock.config(text=f"Welcome to Supermarket Billing System\t\t Date:{str(date_)}\t\t Time: {str(time_)}")
        # self.lbl_clock.after(200,self.update_date_time)
         
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
if __name__=="__main__":       
    root=Tk() 
obj=S_MART(root) 
root.mainloop()  

