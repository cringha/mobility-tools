#!/usr/bin/env python
# coding=utf8
import random;
import urllib
import json
import os;
import sys;

import urllib.request

user_agent = 'Mozilla/7.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.3116';
#
def downloadGDmap( path,  city , key ):

	key1 = urllib.parse.quote(key);

	version = random.randint(5,100);

	user_agent = 'Mozilla/" + str(version) +".0 (compatible; MSIE 5.5; Windows NT)';


	url = "http://ditu.amap.com/service/poiInfo?query_type=TQUERY&city=" + city + "&keywords=" + key1;
	h = None;
	try:
		print(url);

		headers = {'User-Agent': user_agent}
		# data = urllib.parse.urlencode(values)
		req = urllib.request.Request(url, None, headers)
		response = urllib.request.urlopen(req)
		page = response.read()


		# fp = urllib.request.urlopen(url)
		# mybytes = fp.read()
		mystr = page.decode("utf8");

		# page.close();

		result = checkJSON( mystr, key );
		if result == 6: # to fast
			print('JSON ERROR TO FAST : '+ key );
			return False;

		if result == -1:
			print('JSON ERROR EMPTY : ' + key);
			return True;


		basepath = path +"/" + city;
		if not os.path.exists( basepath):
			os.mkdir( basepath );

		h = open( basepath + "/" + key +".json", "w", encoding='utf-8');
		h.write( mystr );
		h.close();


	except Exception as e:
		print('e ' + str(e));
		return False;

	finally:
		if h != None:
			h.close();
		h = None;

	return True;




def checkJSON(content, name):
	_jsonObj = json.loads(content);
	status = _jsonObj['status'];
	if status != '1':
		print(name + ', ' + status + ', ' + _jsonObj['data']);
		return int(status);

	busData = _jsonObj['busData'];
	if (busData == None or len(busData) == 0):
		print(name + ', ' + status + ', empty ');
		return -1;
	return 0;


city = '320500';
key = '19';


# downloadGDmap('./data1', city, key);


def openList(file , city,  path = './data1'):

	basepath = path + "/" + city;
	if not os.path.exists(basepath):
		os.mkdir(basepath);

	list = parseExistJsons( basepath );

	h = None;

	try:
		h = open(file,encoding='utf-8');
		for line in h:
			name = line.strip();
			print('name ', name);
			if name in list:
				print( ' exit ');
			else:
				result = downloadGDmap( path, city, name );
				if not result :
					print('Stop.');
					return ;

	finally:
		if h != None:
			h.close();


def parseExistJsons(path):
	if not path.endswith("/"):
		path = path + "/";

	list = [];

	for file in os.listdir(path):
		#
		if file.endswith('.json') :
			filename = file[:-5];
			print(file + ' --> ' + filename);
			#shutil.move(path + file, to + filename);
			list.append( filename );
	return list;



def usage():
	print('usage : list  city basepath')


if __name__ == "__main__":

	#	print( sys.argv)
	if len(sys.argv) < 3:
		usage()
	else:
		if len(sys.argv) == 3:
			openList(sys.argv[1], sys.argv[2]);
		elif len(sys.argv) == 4:
			openList(sys.argv[1], sys.argv[2], sys.argv[3]);
		else:
			openList(sys.argv[1], sys.argv[2], sys.argv[3]);



