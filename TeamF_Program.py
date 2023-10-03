import tkinter as tk
import cexprtk
import math


### MODEL FUNCTIONS

input_field = '' # integral function
input_upper = '' # upper limit
input_lower = '' # lower limit
N = 5 # number of trapezoids

def parse_expression(expression):
    expression = expression.replace('pow', 'math.pow') # replace exponential symbol
    expression = expression.replace('log', 'math.log')
    expression = expression.replace('π', 'pi')
    expression = expression.replace('sin', 'math.sin')
    expression = expression.replace('cos', 'math.cos')
    expression = expression.replace('tan', 'math.tan')
    return expression

def compute_width_per_trapezoid(upper_lim, lower_lim, n):
    return (upper_lim - lower_lim) / n

def trapezoidal_rule(y, width, N):
    # formula to get integral using trapezoidal rule of integration
    # = (width / 2) * (y[0] + 2(y[1] + y[2] + ... + y[n - 2] + y[n - 1]) + y[n])
    sum_of_inner_heights = 0
    for i in range(1, N):
        sum_of_inner_heights += y[i]

    return (width / 2) * (y[0] + 2 * sum_of_inner_heights + y[N])

def compute_integral(parsed_expression, upper_lim, lower_lim, N):
    upper_lim = parse_expression(upper_lim)
    upper_lim = cexprtk.evaluate_expression(upper_lim, {'pi' : math.pi, 'e' : math.e})
    lower_lim = parse_expression(lower_lim)
    lower_lim = cexprtk.evaluate_expression(lower_lim, {'pi' : math.pi, 'e' : math.e})

    # calculate width per trapezoid
    width = compute_width_per_trapezoid(upper_lim, lower_lim, N)
    x = []

    # calculate values of x iteratively using lower limit and width
    for i in range(N + 1):
        x.append(i * width + lower_lim)

    # calculate values of y iteratively using values of x and the given expression
    y = [0 for i in range(N + 1)]
    for i in range(N + 1): # n + 1 total x points will be used
        y[i] = cexprtk.evaluate_expression(parsed_expression, {'x' : x[i], 'pi' : math.pi, 'e' : math.e})

    # calculate integral using trapezoidal rule
    return trapezoidal_rule(y, width, N)



### VIEW (GUI) FUNCTIONS

def add_to_field(symbol):
    widget = window.focus_get()
    if(widget == window):
        widget = field
    widget.insert('insert', str(symbol)) # insert new expression into field

def calculate():
    global input_field, input_lower, input_upper, N
    input_field = field.get('1.0', 'end')
    input_lower = field_lower.get('1.0', 'end')
    input_upper = field_upper.get('1.0', 'end')
    N = int(field_N.get('1.0', 'end'))
    parsed_expression = parse_expression(input_field)

    result = compute_integral(parsed_expression, input_upper, input_lower, N) # calculate result 
    field.delete('1.0', 'end') # modify gui: delete expression from field
    field_lower.delete('1.0', 'end') # modify gui: delete expression from field
    field_upper.delete('1.0', 'end') # modify gui: delete expression from field
    field_N.delete('1.0', 'end') # modify gui: delete expression from field
    field.insert('1.0', result) # modify gui: insert the result into field

def delete_one():
    widget = window.focus_get()
    if(widget == window):
        widget = field
    reduced_field = widget.get('1.0', 'end')[:-1]
    widget.delete('1.0', 'end')
    new_input = reduced_field[:-1]
    widget.insert('1.0', new_input)

def clear():
    global input_field, input_upper, input_lower, N
    input_field = '' # empty input field
    input_upper = ''
    input_lower = ''
    N = 5
    field.delete('1.0', 'end') # modify gui: delete the expression from field
    field_lower.delete('1.0', 'end')
    field_upper.delete('1.0', 'end')
    field_N.delete('1.0', 'end')


# set up window of gui
window = tk.Tk()
window.geometry("340x570")
window.resizable(False, False)
window.title('Trapezoid Rule')
window.config(bg = '#242424')

# add text field to window to allow input of expressions
l1 = tk.Label(window, text = "Enter Integral Function:", font = 'Helvetica 12 bold', pady = 5, bg = '#242424', fg = '#dadada')
l1.grid(row = 1, column = 1, columnspan = 4, pady = (5, 0))
field = tk.Text(window, height = 5, width = 42, font = ("Helvetica", 11), bg = '#dadada', fg = '#242424')
field.grid(row = 2, column = 1, columnspan = 4) # place the field on the specified coordinates

# place labels for lower and upper limit inputs
l2 = tk.Label(window, text = "Upper Limit:", font = 'Helvetica 12 bold', bg = '#242424', fg = '#dadada')
l2.grid(row = 4, column = 1, columnspan = 2, pady = (10, 0))
l3 = tk.Label(window, text = "Lower Limit:", font = 'Helvetica 12 bold', bg = '#242424', fg = '#dadada')
l3.grid(row = 4, column = 3, columnspan = 2, pady = (10, 0))

# place fields for lower and upper limits
field_upper = tk.Text(window, height = 2, width = 13, font = ("Helvetica", 11), bg = '#dadada', fg = '#242424')
field_upper.grid(row = 5, column = 1, columnspan = 2, pady = (0, 15)) # place the field on the specified coordinates
field_lower = tk.Text(window, height = 2, width = 13, font = ("Helvetica", 11), bg = '#dadada', fg = '#242424')
field_lower.grid(row = 5, column = 3, columnspan = 2, pady = (0, 15)) # place the field on the specified coordinates

# place label for number of trapezoids
l4 = tk.Label(window, text = "Number of Trapezoids:", font = 'Helvetica 12 bold', bg = '#242424', fg = '#dadada')
l4.grid(row = 6, column = 1, columnspan = 4, pady = (0, 0))

# place fields for number of trapezoids
field_N = tk.Text(window, height = 2, width = 13, font = ("Helvetica", 11), bg = '#dadada', fg = '#242424')
field_N.grid(row = 7, column = 1, columnspan = 4, pady = (0, 15)) # place the field on the specified coordinates

# create buttons
btns = [['' for x in range(4)] for y in range(7)]
btns[0][0] = tk.Button(window, text = 'sin()', command = lambda: add_to_field('sin(rad)'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[0][1] = tk.Button(window, text = 'cos()', command = lambda: add_to_field('cos(rad)'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[0][2] = tk.Button(window, text = 'tan()', command = lambda: add_to_field('tan(rad)'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[0][3] = tk.Button(window, text = 'DEL', command = lambda: delete_one(), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[1][0] = tk.Button(window, text = 'log()', command = lambda: add_to_field('log(x, a)'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[1][1] = tk.Button(window, text = 'ln()', command = lambda: add_to_field('log(x)'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[1][2] = tk.Button(window, text = 'pow', command = lambda: add_to_field('pow(x, exp)'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[1][3] = tk.Button(window, text = 'x', command = lambda: add_to_field('x'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[2][0] = tk.Button(window, text = 'e', command = lambda: add_to_field('e'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[2][1] = tk.Button(window, text = 'π', command = lambda: add_to_field('π'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[2][2] = tk.Button(window, text = '(-)', command = lambda: add_to_field('-'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[2][3] = tk.Button(window, text = '√', command = lambda: add_to_field('^ (1/2)'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[3][0] = tk.Button(window, text = '7', command = lambda: add_to_field('7'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[3][1] = tk.Button(window, text = '8', command = lambda: add_to_field('8'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[3][2] = tk.Button(window, text = '9', command = lambda: add_to_field('9'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[3][3] = tk.Button(window, text = '/', command = lambda: add_to_field(' / '), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[4][0] = tk.Button(window, text = '4', command = lambda: add_to_field('4'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[4][1] = tk.Button(window, text = '5', command = lambda: add_to_field('5'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[4][2] = tk.Button(window, text = '6', command = lambda: add_to_field('6'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[4][3] = tk.Button(window, text = '*', command = lambda: add_to_field(' * '), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[5][0] = tk.Button(window, text = '1', command = lambda: add_to_field('1'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[5][1] = tk.Button(window, text = '2', command = lambda: add_to_field('2'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[5][2] = tk.Button(window, text = '3', command = lambda: add_to_field('3'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[5][3] = tk.Button(window, text = '-', command = lambda: add_to_field(' - '), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[6][0] = tk.Button(window, text = '0', command = lambda: add_to_field('0'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[6][1] = tk.Button(window, text = '(', command = lambda: add_to_field('('), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[6][2] = tk.Button(window, text = ')', command = lambda: add_to_field(')'), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btns[6][3] = tk.Button(window, text = '+', command = lambda: add_to_field(' + '), width = 5, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')

# add each button to the grid
for row in range(8, 15):
    for col in range(1, 5):
        btns[row - 8][col - 1].grid(row = row, column = col)

# add submit and clear button
btn_submit = tk.Button(window, text='Calculate', command = lambda: calculate(), width = 9, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btn_submit.grid(row = 15, column = 1, columnspan = 2, pady = (15, 0))

btn_submit = tk.Button(window, text='AC', command = lambda: clear(), width = 9, font = ('Helvetica', 11), bg = '#474747', fg = '#dadada')
btn_submit.grid(row = 15, column = 3, columnspan = 2, pady = (15, 0))

# launch app
print("Trapezoid Rule of Integration Calculator Now Running...")
window.mainloop()