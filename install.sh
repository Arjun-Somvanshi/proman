#!/bin/bash
mkdir ~/.proman
cp -r src/ ~/.proman/
touch ~/.proman/project-directories.json
sudo cp proman /usr/bin/
sudo chmod +x /usr/bin/proman
echo "Installation Succesful"
