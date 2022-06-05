from ast import Num


def month_from_number(number):
    switcher = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"       
    }
    return switcher.get(number, "Invalid Month")

#Function that takes a variable created from a SQLAlchemy query to the database and returns an array of the parameters.
def query_params_array(query_var):
    params = []
    for v in vars(query_var):
        params.append(v)
    return params

#Takes one query object and the array of parameters created above then prints None values and returns positive values
#as an array with value pairs to identify the None values.
def check_query_one(instance):
    if instance == None:
        return instance, 'Empty Query Object'
    else:
        params = []
        params = query_params_array(instance)
        positive_values = []
        none_values = []
        for p in params:
            if getattr(instance, p) == None:
                none_values.append([p, getattr(instance, p)]) 
            else:
                positive_values.append(p)
        return positive_values, none_values


def check_if_float_onerow(instance):
    if instance == None:
        return False
    else:
        params = []
        params = query_params_array(instance)
        float_values = []
        total = 0
        for p in params:
            if type(getattr(instance, p)) == float:
                print(p, getattr(instance, p))
                total += getattr(instance, p)
        print(total)

def check_query_instance(instance):
    if instance == None:
      return False
    elif hasattr(instance, '__iter__'):
        for i in instance:
            check_query_one(i)
    else:
        check_query_one(instance)  







