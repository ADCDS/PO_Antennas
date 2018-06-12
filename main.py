"""
    Adriel Cardoso dos Santos
    RA: 2015.1.08.001

    Implementação do modelo que resolve o problema de telecomunicações utilizando banda parcial

"""

from builtins import len

from docplex.mp.model import Model
from docplex.mp.utils import DOcplexException
import numpy as np
import sys

from read import read_instances

costumers, antennas = read_instances()


def is_adjacent(costumer, antenna):
    a = np.array((antenna['x'], antenna['y'], 1))
    b = np.array((costumer['x'], costumer['y'], 1))
    # print('{} <= {} '.format(np.linalg.norm(a - b), antenna['r']))
    return np.linalg.norm(a - b) <= antenna['r']


mdl = Model()
mdl.parameters.mip.display.set(5)
mdl.set_log_output(sys.stdout)

# decision variables
X = [mdl.binary_var('A_' + str(i)) for i in range(0, len(antennas))]

# Build the usage matrix
usage = [[mdl.continuous_var(0, 999999, name='U_' + str(i) + '_' + str(j))
          for j in range(0, len(antennas))]
         for i in range(0, len(costumers))]

# Usage constraints
for i in range(0, len(usage)):
    expr = 0
    for j in range(0, len(usage[i])):
        expr += usage[i][j]
    mdl.add(expr == costumers.loc[i]['d'])

# Only activated antennas should have usage
for j in range(0, len(usage[0])):
    expr = 0
    for i in range(0, len(usage)):
        expr += usage[i][j]
    mdl.add(X[j] * 999999 >= expr)

# Only adjacent antennas should be used by users
for i in range(0, len(usage)):
    for j in range(0, len(usage[i])):
        if not is_adjacent(costumers.loc[i], antennas.loc[j]):
            mdl.add(usage[i][j] == 0)

# Respect the antenna's limit
for j in range(0, len(usage[0])):
    expr = 0
    for i in range(0, len(usage[j])):
        expr += usage[i][j]
    mdl.add(expr <= antennas.loc[j]['l'])


# Objective function
obj = 0
for i in range(0, len(X)):
    obj += X[i] * antennas.loc[i]['c']

mdl.minimize(obj)

try:
    slv = mdl.solve()

    mdl.print_solution()

    # mdl.prettyprint()

    """
    for i in range(0, len(X)):
        print(slv[X[i]], end=" ")
    print('\n', end="")
    
    for i in range(0, len(usage)):
        for j in range(0, len(usage[i])):
            print(slv[usage[i][j]], end=" ")
        print('\n')
    """
    print('\n', end="")

except Exception as e:
    print("Exception")
    print(e)
