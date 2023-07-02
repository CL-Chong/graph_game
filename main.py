import sympy
from sympy import symbols, diff, sin, cos, exp, log, latex, expand
import numpy as np


def generate_text(feature_type, feature_value):
    # text = generate_text(feature_type,feature_value)
    # inputs: feature_type - string for feature type. Accept: 'x_intercept','y_intercept','local_min','local_max'
    #         feature_value - numerical value for feature
    # output: text - string of text for corresponding insturction
    if feature_type == "x_intercept":
        text = "intersects the x-axis at " + "x = " + str(feature_value)
    elif feature_type == "y_intercept":
        text = "intersects the y-axis at " + "y = " + str(feature_value)
    elif feature_type == "local_min":
        text = "has a local minimum at " + "x = " + str(feature_value)
    elif feature_type == "local_max":
        text = "has a local maximum at " + "x = " + str(feature_value)

    return text


def generate_question(n_criteria):
    # criteria_type, criteria_value = generate_question(n_criteria)
    # input: n_criteria - number of criteria for the polynomial
    # outputs: criteria_type - n_criteria sized array containing strings for criteria type
    #          criteria_value - n_criteria sized array containing numerical values for criteria
    criteria_type = []
    criteria_value = np.array([], dtype=np.int8)
    # check if we use y-intercept
    if np.random.rand() < 0.5:
        criteria_type.append("y_intercept")
        criteria_value = np.append(criteria_value, np.random.randint(-5, 6))
        n_criteria -= 1
    # check how many x-intercept we use
    n_x_intercept = np.random.randint(0, n_criteria + 1)
    if n_x_intercept > 0:
        for k in range(n_x_intercept):
            criteria_type.append("x_intercept")
        x_values = np.random.permutation(np.arange(-5, 6))[:n_x_intercept]
        criteria_value = np.append(criteria_value, x_values)
    # check how many local min or local max we use
    n_min_max = n_criteria - n_x_intercept
    if n_min_max > 0:
        for k in range(n_min_max):
            if np.random.rand() < 0.5:
                criteria_type.append("local_min")
            else:
                criteria_type.append("local_max")
        x_values = np.random.permutation(np.arange(-5, 6))[:n_min_max]
        criteria_value = np.append(criteria_value, x_values)

    return criteria_type, criteria_value


def check_answer(answer, criteria_type, criteria_value):
    # inputs: answer - sympy string containing answer polynomial
    #         criteria_type - n_criteria sized array containing strings for criteria type
    #         criteria_value - n_criteria sized array containing numerical values for criteria
    n_criteria = len(criteria_type)
    d_answer = diff(answer, x)
    dd_answer = diff(d_answer, x)
    for k in range(n_criteria):
        type = criteria_type[k]
        value = criteria_value[k]
        if type == "x_intercept":
            if answer.subs(x, value) != 0:
                print("Sorry, wrong answer!")
                return 0
        if type == "y_intercept":
            if answer.subs(x, 0) != value:
                print("Sorry, wrong answer!")
                return 0
        if type == "local_min":
            if d_answer.subs(x, value) != 0 or dd_answer.subs(x, value) <= 0:
                print("Sorry, wrong answer!")
                return 0
        if type == "local_max":
            if d_answer.subs(x, value) != 0 or dd_answer.subs(x, value) >= 0:
                print("Sorry, wrong answer!")
                return 0
    print("Well done!")
    return 1


x = symbols("x")
while True:
    try:
        n_criteria = int(input("Enter the number of conditions: "))
        if n_criteria <= 0:
            continue
        break
    except ValueError:
        pass
criteria_type, criteria_value = generate_question(n_criteria)
# print(criteria_type)
# print(criteria_value)
print("Give me a polynomial in x that")
for k in range(n_criteria):
    type = criteria_type[k]
    value = criteria_value[k]
    if type == "x_intercept":
        text = str(k + 1) + ". intersects the x-axis at x = " + str(value)
    if type == "y_intercept":
        text = str(k + 1) + ". intersects the y-axis at y = " + str(value)
    if type == "local_min":
        text = str(k + 1) + ". has a local minimum at x = " + str(value)
    if type == "local_max":
        text = str(k + 1) + ". has a local maximum at x = " + str(value)
    print(text)
while True:
    while True:
        answer_raw = input("Enter your polynomial here: ")
        try:
            answer = sympy.sympify(answer_raw)
            break
        except (ValueError, TypeError):
            print("Incorrect format. Please try again.")
    result = check_answer(answer, criteria_type, criteria_value)
    if result == 0:
        yn = input("Retry question? (Enter Y to retry, any other key to skip) ")
        if yn != "Y":
            break
    if result == 1:
        break
