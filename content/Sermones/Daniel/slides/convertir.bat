@echo off
title Convertir PDF a PPTX - GSO

if "%~1"=="" (
    echo.
    echo  Convertidor PDF a PPTX - GSO
    echo.
    echo  Arrastra un PDF sobre este archivo
    echo  o ejecutalo desde la terminal:
    echo.
    echo    convertir.bat mi-sermon.pdf
    echo.
    pause
    exit /b
)

echo.
echo Convirtiendo: %~nx1
echo Por favor espera...
echo.

python "%~dp0pdf_to_pptx.py" "%~1" --poppler "C:\poppler\Library\bin" --dpi 150

echo.
if %errorlevel%==0 (
    echo Listo. El archivo PPTX esta en la misma carpeta que el PDF.
) else (
    echo Hubo un error. Verifica que Python y Poppler esten instalados.
)

echo.
pause
