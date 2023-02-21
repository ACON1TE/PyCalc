"""
скачать PostgreSQL - https://www.postgresql.org/download/windows/

версия бека - 0.6
"""
from modules.interfaces import *
from modules.db_tools import *
from werkzeug.utils import redirect
from flask import Flask, request, session, render_template

# app.secret_key = 'A78Zrejn359854tjnsT98j/3yX R~XHH!jmN]LWXT'

app = Flask(__name__)
# app.secret_key = 'ахуенно секретный ключ'
# app['SESSION_COOKIE_NAME'] = 'наша хуйня'

app.config.update(
    # SECRET_KEY = 'ахуенно секретный ключ',
    SECRET_KEY='cookies1',
)


# стартовая страница, открывает форму для ввода логина и пароля, не имеет меню
@app.route('/')
def index():
    return render_template('none_index.html')


# страница входа получила данные т.е. ввели какой-то логин или пароль
# протестировано и заебато
@app.route('/login', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        login, password = request.form['login'], request.form['password']
        print(login, password)
        answer = get_company(login, password)
        print(answer)
        if answer:
            session['company_id'] = answer[0]
            print(session)
            if 'route' in session:
                return redirect(session['route'])
            else:
                return render_template('index.html', company_name=get_company_name(session['company_id']))
        else:
            message = "Логин или пароль неправильный!"
            return render_template('none_index.html', mes=message)
    else:
        message = "Введите логин и пароль"
        return render_template('none_index.html', mes=message)


# калитка
@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')


# страница для ввода данных о компании
@app.route('/company', methods=['GET', 'POST'])
def company_add():
    if request.method == 'POST':
        name = request.form['name']
        login = request.form['login']
        password = request.form['password']
        answer = add_company(name, login, password)
        #
        result = get_company(login, password)
        print(result)
        #
        return render_template('index.html')
    else:
        return render_template('company.html')


# страница для ввода данных о должностях
# ГЕНЕРИРУЕТ КОД HTML ДЛЯ ВЫБОРА СИСТЕМЫ ПООЩЕРЕНИЙ
# данные берет из БД
# ТРЕБУЕТ ТЕСТОВ но теоретически все заебись
@app.route('/add_positions', methods=['GET', 'POST'])
def positions_add():
    if request.method == 'POST':
        position_name = request.form['position_name']
        salary = float(request.form['salary'])
        function_id = int(request.form['functions_id'])
        if add_position(position_name, salary, function_id, session['company_id']):
            message = f"Должность '{position_name}' добавлена "
            return render_template('add_position.html', mess=message, html=get_data_function())
        else:
            message = f"Ошибка! Должность '{position_name}' не была добавлена. "
            return render_template('add_position.html', mess=message, html=get_data_function())
    else:

        return render_template('add_position.html', html=get_data_function())


def get_data_function():
    data = list()
    sql = get_all_functions()
    for iter, value in enumerate(sql):
        data.append((iter + 1, value[2]))
    return data


# страница введения данных для сотрудников
@app.route('/add_employee', methods=['GET', 'POST'])
def employe_add():
    if 'company_id' in session:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            position_id = int(request.form['position_id'])
            function_id = get_function_id_by_position_id(position_id)
            if add_employee(name, email, phone, position_id, function_id):
                message = f"Сотруник '{name}' успешно добавлен"
                return render_template('add_employee.html', mes=message, html=get_data_position(),
                                       company=get_company_name(session['company_id']))
            else:
                message = f"Ошибка! Сотруник '{name}' не был добавлен"
                return render_template('add_employee.html', mes=message, html=get_data_position(),
                                       company=get_company_name(session['company_id']))

        else:
            message = "Введите данные для нового сотрудника"
            return render_template('add_employee.html', mes=message, html=get_data_position(),
                                   company=get_company_name(session['company_id']))
    else:
        session['route'] = '/add_employee'
        message = "Войдите в свой аккаунт"
        return render_template('none_index.html', mes=message)


def get_data_position():
    data = list()
    sql = get_all_positions()
    for iter, value in enumerate(sql):
        data.append((iter + 1, value[1]))
    return data


"""
ЕСЛИ GET :
1. открывает -> 'section_a.html'
ЕСЛИ POST :
1. перебирает все инпуты по всем разделам
2. сохраняет все значения в 5 списков 
>> titles, weights, ranges_min, ranges_max, coefs
* ranges_min, ranges_max, coefs - двумерные списки 
"""


@app.route('/section_a', methods=['GET', 'POST'])
def section_a_input():
    if request.method == 'POST':
        titles, weights, ranges_min, ranges_max, coefs = list(), list(), list(), list(), list()
        parse = True
        iter_main, iter = 1, 1
        while parse:
            if request.form.get(f"title{iter_main}") is not None:
                titles.append(request.form.get(f"title{iter_main}"))
                weights.append(float(request.form.get(f"weight{iter_main}")))
                ranges_min.append(list())
                ranges_max.append(list())
                coefs.append(list())
                while True:
                    if request.form.get(f"range_min{iter_main}_{iter}") is not None:
                        ranges_min[iter_main - 1].append(float(request.form.get(f"range_min{iter_main}_{iter}")))
                        ranges_max[iter_main - 1].append(float(request.form.get(f"range_max{iter_main}_{iter}")))
                        coefs[iter_main - 1].append(float(request.form.get(f"coef{iter_main}_{iter}")))
                        iter += 1
                    else:
                        iter = 1
                        break
                iter_main += 1
            else:
                parse = False
                break
        print("breakpoint")
        if insert_coefs_a(titles, weights, ranges_min, ranges_max, coefs) == 1:
            message = "Дані збережено!"
            return render_template('section_a.html', alert=message)
        else:
            message = "Виникла помилка. Перевірте дані!"
            return render_template('section_a.html', alert=message)
    else:
        return render_template('section_a.html')


"""
ЕСЛИ GET :
1. открывает -> 'section_b.html'
ЕСЛИ POST :
1. перебирает все инпуты по всем разделам
2. сохраняет все значения в 2 списка и 3 переменные
"""


@app.route('/section_b', methods=['GET', 'POST'])
def section_b_input():
    if request.method == 'POST':
        titles, weights = list(), list()
        parse = True
        line_num = 1
        while parse:
            if request.form.get(f"title{line_num}") is not None:
                titles.append(request.form.get(f"title{line_num}"))
                weights.append(float(request.form.get(f"weight{line_num}")))
                line_num += 1
            else:
                parse = False
                break
        range_min = int(request.form.get("range_min"))
        range_max = int(request.form.get("range_max"))
        coef = int(request.form.get("coef"))
        if insert_coefs("b", titles, weights, range_min, range_max, coef) == 1:
            message = "Дані збережено!"
            return render_template('section_b.html', alert=message)
        else:
            message = "Виникла помилка. Перевірте дані!"
            return render_template('section_b.html', alert=message)
    else:
        return render_template('section_b.html')


"""
ЕСЛИ GET :
1. открывает -> 'section_c.html'
ЕСЛИ POST :
1. перебирает все инпуты по всем разделам
2. сохраняет все значения в 2 списка и 3 переменные
"""


@app.route('/section_c', methods=['GET', 'POST'])
def section_c_input():
    if request.method == 'POST':
        titles, weights = list(), list()
        parse = True
        line_num = 1
        while parse:
            if request.form.get(f"title{line_num}") is not None:
                titles.append(request.form.get(f"title{line_num}"))
                weights.append(float(request.form.get(f"weight{line_num}")))
                line_num += 1
            else:
                parse = False
                break
        range_min = int(request.form.get("range_min"))
        range_max = int(request.form.get("range_max"))
        coef = int(request.form.get("coef"))
        if insert_coefs("c", titles, weights, range_min, range_max, coef) == 1:
            message = "Дані збережено!"
            return render_template('section_c.html', alert=message)
        else:
            message = "Виникла помилка. Перевірте дані!"
            return render_template('section_c.html', alert=message)
    else:
        return render_template('section_c.html')


@app.route('/view_coefficients', methods=['GET'])
def view_coefficients():
    return render_template('view_coefficients.html', section_a_targets=get_coefficients_a(1),
                           section_b_targets=get_coefficients_b(1), section_c_targets=get_coefficients_c(1))


@app.route('/view_positions', methods=['GET'])
def view_positions():
    return render_template('view_positions.html', positions=get_all_positions())


@app.route('/view_employees', methods=['GET'])
def view_employee():
    return render_template('view_employees.html', employees=get_all_employees())

@app.route('/section_abc', methods=['GET', 'POST'])
def section_abc():
    if 'company_id' in session:
        if request.method == 'POST':

            #a
            titles_a, weights_a, ranges_min_a, ranges_max_a, coefs_a = list(), list(), list(), list(), list()
            coefs_abc_weight = [float(request.form.get(f"abc_weight1")),
                                float(request.form.get(f"abc_weight2")),
                                float(request.form.get(f"abc_weight3"))]
            parse = True
            iter_main, iter = 1, 1
            while parse:
                if request.form.get(f"title{iter_main}") is not None:
                    titles_a.append(request.form.get(f"title{iter_main}"))
                    weights_a.append(float(request.form.get(f"weight{iter_main}")))
                    ranges_min_a.append(list())
                    ranges_max_a.append(list())
                    coefs_a.append(list())
                    while True:
                        if request.form.get(f"range_min{iter_main}_{iter}") is not None:
                            ranges_min_a[iter_main - 1].append(float(request.form.get(f"range_min{iter_main}_{iter}")))
                            ranges_max_a[iter_main - 1].append(float(request.form.get(f"range_max{iter_main}_{iter}")))
                            coefs_a[iter_main - 1].append(float(request.form.get(f"coef{iter_main}_{iter}")))
                            iter += 1
                        else:
                            iter = 1
                            break
                    iter_main += 1
                else:
                    parse = False
                    break
            #
            #b
            titles_b, weights_b = list(), list()
            parse = True
            line_num = 1
            while parse:
                if request.form.get(f"title{line_num}_b") is not None:
                    titles_b.append(request.form.get(f"title{line_num}_b"))
                    weights_b.append(float(request.form.get(f"weight{line_num}_b")))
                    line_num += 1
                else:
                    parse = False
                    break
            range_min_b = int(request.form.get("range_min_b"))
            range_max_b = int(request.form.get("range_max_b"))
            coef_b = float(request.form.get("coef_b"))
            #
            #c
            titles_c, weights_c = list(), list()
            parsing = True
            line_num = 1
            while parsing:
                if request.form.get(f"title{line_num}_c") is not None:
                    titles_c.append(request.form.get(f"title{line_num}_c"))
                    weights_c.append(float(request.form.get(f"weight{line_num}_c")))
                    line_num += 1
                else:
                    parsing = False
                    break
            range_min_c = int(request.form.get("range_min_с"))
            range_max_c = int(request.form.get("range_max_с"))
            coef_c = float(request.form.get("coef_с"))
            #c
            result =  coef_abc_add(coefs_abc_weight,
                                     titles_a,
                                     weights_a,
                                     ranges_min_a,
                                     ranges_max_a,
                                     coefs_a,
                                     titles_b,
                                     weights_b,
                                     range_min_b,
                                     range_max_b,
                                     coef_b,
                                     titles_c,
                                     weights_c,
                                     range_min_c,
                                     range_max_c,
                                     coef_c)
            if result:
                session['coefficient_id'] = result[0]
                alert = "Запись добавлена! Укажите название функции"
                return render_template('add_function.html', alert=alert)
            else:
                alert = "Ошибка"
                return render_template('section_abc.html', alert=alert)
        else:
            return render_template('section_abc.html')
    else:
        session['route'] = '/section_abc'
        alert = 'Авторизуйся'
        return render_template('none_index.html', alert=alert)

@app.route('/add_function', methods=['GET', 'POST'])
def add_function():
    if 'company_id' in session:
        if request.method == 'POST':
            if 'coefficient_id' in session:
                res = add_function_sql(session['coefficient_id'],request.form.get("function_name"))
                if res:
                    del session['coefficient_id']
                    alert = 'Функция добавлена !'
                    return render_template('index.html', alert=alert)
        else:
            pass
    else:
        session['route'] = '/section_abc'
        alert = 'Авторизуйся'
        return render_template('none_index.html', alert=alert)

@app.route('/add_report', methods=['GET', 'POST'])
def add_report():
    if 'company_id' in session:
        if request.method == 'POST':
           pass

        else:
            html = get_positions(session['company_id'])
            if html:
                return render_template('add_report.html', html=html)
            else:
                return render_template('add_report.html', html=[[999,'должности не созданы']])
    else:
        session['route'] = '/section_abc'
        alert = 'Авторизуйся'
        return render_template('none_index.html', alert=alert)

if __name__ == "__main__":
    drop_all()
    create_db()
    fill_db()
    create_me()
    #res = coefs(get_coef(4))
    #print(res.coefficients_id)
    app.run()
