"""
В этом файле ложите все функции для работы с бд
import в main уже стоит
con -> менять под себя
"""

import psycopg2
import random

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


# проверяем наличие такого логина и пароля в базе, может быть несколько совпадений
def get_company(login: str, password: str) -> list|bool:
    cur.execute(f"SELECT * FROM company WHERE login='{login}' and password ='{password}'")
    res = cur.fetchone()
    return res if res != None else False


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
                                          salary REAL);''')
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
                                          function_id INTEGER REFERENCES functions (function_id),
                                          company_id INTEGER REFERENCES company (company_id));''')
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
        coefs_abc_weight = [0.3,0.35, 0.35]
        coef_a_names = ['coef_a_names1','coef_a_names2','coef_a_names3','coef_a_names4']
        coef_b_names = ['coef_b_names1','coef_b_names2','coef_b_names3']
        coef_c_names = ['coef_c_names1','coef_c_names2','coef_c_names3']
        a,b,c = random.randint(10,int(100/len(coef_b_names))),random.randint(10,int(100/len(coef_b_names))),random.randint(10,int(100/len(coef_b_names)))
        coef_a_name_weight = [a,b,c, 100 - (a+b+c)]
        a,b,c = random.randint(10,int(100/len(coef_b_names))),random.randint(10,int(100/len(coef_b_names))),random.randint(10,int(100/len(coef_b_names)))
        coef_b_name_weight = [a,b, 100 - (a+b)]
        a,b,c = random.randint(10,int(100/len(coef_b_names))),random.randint(10,int(100/len(coef_b_names))),random.randint(10,int(100/len(coef_b_names)))
        coef_c_name_weight = [a,b, 100 - (a+b)]
        count = random.randint(3,5)
        coef_a_bottom_value = [0]
        coef_a_top_value = [round(random.uniform(0,1/count),2)]
        coef_a_weight = [0]
        for x in range(1,count):
            coef_a_bottom_value.append(round(coef_a_top_value[x-1] + 0.01,2) )

            coef_a_top_value.append(round(coef_a_bottom_value[x] + random.uniform(0.01,1/count),2))

            coef_a_weight.append(round(coef_a_weight[x-1] + random.uniform(0,0.9),2))
        coef_a_bottom_value[0] = 0
        coef_a_top_value[count-1] = 1.5

        coef_b_bottom_value = 1
        coef_b_top_value = 3
        coef_b_weight = random.randint(1,4)

        coef_c_bottom_value = 1
        coef_c_top_value = 3
        coef_c_weight = random.randint(1,4)
        cur.execute(f"INSERT INTO coefficients(coefs_abc_weight, "
                    f"coef_a_names, coef_a_name_weight, coef_a_bottom_value, coef_a_top_value, coef_a_weight, "
                    f"coef_b_names, coef_b_name_weight, coef_b_bottom_value, coef_b_top_value, coef_b_weight, "
                    f"coef_c_names,coef_c_name_weight, coef_c_bottom_value, coef_c_top_value, coef_c_weight) "
                    f"VALUES(ARRAY{coefs_abc_weight},"
                    f"ARRAY{coef_a_names},ARRAY{coef_a_name_weight},ARRAY{coef_a_bottom_value}, ARRAY{coef_a_top_value},ARRAY{coef_a_weight},"
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

    for i in range(positions_num):
        position_name = position_names[i]
        salary = round(random.uniform(12.31, 5023.425), 2)
        cur.execute(f"INSERT INTO positions (functions_id, position_name, salary) VALUES ({function_ids[random.randint(0,len(function_ids)-1)][0]}, '{position_name}', '{salary}')")
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
    cur.execute(f"SELECT company_id FROM company")
    company_id_list = cur.fetchall()
    name_list = ['Yan', 'Novak', 'Anna', 'Maria', 'Sophia', 'Katherine', 'Eva', 'Diana', 'Nika', 'Yato', 'Denis',
                 'Nixat',
                 'Sasa', 'Kosta', 'Sevcov', 'Mazelov', 'Xesus']
    for i in range(employees_num):
        position_id = random.choice(position_id_list)[0]
        function_id = random.choice(function_id_list)[0]
        company_id = random.choice(company_id_list)[0]
        name = random.choice(name_list)[0]
        email = random.choice(name)[0] + '@gmail.com'
        phone = random.randint(103163296, 134215783)
        phone = "+380" + str(phone)
        #profile_image_url = 'https://093241'
        cur.execute(f"INSERT INTO employee (name, email, phone, position_id, function_id, company_id) VALUES "
                    f"('{name}', '{email}', '{phone}', {position_id}, '{function_id}', {company_id})")
        con.commit()


# заполняет все таблицы рандомно сгенерированными значениями
def fill_db(COMPANY_NUM = 7,
            COEF_FUNC_COUNT = 3,
            POSITIONS_NUM = 15,
            REPORTS_NUM = 201,
            EMPLOYEE_NUM = 51) -> None:

    fill_company_data(COMPANY_NUM)
    fill_coefficients_data(COEF_FUNC_COUNT)
    fill_functions_data(COEF_FUNC_COUNT)
    fill_positions_data(POSITIONS_NUM)
    fill_employee_data(EMPLOYEE_NUM)
    # fill_reports_data(REPORTS_NUM)
    print("Таблицы заполнены данными")


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
        return 0


# заполняет часть таблицы всеми значениями из раздела Б и С
def insert_coefs(section: str, titles: list, weights: list, range_min: int, range_max: int, coef: int) -> int:
    if section == "b":
        try:
            cur.execute(
                f"INSERT INTO coefficients(coef_b_names,coef_b_name_weight,coef_b_bottom_value,coef_b_top_value,"
                f"coef_b_weight) VALUES(ARRAY{titles},ARRAY{weights},{range_min},{range_max},{coef}) ")
            con.commit()
            print("ok")
            return 1
        except:
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
            return 0
    else:
        print("Wrong section letter!")

# Target for section A
class TargetFirstType:
    def __init__(self, title: str, weight: float, range_min: list, range_max: list, range_coef: list):
        self.title = title
        self.weight = weight
        self.range_min = list()
        self.range_max = list()
        for i in range(len(range_min)):
            self.range_min.append(int(range_min[i] * 100))
            self.range_max.append(int(range_max[i] * 100))
        self.range_coef = range_coef

# Target for section B and C
class TargetSecondType:
    def __init__(self, title: str, weight: float, range_min: int, range_max: int, range_coef: int):
        self.title = title
        self.weight = weight
        self.range_min = range_min
        self.range_max = range_max
        self.range_coef = range_coef


def get_coefficients_a() -> list:

    cur.execute("SELECT coef_a_names FROM coefficients")
    coef_a_names: list = cur.fetchone()[0]
    cur.execute("SELECT coef_a_name_weight FROM coefficients")
    coef_a_name_weight: list = cur.fetchone()[0]
    cur.execute("SELECT coef_a_bottom_value FROM coefficients")
    coef_a_bottom_value: list = cur.fetchone()[0]
    cur.execute("SELECT coef_a_top_value FROM coefficients")
    coef_a_top_value: list = cur.fetchone()[0]
    cur.execute("SELECT coef_a_weight FROM coefficients")
    coef_a_weight: list = cur.fetchone()[0]
    section_a_targets: list = list()
    for i in range(len(coef_a_names)):
        section_a_targets.append(
            TargetFirstType(coef_a_names[i], coef_a_name_weight[i], coef_a_bottom_value[i], coef_a_top_value[i],
                            coef_a_weight[i]))
    return section_a_targets


def get_coefficients_b() -> list:
    cur.execute("SELECT coef_b_names FROM coefficients")
    coef_b_names: list = cur.fetchone()[0]
    cur.execute("SELECT coef_b_name_weight FROM coefficients")
    coef_b_name_weight: list = cur.fetchone()[0]
    cur.execute("SELECT coef_b_bottom_value FROM coefficients")
    coef_b_bottom_value: int = cur.fetchone()[0]
    cur.execute("SELECT coef_b_top_value FROM coefficients")
    coef_b_top_value: int = cur.fetchone()[0]
    cur.execute("SELECT coef_b_weight FROM coefficients")
    coef_b_weight: int = cur.fetchone()[0]
    section_b_targets: list = list()
    for i in range(len(coef_b_names)):
        section_b_targets.append(
            TargetSecondType(coef_b_names[i], coef_b_name_weight[i], coef_b_bottom_value, coef_b_top_value,
                             coef_b_weight))
    return section_b_targets


def get_coefficients_c() -> list:
    cur.execute("SELECT coef_c_names FROM coefficients")
    coef_c_names: list = cur.fetchone()[0]
    cur.execute("SELECT coef_c_name_weight FROM coefficients")
    coef_c_name_weight: list = cur.fetchone()[0]
    cur.execute("SELECT coef_c_bottom_value FROM coefficients")
    coef_c_bottom_value: int = cur.fetchone()[0]
    cur.execute("SELECT coef_c_top_value FROM coefficients")
    coef_c_top_value: int = cur.fetchone()[0]
    cur.execute("SELECT coef_c_weight FROM coefficients")
    coef_c_weight: int = cur.fetchone()[0]
    section_c_targets: list = list()
    for i in range(len(coef_c_names)):
        section_c_targets.append(
            TargetSecondType(coef_c_names[i], coef_c_name_weight[i], coef_c_bottom_value, coef_c_top_value,
                             coef_c_weight))
    return section_c_targets


def add_company(name: str, login: str, password: str) -> None:
    cur.execute(F"INSERT INTO company(name,login,password) VALUES('{name}','{login}','{password}')")
    con.commit()


# добавляет новые должности НУЖЕН ТЕСТ
def add_positions(name: str, salary: float) -> None:
    cur.execute(F"INSERT INTO positions(position_name, salary) VALUES('{name}', {salary})")
    con.commit()


def get_position() -> list:
    cur.execute("select * from positions")
    res = cur.fetchall()
    con.commit()
    return res


def get_function() -> list:
    cur.execute('select * from functions')
    res = cur.fetchall()
    con.commit()
    return res


def get_all_company() -> list:
    cur.execute('select * from company')
    res = cur.fetchall()
    con.commit()
    return res



def create_test() -> None:
    cur.execute('''CREATE TABLE test(id SERIAL PRIMARY KEY NOT NULL,
                                          login TEXT NOT NULL,
                                          password TEXT);''')
    con.commit()


def test_auth(login:str,password:str) -> list|bool:
    cur.execute(f"select * from test where login='{login}' and password='{password}'")
    res = cur.fetchone()
    if res != None:
        return res
    else:
        return False


def get_company_name(id:int) -> str:
    cur.execute(f'select name from company where company_id={id}')
    return cur.fetchone()

def add_position(position_name:str, salary:float, functions_id:int) -> bool:
    try:
        cur.execute(f"insert into positions(functions_id, position_name, salary) values({functions_id}, '{position_name}', {salary} )")
        con.commit()
        return True
    except:
        con.commit()
        return False

# con.close()
