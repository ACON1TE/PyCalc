"""
скачать PostgreSQL - https://www.postgresql.org/download/windows/

версия бека - 0.5
"""

from modules.db_tools import *
from werkzeug.utils import redirect
from flask import Flask, request, session, render_template
#app.secret_key = 'A78Zrejn359854tjnsT98j/3yX R~XHH!jmN]LWXT'

app = Flask(__name__)
#app.secret_key = 'ахуенно секретный ключ'
#app['SESSION_COOKIE_NAME'] = 'наша хуйня'

app.config.update(
    #SECRET_KEY = 'ахуенно секретный ключ',
    SECRET_KEY = 'cookies1',
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
        login,password = request.form['login'],request.form['password']
        answer = get_company(login, password)
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
        salary = request.form['salary']
        functions_id = request.form['functions_id']
        if add_position(position_name, salary, functions_id):
            message = f"Должность '{position_name}' добавлена "
            return render_template('add_position.html', mess=message, html=get_data_function())
        else:
            message = f"Ошибка! Должность '{position_name}' не была добавлена. "
            return render_template('add_position.html', mess=message, html=get_data_function())
    else:

        return render_template('add_position.html', html=get_data_function())

def get_data_function():
    data = list()
    sql = get_function()
    for iter, value in enumerate(sql):
        data.append((iter + 1,value[2]))
    return data

# страница введения данных для должностей
@app.route('/get_positions', methods=['GET'])
def get_positions():
    return render_template('get_positions.html')


# страница введения данных для сотрудников
@app.route('/add_employee', methods=['GET', 'POST'])
def employe_add():
    if 'company_id' in session:
        if request.method == 'POST':
            message = "Сотрудник добавлен!"
            return render_template('index.html', mess=message)
        else:
            position, company = str(), str()
            sql = get_position()
            print("sql_position >> ", sql)
            for iter, value in enumerate(sql):
                position += f'<option value="{iter}" class="">{value[2]}</option>'
            message = "Введите данные для нового сотрудника"
            return render_template('add_employee.html', mes=message, html=get_data_position(), company=get_company_name(session['company_id']))
    else:
        session['route'] = '/add_employee'
        message = "Войдите в свой аккаунт"
        return render_template('none_index.html',mes=message)

def get_data_position():
    data = list()
    sql = get_position()
    for iter, value in enumerate(sql):
        data.append((iter + 1,value[2]))
    return data

# страница введения данных для сотрудников
@app.route('/get_employe', methods=['GET'])
def get_employe():
    return render_template('all_employe.html')


"""
ЕСЛИ GET :
1. открывает -> 'section_a.html'
ЕСЛИ POST :
1. перебирает все инпуты по всем разделам
2. сохраняет все значения в 5 списков 
>> titles, weights, ranges_min, ranges_max, coefs
* ranges_min, ranges_max, coefs - двумерные списки 
"""
@app.route('/section_abc', methods=['GET', 'POST'])
def section_abc():
    if 'company_id' in session:
        if request.method == 'POST':
            alert = "Запись добавлена!"
            return render_template('section_abc.html', alert=alert)
        else:
            return render_template('section_abc.html')
    else:
        session['route'] = '/section_abc'
        alert = 'Авторизуйся'
        return render_template('none_index.html', alert=alert)

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
    return render_template('view_coefficients.html', section_a_targets=get_coefficients_a(),
                           section_b_targets=get_coefficients_b(), section_c_targets=get_coefficients_c())

# тест сессии
# успешно
@app.route('/test', methods=['GET'])
def test_func():
    return render_template('1_test.html')

@app.route('/test_login', methods=['GET','POST'])
def test_login():
    if request.method == 'POST':
        res = test_auth(request.form['test_login'], request.form['test_password'])
        if res:
            session['auth'] = res[1]
            if 'route' in session:
                return redirect(session['route'])
            else:
                return render_template('1_test.html')
        else:
            alert = 'Неправильный логин или пароль'
            return render_template('1_test_login.html', alert=alert)
    else:
        return render_template('1_test_login.html')

@app.route('/test_check', methods=['GET'])
def test_check():
    if 'auth' in session:
        return render_template('1_test_check.html')
    else:
        session['route'] = '/test_check'
        alert = 'Авторизуйся'
        return render_template('1_test_login.html', alert=alert)

if __name__ == "__main__":
    #drop_all()
    #create_db()
    #fill_db(EMPLOYEE_NUM = 40)
    #cur.execute("insert into company(company_id,name,login,password) values(100,'ASH inc.', 'root','root')")
    #con.commit()

    app.run()