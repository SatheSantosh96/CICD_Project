from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
 
class CategoryClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+250+140")
        self.root.config(bg="#A3E958")
        self.root.title("S_MART- The Supermarket Billing System   |  by Santosh & Dheeraj")
        self.root.focus_force()
        # ========= variables =======
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
        
        # ===== title ======
        lbl_title=Label(self.root,text="Manage Product Categories",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        
        lbl_name=Label(self.root,text="Enter Category Name",font=("goudy old style",30),bg="#1FB2F7",bd=2).place(x=50,y=80,width=350)
        
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",18),bg="lightyellow").place(x=50,y=150,width=300)
        
        btn_add=Button(self.root,text="ADD",command=self.add,font=("goudy old style",15),bg="green",fg="white",cursor="hand2").place(x=360,y=150,width=150,height=30)
        
        btn_delete=Button(self.root,command=self.delete,text="DELETE",font=("goudy old style",15),bg="red",fg="white",cursor="hand2").place(x=520,y=150,width=150,height=30)
        
        
        # ================ category details ========
        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=80,width=380,height=200)
        
        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)
        
        self.CategoryTable=ttk.Treeview(cat_frame,columns=("cat_id","name"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)
        
        self.CategoryTable.heading("cat_id",text="C. ID")
        self.CategoryTable.heading("name",text="category Name")
        
        self.CategoryTable["show"]="headings"
        
        self.CategoryTable.column("cat_id",width=100)
        self.CategoryTable.column("name",width=200)
        
        self.CategoryTable.pack(fill=BOTH,expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>",self.get_data)
        
        
        
        
        
        # ======= images ======
        self.img1=Image.open("images/category2.jpg")
        self.img1=self.img1.resize((620,270),Image.ANTIALIAS)
        self.img1=ImageTk.PhotoImage(self.img1)
        
        self.lbl_img1=Label(self.root,image=self.img1,bd=2,relief=RAISED)
        self.lbl_img1.place(x=50,y=200)
        
        # 
        self.img2=Image.open("images/category1.jpg")
        self.img2=self.img2.resize((375,170),Image.ANTIALIAS)
        self.img2=ImageTk.PhotoImage(self.img2)
        # (x=700,y=80,width=380,height=200)
        self.lbl_img2=Label(self.root,image=self.img2,bd=2,relief=RAISED)
        self.lbl_img2.place(x=700,y=300)
        
        self.show()
        
        # =========== functions ========
        
    def add(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error",f"Category Name Is Required",parent=self.root)
            else:
                cur.execute("Select * from category where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!= None:
                    messagebox.showerror("Error","This Category  is Already Exists, Try Different Category Name",parent=self.root)
                else:
                    cur.execute("Insert into category(name)values(?)",(
                    self.var_name.get(),)) 
                    con.commit() 
                    messagebox.showinfo("Success","Category Added Successfully",parent=self.root)
                    self.show() 
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")
        
        
    def show(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            cur.execute("Select * from category")
            rows=cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('',END,values=row)
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}")    
    
    
    def get_data(self,ev):
        f=self.CategoryTable.focus()    
        content=(self.CategoryTable.item(f))
        row=content['values']
        # print(row)
        self.var_cat_id.set(row[0]) 
        self.var_name.set(row[1])    
        
    
    def delete(self):
        con=sqlite3.connect(database='s_mart.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                messagebox.showerror("Error",f"Please Select Category from the list",parent=self.root)
            else:
                cur.execute("Select * from category where cat_id=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row== None:
                    messagebox.showerror("Error","Error,Please Try Again",parent=self.root)
                else:
                    confirmation_msg=messagebox.askyesno("Confirm Operation","Are you Sure you Want to Delete Category",parent=self.root)
                    if confirmation_msg==True:
                        
                        cur.execute("delete from category where cat_id=?",(self.var_cat_id.get(),))
                        con.commit() 
                        messagebox.showinfo("Delete","Category Deleted Successfully",parent=self.root)

                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")       
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}",parent=self.root)    
        
        # ------------------------------------------------------------------------
if __name__=="__main__":       
    root=Tk() 
    obj=CategoryClass(root) 
    root.mainloop()