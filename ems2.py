#Task 4 :-- Employee Management System



from tkinter import *
from tkinter.scrolledtext import *
from tkinter.messagebox import *
from sqlite3 import *
import matplotlib.pyplot as plt
import requests



#EMS Window
root = Tk()
root.title("Employee Management System")
root.geometry("1000x700+50+50")
f = ("Times New Roman", 24, "bold")
root.configure(bg='#03fcad')
ems_lab = Label(root, text="Employee Management System", font=("Times New Roman",28,"bold"),bg="#03fcad").pack(pady=10)


def f1():
    add_window.deiconify()
    root.withdraw()


def f2():
    root.deiconify()
    add_window.withdraw()


def f3():
    view_window.deiconify()
    root.withdraw()
    vw_st_data.delete(1.0, END)
    info = ""
    con = None
    try:
        con = connect("prj.db")
        cursor = con.cursor()
        sql = "select * from employee"
        cursor.execute(sql)
        data = cursor.fetchall()
        for d in data:
            info = info + "id: " + str(d[0]) + "   name: " + str(d[1]) + "   salary: " + str(d[2]) + "\n"
        vw_st_data.insert(INSERT, info)
    except Exception as e:
        showerror("Issue", e)
    finally:
        if con is None:
            con.close()


def f4():
    root.deiconify()
    view_window.withdraw()


def f5():
    update_window.deiconify()
    root.withdraw()


def f6():
    root.deiconify()
    update_window.withdraw()


def f7():
    delete_window.deiconify()
    root.withdraw()


def f8():
    root.deiconify()
    delete_window.withdraw()


def validate_name(name):
    if name == "" or name.strip() == "":
        showerror("ERROR", "Name can't be empty.")
        return False
    elif not name.isalpha():
        showerror("ERROR", "Invalid Name. Please enter alphabetic characters only.")
        return False
    return True


def validate_id(id):
    if id == "":
        showerror("ERROR", "Id can't be empty.")
        return False
    try:
        int(id)
    except ValueError:
        showerror("ERROR", "Invalid Id. Please enter numeric characters only.")
        return False
    return True


def validate_salary(salary):
    if salary == "":
        showerror("ERROR", "Salary can't be empty.")
        return False
    try:
        float(salary)
    except ValueError:
        showerror("ERROR", "Invalid Salary. Please enter numeric characters only.")
        return False
    return True


def f9():
    con = None
    try:
        con = connect("prj.db")
        cursor = con.cursor()
        sql = "insert into employee values('%d','%s','%s')"
        id = aw_ent_id.get()
        name = aw_ent_name.get()
        salary = aw_ent_salary.get()

        if not validate_id(id):
            aw_ent_id.delete(0,END)
            aw_ent_id.focus() 
            return
        elif not validate_name(name):
            aw_ent_name.delete(0,END)
            aw_ent_name.focus()
            return
        elif not validate_salary(salary):
            aw_ent_salary.delete(0,END)
            aw_ent_salary.focus()
            return
        cursor.execute(sql % (int(id), name, salary))
        con.commit()
        showinfo("Success", "Record added.")
    except Exception as e:
        showerror("Issue", e)
        con.rollback()
    finally:
        if con is not None:
            con.close()
    aw_ent_id.delete(0,END)
    aw_ent_name.delete(0,END)
    aw_ent_salary.delete(0,END)
    aw_ent_id.focus() 

def f10():
    con = None
    try:
        con = connect("prj.db")
        cursor = con.cursor()
        sql = "update employee set name = '%s', salary = '%s' where id = '%d'"
        id = uw_ent_id.get()
        name = uw_ent_name.get()
        salary = uw_ent_salary.get()

        if not validate_id(id):
            uw_ent_id.delete(0, END)
            uw_ent_id.focus()
            return
        elif not validate_name(name):
            uw_ent_name.delete(0, END)
            uw_ent_name.focus()
            return
        elif not validate_salary(salary):
            uw_ent_salary.delete(0,END)
            uw_ent_salary.focus()
            return
        cursor.execute(sql % (name, salary, int(id)))
        if cursor.rowcount == 1:
            con.commit()
            showinfo("Success", "Record updated.")
        else:
            showerror("Invalid", f"Employee with id {id} does not exist.")
    except Exception as e:
        showerror("Issue", e)
    finally:
        if con is not None:
            con.close()
    uw_ent_id.delete(0, END)
    uw_ent_name.delete(0, END)
    uw_ent_salary.delete(0,END)
    uw_ent_id.focus()


def f11():
    con = None
    try:
        con = connect("prj.db")
        cursor = con.cursor()
        sql = "delete from employee where id = '%d'"
        id = dw_ent_id.get()

        if not validate_id(id):
            dw_ent_id.delete(0,END)
            dw_ent_id.focus()
            return

        cursor.execute(sql % int(id))
        if cursor.rowcount == 1:
            showinfo('Success', 'Record deleted.')
            con.commit()
        else:
            showerror("Invalid", f"Employee with id {id} does not exist.")
    except Exception as e:
        showerror("Issue", e)
        con.rollback()
    finally:
        if con is not None:
            con.close()
    dw_ent_id.delete(0,END)
    dw_ent_id.focus()


def f12():
    con = None
    try:
        con = connect("prj.db")
        cursor = con.cursor()
        sql = "SELECT * FROM employee ORDER BY salary DESC LIMIT 5"
        cursor.execute(sql)
        data = cursor.fetchall()
        
        if len(data) == 0:
            showinfo('No Data', 'No employee data found.')
            return

        name = []
        salary = []
        for d in data:
            name.append(d[1])
            salary.append(d[2])
        
        plt.bar(name, salary, linewidth=4, color=['red', 'green', 'blue'])
        plt.title("Top 5 Highest Salary Employees")
        plt.xlabel("Names")
        plt.ylabel("Salaries")
        plt.show()
    except Exception as e:
        showerror('Issue', e)
    finally:
        if con is not None:
            con.close()


def close():
    if askyesnocancel("Quit", "Do you want to exit?"):
        root.destroy()
root.protocol("WM_DELETE_WINDOW", close)




#EMS window
btn_add = Button(root, text="Add", font=f, width=20, fg="black", command=f1)
btn_view = Button(root, text="View", font=f, width=20, fg="black", command=f3)
btn_update = Button(root, text="Update", font=f, width=20, fg="black", command=f5)
btn_delete = Button(root, text="Delete", font=f, width=20, fg="black", command=f7)
btn_charts = Button(root, text="Charts", font=f, fg="black", width=20,  command=f12)


btn_add.place(x=305,y=100)
btn_view.place(x=305,y=175)
btn_update.place(x=305,y=250)
btn_delete.place(x=305,y=325)
btn_charts.place(x=305,y=400)

response = requests.get("https://ipapi.co/json/")
if response.status_code == 200:
    location_data = response.json()
    city = location_data['city']
    region = location_data['region']
    country = location_data['country_name']
    location_text = f"Location: {city}, {region}, {country}"
    lbl_loc = Label(root, text=location_text, font=("Times New Roman",20,"bold"), bg="#03fcad")
    lbl_loc.place(x=50, y=500)
    api_key = "8379921d15b15d6b556e72d8ea3ba8c9"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric"
    weather_response = requests.get(weather_url)
    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        temperature = weather_data['main']['temp']
        temp_text = f"Temperature: {temperature}°C"
        lbl_temp = Label(root, text=temp_text,font=("Times New Roman",20,"bold"), bg="#03fcad")
        lbl_temp.place(x=50, y=550)

#ADD window
add_window = Toplevel(root)
add_window.title("Add Employee")
add_window.geometry("800x800+400+100")
add_window.configure(bg='lightblue')

aw_lbl_id = Label(add_window, text="Enter id", font=f,bg='lightblue')
aw_ent_id = Entry(add_window, bd=4, width=18, font=f)
aw_lbl_name = Label(add_window, text="Enter name", font=f,bg='lightblue')
aw_ent_name = Entry(add_window, bd=4, width=18, font=f)
aw_lbl_salary = Label(add_window, text="Enter salary", font=f,bg='lightblue')
aw_ent_salary = Entry(add_window, bd=4, width=18, font=f)
aw_btn_save = Button(add_window, text="Save", font=f,  command=f9)
aw_btn_back = Button(add_window, text="Back", font=f,  command=f2)
add_lab = Label(add_window, text="Add Employee", font=("Times New Roman", 28,"bold"), bg="lightblue").pack(pady=10)

aw_lbl_id.pack(pady=10)
aw_ent_id.pack(pady=10)
aw_lbl_name.pack(pady=10)
aw_ent_name.pack(pady=10)
aw_lbl_salary.pack(pady=10)
aw_ent_salary.pack(pady=10)
aw_btn_save.pack(pady=10)
aw_btn_back.pack(pady=10)

add_window.withdraw()
add_window.protocol("WM_DELETE_WINDOW", close)


#View window
view_window = Toplevel(root)
view_window.title("View Employee")
view_window.geometry("800x800+400+100")
view_window.configure(bg='lightyellow')
vw_st_data = ScrolledText(view_window, width=40, height=10, font=f)
btn_back = Button(view_window, text="Back", font=f, command=f4)

vw_st_data.pack()
btn_back.pack(pady=50)

view_window.withdraw()
view_window.protocol("WM_DELETE_WINDOW", close)



#Update Window
update_window = Toplevel(root)
update_window.title("Update Employee")
update_window.geometry("800x800+400+100")
update_window.configure(bg='lightsalmon')

lbl_id = Label(update_window, text="Enter id", font=f,bg='lightsalmon')
uw_ent_id = Entry(update_window, bd=4, width=20, font=f,)
lbl_name = Label(update_window, text="Enter name", font=f,bg='lightsalmon')
uw_ent_name = Entry(update_window, bd=4, width=20, font=f)
lbl_salary = Label(update_window, text="Enter salary", font=f,bg='lightsalmon')
uw_ent_salary = Entry(update_window, bd=4, width=20, font=f)
btn_save = Button(update_window, text="Save", font=f, command=f10)
btn_back = Button(update_window, text="Back", font=f,  command=f6)
upt_lab = Label(update_window, text="Update Employee", font=("Times New Roman", 28, "bold"), bg="lightsalmon").pack(pady=10)

lbl_id.pack(pady=10)
uw_ent_id.pack(pady=10)
lbl_name.pack(pady=10)
uw_ent_name.pack(pady=10)
lbl_salary.pack(pady=10)
uw_ent_salary.pack(pady=10)
btn_save.pack(pady=10)
btn_back.pack(pady=10)

update_window.withdraw()
update_window.protocol("WM_DELETE_WINDOW", close)



#Delete Window
delete_window = Toplevel(root)
delete_window.title("Delete Employee")
delete_window.geometry("800x800+400+100")
delete_window.configure(bg='lightpink')

lbl_id = Label(delete_window, text="Enter id", font=f,bg='lightpink')
dw_ent_id = Entry(delete_window, bd=4, width=20, font=f)
btn_save = Button(delete_window, text="Delete", font=f ,command=f11)
btn_back = Button(delete_window, text="Back", font=f, command=f8)
delete_lab = Label(delete_window, text="Delete Employee", font=("Times New Roman",28,"bold"), bg="lightpink").pack(pady=10)

lbl_id.pack(pady=20)
dw_ent_id.pack(pady=20)
btn_save.pack(pady=20)
btn_back.pack(pady=20)
delete_window.withdraw()
delete_window.protocol("WM_DELETE_WINDOW", close)

root.mainloop()