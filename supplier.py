from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
 
class SupplierClass:
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
        
        self.var_sup_id= StringVar()
        self.var_sup_name= StringVar()
        self.var_sup_contact= StringVar()
        self.var_sup_Address= StringVar()
        self.var_sup_Description= StringVar()
        self.var_sup_Email= StringVar()
        
         
        

        # --------------- search frame ------------
        SearchFrame=LabelFrame(self.root,text="Search Supplier",font=("goudy old style",15,"bold"),fg="white",bg="#1FB2F7")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        # options
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_SearchBy, values=("Select","sup_id","Name","Contact","Email"),state="readonly",justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)
        
        txt_search=Entry(SearchFrame,textvariable=self.var_SearchTxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15,"bold"),bg="#A3E958",bd=2,cursor="hand2").place(x=410,y=9,width=150,height=30)

    #   ---------- title-----
        title=Label(self.root,text="Supplier Details",font=("goudy old style",20,"bold"),bg="gray",fg="white").place(x=50,y=100,width=1000)
       
        # ====== content =====
       
        # ---------- ROW 1 -----------
        lbl_sup_id=Label(self.root,text="Supp. ID",font=("goudy old style",15,"bold"),bg="#1FB2F7",fg="white",padx=4,pady=4).place(x=50,y=150,width=100)
        
        lbl_sup_name=Label(self.root,text="Name",font=("goudy old style",15,"bold"),bg="#1FB2F7",fg="white",padx=4,pady=4).place(x=390,y=150,width=100)
        lbl_contact=Label(self.root,text="Mobile No.",font=("goudy old style",15,"bold"),bg="#1FB2F7",fg="white",padx=4,pady=4).place(x=730,y=150,width=100)
        
        
        txt_sup_id=Entry(self.root,textvariable=self.var_sup_id,font=("goudy old style",20),bg="lightyellow").place(x=170,y=150,width=180)
        
        
        txt_sup_name=Entry(self.root,textvariable=self.var_sup_name,font=("goudy old style",20),bg="lightyellow").place(x=510,y=150,width=180)
        
        txt_contact=Entry(self.root,textvariable=self.var_sup_contact,font=("goudy old style",20),bg="lightyellow").place(x=850,y=150,width=180)
        
        # ---------- ROW 2----------
        
        lbl_Address=Label(self.root,text="Address",font=("goudy old style",15,"bold"),bg="#1FB2F7",fg="white",padx=4,pady=4).place(x=50,y=210,width=100)
        lbl_Desc=Label(self.root,text="Description",font=("goudy old style",15,"bold"),bg="#1FB2F7",fg="white",padx=4,pady=4).place(x=390,y=210,width=100)
        lbl_Email=Label(self.root,text="E-Mail",font=("goudy old style",15,"bold"),bg="#1FB2F7",fg="white",padx=4,pady=4).place(x=730,y=210,width=100)
        
        self.txt_Address=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_Address.place(x=170,y=210,width=180 ,height=100)
        self.txt_Description=Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_Description.place(x=510,y=210,width=180,height=50)
        txt_Email=Entry(self.root,textvariable=self.var_sup_Email,font=("goudy old style",20),bg="lightyellow").place(x=850,y=210,width=180)
        
        # ========== buttons==========
        
        btn_add=Button(self.root,command=self.add,text="Save",font=("goudy old style",20,"bold"),bg="skyblue",bd=2,cursor="hand2").place(x=420,y=270,width=120,height=40)
        btn_update=Button(self.root,command=self.update,text="Update",font=("goudy old style",20,"bold"),bg="skyblue",bd=2,cursor="hand2").place(x=570,y=270,width=120,height=40)
        btn_delete=Button(self.root,command=self.delete,text="Delete",font=("goudy old style",20,"bold"),bg="skyblue",bd=2,cursor="hand2").place(x=720,y=270,width=120,height=40)
        btn_clear=Button(self.root,command=self.clear,text="Clear",font=("goudy old style",20,"bold"),bg="skyblue",bd=2,cursor="hand2").place(x=870,y=270,width=120,height=40)
        
        
        # -------------- supplier details --------
        cust_frame=Frame(self.root,bd=3,relief=RIDGE)
        cust_frame.place(x=0,y=320,relwidth=1,height=170)
        
        scrolly=Scrollbar(cust_frame,orient=VERTICAL)
        scrollx=Scrollbar(cust_frame,orient=HORIZONTAL)
        
        self.SuppierTable=ttk.Treeview(cust_frame,columns=("sup_id","name","contact","address","description","email"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.SuppierTable.xview)
        scrolly.config(command=self.SuppierTable.yview)
        
        self.SuppierTable.heading("sup_id",text="Supp. ID")
        self.SuppierTable.heading("name",text="Supp. Name")
        self.SuppierTable.heading("contact",text="Mobile No.")
        self.SuppierTable.heading("address",text="Address")
        self.SuppierTable.heading("description",text="Description")
        self.SuppierTable.heading("email",text="E-Mail")
        self.SuppierTable["show"]="headings"
        
        self.SuppierTable.column("sup_id",width=60)
        self.SuppierTable.column("name",width=200)
        self.SuppierTable.column("contact",width=150)
        self.SuppierTable.column("address",width=390)
        self.SuppierTable.column("description",width=120)
        self.SuppierTable.column("email",width=200)
        self.SuppierTable.pack(fill=BOTH,expand=1)
        self.SuppierTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
    # =======================================
    
    def add(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            if self.var_sup_id.get()=="":
                messagebox.showerror("Error",f"Supplier Id Must Be Required",parent=self.root)
            else:
                cur.execute("Select * from supplier where sup_id=?",(self.var_sup_id.get(),))
                row=cur.fetchone()
                if row!= None:
                    messagebox.showerror("Error","This Supplier Id is Already Assigned, Try Different Id",parent=self.root)
                else:
                    cur.execute("Insert into supplier(sup_id,name,contact,address,description,email)values(?,?,?,?,?,?)",(
                        self.var_sup_id.get(), 
                        self.var_sup_name.get(), 
                        self.var_sup_contact.get(), 
                        self.txt_Address.get('1.0',END), 
                        self.txt_Description.get('1.0',END), 
                        self.var_sup_Email.get(), 
                         
                     )) 
                    con.commit() 
                    messagebox.showinfo("Success","Supplier Added Successfully",parent=self.root)
                    self.show() 
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")    
    
    
    def show(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from supplier")
            rows=cur.fetchall()
            self.SuppierTable.delete(*self.SuppierTable.get_children())
            for row in rows:
                self.SuppierTable.insert('',END,values=row)
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
        
            
    def get_data(self,ev):
        f=self.SuppierTable.focus()    
        content=(self.SuppierTable.item(f))
        row=content['values']
        # print(row)
        self.var_sup_id.set(row[0]) 
        self.var_sup_name.set(row[1]) 
        self.var_sup_contact.set(row[2]) 
        self.txt_Address.delete('1.0',END)
        self.txt_Address.insert(END,row[3]) 
        self.txt_Description.delete('1.0',END)
        self.txt_Description.insert(END,row[4]) 
        self.var_sup_Email.set(row[5]) 
    
    
    def update(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            if self.var_sup_id.get()=="":
                messagebox.showerror("Error",f"supplier Id Must Be Required",parent=self.root)
            else:
                cur.execute("Select * from supplier where sup_id=?",(self.var_sup_id.get(),))
                row=cur.fetchone()
                if row== None:
                    messagebox.showerror("Error","Invalid supplier ID",parent=self.root)
                else:
                    cur.execute("update supplier set name=?,contact=?,address=?,description=?,email=? where sup_id=?",(
                         
                        self.var_sup_name.get(), 
                        self.var_sup_contact.get(), 
                        self.txt_Address.get('1.0',END), 
                        self.txt_Description.get('1.0',END), 
                        self.var_sup_Email.get(),
                        self.var_sup_id.get() 
                         
                     )) 
                    con.commit() 
                    messagebox.showinfo("Success","Supplier Updated Successfully",parent=self.root)
                    self.show() 
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")    
    
    def delete(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            if self.var_sup_id.get()=="":
                messagebox.showerror("Error",f"Supplier Id Must Be Required",parent=self.root)
            else:
                cur.execute("Select * from supplier where sup_id=?",(self.var_sup_id.get(),))
                row=cur.fetchone()
                if row== None:
                    messagebox.showerror("Error","Invalid Supplier ID",parent=self.root)
                else:
                    confirmation_msg=messagebox.askyesno("Confirm Operation","Are you Sure you Want to Delete Supplier",parent=self.root)
                    if confirmation_msg==True:
                        
                        cur.execute("delete from supplier where sup_id=?",(self.var_sup_id.get(),))
                        con.commit() 
                        messagebox.showinfo("Delete","Supplier Deleted Successfully",parent=self.root)

                        self.clear()       
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root)    
    
    def clear(self):
        self.var_sup_id.set("") 
        self.var_sup_name.set("") 
        self.var_sup_contact.set("") 
        self.txt_Address.delete('1.0',END)
        self.txt_Address.insert(END,"") 
        self.txt_Description.delete('1.0',END)
        self.txt_Description.insert(END,"")  
        self.var_sup_Email.set("")
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
                cur.execute("Select * from supplier where "+self.var_SearchBy.get()+" LIKE '%"+ self.var_SearchTxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.SuppierTable.delete(*self.SuppierTable.get_children())
                    for row in rows:
                        self.SuppierTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No Record Found",parent=self.root) 
        
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root) 
        
        
        
            



# ------------------------------------------------------------------------
if __name__=="__main__":       
    root=Tk() 
    obj=SupplierClass(root) 
    root.mainloop()  