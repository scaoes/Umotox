@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo      UMOTOX - WAV / MP3 to BCWAV
echo ========================================
echo.

if not exist "output" (
    mkdir "output"
)

if not exist "tools\\ffmpeg.exe" (
    echo ERROR: ffmpeg.exe is missing in the tools folder.
    pause
    exit /b
)

if not exist "tools\\3DWaves\\src\\main.py" (
    echo ERROR: main.py is missing in the 3DWaves folder.
    pause
    exit /b
)

if not exist "tools\\3DWaves\\src\\bcwav_writer.py" (
    echo ERROR: bcwav_writer.py is missing in the 3DWaves folder.
    pause
    exit /b
)

if "%~1"=="" (
    echo No files dropped. Processing all .mp3 and .wav files in folder...
    for %%f in (*.mp3 *.wav) do call :convert "%%f"
) else (
    :loop
    if "%~1"=="" goto done
    call :convert "%~1"
    shift
    goto loop
)

:done
echo.
echo Done! All BCWAV files are in the 'output' folder.
pause
exit /b

:convert
set "input=%~1"
set "name=%~n1"
set "ext=%~x1"
set "wavfile=!name!.wav"
set "bcwavfile=output\\!name!.bcwav"

echo Converting: !input!

if /I "!ext!"==".mp3" (
    echo Using ffmpeg to convert MP3 to WAV...
    tools\\ffmpeg.exe -i "!input!" -ar 44100 -ac 2 "!wavfile!" -y >nul 2>&1
    if errorlevel 1 (
        echo ERROR: ffmpeg failed to convert !input! to WAV.
        pause
        exit /b
    )
) else (
    copy "!input!" "!wavfile!" >nul
)

if exist "!wavfile!" (
    echo Running main.py to convert WAV to BCWAV...
    echo Command: py tools\\3DWaves\\src\\main.py "!wavfile!" -o "!bcwavfile!" >debug_log.txt 2>&1
    py tools\\3DWaves\\src\\main.py "!wavfile!" -o "!bcwavfile!" >>debug_log.txt 2>&1
    if exist "!bcwavfile!" (
        del "!wavfile!"
        echo Output: !bcwavfile!
    ) else (
        echo ERROR: Conversion to BCWAV failed for "!input!". Check debug_log.txt for details.
        pause
    )
) else (
    echo Failed to convert "!input!" to WAV.
)
