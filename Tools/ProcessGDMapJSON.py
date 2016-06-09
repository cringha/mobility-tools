#encoding:utf-8 
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
	def __init__(self,  company , name, line  , schedule, type1, note, price):
		self.company = company
		self.line  = line
		self.name  = name
		self.schedule = schedule
		self.note= note
		self.type = type1
		self.price = price



class SubLine:
	def __init__(self,  line , name, id  , front , terminal, 
		iccard, start , end, totalPrice , interval , length, type1, note, basePrice , path ):
		self.company = company
		self.line  = line
		self.name  = name;
		self.id = id;
		self.front = front;
		self.terminal = terminal; 
		self.iccard = iccard;
		self.start = start ;
		self.end = end;
		self.totalPrice = totalPrice;
		self.interval = interval;
		self.length = length;
		self.schedule = schedule
		self.note= note
		self.type = type1
		self.basePrice = basePrice;
		self.path = path;
		
		
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



def getJSONLine ( line , name ):
	for type in line:
		if type.type == name :
			return type;
	return None;
	

def processLineInfo( city , line ):
	
	company = city.addCompany( line.company);
	# line info 
	name = line.key_name ;
	ln = Line( company.id , name, name , '',  '' , '', '')
	city.addLine(ln) 
	
def processJSONLine( city , json ):
	
	line = getJSONLine(json, 'polyline');
	

	for type in line:
		if type.type == 'polyline' :
			# line stop info ;
		elif type.type == 'marker':
			for stop in type.list:
				# stop info 
				# id": "BS10014223",
				# "location": {
					# "lat": 39.9515,
					# "lng": 116.40673800000002
				# },
				# "name": "安定门外",
				# "sequence": "1",
				# "bus_type": "bus",
				# "markerType": "marker-busStop",
				# "tType": "2"
				
				id = stop.id ;
				_stop = city.findStop( id );
				if _stop == None:
					_stop = Stop(stop.name , None , stop.location.lng ,stop.location.lat ,id ,id );
					city.addStop( _stop );
				
		else :
			print('UNKNOWN type '+ type.type);

def processJSON( _jsonObj ):
	
	busData = _jsonObj.busData;
	
	for line in busData:
		processJSONLine( line );
	
	
	
def loadJSON( name ): 
	h  = open(name, encoding='utf-8');
	if h != None :
		_jsonObj = json.load(h);
		print (_jsonObj);
		
		if _jsonObj.status == '1':
			processJSON(_jsonObj);
		else:
			print('ERROR : json file ' + name +', status '+ _jsonObj.status );
	
		h.close();
		
		
	




def usage():
	print ('usage : dbfile')


if __name__ == "__main__":
	


#	print( sys.argv) 
	if len(sys.argv)<2:
		usage()
	else:
		loadJSON(sys.argv[1] ) 



 