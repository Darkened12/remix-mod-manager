import os


os.system(r'python -m PyInstaller --noconsole --name remix-mod-manager --icon assets/app.ico '
          r'--add-data="assets;assets" --add-data="style.kv;." --add-data="path.txt;." app.py')


