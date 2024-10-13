#!/bin/bash

uninstallName="uninstall.sh"
rm $uninstallName
touch $uninstallName
echo "#!/bin/bash" >> $uninstallName

. ./.venv/bin/activate

for file in $(ls); do
  if [ ${file:(-3)} == ".py" ]; then
    pyinstaller --onefile $file
    cp dist/${file:0:-3} /usr/local/bin/
    echo "rm /usr/local/bin/${file:0:-3}" >> $uninstallName
  fi
done

deactivate
