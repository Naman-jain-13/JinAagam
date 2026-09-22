@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "E:\Projects\JinAagam\granth-vyakhya-skill\granth-vyakhya\scripts\finalize_word.ps1" -Docx "E:\Projects\JinAagam\Ashtasahasri_Vyakhya.docx" -ChunkPages 200 -IdleMinutes 10 -SkipUpdate > "E:\Projects\JinAagam\ashtasahasri_work\finalize.log" 2>&1
