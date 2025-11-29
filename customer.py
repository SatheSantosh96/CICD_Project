from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
 
class CustomerClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+250+140")
        self.root.config(bg="#A3E958")
        self.root.title("S_MART- The Supermarket Billing System   |  by Santosh & Dheeraj")
        self.root.focus_force()
        # =white
        #  all variables
        self.var_SearchBy= StringVar()
        self.var_SearchTxt= StringVar()
        
        self.var_custId= StringVar()
        self.var_custName= StringVar()
        self.var_custContact= StringVar()
        self.var_custAddress= StringVar()
        self.var_custDob= StringVar()
        self.var_custEmail= StringVar()
        
         
        

        # --------------- search frame ------------
        SearchFrame=LabelFrame(self.root,text="Search Customer",font=("goudy old style",15,"bold"),fg="white",bg="#1FB2F7")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        # options
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_SearchBy, values=("Select","cust_id","Name","Contact","Email"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)
        
        txt_search=Entry(SearchFrame,textvariable=self.var_SearchTxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15,"bold"),bg="#A3E958",bd=2,cursor="hand2").place(x=410,y=9,width=150,height=30)

    #   ---------- title-----
        title=Label(self.root,text="Customer Details",font=("goudy old style",20,"bold"),bg="gray",fg="white").place(x=50,y=100,width=1000)
       
        # ====== content =====
       
        # ---------- ROW 1 -----------
        lbl_custid=Label(self.root,text="ID",font=("goudy old style",15,"bold"),bg="#1FB2F7",fg="white",padx=4,pady=4).place(x=50,y=150,width=90)
        lbl_custname=Label(self.root,text="Name",font=("goudy old style",15,"bold"),bg="#1FB2F7",fg="white",padx=4,pady=4).place(x=390,y=150,width=90)
        lbl_contact=Label(self.root,text="Mobile No.",font=("goudy old style",15,"bold"),bg="#1FB2F7",fg="white",padx=4,pady=4).place(x=750,y=150,width=90)
        
        
        
        txt_custid=Entry(self.root,textvariable=self.var_custId,font=("goudy old style",20),bg="lightyellow").place(x=150,y=150,width=180)
        
        txt_custname=Entry(self.root,textvariable=self.var_custName,font=("goudy old style",20),bg="lightyellow").place(x=500,y=150,width=180)
        
        txt_contact=Entry(self.root,textvariable=self.var_custContact,font=("goudy old style",20),bg="lightyellow").place(x=850,y=150,width=180)
        
        # ---------- ROW 2----------
        
        lbl_Address=Label(self.root,text="Address",font=("goudy old style",15,"bold"),bg="#1FB2F7",fg="white",padx=4,pady=4).place(x=50,y=210,width=90)
        lbl_Dob=Label(self.root,text="D.O.B",font=("goudy old style",15,"bold"),bg="#1FB2F7",fg="white",padx=4,pady=4).place(x=420,y=210,width=90)
        lbl_Email=Label(self.root,text="E-Mail",font=("goudy old style",15,"bold"),bg="#1FB2F7",fg="white",padx=4,pady=4).place(x=750,y=210,width=90)
        
        self.txt_Address=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_Address.place(x=150,y=210,width=250 ,height=100)
        txt_Dob=Entry(self.root,textvariable=self.var_custDob,font=("goudy old style",20),bg="lightyellow").place(x=530,y=210,width=150)
        txt_Email=Entry(self.root,textvariable=self.var_custEmail,font=("goudy old style",20),bg="lightyellow").place(x=850,y=210,width=180)
        
        # ========== buttons==========
        
        btn_add=Button(self.root,command=self.add,text="Save",font=("goudy old style",20,"bold"),bg="skyblue",bd=2,cursor="hand2").place(x=420,y=270,width=120,height=40)
        btn_update=Button(self.root,command=self.update,text="Update",font=("goudy old style",20,"bold"),bg="skyblue",bd=2,cursor="hand2").place(x=570,y=270,width=120,height=40)
        btn_delete=Button(self.root,command=self.delete,text="Delete",font=("goudy old style",20,"bold"),bg="skyblue",bd=2,cursor="hand2").place(x=720,y=270,width=120,height=40)
        btn_clear=Button(self.root,command=self.clear,text="Clear",font=("goudy old style",20,"bold"),bg="skyblue",bd=2,cursor="hand2").place(x=870,y=270,width=120,height=40)
        
        
        # -------------- customer details --------
        cust_frame=Frame(self.root,bd=3,relief=RIDGE)
        cust_frame.place(x=0,y=320,relwidth=1,height=170)
        
        scrolly=Scrollbar(cust_frame,orient=VERTICAL)
        scrollx=Scrollbar(cust_frame,orient=HORIZONTAL)
        
        self.CustomerTable=ttk.Treeview(cust_frame,columns=("cust_id","name","contact","address","dob","email"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CustomerTable.xview)
        scrolly.config(command=self.CustomerTable.yview)
        
        self.CustomerTable.heading("cust_id",text="Cust. ID")
        self.CustomerTable.heading("name",text="Cust. Name")
        self.CustomerTable.heading("contact",text="Mobile No.")
        self.CustomerTable.heading("address",text="Address")
        self.CustomerTable.heading("dob",text="D.O.B")
        self.CustomerTable.heading("email",text="E-Mail")
        self.CustomerTable["show"]="headings"
        
        self.CustomerTable.column("cust_id",width=50)
        self.CustomerTable.column("name",width=200)
        self.CustomerTable.column("contact",width=150)
        self.CustomerTable.column("address",width=400)
        self.CustomerTable.column("dob",width=120)
        self.CustomerTable.column("email",width=250)
        self.CustomerTable.pack(fill=BOTH,expand=1)
        self.CustomerTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
    # =======================================
    
    def add(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            if self.var_custId.get()=="":
                messagebox.showerror("Error",f"Customer Id Must Be Required",parent=self.root)
            else:
                cur.execute("Select * from customer where cust_id=?",(self.var_custId.get(),))
                row=cur.fetchone()
                if row!= None:
                    messagebox.showerror("Error","This Customer Id is Already Assigned, Try Different Id",parent=self.root)
                else:
                    cur.execute("Insert into customer(cust_id,name,contact,address,dob,email)values(?,?,?,?,?,?)",(
                        self.var_custId.get(), 
                        self.var_custName.get(), 
                        self.var_custContact.get(), 
                        self.txt_Address.get('1.0',END), 
                        self.var_custDob.get(), 
                        self.var_custEmail.get(), 
                         
                     )) 
                    con.commit() 
                    messagebox.showinfo("Success","Customer Added Successfully",parent=self.root)
                    self.show() 
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")    
    
    
    def show(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from customer")
            rows=cur.fetchall()
            self.CustomerTable.delete(*self.CustomerTable.get_children())
            for row in rows:
                self.CustomerTable.insert('',END,values=row)
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
        
            
    def get_data(self,ev):
        f=self.CustomerTable.focus()    
        content=(self.CustomerTable.item(f))
        row=content['values']
        # print(row)
        self.var_custId.set(row[0]) 
        self.var_custName.set(row[1]) 
        self.var_custContact.set(row[2]) 
        self.txt_Address.delete('1.0',END)
        self.txt_Address.insert(END,row[3]) 
        self.var_custDob.set(row[4]) 
        self.var_custEmail.set(row[5]) 
    
    
    def update(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            if self.var_custId.get()=="":
                messagebox.showerror("Error",f"Customer Id Must Be Required",parent=self.root)
            else:
                cur.execute("Select * from customer where cust_id=?",(self.var_custId.get(),))
                row=cur.fetchone()
                if row== None:
                    messagebox.showerror("Error","Invalid Customer ID",parent=self.root)
                else:
                    cur.execute("update customer set name=?,contact=?,address=?,dob=?,email=? where cust_id=?",(
                         
                        self.var_custName.get(), 
                        self.var_custContact.get(), 
                        self.txt_Address.get('1.0',END), 
                        self.var_custDob.get(), 
                        self.var_custEmail.get(),
                        self.var_custId.get() 
                         
                     )) 
                    con.commit() 
                    messagebox.showinfo("Success","Customer Updated Successfully",parent=self.root)
                    self.show() 
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")    
    
    def delete(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            if self.var_custId.get()=="":
                messagebox.showerror("Error",f"Customer Id Must Be Required",parent=self.root)
            else:
                cur.execute("Select * from customer where cust_id=?",(self.var_custId.get(),))
                row=cur.fetchone()
                if row== None:
                    messagebox.showerror("Error","Invalid Customer ID",parent=self.root)
                else:
                    confirmation_msg=messagebox.askyesno("Confirm Operation","Are you Sure you Want to Delete Customer",parent=self.root)
                    if confirmation_msg==True:
                        
                        cur.execute("delete from customer where cust_id=?",(self.var_custId.get(),))
                        con.commit() 
                        messagebox.showinfo("Delete","Customer Deleted Successfully",parent=self.root)

                        self.clear()       
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root)    
    
    def clear(self):
        self.var_custId.set("") 
        self.var_custName.set("") 
        self.var_custContact.set("") 
        self.txt_Address.delete('1.0',END)
        self.txt_Address.insert(END,"") 
        self.var_custDob.set("") 
        self.var_custEmail.set("")
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
                cur.execute("Select * from customer where "+self.var_SearchBy.get()+" LIKE '%"+ self.var_SearchTxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.CustomerTable.delete(*self.CustomerTable.get_children())
                    for row in rows:
                        self.CustomerTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No Record Found",parent=self.root) 
        
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root) 
        
        
        
            



# ------------------------------------------------------------------------
if __name__=="__main__":       
    root=Tk() 
    obj=CustomerClass(root) 
    root.mainloop()  