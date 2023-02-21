"""
В этом файле ложите все функции для работы с бд
import в main уже стоит
con -> менять под себя
"""

import psycopg2
import random
from modules.interfaces import *

# подключение к БД
con = psycopg2.connect(
    database="PyCalc",
    user="postgres",
    password="james132587",
    host="127.0.0.1",
    port="5432"
)
print("БД подключена!")
cur = con.cursor()


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
                                          position_name TEXT UNIQUE NOT NULL,
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
                                        amount_plan INTEGER,
                                        completed_amount INTEGER,
                                        quality_plan INTEGER,
                                        completed_quality INTEGER,
                                        tasks_plan INTEGER,
                                        completed_tasks INTEGER,
                                        budget_plan REAL,
                                        budget_spend REAL);''')
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


def fill_company_data(companies_num: int) -> None:
    companies = []
    for i in range(companies_num):
        name = f"Company {i + 1}"
        login = f"company{i + 1}_login"
        password = f"company{i + 1}_password"
        companies.append((name, login, password))
    for company in companies:
        cur.execute(
            f"INSERT INTO company (name, login, password) VALUES ('{company[0]}', '{company[1]}', '{company[2]}')")
    con.commit()


def fill_coefficients_data(count) -> None:
    for kek in range(count):
        coefs_abc_weight = [0.3, 0.35, 0.35]
        coef_a_names = ['coef_a_names1', 'coef_a_names2', 'coef_a_names3', 'coef_a_names4']
        coef_b_names = ['coef_b_names1', 'coef_b_names2', 'coef_b_names3']
        coef_c_names = ['coef_c_names1', 'coef_c_names2', 'coef_c_names3']
        # Весы для каждой записи
        a, b, c = random.randint(10, int(100 / len(coef_b_names))), random.randint(10, int(100 / len(
            coef_b_names))), random.randint(10, int(100 / len(coef_b_names)))
        coef_a_name_weight = [a, b, c, 100 - (a + b + c)]
        a, b, c = random.randint(10, int(100 / len(coef_b_names))), random.randint(10, int(100 / len(
            coef_b_names))), random.randint(10, int(100 / len(coef_b_names)))
        coef_b_name_weight = [a, b, 100 - (a + b)]
        a, b, c = random.randint(10, int(100 / len(coef_b_names))), random.randint(10, int(100 / len(
            coef_b_names))), random.randint(10, int(100 / len(coef_b_names)))
        coef_c_name_weight = [a, b, 100 - (a + b)]
        # Диапазоны значений и коэффы для них
        coef_a_bottom_all_values = list()
        coef_a_top_all_values = list()
        coef_a_all_weights = list()
        for i in range(len(coef_a_names)):
            # count = random.randint(3, 5)
            count = 4
            coef_a_bottom_value = [0]
            coef_a_top_value = [round(random.uniform(0, 1 / count), 2)]
            coef_a_weight = [0]
            for x in range(1, count):
                coef_a_bottom_value.append(round(coef_a_top_value[x - 1] + 0.01, 2))

                coef_a_top_value.append(round(coef_a_bottom_value[x] + random.uniform(0.01, 1 / count), 2))

                coef_a_weight.append(round(coef_a_weight[x - 1] + random.uniform(0, 0.9), 2))
            coef_a_bottom_value[0] = 0
            coef_a_top_value[count - 1] = 1.5

            coef_a_bottom_all_values.append(coef_a_bottom_value)
            coef_a_top_all_values.append(coef_a_top_value)
            coef_a_all_weights.append(coef_a_weight)

        coef_b_bottom_value = 1
        coef_b_top_value = 3
        coef_b_weight = random.randint(1, 4)

        coef_c_bottom_value = 1
        coef_c_top_value = 3
        coef_c_weight = random.randint(1, 4)
        cur.execute(f"INSERT INTO coefficients(coefs_abc_weight, "
                    f"coef_a_names, coef_a_name_weight, coef_a_bottom_value, coef_a_top_value, coef_a_weight, "
                    f"coef_b_names, coef_b_name_weight, coef_b_bottom_value, coef_b_top_value, coef_b_weight, "
                    f"coef_c_names,coef_c_name_weight, coef_c_bottom_value, coef_c_top_value, coef_c_weight) "
                    f"VALUES(ARRAY{coefs_abc_weight},"
                    f"ARRAY{coef_a_names},ARRAY{coef_a_name_weight},ARRAY{coef_a_bottom_all_values}, ARRAY{coef_a_top_all_values},ARRAY{coef_a_all_weights},"
                    f"ARRAY{coef_b_names},ARRAY{coef_b_name_weight}, {coef_b_bottom_value}, {coef_b_top_value}, {coef_b_weight},"
                    f"ARRAY{coef_c_names},ARRAY{coef_c_name_weight}, {coef_c_bottom_value}, {coef_c_top_value}, {coef_c_weight})")
        con.commit()


def fill_functions_data(functions_num: int) -> None:
    cur.execute(f"SELECT coefficients_id FROM coefficients")
    coefficients_id_list = cur.fetchall()
    for i in range(functions_num):
        name = random.choice(['function1', 'function2', 'function3', 'function4', 'function5'])
        coefficients_id = random.choice(coefficients_id_list)[0]
        cur.execute(f"INSERT INTO functions(coefficients_id, name) VALUES({coefficients_id}, '{name}')")
        con.commit()


def fill_positions_data(positions_num: int) -> None:
    cur.execute(f"SELECT * FROM functions")
    function_ids = cur.fetchall()
    position_names = ['Manager', 'Designer', 'Master', 'Developer', 'Worker', 'Logist', 'TEST1', 'TEST8', 'TEST9',
                      'TEST10', 'TEST11', 'TEST12', 'TEST13', 'TEST14', 'TEST15']
    cur.execute(f"SELECT company_id FROM company")
    company_id_list = cur.fetchall()

    for i in range(positions_num):
        company_id = random.choice(company_id_list)[0]
        position_name = position_names[i]
        salary = round(random.uniform(12.31, 5023.425), 2)
        cur.execute(
            f"INSERT INTO positions (functions_id, position_name, salary, company_id) VALUES ({function_ids[random.randint(0, len(function_ids) - 1)][0]}, '{position_name}', '{salary}', {company_id})")
    con.commit()


def fill_reports_data(reports_num: int) -> None:
    cur.execute(f"SELECT company_id FROM company")
    company_id_list = cur.fetchall()
    cur.execute(f"SELECT position_id FROM positions")
    position_id_list = cur.fetchall()
    for i in range(reports_num):
        company_id = random.choice(company_id_list)[0]
        position_id = random.choice(position_id_list)[0]
        amount_plan = random.randint(0, 100)
        completed_amount = random.randint(0, 100)
        quality_plan = random.randint(0, 100)
        completed_quality = random.randint(0, 100)
        tasks_plan = random.randint(0, 100)
        completed_tasks = random.randint(0, 100)
        budget_plan = round(random.uniform(99.99, 50000.99), 2)
        budget_spend = round(random.uniform(99.99, 50000.99), 2)
        cur.execute(f"INSERT INTO reports (company_id, position_id, amount_plan, completed_amount, quality_plan,"
                    f"completed_quality, tasks_plan, completed_tasks, budget_plan, budget_spend)"
                    f"VALUES ({company_id}, {position_id}, {amount_plan}, {completed_amount}, {quality_plan}, "
                    f"{completed_quality}, {tasks_plan}, {completed_tasks}, {budget_plan}, {budget_spend})")
        con.commit()


def fill_employee_data(employees_num: int) -> None:
    cur.execute(f"SELECT position_id FROM positions")
    position_id_list = cur.fetchall()
    cur.execute(f"SELECT function_id FROM functions")
    function_id_list = cur.fetchall()
    name_list = ['Yan', 'Novak', 'Anna', 'Maria', 'Sophia', 'Katherine', 'Eva', 'Diana', 'Nika', 'Yato', 'Denis',
                 'Nixat',
                 'Sasa', 'Kosta', 'Sevcov', 'Mazelov', 'Xesus']
    for i in range(employees_num):
        position_id = random.choice(position_id_list)[0]
        function_id = random.choice(function_id_list)[0]
        name = random.choice(name_list)[0]
        email = random.choice(name)[0] + '@gmail.com'
        phone = random.randint(103163296, 134215783)
        phone = "+380" + str(phone)
        # profile_image_url = 'https://093241'
        cur.execute(f"INSERT INTO employee (name, email, phone, position_id, function_id) VALUES "
                    f"('{name}', '{email}', '{phone}', {position_id}, '{function_id}')")
        con.commit()


# заполняет все таблицы рандомно сгенерированными значениями
def fill_db(COMPANY_NUM=7,
            COEF_FUNC_COUNT=3,
            POSITIONS_NUM=15,
            REPORTS_NUM=201,
            EMPLOYEE_NUM=51) -> None:
    fill_company_data(COMPANY_NUM)
    fill_coefficients_data(COEF_FUNC_COUNT)
    fill_functions_data(COEF_FUNC_COUNT)
    fill_positions_data(POSITIONS_NUM)
    fill_employee_data(EMPLOYEE_NUM)
    # fill_reports_data(REPORTS_NUM)
    print("Таблицы заполнены данными")


# удаляет и создает таблицу company + добавляет в нее запись (1, 'тестовое имя', 'root', 'root')
def test_table() -> None:
    print("Запущена функция test_table()")
    cur.execute('DROP TABLE company')
    cur.execute('''CREATE TABLE  company  
         (company_id SERIAL PRIMARY KEY NOT NULL ,
         name TEXT,
         login TEXT NOT NULL,
         password TEXT NOT NULL);''')
    print("Таблица создана")
    con.commit()

    cur.execute(
        "INSERT INTO company (name,login,password) VALUES ('тестовое имя', 'root', 'root')"
    )
    con.commit()
    print("Тестовая запись добавлена")


# заполняет часть таблицы всеми значениями из раздела А
def insert_coefs_a(titles: list, weights: list, ranges_min: list, ranges_max: list, coefs: list) -> int:
    test_only = [0.35, 0.35, 0.3]  # coefs_abc_weight
    try:
        cur.execute(
            f"INSERT INTO coefficients(coef_a_names,coefs_abc_weight,coef_a_name_weight,coef_a_bottom_value,"
            f"coef_a_top_value,coef_a_weight) VALUES(ARRAY{titles},ARRAY{test_only},ARRAY{weights},ARRAY{ranges_min},"
            f"ARRAY{ranges_max},ARRAY{coefs})")
        con.commit()
        print("ok")
        return 1
    except:
        con.commit()
        return 0


# заполняет часть таблицы всеми значениями из раздела Б и С
def insert_coefs(section: str, titles: list, weights: list, range_min: int, range_max: int, coef: int) -> int:
    if section == "b":
        try:
            cur.execute(
                f"INSERT INTO coefficients(coef_b_names,coef_b_name_weight,coef_b_bottom_value,coef_b_top_value,"
                f"coef_b_weight) VALUES(ARRAY{titles},ARRAY{weights},{range_min},{range_max},{coef})")
            con.commit()
            print("ok")
            return 1
        except:
            con.commit()
            return 0
    elif section == "c":
        try:
            cur.execute(
                f"INSERT INTO coefficients(coef_c_names,coef_c_name_weight,coef_c_bottom_value,coef_c_top_value,"
                f"coef_c_weight) VALUES(ARRAY{titles},ARRAY{weights},{range_min},{range_max},{coef})")
            con.commit()
            print("ok")
            return 1
        except:
            con.commit()
            return 0
    else:
        print("Wrong section letter!")


# Возвращает список объектов раздела А из таблицы coefficients для вывода в таблицу
def get_coefficients_a(coefficients_id: int) -> list:
    cur.execute(
        f"SELECT coef_a_names,coef_a_name_weight,coef_a_bottom_value,coef_a_top_value,coef_a_weight FROM coefficients "
        f"WHERE coefficients_id={coefficients_id} ")
    res = cur.fetchone()
    coef_a_names: list = res[0]
    coef_a_name_weight: list = res[1]
    coef_a_bottom_value: list = res[2]
    coef_a_top_value: list = res[3]
    coef_a_weight: list = res[4]
    section_a_targets: list = list()
    for i in range(len(coef_a_names)):
        section_a_targets.append(
            TargetFirstType(coef_a_names[i], coef_a_name_weight[i], coef_a_bottom_value[i], coef_a_top_value[i],
                            coef_a_weight[i]))
    con.commit()
    return section_a_targets


# Возвращает список объектов раздела Б из таблицы coefficients для вывода в таблицу
def get_coefficients_b(coefficients_id: int) -> list:
    cur.execute(
        f"SELECT coef_b_names,coef_b_name_weight,coef_b_bottom_value,coef_b_top_value,coef_b_weight FROM coefficients "
        f"WHERE coefficients_id={coefficients_id} ")
    res = cur.fetchone()
    coef_b_names: list = res[0]
    coef_b_name_weight: list = res[1]
    coef_b_bottom_value: int = res[2]
    coef_b_top_value: int = res[3]
    coef_b_weight: int = res[4]
    section_b_targets: list = list()
    for i in range(len(coef_b_names)):
        section_b_targets.append(
            TargetSecondType(coef_b_names[i], coef_b_name_weight[i], coef_b_bottom_value, coef_b_top_value,
                             coef_b_weight))
    con.commit()
    return section_b_targets


# Возвращает список объектов раздела С из таблицы coefficients для вывода в таблицу
def get_coefficients_c(coefficients_id: int) -> list:
    cur.execute(
        f"SELECT coef_c_names,coef_c_name_weight,coef_c_bottom_value,coef_c_top_value,coef_c_weight FROM coefficients "
        f"WHERE coefficients_id={coefficients_id} ")
    res = cur.fetchone()
    coef_c_names: list = res[0]
    coef_c_name_weight: list = res[1]
    coef_c_bottom_value: int = res[2]
    coef_c_top_value: int = res[3]
    coef_c_weight: int = res[4]
    section_c_targets: list = list()
    for i in range(len(coef_c_names)):
        section_c_targets.append(
            TargetSecondType(coef_c_names[i], coef_c_name_weight[i], coef_c_bottom_value, coef_c_top_value,
                             coef_c_weight))
    con.commit()
    return section_c_targets


# Возвращает ид функции, которая привязана к должности, если все прошло успешно, в противном случае - False
def get_function_id_by_position_id(position_id: int) -> int | bool:
    cur.execute(f"SELECT functions_id FROM positions WHERE position_id={position_id}")
    res = cur.fetchone()[0]
    return res if res is not None else False


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
            f"insert into employee(name, email, phone, position_id, function_id) values('{name}','{email}','{phone}',{position_id},{function_id})")
        con.commit()
        return True
    except:
        con.commit()
        return False


# Возвращает список всех записей из таблицы positions
def get_all_positions() -> list:
    cur.execute(
        "select functions.name, positions.position_name, positions.salary from positions INNER JOIN functions ON positions.functions_id=functions.function_id")
    res = cur.fetchall()
    con.commit()
    return res


def get_positions(company_id) -> list:
    if company_id == 100:
        cur.execute(f"select position_id,position_name from positions")
        res = cur.fetchall()
        con.commit()
        return res
    else:
        cur.execute(f"select position_id,position_name from positions where company_id ={company_id}")
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
def get_all_employees() -> list:
    cur.execute(
        'select employee.name, employee.email, employee.phone, positions.position_name, functions.name, company.name from employee '
        'INNER JOIN positions ON employee.position_id=positions.position_id '
        'INNER JOIN functions ON employee.function_id=functions.function_id '
        'INNER JOIN company ON employee.company_id=company.company_id')
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
    return res if res != None else False


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
        raise
        print("stop")
        return False


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


def add_function_sql(coefficients_id, name):
    try:
        cur.execute(f"INSERT INTO functions(coefficients_id, name) values({coefficients_id},'{name}')")
        con.commit()
        return True
    except:
        con.commit()
        return False


def get_company_name(id: int) -> str:
    cur.execute(f'select name from company where company_id={id}')
    return cur.fetchone()[0]

# Создание суперюзера с id 100
def create_superuser():
    cur.execute("insert into company(company_id,name,login,password) values(100,'ASH inc.', 'root','root')")
    con.commit()

# Ручное заполнение таблиц coefficients, positions, employee
def test_coeffs():
    coefficients_id = 100
    coefs_abc_weight = [0.3, 0.3, 0.4]
    coef_a_names = ['Выполнение плана продаж', 'Выполнение плана по прибыли',
                    'Контроль общехозяйственных и операционных расходов',
                    'Оборачиваемость по дебиторской задолженности']
    coef_a_name_weight = [25, 15, 30, 30]
    coef_a_bottom_all_values = [[0, 0.25, 0.60, 0.75], [0, 0.33, 0.70, 0.9], [0, 0.4, 0.9, 1], [0, 0.5, 0.7, 1]]
    coef_a_top_all_values = [[0.24, 0.59, 0.74, 1.2], [0.32, 0.69, 0.89, 1.1], [0.39, 0.89, 0.99, 1.5],
                             [0.49, 0.69, 0.99, 1.2]]
    coef_a_all_weights = [[0, 0.3, 0.55, 0.9], [0, 0.5, 0.75, 1], [0, 0.45, 0.6, 1.2], [0, 0.25, 0.8, 1.1]]
    coef_b_names = ['Ведение достоверного и своевременного финансового учета и отчетности',
                    'Планирование и организация работы', 'Быстрое обрабатывание заказов']
    coef_b_name_weight = [30, 25, 45]
    coef_b_bottom_value = 1
    coef_b_top_value = 3
    coef_b_weight = 3
    coef_c_names = ['Запуск продаж икорной продукции', 'Запуск личного бренда одежды',
                    'Запуск производства ядерки в Украине']
    coef_c_name_weight = [25, 65, 10]
    coef_c_bottom_value = 1
    coef_c_top_value = 3
    coef_c_weight = 3
    cur.execute(f"INSERT INTO coefficients(coefficients_id, coefs_abc_weight, "
                f"coef_a_names, coef_a_name_weight, coef_a_bottom_value, coef_a_top_value, coef_a_weight, "
                f"coef_b_names, coef_b_name_weight, coef_b_bottom_value, coef_b_top_value, coef_b_weight, "
                f"coef_c_names,coef_c_name_weight, coef_c_bottom_value, coef_c_top_value, coef_c_weight) "
                f"VALUES({coefficients_id},ARRAY{coefs_abc_weight},"
                f"ARRAY{coef_a_names},ARRAY{coef_a_name_weight},ARRAY{coef_a_bottom_all_values}, ARRAY{coef_a_top_all_values},ARRAY{coef_a_all_weights},"
                f"ARRAY{coef_b_names},ARRAY{coef_b_name_weight}, {coef_b_bottom_value}, {coef_b_top_value}, {coef_b_weight},"
                f"ARRAY{coef_c_names},ARRAY{coef_c_name_weight}, {coef_c_bottom_value}, {coef_c_top_value}, {coef_c_weight})")
    con.commit()

def test_function():
    function_id = 100
    coefficients_id = 100
    name = 'Кипсолид'
    cur.execute(f"INSERT INTO functions(function_id, coefficients_id, name) VALUES({function_id},{coefficients_id}, '{name}')")
    con.commit()

def test_position():
    position_id = 100
    functions_id = 100
    position_name = 'Управляющий отделом маркетинга'
    salary = 1250.0
    company_id = 100
    cur.execute(
        f"INSERT INTO positions (position_id, functions_id, position_name, salary, company_id) VALUES ({position_id},{functions_id}, '{position_name}', {salary}, {company_id})")
    con.commit()


def test_employee():
    name = 'Степан Бандера'
    email = 'bandera@gmail.com'
    phone = '+380999999999'
    position_id = 100
    function_id = 100
    cur.execute(f"INSERT INTO employee (name, email, phone, position_id, function_id) VALUES "
                f"('{name}', '{email}', '{phone}', {position_id}, '{function_id}')")
    con.commit()
    name = 'Симон Петлюра'
    email = 'petliura@gmail.com'
    phone = '+3806777777777'
    position_id = 100
    function_id = 100
    cur.execute(f"INSERT INTO employee (name, email, phone, position_id, function_id) VALUES "
                f"('{name}', '{email}', '{phone}', {position_id}, '{function_id}')")
    con.commit()


def test_inserts():
    create_superuser()
    test_coeffs()
    test_function()
    test_position()
    test_employee()

def calculate_report(report: object, coefs: object) -> int:
    budget_diff = report.budget_plan - report.budget_spend
    if budget_diff < 0:
        return f"Бюджет перерасходован. Премии невозможны. Сумма нестачи бюджета - {budget_diff}"
    # количество бабла на каждый раздел
    bonuses_sum_list = [budget_diff * coefs.coefs_abc_weight[0],
                        budget_diff * coefs.coefs_abc_weight[1],
                        budget_diff * coefs.coefs_abc_weight[2]]
    print("Суммы равны - ", budget_diff == sum(bonuses_sum_list))
    bonuses_a_sum_list = list()  # сумма начисленной премии на каждый подраздел A
    weight_a_percentage = list() # на какой % был выполненен план подраздела А
    print("Раздел А")
    # раздел а
    for index, line in enumerate(coefs.coef_a_names):
        print(f"*****\n"
              f"weight_a_percentage.append(report.completed_amount[index] / (report.amount_plan[index] / 100))\n"
              f"{int(report.completed_amount[index]) / (int(report.amount_plan[index]) / 100)} % \n"
              f"*****\n")
        weight_a_percentage.append(int(report.completed_amount[index]) / (int(report.amount_plan[index]) / 100)) # на сколько % вып. план подраздела А

        for index_weight,value in enumerate(coefs.coef_a_bottom_all_values[index]): # узнаем че там он получит за это
            if weight_a_percentage[index] > coefs.coef_a_top_all_values[index][index_weight]: # проверяем не больше ли верхнего порога диапазона

                if index_weight < len(coefs.coef_a_bottom_all_values[index]) - 1: # проверяем не вышли ли за пределы массива
                    continue

                else: # если % больше верхнего порога и у нас последний элемент массива
                    """
                        Вес подраздела * коэфициент диапазона / % выполненного плана
                        Вес подраздела -> coefs.coef_a_name_weight[index] 
                        коэфициент диапазона -> coef_a_all_weights[index][index_weight]
                        % выполненного плана -> weight_percentage[index]
                    """
                    print(f"*****\n"
                          f"качеля: {coefs.coef_a_bottom_all_values[index][index_weight]} < x < {coefs.coef_a_top_all_values[index][index_weight]}\n"
                          f"index = {index} index_weight = {index_weight}\n"
                          f"bonuses_a_sum_list.append((coefs.coef_a_name_weight[{index}] * coef_a_all_weights[{index}][{index_weight}]) / weight_a_percentage[{index}])\n"
                          f"{(coefs.coef_a_name_weight[index] * coefs.coef_a_all_weights[index][index_weight]) / weight_a_percentage[index]}\n"
                          f"*****\n")
                    bonuses_a_sum_list.append((coefs.coef_a_name_weight[index] * coefs.coef_a_all_weights[index][index_weight]) / weight_a_percentage[index])
            else:
                print(f"*****\n"
                      f"качеля: {coefs.coef_a_bottom_all_values[index][index_weight]} < x < {coefs.coef_a_top_all_values[index][index_weight]}\n"
                      f"index = {index} index_weight = {index_weight}\n"
                      f"bonuses_a_sum_list.append((coefs.coef_a_name_weight[{index}] * coef_a_all_weights[{index}][{index_weight}]) / weight_a_percentage[{index}])\n"
                      f"{(coefs.coef_a_name_weight[index] * coef_a_all_weights[index][index_weight]) / weight_a_percentage[index]}\n"
                      f"*****\n")
                bonuses_a_sum_list.append((coefs.coef_a_name_weight[index] * coef_a_all_weights[index][index_weight]) / weight_a_percentage[index])
    bonuses_b_sum_list = list()  # сумма начисленной премии на каждый подраздел B

    print("Раздел Б")
    # раздел б
    for index, line in enumerate(coefs.coef_b_names):
        # вес * КПЭ (оценка) / коэфициент
        print(f"******\n"
              f"coefs.coef_b_name_weight[index] * report.completed_quality[index] ) / coefs.coef_b_weight[index]\n"
              f"coefs.coef_b_name_weight[{index}] * int(report.completed_quality[{index}]) ) / coefs.coef_b_weight\n"
              f"{coefs.coef_b_name_weight[index]} * {int(report.completed_quality[index])} ) / {coefs.coef_b_weight} = {(coefs.coef_b_name_weight[index] * int(report.completed_quality[index]) ) / coefs.coef_b_weight}\n"
              f"*****\n")
        bonuses_b_sum_list.append(
            ( coefs.coef_b_name_weight[index] * int(report.completed_quality[index]) ) / coefs.coef_b_weight
        )
    bonuses_c_sum_list = list()  # сумма начисленной премии на каждый подраздел C
    # раздел с
    print("Раздел С")
    for index, line in enumerate(coefs.coef_c_names):
        # вес * КПЭ (оценка) / коэфициент
        print(f"******\n"
              f"coefs.coef_c_name_weight[index] * int(report.completed_task[index]) ) / coefs.coef_c_weight\n"
              f"coefs.coef_c_name_weight[{index}] * int(report.completed_task[{index}]) ) / coefs.coef_c_weight\n"
              f"({coefs.coef_c_name_weight[index]} * {int(report.completed_task[index])} ) / {coefs.coef_c_weight} = {(coefs.coef_c_name_weight[index] * int(report.completed_task[index]) ) / coefs.coef_c_weight}\n"
              f"*****\n")
        bonuses_c_sum_list.append(
            ( coefs.coef_c_name_weight[index] * int(report.completed_task[index]) ) / coefs.coef_c_weight
        )
    print("BREAKPOINT")   # </заебца>
