# -*- coding: utf-8 -*-
"""
    Importação e parser do usuário
"""
import csv
import re
import os

from neo4j import GraphDatabase
from logger import *

def main():

	# conexão com o banco
	try:
	    driver = GraphDatabase.driver("bolt://172.21.0.2:7687", auth=("neo4j", "201125"))

	    logger.info("Conexão efetuada com sucesso!")
	except Exception as e:
	    logger.error("Houve erro ao efetuar a conexão com o banco. Erro: {0}".format(e))

	# path onde se encontra o csv
	filename = os.path.dirname(os.path.abspath(__file__)) + '/user-books.csv'

	user_dict = {}
	list_users = []
	# leitura do csv
	try:
		# abro a sessão do banco
	    with open(filename, 'r') as userscsv:
	    	users = csv.reader(userscsv, delimiter=',', quotechar='|')
	    	next(users)

	    	dbg = driver.session()

	    	for user in users:
	    		user_dict = {"name": user[0], "op_1": user[1], "op_2": user[2], "op_3": user[3]}
	    		name = user_dict["name"].replace(" ", "")
	    		
	    		ret = dbg.run("CREATE (" + name + ":User {name:'" + user_dict['name'] + "'})," + 
                    "("+ user_dict['op_1'] +":Book {genre:'"+ user_dict['op_1'] +"'}), " +
                    "("+ user_dict['op_2'] +":Book {genre:'"+ user_dict['op_2'] +"'}), " +
                    "("+ user_dict['op_3'] +":Book {genre:'"+ user_dict['op_3'] +"'}), " +
                    "("+ name +")-[:LIKES]->(" + user_dict['op_1'] + "), "  + 
                    "("+ name +")-[:LIKES]->(" + user_dict['op_2'] + "), "  + 
                   	"("+ name +")-[:LIKES]->(" + user_dict['op_3'] + ")")

	    	logger.info("Sucesso ao gravar no banco!")
			# fechando sessão
	    	dbg = driver.close()
	except Exception as e:
	    logger.error("Houve erro ao ler o arquivo de CSV. Erro: {0}".format(e))


if __name__ == '__main__':
    main()