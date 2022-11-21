import json
import numpy as np
import scipy as sp
import pandas as pd
from scipy.optimize import linprog

f = open('bafra.json')
data = json.load(f)
f.close()

c = data['coefficients']
a = []
b = []
for i in data['matrices']:
  a.append(i['coefficients'])  
  b.append(i['source'])

bounds = tuple([(0, None)] * len(data['coefficients']))
result = linprog([-x for x in c], A_ub=a, b_ub=b, A_eq=None, b_eq=None, bounds=None, method='simplex', callback=None, options={'maxiter': 5000, 'disp': False, 'presolve': True, 'tol': 1e-12, 'autoscale': True, 'rr': True, 'bland': False}, x0=None)

if result.success:
    print ("{:<25} {:<20} {:<20}".format('Variable','Value','Original Value'))
    for i, variable in enumerate(data['decision_variables']):
        value = result.x[i]
        original_value = data['coefficients'][i]
        print ("{:<25} {:<20} {:<20}".format(variable, "%.2f" % value, "%.2f" % original_value))

    print("\n")
    print ("{:<25} {:<20} {:<20}".format('Contraint', 'Slack','Original Value'))
    for i, matrice in enumerate(data['matrices']):
        constraint = matrice['name']
        original_value = matrice['source']
        slack = result.slack[i]
        print ("{:<25} {:<20} {:<20}".format(constraint, "%.2f" % slack, "%.2f" % original_value))
else:
    print(result)