set root=%~dp0
set conda=C:\anaconda
call %conda%\condabin\activate.bat base
call conda run -n Server uvicorn src.main:app
pause