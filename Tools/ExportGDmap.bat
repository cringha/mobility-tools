http://ditu.amap.com/service/poiInfo?query_type=TQUERY&city=110000&keywords=27
REM values.put(DataService.NAME_LONGITUDE, 116.47761 );
rem values.put(DataService.NAME_LATITUDE, 39.99051 );
rem values.put(DataService.NAME_PASSENGERS, 39 );
rem values.put(DataService.NAME_NEXT, 61140 );
REM 

SET H1="Accept: application/json"
SET H2="charset: utf-8"
SET URL=http://ditu.amap.com/service/poiInfo?query_type=TQUERY&city=110000&keywords=27

curl -H %H1% -H %H2% -G -vvvvv   "%URL%"