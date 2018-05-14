import pandas as pd


def read_instances():
    return pd.read_csv('instances/consumidores3.csv', delimiter=','), pd.read_csv('instances/fornecedores3.csv', delimiter=',')

