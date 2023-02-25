"""
В этом файле ложите все функции для работы с бд
import в main уже стоит
con -> менять под себя
"""

import psycopg2
import csv
from modules.interfaces import *

# подключение к БД
con = psycopg2.connect(
    database="PyCalc",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432"
)
print("БД подключена!")
cur = con.cursor()

SUPERUSER_ID: int = 100


# удаляет все таблицы
def drop_all() -> None:
    # answer = input("Вы уверены что нужно удалить все таблицы? - (да)")
    answer = 'да'
    if answer == 'да':
        if cur.execute('DROP TABLE IF EXISTS employee'):
            con.commit()
            print("Таблица employee удалена")
        if cur.execute('DROP TABLE IF EXISTS reports'):
            con.commit()
            print("Таблица reports удалена")
        if cur.execute('DROP TABLE IF EXISTS positions'):
            con.commit()
            print("Таблица positions удалена")
        if cur.execute('DROP TABLE IF EXISTS functions'):
            con.commit()
            print("Таблица functions удалена")
        if cur.execute('DROP TABLE IF EXISTS coefficients'):
            con.commit()
            print("Таблица coefficients удалена")
        if cur.execute('DROP TABLE IF EXISTS company'):
            con.commit()
            print("Таблица company удалена")
    else:
        print("Действие отменено")


# создает все таблицы в БД
def create_db() -> None:
    """
    Таблица company - компания
    company_id - целое число, уникальный, первичный ключ, не может быть пустым
    name - строка неограниченного размера, по умолчанию - 'стандартное имя'
    login - строка неограниченного размера, не может быть пустым
    password - строка неограниченного размера, не может быть пустым
    """
    cur.execute('''CREATE TABLE company(company_id SERIAL PRIMARY KEY NOT NULL ,
                                         name TEXT DEFAULT 'стандартное имя',
                                         login TEXT UNIQUE NOT NULL,
                                         password TEXT NOT NULL);''')
    con.commit()
    print("Таблица 'company' создана")
    """
    Таблицa coefficients - для ccылок на значения коэфициентов
    coefficients_id - целое число, уникальный, первичный ключ, не может быть пустым
    coefs_abc_weight - нецелое число, весовой коэфициент для каждого раздела. 3 значения, в сумме 1. 
    *ДОЛЖНО БЫТЬ ОДИНАКОВОЕ КОЛИЧЕСТВО ЗНАЧЕНИЙ В КАЖДОМ ИЗ МАССИВОВ СВОЕЙ ГРУППЫ
    **Т.Е. в разделе 'а' может быть всего по 4, в разделе 'b' всего по 2 и в 'с' всего по 3
    coef_[a или b или с]_names - строка неограниченного размера, массив ->  имена для подразделов. 
    coef_[a или b или с]_name_weight - целое число, массив -> вес каждого подраздела. 
    coef_[a или b или с]_bottom_value - нецелое число -> весовой коэфициент нижнего порога
    coef_[a или b или с]_top_value - нецелое число -> весовой коэфициент верхнего порога
    coef_[a или b или с]_weight - нецелое число -> вес пары коэфициентов 
    (т.е. какая часть премий получается за этот подраздел от суммы всего раздела НО НЕ ВСЕЙ ПРЕМИИ)
    """
    cur.execute('''CREATE TABLE coefficients(coefficients_id SERIAL PRIMARY KEY NOT NULL,
                                            coefs_abc_weight REAL[3],

                                            coef_a_names TEXT[], 
                                            coef_a_name_weight INTEGER[],
                                            coef_a_bottom_value REAL[],
                                            coef_a_top_value REAL[],
                                            coef_a_weight REAL[],

                                            coef_b_names TEXT[],
                                            coef_b_name_weight INTEGER[],
                                            coef_b_bottom_value INTEGER,
                                            coef_b_top_value INTEGER,
                                            coef_b_weight INTEGER,

                                            coef_c_names TEXT[],
                                            coef_c_name_weight INTEGER[],
                                            coef_c_bottom_value INTEGER,
                                            coef_c_top_value INTEGER,
                                            coef_c_weight INTEGER);''')
    con.commit()
    print("Таблица 'coefficients' создана")
    """
    Таблицa functions - для функций
    function_id - целое число, уникальный, первичный ключ, не может быть пустым
    coefficients_id - целое число, внешний ключ на таблицу coefficients (поле->coefficients_id) -> посылает на коэфициенты по этой функции
    name - строка неограниченного размера, не может быть пустым -> название системы поощерения (ну мало ли их там будет много разных на одну должность)
    """
    cur.execute('''CREATE TABLE functions(function_id SERIAL PRIMARY KEY NOT NULL,
                                          coefficients_id INTEGER REFERENCES coefficients (coefficients_id),
                                          name TEXT NOT NULL);''')
    con.commit()
    print("Таблица 'functions' создана")
    """
    Таблица - position для должностей
    position_id - целое число, уникальный, первичный ключ, не может быть пустым
    functions_id - целое число, внешний ключ на таблицу functions (поле->function_id) -> посылает на функцию разчета премии
    position_name - строка неограниченного размера, уникальный, не может быть пустым -> название должности
    salary - нецелое число -> зарплата (на нее не влияет коэфициенты)
    """
    cur.execute('''CREATE TABLE positions(position_id SERIAL PRIMARY KEY NOT NULL,
                                          functions_id INTEGER REFERENCES functions (function_id),
                                          position_name TEXT NOT NULL,
                                          salary REAL,
                                          company_id INTEGER REFERENCES company (company_id));''')
    con.commit()
    print("Таблица 'positions' создана")
    """
    Таблица reports - отчеты
    orders_id - целое число, уникальный, первичный ключ, не может быть пустым
    company_id целое число, внешний ключ на таблицу company (поле->company_id),
    position_id целое число, внешний ключ на таблицу position (поле->position_id),
    amount_plan целое число -> план по количеству
    completed_amount целое число -> выполненые количество
    quality_plan целое число -> план по качеству
    completed_quality целое число -> выполненое качество
    tasks_plan целое число -> план по задачам
    completed_tasks целое число -> выполненые задачи
    budget_plan нецелое число -> запланированный бюджет
    budget_spend нецелое число -> потраченый бюджет
    """
    cur.execute('''CREATE TABLE reports(orders_id SERIAL PRIMARY KEY NOT NULL,
                                            company_id INTEGER REFERENCES company (company_id),
                                            position_id INTEGER REFERENCES positions (position_id),
                                            amount_plan TEXT,
                                            completed_amount TEXT,
                                            completed_quality TEXT,
                                            completed_tasks TEXT,
                                            budget_plan REAL,
                                            budget_spend REAL,
                                            bonuses_abc_sum_list REAL[],
                                            bonuses_a_coef_list REAL[],
                                            bonuses_b_coef_list REAL[],
                                            bonuses_c_coef_list REAL[]);''')
    con.commit()
    print("Таблица 'reports' создана")
    """
    Таблица - employee для сотрудников
    name - строка неограниченного размера, не может быть пустым -> имя сотрудника
    email - строка неограниченного размера -> электронная почта
    phone - строка неограниченного размера -> номер телефона
    profile_image_url - строка неограниченного размера -> ссылка на картинку для профиля
    position_id - целое число, внешний ключ на таблицу positions (поле->position_id) -> посылает на должность
    company_id - целое число, внешний ключ на таблицу company (поле->company_id) -> посылает на компанию

    * на удаление
    function_id - целое число, внешний ключ на таблицу functions (поле->function_id) -> посылает на функцию разчета премии
    *
    """
    cur.execute('''CREATE TABLE employee(employee_id SERIAL PRIMARY KEY NOT NULL,
                                          name TEXT NOT NULL,
                                          email TEXT,
                                          phone TEXT,
                                          position_id INTEGER REFERENCES positions (position_id),
                                          function_id INTEGER REFERENCES functions (function_id));''')
    con.commit()
    print("Таблица 'employee' создана")


# ----- Методы для добавления данных в бд -----

# Добавляет одну запись в таблицу company, возвращает: True - если прошло успешно, в противном случае - False
def add_company(name: str, login: str, password: str) -> bool:
    try:
        cur.execute(F"INSERT INTO company(name,login,password) VALUES('{name}','{login}','{password}')")
        con.commit()
        return True
    except:
        con.commit()
        return False


# Добавляет одну запись в таблицу positions, возвращает: True - если прошло успешно, в противном случае - False
def add_position(position_name: str, salary: float, function_id: int, company_id: int) -> bool:
    try:
        cur.execute(
            f"insert into positions(functions_id, position_name, salary, company_id) values({function_id}, '{position_name}', {salary}, {company_id})")
        con.commit()
        return True
    except:
        con.commit()
        return False


# Добавляет одну запись в таблицу employee, возвращает: True - если прошло успешно, в противном случае - False
def add_employee(name: str, email: str, phone: str, position_id: int, function_id: int) -> bool:
    try:
        cur.execute(
            f"insert into employee(name, email, phone, position_id, function_id) "
            f"values('{name}','{email}','{phone}',{position_id},{function_id})")
        con.commit()
        return True
    except:
        con.commit()
        return False


# Добавляет одну запись в таблицу function, возвращает: True - если прошло успешно, в противном случае - False
def add_function(coefficients_id: int, name: str) -> bool:
    try:
        cur.execute(f"INSERT INTO functions(coefficients_id, name) values({coefficients_id},'{name}')")
        con.commit()
        return True
    except:
        con.commit()
        return False


def coef_abc_add(coefs_abc_weight: list,
                 coef_a_names,
                 coef_a_name_weight,
                 coef_a_bottom_all_values,
                 coef_a_top_all_values,
                 coef_a_all_weights,
                 coef_b_names,
                 coef_b_name_weight,
                 coef_b_bottom_value,
                 coef_b_top_value,
                 coef_b_weight,
                 coef_c_names,
                 coef_c_name_weight,
                 coef_c_bottom_value,
                 coef_c_top_value,
                 coef_c_weight):
    try:
        cur.execute(f"INSERT INTO coefficients(coefs_abc_weight, "
                    f"coef_a_names, coef_a_name_weight, coef_a_bottom_value, coef_a_top_value, coef_a_weight, "
                    f"coef_b_names, coef_b_name_weight, coef_b_bottom_value, coef_b_top_value, coef_b_weight, "
                    f"coef_c_names,coef_c_name_weight, coef_c_bottom_value, coef_c_top_value, coef_c_weight) "
                    f"VALUES(ARRAY{coefs_abc_weight},"
                    f"ARRAY{coef_a_names},ARRAY{coef_a_name_weight},ARRAY{coef_a_bottom_all_values}, ARRAY{coef_a_top_all_values},ARRAY{coef_a_all_weights},"
                    f"ARRAY{coef_b_names},ARRAY{coef_b_name_weight}, {coef_b_bottom_value}, {coef_b_top_value}, {coef_b_weight},"
                    f"ARRAY{coef_c_names},ARRAY{coef_c_name_weight}, {coef_c_bottom_value}, {coef_c_top_value}, {coef_c_weight})")
        con.commit()
        cur.execute("SELECT * FROM coefficients ORDER BY coefficients_id DESC LIMIT 1;")
        return cur.fetchone()
    except:
        con.commit()
        return False


# ----- Методы для получения данных из бд -----

# Возвращает ид функции, которая привязана к должности, если все прошло успешно, в противном случае - False
def get_function_id_by_position_id(position_id: int) -> int | bool:
    cur.execute(f"SELECT functions_id FROM positions WHERE position_id={position_id}")
    res = cur.fetchone()
    return res[0] if res is not None else False


# Возвращает список всех записей из таблицы positions
def get_all_positions(company_id: int) -> list:
    global SUPERUSER_ID
    if company_id == SUPERUSER_ID:
        cur.execute(
            "select positions.position_id, functions.name, positions.position_name, positions.salary from positions "
            "INNER JOIN functions ON positions.functions_id=functions.function_id")
    else:
        cur.execute(
            f"select positions.position_id, functions.name, positions.position_name, positions.salary from positions "
            f"INNER JOIN functions ON positions.functions_id=functions.function_id WHERE company_id = {company_id}")
    res = cur.fetchall()
    con.commit()
    return res


# Возвращает список всех записей из таблицы functions
def get_all_functions() -> list:
    cur.execute('select * from functions')
    res = cur.fetchall()
    con.commit()
    return res


# Возвращает список всех записей из таблицы employee
def get_all_employees(company_id: int) -> list:
    global SUPERUSER_ID
    if company_id == SUPERUSER_ID:
        cur.execute(
            'SELECT employee.name, positions.salary, employee.email, employee.phone, positions.position_name, '
            'functions.name from employee INNER JOIN positions ON employee.position_id=positions.position_id INNER '
            'JOIN functions ON employee.function_id=functions.function_id ')
    else:
        cur.execute(
            f'SELECT employee.name, positions.salary, employee.email, employee.phone, positions.position_name,'
            f'functions.name from positions INNER JOIN employee ON positions.position_id=employee.position_id INNER '
            f'JOIN functions ON positions.functions_id=functions.function_id WHERE company_id={company_id}')
    res = cur.fetchall()
    con.commit()
    return res


# Возвращает список всех записей из таблицы reports
def get_all_reports(company_id: int) -> list:
    global SUPERUSER_ID
    if company_id == SUPERUSER_ID:
        cur.execute('SELECT * FROM reports')
    else:
        cur.execute(
            f'SELECT * FROM reports WHERE company_id={company_id}')
    res = cur.fetchall()
    con.commit()
    return res


# Возвращает список всех записей из таблицы company
def get_all_company() -> list:
    cur.execute('select * from company')
    res = cur.fetchall()
    con.commit()
    return res


# проверяем наличие такого логина и пароля в базе, может быть несколько совпадений
def get_company(login: str, password: str) -> list | bool:
    cur.execute(f"SELECT * FROM company WHERE login='{login}' and password ='{password}'")
    res = cur.fetchone()
    con.commit()
    return res if res != None else False


def get_coef_id(function_id):
    cur.execute(f"select coefficients_id from functions where function_id = {function_id}")
    res = cur.fetchone()[0]
    con.commit()
    return res


def get_coef(function_id):
    cur.execute(f"select * from coefficients where coefficients_id={get_coef_id(function_id)}")
    res = cur.fetchone()
    con.commit()
    return res


def get_company_name_by_id(id: int) -> str:
    cur.execute(f'select name from company where company_id={id}')
    return cur.fetchone()[0]


def calculate_report(report: report, coefs: coefs, position_id: int, company_id: int) -> object | str:
    budget_diff = report.budget_plan - report.budget_spend
    if budget_diff < 0:
        return f"Бюджет перерасходован. Премии невозможны. Сумма нестачи бюджета - {budget_diff}"
    # количество бабла на каждый раздел
    bonuses_sum_list = [budget_diff * coefs.coefs_abc_weight[0],
                        budget_diff * coefs.coefs_abc_weight[1],
                        budget_diff * coefs.coefs_abc_weight[2]]
    print("Суммы равны - ", budget_diff == sum(bonuses_sum_list))
    bonuses_a_coef_list = list()  # значение коєфициента премии на каждый подраздел A
    weight_a_percentage = list()  # на какой % был выполненен план подраздела А
    print("Раздел А")
    # раздел а
    for index, line in enumerate(coefs.coef_a_names):
        weight_a_percentage.append(int(report.completed_amount[index]) / (
                int(report.amount_plan[index]) / 100))  # на сколько % вып. план подраздела А
        for index_weight, value in enumerate(coefs.coef_a_bottom_all_values[index]):  # узнаем че там он получит за это
            if weight_a_percentage[index] / 100 > coefs.coef_a_top_all_values[index][
                index_weight]:  # проверяем не больше ли верхнего порога диапазона
                if index_weight < len(
                        coefs.coef_a_bottom_all_values[index]) - 1:  # проверяем не вышли ли за пределы массива
                    continue

                else:  # если % больше верхнего порога и у нас последний элемент массива
                    """
                        Вес подраздела * коэфициент диапазона / % выполненного плана
                        Вес подраздела -> coefs.coef_a_name_weight[index] 
                        коэфициент диапазона -> coef_a_all_weights[index][index_weight]
                        % выполненного плана -> weight_percentage[index]
                    """
                    count = round((coefs.coef_a_name_weight[index] * coefs.coef_a_all_weights[index][index_weight]) /
                                  weight_a_percentage[index], 4)
                    bonuses_a_coef_list.append(count)
                    break
            else:
                count = round((coefs.coef_a_name_weight[index] * coefs.coef_a_all_weights[index][index_weight]) /
                              weight_a_percentage[index], 4)
                bonuses_a_coef_list.append(count)
                break
    bonuses_b_coef_list = list()  # сумма начисленной премии на каждый подраздел B
    print("Раздел Б")  # раздел б
    for index, line in enumerate(coefs.coef_b_names):
        # вес * КПЭ (оценка) / коэфициент
        count = round(
            (coefs.coef_b_name_weight[index] / 100 * int(report.completed_quality[index])) / coefs.coef_b_weight, 4)
        bonuses_b_coef_list.append(count)
    bonuses_c_coef_list = list()  # сумма начисленной премии на каждый подраздел C
    print("Раздел С")  # раздел с
    for index, line in enumerate(coefs.coef_c_names):
        # вес * КПЭ (оценка) / коэфициент
        count = round((coefs.coef_c_name_weight[index] / 100 * int(report.completed_task[index])) / coefs.coef_c_weight,
                      4)
        bonuses_c_coef_list.append(count)
    calc = calculated_report(bonuses_sum_list, bonuses_a_coef_list, bonuses_b_coef_list, bonuses_c_coef_list)
    # generating csv file
    filename = "report.csv"
    with open(filename, mode='w', newline='') as report_file:
        report_writer = csv.writer(report_file)
        report_writer.writerow(
            ['Розмір бази премії по розділам (А,Б,С)', 'Значення коефіцієнтів розділу А',
             'Значення коефіцієнтів розділу Б', 'Значення коефіцієнтів розділу С'])
        for i in range(len(bonuses_a_coef_list)):
            row = list()
            row.append(bonuses_sum_list[i] if i < len(bonuses_sum_list) else "")
            row.append(bonuses_a_coef_list[i] if i < len(bonuses_a_coef_list) else "")
            row.append(bonuses_b_coef_list[i] if i < len(bonuses_b_coef_list) else "")
            row.append(bonuses_c_coef_list[i] if i < len(bonuses_c_coef_list) else "")
            report_writer.writerow(row)

    return create_report(report, calc, position_id, company_id)


def create_report(report: report, calculated_report: calculated_report, position_id: int, company_id: int) -> int:
    cur.execute(f'select position_name from positions where position_id={position_id}')
    # position_id = session['position_id']
    # company_id = session['company_id']
    cur.execute(
        f"insert into reports(position_id,company_id,amount_plan,completed_amount,completed_quality,completed_tasks,budget_plan,budget_spend,bonuses_abc_sum_list,bonuses_a_coef_list,bonuses_b_coef_list,bonuses_c_coef_list) values({position_id},{company_id},ARRAY{report.amount_plan},ARRAY{report.completed_amount},ARRAY{report.completed_quality},ARRAY{report.completed_task},{report.budget_plan},{report.budget_spend},ARRAY{calculated_report.bonuses_abc_sum_list},ARRAY{calculated_report.bonuses_a_coef_list},ARRAY{calculated_report.bonuses_b_coef_list},ARRAY{calculated_report.bonuses_c_coef_list})")
    con.commit()
    cur.execute("SELECT orders_id FROM reports ORDER BY orders_id DESC LIMIT 1;")
    return cur.fetchone()[0]


def get_report(report_id):
    cur.execute(f"select * from reports where orders_id={report_id}")
    res = cur.fetchone()
    return res


def get_position_name(position_id: int) -> str:
    cur.execute(f"select * from positions where position_id={position_id}")
    return cur.fetchone()[2]
