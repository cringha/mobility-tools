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
import shutil
import urllib.parse;

'''
  检查 gaode 地图 导出的数据是否成功

'''

def saveLog( log , file ):
	#file=urllib.parse.quote(file)
	#file 

	log.write( file+'\n');
	
'''
  检查JSON数据是否合法， 
   -  status ==  1 
   -  busData 不为空
'''
def checkJSON( log , path , name ): 
	h = None;
	try:
		h  = open(path + name, encoding='utf-8');
		if h != None :
			_jsonObj = json.load(h);
			status = _jsonObj['status'];
			if status != '1':
				print(   name[:-5] +', '+ status + ', ' + _jsonObj['data'] );
				saveLog(log, name[:-5] );
				return False ;
				
			busData = _jsonObj['busData'];
			if( busData == None or len(busData) == 0 ):
				print(   name[:-5] +', '+ status + ', empty '   );
				saveLog(log, name[:-5] );
				return False ;
				
			return True;
	except Exception as e:
		saveLog(log, name[:-5] );
		print('e ' + str(e));
		return False;
	finally:
		if h!=None :
			h.close();
		h = None;
		

	

'''
   
   遍历目录，检查所有的 JSON 文件， 如果合法文件
   移动到目录2
  
'''
def parseDir( path , path2 =None ):  
	
	log = open("error.list", "w", encoding="gbk")

	if not path.endswith("/"):
		path = path +"/"
	if path2 != None and not path2.endswith("/"):
		path2 = path2 +"/"	
		
	for file in os.listdir(path):  
		#
		if checkJSON( log, path , file):
			if path2!=None:
				shutil.move(path + file, path2 + file );
				print('move file to ' + (path2 + file) );

	log.close();
	
def usage():
	print ('usage : path , path_to_move')


if __name__ == "__main__":
	


#	print( sys.argv) 
	if len(sys.argv)<2:
		usage()
	else:
		if len(sys.argv) == 2:
			parseDir(sys.argv[1]) 
		elif len(sys.argv) == 2:
			parseDir(sys.argv[1],sys.argv[2] ) ;
		else:
			parseDir(sys.argv[1],sys.argv[2] ) ;



 