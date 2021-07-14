#!/usr/bin/env python
# coding: utf-8

import hashlib
import hmac
import time
import requests




class Poloniex_Loan:
	def __init__(self,key,secret):
		self.key    = key
		self.secret = secret 

		self.url_api    = 'https://poloniex.com/tradingApi'

	def get_Loans_public(self,cripto):
		url = 'https://poloniex.com/public?command=returnLoanOrders&currency={}'.format(cripto)

		payload = {}

		headers = {
		'Accept': 'application/json',
		'Content-Type': 'application/json'
		}

		response = requests.request('GET', url, headers = headers, data = payload, timeout= 60.0)

		return response

	def balance_now(self):

		nonce = int(time.time() * 1000)
		data  = 'command=returnAvailableAccountBalances&nonce={}'.format(nonce)

		# Gera novo sing de comando com o secret
		signature = hmac.new(self.secret.encode(), data.encode(), digestmod=hashlib.sha512)

		headers = {'Content-Type': 'application/x-www-form-urlencoded',
		'Key' : self.key,
		'Sign': signature.hexdigest(),
		}

		balance = requests.request('POST', self.url_api, headers = headers, data = data)

		try:
			balance = balance.json()
			self.balance = balance['lending']
		except:
			self.balance = []

	def create_LoanOffer(self,cripto,amount,duration,rate):
		'''
		Cria uma nova oferta para o usuario
		'''

		nonce = int(time.time() * 1000)
		data  = 'command=createLoanOffer&currency={}&amount={}&duration={}&autoRenew=0&lendingRate={}&nonce={}'.format(cripto,amount,duration,rate,nonce)

		# Gera novo sing de comando comc secret
		signature = hmac.new(self.secret.encode(), data.encode(), digestmod=hashlib.sha512)

		headers = {'Content-Type': 'application/x-www-form-urlencoded',
		'Key' : self.key,
		'Sign': signature.hexdigest(),
		}

		result_create = requests.request('POST', self.url_api, headers = headers, data = data)

		return result_create


	def get_open_LoanOffer(self):
		'''
		Retorna as ofertas em abertos criadas pelo usuario
		'''

		nonce = int(time.time() * 1000)
		data  = 'command=returnOpenLoanOffers&nonce={}'.format(nonce)

		# Gera novo sing de comando comc secret
		signature = hmac.new(self.secret.encode(), data.encode(), digestmod=hashlib.sha512)

		headers = {'Content-Type': 'application/x-www-form-urlencoded',
		'Key' : self.key,
		'Sign': signature.hexdigest(),
		}

		open_loan_offer =  requests.request('POST', self.url_api, headers = headers, data = data)

		self.open_loan_offer = open_loan_offer.json()


	def cancel_LoanOffer(self,orderNumber):
		'''
		Cancela um oferta de loan
		'''

		nonce = int(time.time() * 1000)
		data  = 'command=cancelLoanOffer&orderNumber={}&nonce={}'.format(orderNumber,nonce)

		# Gera novo sing de comando comc secret
		signature = hmac.new(self.secret.encode(), data.encode(), digestmod=hashlib.sha512)

		headers = {'Content-Type': 'application/x-www-form-urlencoded',
		'Key' : self.key,
		'Sign': signature.hexdigest(),
		}

		return requests.request('POST', self.url_api, headers = headers, data = data)


	def get_active_LoanOffer(self):
		'''
		Retorna as ofertas em ativas do usuario
		'''

		nonce = int(time.time() * 1000)
		data  = 'command=returnActiveLoans&nonce={}'.format(nonce)

		# Gera novo sing de comando comc secret
		signature = hmac.new(self.secret.encode(), data.encode(), digestmod=hashlib.sha512)

		headers = {'Content-Type': 'application/x-www-form-urlencoded',
		'Key' : self.key,
		'Sign': signature.hexdigest(),
		}

		active_loan =  requests.request('POST', self.url_api, headers = headers, data = data)

		self.active_loan = active_loan.json()['provided']

	def get_lending_History(self,start_date,end_date=time.time(),limite=100):

		nonce = int(time.time() * 1000)
		data  = 'command=returnLendingHistory&start={}&end={}&limit={}&nonce={}'.format(start_date,end_date,limite,nonce)

		# Gera novo sing de comando comc secret
		signature = hmac.new(self.secret.encode(), data.encode(), digestmod=hashlib.sha512)

		headers = {'Content-Type': 'application/x-www-form-urlencoded',
		'Key' : self.key,
		'Sign': signature.hexdigest(),
		}

		LendingHistory =  requests.request('POST', self.url_api, headers = headers, data = data)

		self.LendingHistory = LendingHistory.json()