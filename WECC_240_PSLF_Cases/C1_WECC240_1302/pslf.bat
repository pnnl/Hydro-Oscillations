@echo off
@set PSLFDIR=%1
@set classpath=%1jclasses
%1jre\bin\java -Dsun.java2d.dpiaware=false -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -jar %1jclasses\pslf.jar 
pause.



