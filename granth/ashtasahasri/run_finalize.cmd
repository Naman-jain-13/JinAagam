@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0..\..\granth-vyakhya-skill\granth-vyakhya\scripts\finalize_word.ps1" -Docx "%~dp0vyakhya\Ashtasahasri_Vyakhya.docx" -ChunkPages 200 -IdleMinutes 10 -SkipUpdate > "%~dp0finalize.log" 2>&1
