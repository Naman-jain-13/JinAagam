@echo off
title JinAagam Kosh
cd /d "%~dp0"
echo.
echo   जिनागम कोश  /  JinAagam Kosh
echo   ---------------------------------------------
echo   Browser opening at  http://localhost:8777
echo   (इस काली खिड़की को खुला रहने दें; बंद करने पर कोश बंद हो जाएगा)
echo.
start "" http://localhost:8777/index.html
python -m http.server 8777 >nul 2>&1
if errorlevel 1 (
  echo Python nahi mila. Python install kijiye: https://python.org
  pause
)
