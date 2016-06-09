REM 320500 SUZHOU 
REM 110000 BEIJING 
@echo OFF

SET CITY=320500
SET LIST=suzhou.txt
SET LIST=error.list
SET CURL=curl
SET PROXY=-x http://127.0.0.1:5080

FOR /f %%a in ( %LIST%) DO CALL :AddToPath %%a
GOTO :RUN

:AddToPath
ECHO 'DOWNLOAD LINE: ' %1 
SET URL="http://ditu.amap.com/service/poiInfo?query_type=TQUERY&city=%CITY%&keywords=%1"
SET URL1="http://ditu.amap.com/service/poiInfo?query_type=TQUERY&city=320500&keywords=63%E8%B7%AF&pagesize=20&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&geoobj=120.282059%7C31.158419%7C120.721512%7C31.361213"
ECHO %URL%
%CURL% -vvvv %PROXY% -G %URL% -o "data1\%1.json"

REM 睡 3秒
timeout /t 1 /nobreak > nul  
GOTO :EOF
 

:RUN  
rem ECHO %CLASSPATH%
echo 'EXIT'