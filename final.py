import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import login_database
import test_database

def log_out(clouse_window):
    login_field.delete(0, tk.END)
    password_field.delete(0, tk.END)
    clouse_window.destroy()
    window.deiconify()


def open_grades_window(parent_window):
    grades_win = Toplevel(parent_window)
    grades_win.title("Оценки за тест")
    grades_win.geometry("600x400")
    
    tk.Label(grades_win, text="Оценки учеников").pack(pady=10)

    columns = ("username", "score", "grade")

    tree = ttk.Treeview(grades_win, columns=columns, show="headings")
    tree.heading("username", text="Ученик")
    tree.heading("score", text="Верных из 5")
    tree.heading("grade", text="Оценка")
    tree.column("username", width=150, anchor='center')
    tree.column("score", width=100, anchor='center')
    tree.column("grade", width=100, anchor='center')    
    tree.pack(fill='both', expand=True, padx=20, pady=10)


    def load_data():
        for item in tree.get_children():
            tree.delete(item)
            
        try:
            results = test_database.get_all_results()
            for row in results:
                tree.insert("", "end", values=row)
        except Exception as error:
            messagebox.showerror("Ошибка", str(error))
    load_data()

    tk.Button(grades_win, text="Обновить", command=load_data).pack(pady=10)


def open_test_window(username, parent_window):
    test_win = Toplevel(parent_window)
    test_win.title('Прохождение теста')
    test_win.geometry('1440x1080')

    questions = [
        'Какой запрос читает данные?', ['SELECT', 'INSERT', 'UPDATE', 'CREATE'],
        'Какое слово указывает таблицу в SELECT?', ['ORDER', 'FROM', 'VALUES', 'SET'],
        'Какой запрос добавляет строку?', ['DROP', 'SELECT', 'INSERT', 'WHERE'],
        'Какой тип хранит целое число?', ['DATE','TEXT','NUMERIC','INTEGER'],
        'Как сортировать по возрастанию?', ['ASC','DESC','NULL','CHECK']
    ]
    
    correct_answers = ['SELECT', 'FROM', 'INSERT', 'INTEGER', 'ASC']

    answers = [] 

    for i in range(0, len(questions), 2):
        q_text = questions[i]
        q_options = questions[i+1] 
        
        frame = tk.Frame(test_win)
        frame.pack(fill="x", pady=5, padx=20)

        tk.Label(frame, text=q_text, font=('Arial', 10, 'bold')).pack(anchor="w")
        
        var = tk.StringVar(value="None")
        answers.append(var)

        for option in q_options:
            tk.Radiobutton(frame, text=option, variable=var, value=option).pack(anchor="w", padx=20)

    def finish_test():
        score = 0
        for i in range(len(answers)):
            if answers[i].get() == correct_answers[i]:
                score += 1
        grade = score if score > 2 else 2
        try:
            test_database.save_test_result(username, score, grade)
            messagebox.showinfo("Результат", f"Правильных ответов: {score} из {len(answers)}.\nВаша оценка: {grade}")
            test_win.destroy()
        except Exception as error:
            messagebox.showerror("Ошибка БД", str(error))

    tk.Button(test_win, text="Завершить тест", command=finish_test).pack(pady=20) 
    return
def open_main_window(role, username):
    window.withdraw()
    main_window = Toplevel(window)
    main_window.title('Моя информационная система')
    main_window.geometry('980x620')

    panel = tk.Frame(main_window,bg="#f0f0f0", bd=1, relief="solid")
    panel.pack(padx=20, pady=20, fill="x") 
    Label(panel, text='Вы вошли в систему', font=('Arial', 12),bg="#f0f0f0", fg='black').pack(side='left', padx=10,pady=10)
    ext = tk.Button(panel,text="Выйти",font=("Arial", 10, "bold"),bg="#e1e1e1",activebackground="#d0d0d0",relief="raised",bd=2,padx=15,pady=5,)
    ext.pack(side="right", padx=10, pady=10)

    ext.config(command=lambda: log_out(main_window))#
    main_window.protocol('WM_DELETE_WINDOW', lambda: log_out(main_window))

    if role == 'Ученик':
        Label(main_window, text='Личный кабинет ученика').pack(pady=40)
        button_test = tk.Button(main_window, text='Начать тестирование', command=lambda: open_test_window(username,main_window))
        button_test.pack(pady=40)

    elif role == 'Учитель':
        Label(main_window, text='Личный кабинет преподователя').pack(pady=40)
        button_grades = tk.Button(main_window, text='Оценки учеников', command=lambda: open_grades_window(main_window))
        button_grades.pack(pady=40)


def regist_window():
    window.withdraw()
    regist_wind = Toplevel(window)
    regist_wind.title('Окно регистрации')
    regist_wind.geometry('680x420')

    ttk.Label(regist_wind, text='Логин:').pack()
    reg_login = ttk.Entry(regist_wind, width=32)
    reg_login.pack(pady=5)

    ttk.Label(regist_wind, text='Пароль:').pack()
    reg_password = ttk.Entry(regist_wind, width=32, show='*')
    reg_password.pack(pady=5)

    ttk.Label(regist_wind, text='Роль').pack(pady=(10, 0))
    roles = ['Ученик', 'Учитель']
    role_combo = ttk.Combobox(regist_wind, values=roles, state='readonly')
    role_combo.pack(pady=20)
    role_combo.set('Вывебете роль')
    def do_regist_window():
        username = reg_login.get().strip()
        password = reg_password.get()
        role = role_combo.get()

        if not username or not password or role == 'Выберете роль':
            messagebox.showwarning('Ошибка','Заколните все поля и выберете свою роль')
            return
        if len(username) < 3:
            messagebox.showwarning('Ошибка', 'Логин должен содержать минимум 3 символа')
            return    
        if len(password) < 8:
            messagebox.showwarning('Ошибка','Пароль должен содержать минимум 8 символов')
            return
        try:
            login_database.registration(username,password,role)
            regist_wind.destroy()
            open_main_window(role, username)
            messagebox.showinfo('Регистрация', 'Регистрация прошла успешно')
        except Exception as error:
            messagebox.showerror('Ошибка', str(error))
    def on_close():
        regist_wind.destroy()
        window.deiconify()
    regist_wind.protocol('WM_DELETE_WINDOW', on_close)

    button_reg = ttk.Button(regist_wind, text='Зарегистрироваться', command=do_regist_window)
    button_reg.pack(pady=8)
    reg_login.focus_set()

# def regist():
#     username = login_field.get().strip()
#     password = password_field.get()
#     if username == '' or password == '':
#         messagebox.showwarning('Ошибка','Заполните все поля')
#         return
#     if not 3 <= len(username):
#         messagebox.showwarning('Ошибка', 'Логин должен содержать минимум 3 символа')
#     if not 8 <=len(password):
#         messagebox.showwarning('Ошибка','Пароль должен содержать минимум 8 символов')
#         return
#     try:
#         database.registration(username,password)
#         open_main_window()
#         messagebox.showinfo('Регистрация', 'Регистрация прошла успешно')
#     except Exception as error:
#         messagebox.showerror('Ошибка', str(error))


def login():
    username = login_field.get().strip()
    password = password_field.get()
    if username == '' or password == '':
            messagebox.showwarning('Заполните все поля')
            return
    try:
        role = login_database.check_user(username,password)
        if login_database.check_user(username,password):
            open_main_window(role, username)
            messagebox.showinfo('Авторизация', 'Успешно')
        else:
            messagebox.showerror('Ошибка', 'Неверный логин или пароль')
    except Exception as error:
        messagebox.showerror('Ошибка', str(error))

#окно авторизации
window = tk.Tk()
window.title('Окно авторизации')
window.geometry('680x420')

label= ttk.Label(window, text='Войдите в свой аккаунт или зарегестрируйте новый')
label.pack(pady=20)

ttk.Label(window, text='Логин:').pack()
login_field = ttk.Entry(window, width=32)
login_field.pack(pady=5)

ttk.Label(window, text='Пароль:').pack()
password_field = ttk.Entry(window, width=32, show='*')
password_field.pack(pady=5)

button_regist = ttk.Button(window, text='Зарегистрироваться')
button_regist.pack(pady=8)
button_login = ttk.Button(window, text='Войти')
button_login.pack(pady=8)
login_field.focus_set()

button_regist.config(command=regist_window)
button_login.config(command=login)

window.mainloop()