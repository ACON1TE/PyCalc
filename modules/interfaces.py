# Дата-класс для коэфициентов
class coefs:
    def __init__(self, sql_response:tuple):
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