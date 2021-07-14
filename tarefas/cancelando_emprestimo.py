#!/usr/bin/env python
# coding: utf-8

# Script para cancelar emprestimos da poloniex que estão parados a um tempo
# 2020/05/08

import datetime
import yaml
import sqlite3

import sys
caminho = sys.path[0]
sys.path.append(caminho.replace(caminho.split('\\')[-1],'Modulo'))
from poloniex_class import Poloniex_Loan

# encontro caminho para o banco
db_polo = caminho.replace(caminho.split('\\')[-1],'db') + '\\db_poloniex.db'


caminho_conf = caminho.replace(caminho.split('\\')[-1],'') + 'poloniex_config.yaml'
conf =  yaml.full_load(open(caminho_conf))


conf_min_cancelamento = conf['Minutos_cancelamento']
key    = conf['Chaves']['key']
secret = conf['Chaves']['secret']

if __name__ =='__main__':
    loan = Poloniex_Loan(key,secret)
    loan.get_open_LoanOffer()
    for cripto in loan.open_loan_offer:
        for  i in loan.open_loan_offer[cripto]:
            i['date'] = datetime.datetime.strptime(i['date'] ,'%Y-%m-%d %H:%M:%S')
            i['time_delta'] = (datetime.datetime.utcnow() - i['date']).seconds
        
            if i['time_delta'] > 60*int(conf_min_cancelamento):
                loan.cancel_LoanOffer(i['id'])

                conn = sqlite3.connect(db_polo)
                # conecto ao banco
                cursor = conn.cursor()

                cursor.execute('''UPDATE orders_lending SET  status="canceled"
                	              WHERE orderID = {}
                	              AND currencyPair = "{}" '''.format(i['id'], cripto))                

                conn.commit()
                conn.close()