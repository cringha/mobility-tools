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
  Export 8684 网站公交数据到 JSON 格式

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
		self.stops = []
		self.refs = [] 
		self.__stops = {}
		self.__refs = {}


	def clear(self):
		self.__stops = None
		self.__refs = None

	def addStop(self , stop ):
		self.stops.append(stop)
		self.__stops[stop.sid] =stop

	def findStop( self , sid  ):
		if sid in self.__stops:
			return self.__stops[sid];

		return None 



	def addLineStop( self , ref ):
		#  sid, lineId , updown
		rid = ref.sid + '_' + str(ref.line)+'_' + str(ref.updown)

		if rid not in self.__refs:
			self.__refs[rid] = ref;
			self.refs.append(ref)

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


class LineStop:
	def __init__(self, sid,  line ,  updown , sequence ):
		self.sid   = sid
		self.line  = line
	#	self.stop  = stop
		self.updown = updown
		self.sequence= sequence
	 


class Line:
	def __init__(self,  company , name, line , schedule, type1, note, price):
		self.company = company
		self.line  = line
		self.name  = name
		self.schedule = schedule
		self.note= note
		self.type = type1
		self.price = price


class Stop:
	def __init__(self,  name, alias, x , y, code , sid ):
		self.name  = name
		self.alias = alias 
		self.x = x
		self.y= y
		self.code = code
		self.sid  = sid 
		
def toType(updown):
	if updown ==  1:
		return "UP"
	elif updown == 2:
		return "DOWN"
	elif updown == 3:
		return "CIRCLE"
	else:
		return "UNKNOWN"



def makeStopID(code , x, y ):
	return code + '_' +x + '_' + y


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

	def processStops(self , city ):
		
		cmd = 'SELECT * FROM CNBUS order by kind , pm  ' 
		
		# ID, BUSW,  shijian, zxdate , kind, gjgs, note, piao, shuzi 
		cur = self.conn.execute( cmd )
		
		for row in cur:

			lineId  = row[0]
			sequence    = row[1]
			name = row[2]
			updown = toType( row[3])


			alias = row[5]
			x = row[6]
			y = row[7]
			code = row[8]
			
			# 使用 站牌CODE +X+Y 作为唯一标示
			sid = makeStopID( code, x, y)

			find  = city.findStop( sid )
			if find == None:
				find = Stop(name,alias,x,y,code,sid)
				city.addStop( find )


			ref = LineStop( sid, lineId , updown, sequence)
			city.addLineStop(ref) 




def processDB( dbfile  ): 

	db   = DB(dbfile)
	city = City();

	
	 
#	print ('CONN,COUNT,MAX,MIN,OFF,O1,O2')
	db.processLines(city)
	db.processStops(city)
	db.close()

	city.clear()
	encodedjson = json.dumps(city,default=object2dict ,ensure_ascii=False, sort_keys=True,indent=4 )
	print (encodedjson)




def usage():
	print ('usage : dbfile')


if __name__ == "__main__":
	


#	print( sys.argv) 
	if len(sys.argv)<2:
		usage()
	else:
		processDB(sys.argv[1] ) 



 