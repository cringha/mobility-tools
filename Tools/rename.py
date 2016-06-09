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

'''
	工具， 批量改名。

'''


def parseDir( path , to ):  
	
	if not path.endswith("/"):
		path = path +"/"
	if not to.endswith("/"):
		to = to +"/"
		
	for file in os.listdir(path):  
		#
		if file.endswith('.json') and file.startswith('data'):
			filename = file[4:];
			print( file + ' --> ' + filename );
			shutil.move(path + file, to + filename );
	
	
def usage():
	print ('usage : path')


if __name__ == "__main__":
	


#	print( sys.argv) 
	if len(sys.argv)<2:
		usage()
	else:
		parseDir(sys.argv[1] ,sys.argv[2]  ) 



 