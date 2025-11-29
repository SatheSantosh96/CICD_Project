from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import os 
 
class SalesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+250+140")
        self.root.config(bg="White")
        self.root.title("S_MART- The Supermarket Billing System   |  by Santosh & Dheeraj")
        self.root.focus_force()
        # ====== Variables =========
        self.bill_list=[]
        self.var_bill_no=StringVar()


         # ===== title ======
        lbl_title=Label(self.root,text="View Customer Bills ",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        
        lbl_bill_no=Label(self.root,text="Bill No. ",font=("times new roman",15),bg="white").place(x=50,y=100)
        txt_bill_no=Entry(self.root,textvariable=self.var_bill_no,font=("times new roman",15),bg="lightyellow").place(x=160,y=100,width=180,height=28)
        
        btn_search=Button(self.root,text="Search",command=self.search,font=("times new roman",15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=360,y=100,width=120,height=28)

        btn_Clear=Button(self.root,text="Clear",command=self.clear,font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=490,y=100,width=120,height=28)
        
        # ======== Bill List +============
        Sales_Frame=Frame(self.root,bd=3,relief=RIDGE)
        Sales_Frame.place(x=30,y=140,width=200,height=330)
        
        scrolly=Scrollbar(Sales_Frame,orient=VERTICAL)
        
        self.Sales_List=Listbox(Sales_Frame,font=("goudy old style",15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH,expand=1)
        self.Sales_List.bind("<ButtonRelease-1>",self.get_data)
        
        # =====Bill Area =====
        bill_Frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_Frame.place(x=280,y=140,width=410,height=330)
        
        lbl_title2=Label(bill_Frame,text="Customer Bill Area ",font=("goudy old style",20),bg="orange").pack(side=TOP,fill=X)
        
        
        scrolly2=Scrollbar(bill_Frame,orient=VERTICAL)
        
        self.Bill_Area=Text(bill_Frame,bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.Bill_Area.yview)
        self.Bill_Area.pack(fill=BOTH,expand=1)
        
        # ======image=====
        self.bill_photo=Image.open("images/bill1.png")
        self.bill_photo=self.bill_photo.resize((450,300),Image.LANCZOS)
        self.bill_photo=ImageTk.PhotoImage(self.bill_photo)
        
        lbl_image=Label(self.root,image=self.bill_photo,bd=0)
        lbl_image.place(x=700,y=110)
        self.show()
        
        # ======================================================================
    def show(self):
        del self.bill_list[:]
        self.Sales_List.delete(0,END)
        # print(os.listdir('bill'))
        for i in os.listdir('bill'):
            # print(i.split('.'),i.split('.') [-1])
            if i.split('.')[-1]=='txt':
                self.Sales_List.insert(END,i)
                self.bill_list.append(i.split('.')[0])


    def get_data(self,ev):
        index_ =self.Sales_List.curselection()
        file_name=self.Sales_List.get(index_)
        print(file_name)
        self.Bill_Area.delete('1.0',END)
        fp=open(f'bill/{file_name}','r')
        for i in fp:
            self.Bill_Area.insert(END,i) 
        fp.close()

    def search(self):
        if self.var_bill_no.get()=="":
            messagebox.showerror("Error","Bill No. is Required",parent=self.root)
        else:
            if self.var_bill_no.get() in self.bill_list:
            
                fp=open(f'bill/{self.var_bill_no.get()}.txt','r')
                self.Bill_Area.delete('1.0',END)
                for i in fp:
                    self.Bill_Area.insert(END,i) 
            
                fp.close()
            else:
                 messagebox.showerror("Error","Invalid Bill No",parent=self.root)   
                
    def clear(self):
        self.show()
        self.Bill_Area.delete('1.0',END)
        self.var_bill_no.set("") 
        self.show()                  
        



        # ------------------------------------------------------------------------
if __name__=="__main__":       
    root=Tk() 
    obj=SalesClass(root) 
    root.mainloop()