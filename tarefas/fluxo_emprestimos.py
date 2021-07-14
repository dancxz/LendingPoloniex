#!/usr/bin/env python
# coding: utf-8

import yaml
import sqlite3
import datetime

import sys
caminho = sys.path[0]
sys.path.append(caminho.replace(caminho.split('\\')[-1],'Modulo'))
from poloniex_class import Poloniex_Loan

# encontro caminho para o banco
db_polo = caminho.replace(caminho.split('\\')[-1],'db') + '\\db_poloniex.db'


caminho_conf = caminho.replace(caminho.split('\\')[-1],'') + 'poloniex_config.yaml'
conf =  yaml.full_load(open(caminho_conf))

conf_minimos = conf['Minimo']
key    = conf['Chaves']['key']
secret = conf['Chaves']['secret']

if __name__ =='__main__':

    #Formando classe e pegando os valores em balanço
    loan = Poloniex_Loan(key,secret)
    loan.balance_now()

    #For para tds as cripts disponiveis para emprestar
    for i in loan.balance:
        #Verifico se ja existe uma quantia minima para a cripto, se não existir crio com 0
        if i not in conf_minimos:
            conf_minimos[i] = 0

        #Agora capturo emprestimos em aberto de outros clientes, o segundo % de emprestimo e a quantidade disponivel para emprestar
        segundo_emprestimo=  loan.get_Loans_public(i).json()['offers'][1]
        rate_emrprestimo = segundo_emprestimo['rate']
        quantidade_cripto = float(loan.balance[i])
    
        #Se a quantidade for suficiente para emprestar continuo o processo
        if quantidade_cripto >= conf_minimos[i]:

            # Crio o emprestimo
            resultado = loan.create_LoanOffer(i,quantidade_cripto,2,rate_emrprestimo)

            try:
                resultado_json = resultado.json()

                

                #Em caso de encontrar o erro começo algumas etapas de tratamento
                if 'error' in resultado_json:

                    #Se for um erro de quantidade gero o limite e slavo no conf
                    if 'Amount must be at least' in  resultado_json['error']:
                        limite_minimo = resultado_json['error'].replace('Amount must be at least ','')

                        if limite_minimo.count('.')>1:
                            limite_minimo = limite_minimo[:-1]

                        print('%s adicionado ou limiete alterado'%i)
                        print('%s: Sem abaixo do valor minimo'%i)

                        conf_minimos[i]=float(limite_minimo)
                        with open(caminho_conf, 'w') as file:
                            documents = yaml.dump(conf, file)
                else:
                    orderID = resultado_json['orderID']
                    currencyPair = resultado_json['currencyPair']
                    status = 'created'
                    now = str(datetime.datetime.utcnow())
                    
                    valores = (orderID,currencyPair,float(rate_emrprestimo),quantidade_cripto,status,now)

                    conn = sqlite3.connect(db_polo)
                    # conecto ao banco
                    cursor = conn.cursor()
                    cursor.execute('''INSERT OR REPLACE INTO orders_lending (orderID,currencyPair,rate,amount,status,createAt)
                        VALUES {}'''.format(valores))

                    conn.commit()
                    conn.close()



            except:
                print('erro ao ler o json')
        
        else:
            print('%s: Sem abaixo do valor minimo'%i)