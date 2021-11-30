## proman 
## //////////////
## \[   ]--[   ]/
##        L
##      -----
proman is a project manager. It helps you manage your
projects from a terminal. The features are listed below.

## Installation
Step 1: Download or Clone this repository to any location.
Step 2: cd proman/
Step 3: bash install.sh

Now you can use proman from anywhere, it's in your path.
To UNINSTALL come back to the directory and run: bash uninstall.sh 

To UNINSTALL go to the cloned directory and run: bash uninstall.sh 

## Features

# Add your project directories 
proman reads your project directories and imports all the absolute paths
to your projects. 
To add a project directory do this:
proman -d /home/user/pythonProjects

# Access your projects from any directory instantly
Now all the directories under pythonProjects will be added to the
~/.proman/project-directories.json file. 

Now you can open them using the terminal instantly with the editor of 
your choice by typing:

proman -p ProjectName

or simply use:

proman ProjectName

# Open your projects in an editor or file manager of choice
By default the editor is vim, to set the editor to something else
use the name your editor uses to identify itself in the terminal. 
Then run this command:
proman -e EditorName

Default FileManger is thunar set it to something else with:
proman -f fileManagerName

Open a project directory in the filemanager with:
proman -o projectName

# Remove and list projects
To list all projects run:
proman -s

To remove a project run:
proman -r ProjectName

# Generate ctags for your projects before opening
Pre-requiste: ctags

proman -p ProjectName -t

-t is to be used after specifying the project name not before.

Use proman -v to see the version and -h to see the usage

## Contributing
Pull requests are welcome. For major changes, please open an 
issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.
https://github.com/Arjun-Somvanshi/proman

## License
[GNU GPL](https://www.gnu.org/licenses/)
