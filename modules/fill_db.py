from modules.db_tools import con, cur
import random

SUPERUSER_ID: int = 100


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


# Создание суперюзера с id 100
def create_superuser():
    company_id = SUPERUSER_ID
    cur.execute(f"insert into company(company_id,name,login,password) values({company_id},'Пчеловод 🐝', 'root','root')")
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
    position_names = ['Manager', 'Designer', 'Master', 'Back-end Developer', 'Worker', 'Logist', 'Front-end Developer',
                      'Cleaning', 'Art-Director',
                      'Accountant', 'Driver', 'Waiter', 'Bartender', 'Courier', 'Dispatcher']
    cur.execute(f"SELECT company_id FROM company")
    company_id_list = cur.fetchall()

    for i in range(positions_num):
        company_id = random.choice(company_id_list)[0]
        position_name = position_names[i]
        salary = round(random.uniform(12.31, 5023.425), 2)
        cur.execute(
            f"INSERT INTO positions (functions_id, position_name, salary, company_id) VALUES ({function_ids[random.randint(0, len(function_ids) - 1)][0]}, '{position_name}', '{salary}', {company_id})")
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
        name = random.choice(name_list)
        email = name.lower() + '@gmail.com'
        phone = random.randint(103163296, 134215783)
        phone = "+380" + str(phone)
        cur.execute(f"INSERT INTO employee (name, email, phone, position_id, function_id) VALUES "
                    f"('{name}', '{email}', '{phone}', {position_id}, '{function_id}')")
        con.commit()


# заполняет все таблицы рандомно сгенерированными значениями
def fill_db(company_num=7,
            coef_func_count=3,
            positions_num=15,
            employee_num=51) -> None:
    create_superuser()
    fill_company_data(company_num)
    fill_coefficients_data(coef_func_count)
    fill_functions_data(coef_func_count)
    fill_positions_data(positions_num)
    fill_employee_data(employee_num)

    print("Таблицы заполнены данными")
