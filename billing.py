from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import sqlite3
import os
import tempfile
import time
class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="lightgray")
        self.root.title("S_MART- The Supermarket Billing System   |  by Santosh & Dheeraj")
        self.cart_list=[]
        self.chk_print=0
        # ----------- title -------
        self.icon_title=PhotoImage(file="images/logo.png")
        title=Label(self.root,text="S-MART Billing System",image=self.icon_title,compound=LEFT, font=("times new roman",40,"bold"),bg="#A3E958",fg="#3D5D1B",anchor='w',padx=50).place(x=0,y=0,relwidth=1,height=80)
        
        
        # ---------logout button------
        btn_logout=Button(self.root,text="LOGOUT",font=("times new roman",15,"bold"),bd=5,bg="lightyellow",cursor="hand2", anchor='w',padx=20 ).place(x=1150 ,y=15,height=50,width=150)
        
        # ---------clock-------
        self.lbl_clock=Label(self.root,text="Welcome to Supermarket Billing System\t\t Date:  DD-MM-YYYY\t\t Time: HH:MM:SS ",font=("times new roman",15,),bg="#1FB2F7",fg="white",anchor='w')
        self.lbl_clock.place(x=0,y=80,relwidth=1,height=30)
        
        
        
        
        # =========== productFrame ============
        
    
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=120,width=410,height=540)
        
        pTitle=Label(ProductFrame1,text="All Products",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)
        # ======= Product Search Frame =====
        self.var_search=StringVar()
        self.var_searchBY=StringVar()
        
        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)
        
        lbl_search=Label(ProductFrame2,text="Search Product",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)
        
        
        
        lbl_name=Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=2,y=45)
        
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15,),bg="lightyellow").place(x=128,y=47,width=150,height=22)
        
        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=285,y=45,width=100,height=25)
        btn_showall=Button(ProductFrame2,text="Show All",command=self.show,font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=285,y=10,width=100,height=25)
        
        
         # ========== Product Details  frame =======
        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=365)
        
        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)
        
        self.ProductTable=ttk.Treeview(ProductFrame3,columns=("P_Id","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)
        
        self.ProductTable.heading("P_Id",text="P_ID")
        self.ProductTable.heading("name",text="Name")
        self.ProductTable.heading("price",text="Price")
        self.ProductTable.heading("qty",text="Qty")
        self.ProductTable.heading("status",text="Status")
        
        self.ProductTable["show"]="headings"
        
        self.ProductTable.column("P_Id",width=40)
        self.ProductTable.column("name",width=100)
        self.ProductTable.column("price",width=90)
        self.ProductTable.column("qty",width=40)
        self.ProductTable.column("status",width=90)
    
        self.ProductTable.pack(fill=BOTH,expand=1)
        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)
        
        lbl_note=Label(ProductFrame1,text="Note : 'Enter 0 quantity to remove from Cart' ",font=("goudy old style",12),bg="white",fg="red",anchor='w').pack(side=BOTTOM,fill=X)

        # ============== customer Frame ========
        self.var_cname=StringVar()
        self.var_contact=StringVar()
        
        
        CustomerFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame1.place(x=420,y=120,width=530,height=100)
        
        cTitle=Label(CustomerFrame1,text="Customer Details",font=("goudy old style",15),bg="lightgray").pack(side=TOP,fill=X)
        
        
        lbl_name=Label(CustomerFrame1,text="Cust. Name",font=("times new roman",15,"bold"),bg="white").place(x=5,y=65)
        
        txt_name=Entry(CustomerFrame1,textvariable=self.var_cname,font=("times new roman",13,),bg="lightyellow",state='readonly').place(x=140,y=65,width=180)

        lbl_contact=Label(CustomerFrame1,text="Mobile N0.",font=("times new roman",15,"bold"),bg="white").place(x=5,y=35)
        
        txt_contact=Entry(CustomerFrame1,textvariable=self.var_contact,font=("times new roman",13,),bg="lightyellow").place(x=140,y=35,width=180) 
        
        btn_fetch_cust=Button(CustomerFrame1,command=self.fetch_customer,text="Enter",font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=340,y=45,width=80,height=40)
        btn_clear_cust=Button(CustomerFrame1,command=self.clear_cust,text="Clear",font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=430,y=45,width=80,height=40)
        
        
        # ========== CALCART frame =======
        CalCartFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        CalCartFrame.place(x=420,y=220,width=530,height=260)
        
      
        
        
        # -------------- Cart Frame --------
        CartFrame=Frame(CalCartFrame,bd=3,relief=RIDGE)
        CartFrame.place(x=5,y=5,width=515,height=245)
        
        self.cartTitle=Label(CartFrame,text="Cart\t Total Product:[0]",font=("goudy old style",15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)
       
        
        scrolly=Scrollbar(CartFrame,orient=VERTICAL)
        scrollx=Scrollbar(CartFrame,orient=HORIZONTAL)
        
        self.CartTable=ttk.Treeview(CartFrame,columns=("P_Id","name","price","qty","total"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)
        
        self.CartTable.heading("P_Id",text="P_ID")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price",text="Price")
        self.CartTable.heading("qty",text="Qty")
        self.CartTable.heading("total",text="Total")
        
        
        self.CartTable["show"]="headings"
        
        self.CartTable.column("P_Id",width=40)
        self.CartTable.column("name",width=100)
        self.CartTable.column("price",width=90)
        self.CartTable.column("qty",width=40)
        self.CartTable.column("total",width=90)
        

        self.CartTable.pack(fill=BOTH,expand=1)
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)
        
         # ========== Add Cart Widgets frame =======
         
        self.var_pid=StringVar()
        self.var_pname=StringVar()
        self.var_pprice=StringVar() 
        self.var_qty=StringVar()
        self.var_getqty=StringVar() 
        self.var_stock=StringVar()   
        #  ===========
        add_CartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        add_CartWidgetsFrame.place(x=420,y=490,width=530,height=170)
        
        lbl_p_id=Label(add_CartWidgetsFrame,text="Product Id",font=("times new roman",15),bg="white").place(x=20,y=5)
        txt_p_id=Entry(add_CartWidgetsFrame,textvariable=self.var_pid,font=("times new roman",15),bg="lightyellow").place(x=20,y=35,width=80,height=22)
        
        btn_view_p=Button(add_CartWidgetsFrame,command=self.view_details,text="View",font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=110,y=35,width=70,height=22)
        
     
        
        lbl_p_name=Label(add_CartWidgetsFrame,text="ProductName",font=("times new roman",15),bg="white").place(x=300,y=5)
        txt_p_name=Entry(add_CartWidgetsFrame,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=300,y=35,width=190,height=22)
        
        lbl_p_price=Label(add_CartWidgetsFrame,text="Price Per Qty",font=("times new roman",15),bg="white").place(x=20,y=65)
        txt_p_price=Entry(add_CartWidgetsFrame,textvariable=self.var_pprice,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=20,y=100,width=150,height=22)
        
        lbl_p_qty=Label(add_CartWidgetsFrame,text="Quantity",font=("times new roman",15),bg="white").place(x=300,y=65)
        txt_p_qty=Entry(add_CartWidgetsFrame,textvariable=self.var_getqty,font=("times new roman",15),bg="lightyellow").place(x=300,y=100,width=120,height=22)
        
        self.lbl_inStock=Label(add_CartWidgetsFrame,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_inStock.place(x=5,y=130)
        
        btn_clear_cart=Button(add_CartWidgetsFrame,command=self.clear_cart,text="Clear",font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=180,y=130,width=150,height=30)
        
        btn_add_cart=Button(add_CartWidgetsFrame,command=self.add_update_cart,text="Add | Update Cart",font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=340,y=130,width=180,height=30)
        
        # ================= Biling Area ========
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=953,y=110,width=395,height=410)
        bTitle=Label(billFrame,text="Customer Bill",font=("goudy old style",20,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
       
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)
        
        # ======== Biling BUttons
        
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=953,y=520,width=395,height=140)
        
        self.lbl_amt=Label(billMenuFrame,text="Bill Amt \n[0]",font=("goudy old style",15,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amt.place(x=2,y=5,width=120,height=70)

        self.lbl_discount=Label(billMenuFrame,text="Discount \n[5%]",font=("goudy old style",15,"bold"),bg="#8bc34a",fg="white")
        self.lbl_discount.place(x=124,y=5,width=120,height=70)

        self.lbl_net_pay=Label(billMenuFrame,text="Net Pay \n[0]",font=("goudy old style",15,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=246,y=5,width=160,height=70)
        
        # =========
        btn_print=Button(billMenuFrame,text="Print",command=self.printbill,font=("goudy old style",15,"bold"),bg="lightgreen",fg="white",cursor="hand2")
        btn_print.place(x=2,y=80,width=120,height=50)

        btn_clear_all=Button(billMenuFrame,command=self.clear_all,text="Clear All",font=("goudy old style",15,"bold"),bg="gray",fg="white",cursor="hand2")
        btn_clear_all.place(x=124,y=80,width=120,height=50)

        btn_generate=Button(billMenuFrame,command=self.generate_bill,text="Generate Bill",font=("goudy old style",15,"bold"),bg="#009688",fg="white",cursor="hand2")
        btn_generate.place(x=246,y=80,width=160,height=50)
        
        # ======footer =======
        footer=Label(self.root,text="Supermarket Billing System Developed By Santosh & Dheeraj \n For Any Technical Issue, Contact: 8975228215",font=("times new roman",11),bd=0,bg="#1FB2F7",fg="black")
        footer.pack(side=BOTTOM,fill=X)
        
        self.show()
        self.update_date_time()
        # self.bill_top()
        # ============== functions ==========
        
    def show(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            # self.ProductTable=ttk.Treeview(ProductFrame3,columns=("P_Id","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
       
            cur.execute("Select P_Id,name,price,quantity,availability from Product where availability='IN STOCK'")
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")    

    def search(self):
        
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search Input Required",parent=self.root) 
            else:      
                cur.execute("Select P_Id,name,price,quantity,availability from Product where Name  LIKE '%" + self.var_search.get()+"%'and availability='IN STOCK' " )
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No Record Found",parent=self.root) 
        
        except Exception as ex:
                messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root)     
        
        
    def get_data(self,ev):
        f=self.ProductTable.focus()    
        content=(self.ProductTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_pprice.set(row[2]) 
        self.var_getqty.set('1')
        self.lbl_inStock.config(text=f"In Stock[{str(row[3])}]")
        self.var_stock.set(row[3])
    #    P_Id,name,price,quantity,availability
        
    def get_data_cart(self,ev):
        f=self.CartTable.focus()    
        content=(self.CartTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_pprice.set(row[2]) 
        self.var_getqty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock[{str(row[5])}]")
        self.var_stock.set(row[5])
    #    P_Id,name,price,quantity,availability
    
    
    
    
        
    def view_details(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Search Input Required",parent=self.root) 
            else:
                s=self.var_pid.get()
                cur.execute("Select P_Id,name,price,quantity,availability from Product where P_Id  LIKE '%" + self.var_pid.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    for row in rows:
                        self.var_pname.set(row[1])
                        self.var_pprice.set(row[2]) 
                        self.var_getqty.set('1')
                        self.var_stock.set(row[3])
                        self.lbl_inStock.config(text=f"In Stock[{str(row[3])}]")
    
                else:
                     messagebox.showerror("Error","No Record Found",parent=self.root)
        except Exception as ex:
                messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root)
    
    
    def fetch_customer(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            if self.var_contact.get()=="":
                messagebox.showerror("Error","Mobile No Required",parent=self.root) 
            else:
                s=self.var_contact.get()
                cur.execute("Select Cust_id,name,contact from customer where contact  LIKE '%" + self.var_contact.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    for row in rows:
                        self.var_cname.set(row[1])
                else:
                     messagebox.showerror("Error","No Record Found",parent=self.root)
        except Exception as ex:
                messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root)
        
    
    def clear_cust(self):
        self.var_contact.set('')        
        self.var_cname.set('')
   
    
    
        
    def add_update_cart(self):
        if self.var_pid.get()=='':
            messagebox.showerror("Error","Please Select Product ",parent=self.root)
        elif self.var_getqty.get()=='': 
            messagebox.showerror("Error","Quantity Required",parent=self.root)
        elif int(self.var_getqty.get()) > int(self.var_stock.get()): 
            messagebox.showerror("Error","Invalid Quantity",parent=self.root)   
        else:    
            price_cal=int(self.var_getqty.get())*float(self.var_pprice.get())
            price_cal=float(price_cal)
            # price_cal=self.var_pprice.get()
            
            # P_Id,name,price,quantity,total,stock
            cart_data=[self.var_pid.get(),self.var_pname.get(),self.var_pprice.get(),self.var_getqty.get(),price_cal,self.var_stock.get()]
            
            
            # ============== update cart ========
            present='no'
            index_= 0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno('Confirm',"Product already present \n Do you want to Update| Remove from the cart list?",parent=self.root)
                if op==True:
                    if self.var_getqty.get=="0":
                        self.cart_list.pop(index_)
                    
                    else:
                        # P_Id,name,price,quantity,availability
                
                        self.cart_list[index_][3]= self.var_getqty.get() #qty
                        # self.cart_list[index_][4]= price_cal  #price

            else:            
                        
                self.cart_list.append(cart_data)
            self.show_cart()
            self.billupdate()
            
            
            
    def billupdate(self):
        self.bill_amt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            
            
            #  P_Id,name,price,quantity,availability
            self.bill_amt=self.bill_amt+((float(row[2]))*int(row[3])) #qty
        self.discount=(self.bill_amt*5)/100
        self.net_pay=self.bill_amt-self.discount
        self.lbl_amt.config(text=f'Bill Amt\n{str(self.bill_amt)}')
        self.lbl_net_pay.config(text=f'Net Pay\n{str(self.net_pay)}') 
        self.cartTitle.config(text=f"Cart\t Total Product:[{str(len(self.cart_list))}]")           
                 
    def show_cart(self):
        
        try:
    
            
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root)    

    
    def generate_bill(self):
        if self.var_cname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error", f" Customer Details are Required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error", f"Please Add Products To The Cart !!!",parent=self.root)
            
        else:
            
            #=========== bill  top ============
            self.bill_top()
            # ================== bill middle===========
            self.bill_middle()
            #========= bill bottom ==============  
            self.bill_bottom()
            self.chk_print=1
               
    def bill_top(self):       
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        # print(self.invoice)
        bill_top_temp=f'''
\t\t S_MART BILLING
\t Phone No.8975228215,pune 04
{str("="*45)}
Customer Name:{self.var_cname.get()}
Ph No.:{self.var_contact.get()}
Bill No.{str(self.invoice)}\t\t\tDate:{str(time.strftime("%d/%m/%Y"))}
{str("="*45)}
Product Name\t\t\tQTy Price\t  Total
{str("="*45)}
    
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)
        
    def bill_middle(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        
        try:
            
         
            for row in self.cart_list:

                # P_Id,name,price,quantity,total,stock
                pid=row[0]
                name=row[1]
                qty=row[3]
                if int(row[3])==int(row[5]):
                    Availability='OUT OF STOCK'
                if int(row[3])!=int(row[5]):
                    Availability='IN STOCK'
                quantity=int(row[5])-int(row[3])
                
                qty=str(qty) 
                price=float(row[2])
                price=str(price)

                total=str(row[4])


                self.txt_bill_area.insert(END,"\n"+name+"\t\t\t"+qty+" "+price+"\t  "+total)
                # ============ update quantity in product table===========
                cur.execute('Update Product set Quantity=?,Availability=? where P_Id=?',(
                    quantity,
                    Availability,
                    pid
                ))
                con.commit()
            con.close()
            self.show()    
                
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root)    
            


    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*45)}
Bill Amount:\t\t\t\t  Rs.{self.bill_amt}
Discount\t\t\t\t  Rs.{self.discount}
Net Pay\t\t\t\t  Rs.{self.net_pay}
{str("="*45)}\n  
  Thank  You !..Visit Again    
   '''    
        self.txt_bill_area.insert(END,bill_bottom_temp)  
        
        fp=open(f'bill/{str(self.invoice)}.txt','w')
        fp.write(self.txt_bill_area.get('1.0',END))
        fp.close()
        messagebox.showinfo('Saved',"Bill has been generated & Saved",parent=self.root)
        
        
        
        
         
#   ===========
    
    def clear_cart(self):
        self.var_pid.set('')        
        self.var_pname.set('')
        self.var_pprice.set('') 
        self.var_getqty.set('')
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set('')
         
     
    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.var_search.set('')
        self.cartTitle.config(text=f"Cart\t Total Product:[0]")
        self.clear_cart()
        self.show()
        self.show_cart()
        
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        
        self.lbl_clock.config(text=f"Welcome to Supermarket Billing System\t\t Date:{str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)
                
    def printbill(self):
        if self.chk_print==1:
            messagebox.showinfo('print',"Printing Bill,Please wait ",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
        else:
            messagebox.showerror('print',"Please Generate Bill To Print the Receipt ",parent=self.root)    
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
            os.startfile(new_file,'print')
if __name__=="__main__":       
    root=Tk() 
    obj=BillClass(root) 
    root.mainloop()  


