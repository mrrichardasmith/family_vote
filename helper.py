from sqlalchemy import false


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
def check_query_none_onerow(instance):
    if instance == None:
        return instance, 'Empty Query Object'
    else:
        params = []
        params = query_params_array(instance)
        none_values = []
        for p in params:
            if getattr(instance, p) == None:
                none_values.append([p, getattr(instance, p)])
        return none_values


def check_if_float_onerow(instance):
    if instance == None:
        return False
    else:
        params = []
        params = query_params_array(instance)
        float_values = {}
        for p in params:
            if type(getattr(instance, p)) == float:
                key = p
                value = getattr(instance, p)
                float_values.update({key:value})
        return float_values

def total_floats(object):
    total = 0
    if hasattr(object, '__iter__'):
        for float in object:
            total += object[float]
    return total
        

def check_query_instance(instance):
    if instance == None:
      return False
    elif hasattr(instance, '__iter__'):
        for i in instance:
            check_query_one(i)
    else:
        check_query_one(instance)  


def sum_combined_totals(combined_totals_arr):
      total = 0
      for t in combined_totals_arr:
        total += int(t)
      return(total)

# Function takes one of the multi line account queries and totals the cost of each line returning the total.
def sum_query_cost(account_query):
      total_cost = 0
      if account_query != None:
        for lineitem in account_query:
            if lineitem.cost != None:
                total_cost += lineitem.cost   
      return total_cost

def find_zero_balance(query):
    values = list(query.__dict__.values())
    keys = list(query.__dict__.keys())
    combined = zip(keys,values)
    list_combined = list(combined)
    zero_balance = [] 

    for c in list_combined:
      if c[-1] == 0.0:
        zero_balance.append(c)
    return zero_balance