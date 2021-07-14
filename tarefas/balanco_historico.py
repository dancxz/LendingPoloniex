#!/usr/bin/env python
# coding: utf-8
import yaml
import time
import datetime

import sqlite3
import pandas as pd

# Reconheco caminho da pasta
import sys
caminho = sys.path[0]

# gero novo caminho para importar as funcoes poloniex
sys.path.append(caminho.replace(caminho.split('\\')[-1],'Modulo'))
from poloniex_class import Poloniex_Loan

# encontro caminho para o banco
db_polo = caminho.replace(caminho.split('\\')[-1],'db') + '\\db_poloniex.db'



caminho_conf = caminho.replace(caminho.split('\\')[-1],'') + 'poloniex_config.yaml'
conf =  yaml.full_load(open(caminho_conf))

key    = conf['Chaves']['key']
secret = conf['Chaves']['secret']


def get_ultima_data():
  conn = sqlite3.connect(db_polo)
  ultima_data = conn.execute('''SELECT max(open)
    FROM Lending_History''')

  ultima_data = ultima_data.fetchall()[0][0]

  if ultima_data is None:
    ultima_data = '2016-12-01 00:00:00'
  
  ultima_data = datetime.datetime.strptime(ultima_data,'%Y-%m-%d %H:%M:%S')

  conn.close()

  return ultima_data


# Defino novo start e um end
# Start sendo D-1 da ultima data encontrada no banco
# End sendo + 15 dias do start se end maior q hj end vira agora
start  = get_ultima_data() - datetime.timedelta(1)
end = start + datetime.timedelta(60)

if end > datetime.datetime.now():
    end = datetime.datetime.now()
    
start = time.mktime(start.timetuple())
end = time.mktime(end.timetuple())


# Crio a class para consulta o historico
loan = Poloniex_Loan(key,secret)

# Gero historico do periodo de data
# onde loan.LendingHistory é o historico em json
loan.get_lending_History(start_date=start, end_date=end,limite=1000)

# formo recuros para salvar os dados no banco
list_historico = []
for his in loan.LendingHistory:
    list_historico.append((his['id'],
                           his['currency'],
                           float(his['rate']),
                           float(his['amount']),
                           float(his['duration']),
                           float(his['interest']),
                           float(his['fee']),
                           float(his['earned']),
                           his['open'],
                           his['close']))


conn = sqlite3.connect(db_polo)
# conecto ao banco
cursor = conn.cursor()

# gero um loop por toda lista de dados para
## dar o comando de execute
for i in list_historico:

    # inserindo dados na tabela
    cursor.execute("""
    INSERT OR REPLACE INTO Lending_History (id,currency,rate,amount,duration,interest,fee,earned,open,close)
    VALUES {}
    """.format(i))
conn.commit()
conn.close()