pyinstaller sorter.py --clean --onefile --noconfirm --noupx --icon=icon.ico
move "dist\sorter.exe" "sorter.exe"

rd /s /q "dist"
rd /s /q "build"
del sorter.spec