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

def check_query_one(instance):
    params = []
    params = query_params_array(instance)
    positive_values = []
    for p in params:
        if getattr(instance, p) == None:
            print(p, getattr(instance, p)) 
        else:
            positive_values.append(p)
    return positive_values

def check_query_instance(instance):
    if instance == None:
      return False
    elif hasattr(instance, '__iter__'):
        for i in instance:
            check_query_one(i)
    else:
        check_query_one(instance)  





