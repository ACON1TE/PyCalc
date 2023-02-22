# Дата-класс для коэфициентов
class coefs:
    def __init__(self, sql_response: tuple):
        self.coefficients_id = sql_response[0]
        self.coefs_abc_weight = sql_response[1]
        self.coef_a_names = sql_response[2]
        self.coef_a_name_weight = sql_response[3]
        self.coef_a_bottom_all_values = sql_response[4]
        self.coef_a_top_all_values = sql_response[5]
        self.coef_a_all_weights = sql_response[6]
        self.coef_b_names = sql_response[7]
        self.coef_b_name_weight = sql_response[8]
        self.coef_b_bottom_value = sql_response[9]
        self.coef_b_top_value = sql_response[10]
        self.coef_b_weight = sql_response[11]
        self.coef_c_names = sql_response[12]
        self.coef_c_name_weight = sql_response[13]
        self.coef_c_bottom_value = sql_response[14]
        self.coef_c_top_value = sql_response[15]
        self.coef_c_weight = sql_response[16]


# Дата-класс для записей в разделе A
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


# Дата-класс для записей в разделе Б и С
class TargetSecondType:
    def __init__(self, title: str, weight: float, range_min: int, range_max: int, range_coef: int):
        self.title = title
        self.weight = weight
        self.range_min = range_min
        self.range_max = range_max
        self.range_coef = range_coef


class report:
    def __init__(self, amount_plan, completed_amount, completed_quality, completed_task, budget_plan, budget_spend):
        self.amount_plan = amount_plan
        self.completed_amount = completed_amount
        self.completed_quality = completed_quality
        self.completed_task = completed_task
        self.budget_plan = budget_plan
        self.budget_spend = budget_spend


class calculated_report:
    def __init__(self, bonuses_abc_sum_list, bonuses_a_coef_list, bonuses_b_coef_list, bonuses_c_coef_list):
        self.bonuses_abc_sum_list = bonuses_abc_sum_list
        self.bonuses_a_coef_list = bonuses_a_coef_list
        self.bonuses_b_coef_list = bonuses_b_coef_list
        self.bonuses_c_coef_list = bonuses_c_coef_list


class show_report_interface:
    def __init__(self, data):
        self.company_id = data[1]
        self.position_id = data[2]
        self.amount_plan = data[3]
        self.completed_amount = data[4]
        self.completed_quality = data[5]
        self.completed_task = data[6]
        self.budget_plan = data[7]
        self.budget_spend = data[8]
        self.bonuses_abc_sum_list = data[9]
        self.bonuses_a_coef_list = data[10]
        self.bonuses_b_coef_list = data[11]
        self.bonuses_c_coef_list = data[12]
