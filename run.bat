@echo off

set T10_USER=postgres
set T10_PASSWORD=
cd backend
REM pip install -r requirements.txt
start python app.py

cd..
