#!/bin/bash
mkdir ~/.proman
cp -r src/ ~/.proman/
touch ~/.proman/project-directories.json
touch ~/.proman/editor.txt
touch ~/.proman/fm.txt
sudo cp proman /usr/bin/
sudo chmod +x /usr/bin/proman
echo "Installation Succesful"
