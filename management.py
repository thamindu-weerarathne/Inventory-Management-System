import pymysql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk

def connection():
    conn = pymysql.connect(
        host='localhost', user='root', password='', db='products_db'
    )
    return conn

def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)

    for array in read():
        my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="o row")

    my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))
    my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=10, pady=20)

# GUI setup
root = Tk()
root.title("Inventory Management System")
root.geometry("1080x720")
my_tree = ttk.Treeview(root)

def read():
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    results = cursor.fetchall()
    conn.close()
    return results

def add():
    productid = productidEntry.get().strip()
    productname = productnameEntry.get().strip()
    productquantity = productquantityEntry.get().strip()
    productprice = productpriceEntry.get().strip()

    if not productid or not productname or not productquantity or not productprice:
        messagebox.showinfo("Error", "Please fill up the blank entry")
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO inventory VALUES (%s, %s, %s, %s)", 
                           (productid, productname, productquantity, productprice))
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showinfo("Error", f"An error occurred: {e}")
            return
        
        refreshTable()

def delete():
    decision = messagebox.askquestion("Warning!!", "Delete the selected data?")
    if decision != "yes":
        return
    else:
        selected_item = my_tree.selection()[0]
        deleteData = str(my_tree.item(selected_item)['values'][0])
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM inventory WHERE id=%s", (deleteData,))
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showinfo("Error", f"An error occurred: {e}")
            return
        
        refreshTable()

def reset():
    decision = messagebox.askquestion("Warning!!", "Delete all data?")
    if decision != "yes":
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM inventory")
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showinfo("Error", f"An error occurred: {e}")
            return
        
        refreshTable()

def update():
    selectedid = ""
    try:
        selected_item = my_tree.selection()[0]
        selectedid = str(my_tree.item(selected_item)['values'][0])
    except:
        messagebox.showinfo("Error", "Please select a data")
        return

    productid = str(productidEntry.get())
    productname = str(productnameEntry.get())
    productquantity = str(productquantityEntry.get())
    productprice = str(productpriceEntry.get())

    if not productid or not productname or not productquantity or not productprice:
        messagebox.showinfo("Error", "Please fill up the blank entry")
        return
    else:
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE inventory SET id=%s, name=%s, quantity=%s, price=%s WHERE id=%s", 
                           (productid, productname, productquantity, productprice, selectedid))
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showinfo("Error", f"An error occurred: {e}")
            return
        
        refreshTable()

# GUI labels
label = Label(root, text="Inventory Management System", font=('Arial Bold', 30))
label.grid(row=0, column=0, columnspan=8, rowspan=2, padx=50, pady=40)

productidLabel = Label(root, text="Product ID", font=('Arial', 15))
productnameLabel = Label(root, text="Name", font=('Arial', 15))
productquantityLabel = Label(root, text="Quantity", font=('Arial', 15))
productpriceLabel = Label(root, text="Price", font=('Arial', 15))

productidLabel.grid(row=3, column=0, columnspan=1, padx=50, pady=5)
productnameLabel.grid(row=4, column=0, columnspan=1, padx=50, pady=5)
productquantityLabel.grid(row=5, column=0, columnspan=1, padx=50, pady=5)
productpriceLabel.grid(row=6, column=0, columnspan=1, padx=50, pady=5)

# Entry fields
productidEntry = Entry(root, width=55, bd=5, font=('Arial', 15))
productnameEntry = Entry(root, width=55, bd=5, font=('Arial', 15))
productquantityEntry = Entry(root, width=55, bd=5, font=('Arial', 15))
productpriceEntry = Entry(root, width=55, bd=5, font=('Arial', 15))

productidEntry.grid(row=3, column=1, columnspan=4, padx=5, pady=0)
productnameEntry.grid(row=4, column=1, columnspan=4, padx=5, pady=0)
productquantityEntry.grid(row=5, column=1, columnspan=4, padx=5, pady=0)
productpriceEntry.grid(row=6, column=1, columnspan=4, padx=5, pady=0)

# Buttons
addBtn = Button(root, text="Add", padx=65, pady=25, width=10, bd=5, font=('Arial', 15), bg="#84F894", command=add)
deleteBtn = Button(root, text="Delete", padx=65, pady=25, width=10, bd=5, font=('Arial', 15), bg="#84F894", command=delete)
updateBtn = Button(root, text="Update", padx=65, pady=25, width=10, bd=5, font=('Arial', 15), bg="#84F894", command=update)
resetBtn = Button(root, text="Reset", padx=65, pady=25, width=10, bd=5, font=('Arial', 15), bg="#84F894", command=reset)
exitBtn = Button(root, text="Exit", padx=65, pady=25, width=10, bd=5, font=('Arial', 15), bg="#84F894", command=root.quit)

addBtn.grid(row=3, column=5, columnspan=1, rowspan=2)
deleteBtn.grid(row=5, column=5, columnspan=1, rowspan=2)
updateBtn.grid(row=7, column=5, columnspan=1, rowspan=2)
resetBtn.grid(row=9, column=5, columnspan=1, rowspan=2)
exitBtn.grid(row=11, column=5, columnspan=1, rowspan=2)

# Treeview styling
style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial Bold', 15))
my_tree['columns'] = ("Product ID", "Name", "Quantity", "Price")

my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Product ID", anchor=W, width=170)
my_tree.column("Name", anchor=W, width=170)
my_tree.column("Quantity", anchor=W, width=170)
my_tree.column("Price", anchor=W, width=170)

my_tree.heading("Product ID", text="Product ID", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("Quantity", text="Quantity", anchor=W)
my_tree.heading("Price", text="Price", anchor=W)

refreshTable()

root.mainloop()