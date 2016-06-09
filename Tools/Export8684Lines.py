#encoding:utf-8 
import sqlite3
import sys
import re
import os
import string
import tarfile
import time
import  datetime
import json

'''
  Export 8684 网站公交数据 线路导出

'''

def object2dict(obj):
    #convert object to a dict
    d = {}
#    d['__class__'] = obj.__class__.__name__
#    d['__module__'] = obj.__module__
    d.update(obj.__dict__)
    return d



class Company:
	def __init__(self,  id1, name ):
		self.name = name
		self.id   = id1
	
class City:

	def __init__(self):
		self.companies  = [] 
		self.lines = []
		self.__stops = {}
		self.__refs = {}

		
	def dumpLines(self):
		for line in self.lines :
			print(line.name)

	def clear(self):
		self.__stops = None
		self.__refs = None


	def addLine( self , line ):
		self.lines.append(line)

	def addCompany( self , company ):
		find = self.findCompany(company)
		if find == None:
			length = len( self.companies ) + 1
			com  =   Company( "C"+ str(length) , company )
			self.companies.append( com )
			return com 

		return find 


	def findCompany( self , company ):
		for com in self.companies:
			if com.name == company :
				return com ;

		return None 


class Line:
	def __init__(self,  company , name, line , schedule, type1, note, price):
		self.company = company
		self.line  = line
		self.name  = name
		self.schedule = schedule
		self.note= note
		self.type = type1
		self.price = price


class DB:
	def __init__(self,  file):
		self.file = file
		self.conn = None
		self.open()

	def open( self):	
		self.conn = sqlite3.connect(self.file)
		self.conn.isolation_level = None
		return self.conn

	def close(self):
		if self.conn!=None:
			self.conn.close()
			self.conn = None

	def processLines(self , city ):
		
		cmd = 'SELECT * FROM CNBUSW order by ID ' 
		
		# ID, BUSW,  shijian, zxdate , kind, gjgs, note, piao, shuzi 
		cur = self.conn.execute( cmd )
		
		for row in cur:

			company = row[5]
			line = row[0]
			name = row[1]
			schedule = row[2]
			# updated time
			type1 = row[4]
			note = row[7]
			price = row[8]
			num = row[9]
		#	print(company)

			_company = city.addCompany(company)

			_line = Line( _company.id , name, line , schedule, type1, note, price)
			city.addLine(_line) 

	



def processDB( dbfile  ): 

	db   = DB(dbfile)
	city = City();

	
	 
#	print ('CONN,COUNT,MAX,MIN,OFF,O1,O2')
	db.processLines(city)
	
	db.close()

	city.clear()
	
	city.dumpLines();
	
#	encodedjson = json.dumps(city,default=object2dict ,ensure_ascii=False, sort_keys=True,indent=4 )
#	print (encodedjson)




def usage():
	print ('usage : dbfile')


if __name__ == "__main__":
	


#	print( sys.argv) 
	if len(sys.argv)<2:
		usage()
	else:
		processDB(sys.argv[1] ) 



 