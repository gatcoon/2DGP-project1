import os
import PyInstaller.__main__

# SDL2.dll 경로 설정
sdl2_path = r"C:\Python\Lib\site-packages\pygame\SDL2.dll"

# 데이터 파일과 바이너리 추가 설정
data_files = [
    # 기존 추가 데이터 파일들
    ('C:/Python/Lib/site-packages/pygame/SDL2.dll', '.'),
    ('C:/Python/Lib/site-packages/pygame/SDL2_image.dll', '.'),
    ('C:/Python/Lib/site-packages/pygame/SDL2_mixer.dll', '.'),
    ('C:/Python/Lib/site-packages/pygame/SDL2_ttf.dll', '.'),
    # 게임 데이터
    ('sounds', 'sounds'),
    ('sprites', 'sprites'),
]

binaries = [
    (sdl2_path, '.')  # SDL2.dll을 실행 파일의 루트로 복사
]

# PyInstaller 실행 명령 구성
pyinstaller_args = [
    'main.py',
    '--onefile',
    '--windowed',
    '--noconsole',
    '--distpath', './dist',  # 빌드 결과 경로 설정
    '--workpath', './build',  # 빌드 작업 경로 설정
    '--specpath', './',  # spec 파일 저장 경로 설정
]

# 데이터 파일 추가
for src, dest in data_files:
    pyinstaller_args.extend(['--add-data', f'{src};{dest}'])

# 바이너리 추가
for src, dest in binaries:
    pyinstaller_args.extend(['--add-binary', f'{src};{dest}'])

# PyInstaller 실행
PyInstaller.__main__.run(pyinstaller_args)
