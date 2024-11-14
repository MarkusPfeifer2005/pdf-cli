#!/bin/bash

uninstallName="uninstall.sh"
rm $uninstallName
touch $uninstallName
echo "#!/bin/bash" >> $uninstallName

python3 -m venv .venv
. ./.venv/bin/activate
pip install -r requirements.txt

pyinstaller --onefile pdf-cli.py
cp "dist/pdf-cli" "/usr/local/bin/"
echo "rm /usr/local/bin/pdf-cli" >> $uninstallName

deactivate
