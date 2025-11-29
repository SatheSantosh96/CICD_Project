from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
 
class ProductClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+250+140")
        self.root.config(bg="#A3E958")
        self.root.title("S_MART- The Supermarket Billing System   |  by Santosh & Dheeraj")
        self.root.focus_force()
        # =======variables========
        self.var_p_id=StringVar()
        self.var_p_name=StringVar()
        self.var_p_category=StringVar()
        self.var_p_Supplier=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()
        self.var_p_price=StringVar()
        self.var_p_description=StringVar()
        self.var_p_quantity=StringVar()
        self.var_p_availability=StringVar()
        
        self.var_SearchBy= StringVar()
        self.var_SearchTxt= StringVar()
    
        
            
        
        
        
        
        
        # ===========
        product_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=10,width=450,height=480)
        
        #   ---------- title-----
        title=Label(product_Frame,text="Manage Product Details",font=("goudy old style",18,"bold"),bg="#1FB2F7",fg="white").pack(side=TOP,fill=X)
        
        
        # =========== COLUMN 1 =================
        # lbl_p_id=Label(product_Frame,text="Product ID",font=("goudy old style",18,"bold"),bg="white").place(x=30,y=40)
        lbl_p_name=Label(product_Frame,text="Name",font=("goudy old style",18,"bold"),bg="white").place(x=30,y=80)
        
        lbl_p_category=Label(product_Frame,text="Category",font=("goudy old style",18,"bold"),bg="white").place(x=30,y=120)
        
        lbl_p_supplier=Label(product_Frame,text="Supplier",font=("goudy old style",18,"bold"),bg="white").place(x=30,y=160)
        
        lbl_p_price=Label(product_Frame,text="Price",font=("goudy old style",18,"bold"),bg="white").place(x=30,y=200) 
        
        lbl_p_description=Label(product_Frame,text="Description",font=("goudy old style",18,"bold"),bg="white").place(x=30,y=240)
        
        lbl_p_quantity=Label(product_Frame,text="Quantity",font=("goudy old style",18,"bold"),bg="white").place(x=30,y=280)
        
        lbl_p_Availability=Label(product_Frame,text="Availability",font=("goudy old style",18,"bold"),bg="white").place(x=30,y=320)  
        
        # ============ COLUMN 2 ===========
        # txt_p_id=Entry(product_Frame,textvariable=self.var_p_id,font=("goudy old style",18,"bold"),bg="lightyellow").place(x=170,y=40,width=250)
        txt_p_name=Entry(product_Frame,textvariable=self.var_p_name,font=("goudy old style",18,"bold"),bg="lightyellow").place(x=170,y=80,width=250)
        
        # -----------
        cmb_category=ttk.Combobox(product_Frame,textvariable=self.var_p_category, values=self.cat_list,state="readonly",justify=CENTER,font=("goudy old style",18))
        cmb_category.place(x=170,y=120,width=250)
        cmb_category.current(0)
        
        cmb_supplier=ttk.Combobox(product_Frame,textvariable=self.var_p_Supplier, values=self.sup_list,state="readonly",justify=CENTER,font=("goudy old style",18))
        cmb_supplier.place(x=170,y=160,width=250)
        cmb_supplier.current(0)
        
        
        txt_p_price=Entry(product_Frame,textvariable=self.var_p_price,font=("goudy old style",18,"bold"),bg="lightyellow").place(x=170,y=200,width=250)
        
        txt_p_Description=Entry(product_Frame,textvariable=self.var_p_description,font=("goudy old style",18,"bold"),bg="lightyellow").place(x=170,y=240,width=250)
        
        txt_p_quantity=Entry(product_Frame,textvariable=self.var_p_quantity,font=("goudy old style",18,"bold"),bg="lightyellow").place(x=170,y=280,width=250)
        
        cmb_availablity=ttk.Combobox(product_Frame,textvariable=self.var_p_availability, values=("Select","IN STOCK","OUT OF STOCK"),state="readonly",justify=CENTER,font=("goudy old style",18))
        cmb_availablity.place(x=170,y=320,width=250)
        cmb_availablity.current(0)
        
        
        # ========== buttons==========
        
        btn_add=Button(product_Frame,command=self.add,text="Save",font=("goudy old style",20,"bold"),bg="skyblue",bd=2,cursor="hand2").place(x=10,y=400,width=100,height=40)
        btn_update=Button(product_Frame,command=self.update,text="Update",font=("goudy old style",20,"bold"),bg="skyblue",bd=2,cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_delete=Button(product_Frame,command=self.delete,text="Delete",font=("goudy old style",20,"bold"),bg="skyblue",bd=2,cursor="hand2").place(x=230,y=400,width=100,height=40)
        btn_clear=Button(product_Frame,command=self.clear,text="Clear",font=("goudy old style",20,"bold"),bg="skyblue",bd=2,cursor="hand2").place(x=340,y=400,width=100,height=40)
        
        # --------------- search frame ------------
        SearchFrame=LabelFrame(self.root,text="Search Product",font=("goudy old style",15,"bold"),fg="white",bg="#1FB2F7")
        SearchFrame.place(x=480,y=10,width=600,height=80)

              # options
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_SearchBy, values=("Select","P_Id","Name","Category","Supplier","Price"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)
        
        txt_search=Entry(SearchFrame,textvariable=self.var_SearchTxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15,"bold"),bg="#A3E958",bd=2,cursor="hand2").place(x=410,y=9,width=150,height=30)
       
        # -------------- Product details --------
        Prod_frame=Frame(self.root,bd=3,relief=RIDGE)
        Prod_frame.place(x=480,y=100,width=600,height=390)
        
        scrolly=Scrollbar(Prod_frame,orient=VERTICAL)
        scrollx=Scrollbar(Prod_frame,orient=HORIZONTAL)
        
        self.ProductTable=ttk.Treeview(Prod_frame,columns=("P_Id","Name","Category","Supplier","Price","Description","Quantity","Availability"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)
        
        self.ProductTable.heading("P_Id",text="Prod. ID")
        self.ProductTable.heading("Name",text="Prod. Name")
        self.ProductTable.heading("Category",text="Category")
        self.ProductTable.heading("Supplier",text="Supplier")
        self.ProductTable.heading("Price",text="Price")
        self.ProductTable.heading("Description",text="Description")
        self.ProductTable.heading("Quantity",text="Quantity")
        self.ProductTable.heading("Availability",text="Availability")
        
        self.ProductTable["show"]="headings"
        
        self.ProductTable.column("P_Id",width=50)
        self.ProductTable.column("Name",width=150)
        self.ProductTable.column("Category",width=120)
        self.ProductTable.column("Supplier",width=100)
        self.ProductTable.column("Price",width=100)
        self.ProductTable.column("Description",width=200)
        self.ProductTable.column("Quantity",width=50)
        self.ProductTable.column("Availability",width=100)
        self.ProductTable.pack(fill=BOTH,expand=1)
        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
    
        
    
    
        
    # =======================================
    
    
    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            cur.execute("Select name from Category")
            cat=cur.fetchall()
            
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])
                    
            
            cur.execute("Select name from Supplier")
            sup=cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])    
        
        
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")    
         
    
    
    def add(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        
        
        try:
            if self.var_p_category.get()=="Select" or self.var_p_category.get()=="Empty" or self.var_p_Supplier.get()=="Select" or self.var_p_name.get()==""  or self.var_p_price.get()=="" or  self.var_p_quantity.get()=="" or self.var_p_availability.get()=="Select":
                messagebox.showerror("Error",f"All Imput Fields Except Description Are Required Required",parent=self.root)
            else:
                cur.execute("Select * from Product where Name=?",(self.var_p_name.get(),))
                row=cur.fetchone()
                if row!= None:
                    messagebox.showerror("Error","This Product with same Name Already Exists, Try Different Product Name",parent=self.root)
                else:
                    cur.execute("Insert into Product(Name,Category,Supplier,Price,Description,Quantity,Availability)values(?,?,?,?,?,?,?)",(
                        # self.var_p_id.get(), 
                        self.var_p_name.get(), 
                        self.var_p_category.get(), 
                        self.var_p_Supplier.get(), 
                        self.var_p_price.get(),
                        self.var_p_description.get(),
                        self.var_p_quantity.get(),
                        self.var_p_availability.get(), 
                         
                     )) 
                    con.commit() 
                    messagebox.showinfo("Success","Product Added Successfully",parent=self.root)
                    self.show() 
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")    
    
    
    def show(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from Product")
            rows=cur.fetchall()
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('',END,values=row)
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
        
            
    def get_data(self,ev):
        f=self.ProductTable.focus()    
        content=(self.ProductTable.item(f))
        row=content['values']
        self.var_p_id.set(row[0]), 
        self.var_p_name.set(row[1]), 
        self.var_p_category.set(row[2]), 
        self.var_p_Supplier.set(row[3]), 
        self.var_p_price.set(row[4]),
        self.var_p_description.set(row[5]),
        self.var_p_quantity.set(row[6]),
        self.var_p_availability.set(row[7]),
        
        
        
         
    
    
    def update(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            if self.var_p_id.get()=="":
                messagebox.showerror("Error",f"Please Select Product From List",parent=self.root)
            else:
                cur.execute("Select * from Product where P_Id=?",(self.var_p_id.get(),))
                row=cur.fetchone()
                if row== None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    cur.execute("update Product set Name=?,Category=?,Supplier=?,Price=?,Description=?,Quantity=?,Availability=? where P_Id=?",(
                         
                         
                        self.var_p_name.get(), 
                        self.var_p_category.get(), 
                        self.var_p_Supplier.get(), 
                        self.var_p_price.get(),
                        self.var_p_description.get(),
                        self.var_p_quantity.get(),
                        self.var_p_availability.get(),
                        self.var_p_id.get(),
                     )) 
                    con.commit() 
                    messagebox.showinfo("Success","Product Updated Successfully",parent=self.root)
                    self.show() 
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")    
    
    def delete(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            if self.var_p_id.get()=="":
                messagebox.showerror("Error",f"Select Product From The List ",parent=self.root)
            else:
                cur.execute("Select * from Product where P_Id=?",(self.var_p_id.get(),))
                row=cur.fetchone()
                if row== None:
                    messagebox.showerror("Error","Invalid Product ",parent=self.root)
                else:
                    confirmation_msg=messagebox.askyesno("Confirm Operation","Are you Sure you Want to Delete Product?",parent=self.root)
                    if confirmation_msg==True:
                        
                        cur.execute("delete from Product where P_Id=?",(self.var_p_id.get(),))
                        con.commit() 
                        messagebox.showinfo("Delete","Product Deleted Successfully",parent=self.root)

                        self.clear()       
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root)    
    
    def clear(self):
        self.var_p_id.set("")
        self.var_p_name.set("") 
        self.var_p_category.set("Select") 
        self.var_p_Supplier.set("Select")
        self.var_p_price.set("")
        self.var_p_description.set("")
        self.var_p_quantity.set("")
        self.var_p_availability.set("Select")
        
        
        self.var_SearchTxt.set("")
        self.var_SearchBy.set("Select")
        self.show()
    
    
    def search(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            if self.var_SearchBy.get()=="Select":
                messagebox.showerror("Error","Select Search By option",parent=self.root)
            elif self.var_SearchTxt.get()=="":
                messagebox.showerror("Error","Search Input Required",parent=self.root) 
            else:      
                cur.execute("Select * from Product where "+self.var_SearchBy.get()+" LIKE '%"+ self.var_SearchTxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.ProductTable.delete(*self.ProductTable.get_children())
                    for row in rows:
                        self.ProductTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No Record Found",parent=self.root) 
        
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root)     
        
        
        
        
        
        
        
        
        # ------------------------------------------------------------------------
if __name__=="__main__":       
    root=Tk() 
    obj=ProductClass(root) 
    root.mainloop()