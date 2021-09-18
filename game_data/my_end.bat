@echo off
chcp 65001

:: 设置前端当前目录环境
set BASEPATH=%~dp0

set SrcPath=%BASEPATH%data
:: echo %SrcPath%

:: 这里修改后端的data目录下
set ObjPath=D:\
:: echo %ObjPath%

xcopy %SrcPath% %ObjPath% /s/i

PAUSE