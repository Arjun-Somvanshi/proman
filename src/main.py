import getopt
import sys
import json
import os
import subprocess

class ProjectManager:
    def __init__(self):
        self.directories = {}
        self.container_directories = {"containers": []}
        self.editor = ""
        self.ctags_project_dir = ""
        self.project_dir_path = os.path.expanduser("~/.proman/project-directories.json")
        self.editor_file_path = os.path.expanduser("~/.proman/editor.txt")
        self.fm_file_path = os.path.expanduser("~/.proman/fm.txt")
        self.project_container_path = os.path.expanduser("~/.proman/project-container-directories.json")
        self.filemanager = ""
        try:
            with open(self.project_dir_path, 'r') as f:
                self.directories = json.load(f)
        except:
            pass
        with open(self.editor_file_path, 'r') as f:
            self.editor = f.read()
        with open(self.fm_file_path, 'r') as f:
            self.filemanager = f.read()
        if not self.editor:
            self.editor = "vim"
            self.write_editor()
        if not self.filemanager:
            self.filemanager = "thunar"
            self.write_filemanager()
        self.options = {"-p": self.runProject, "-a": self.addProject, 
                        "-r": self.deleteProject, "-t": self.ctags,
                        "-d": self.parseProjectDirectory, "-s": self.showDirectories,
                        "-v": self.printVersion, "-e": self.setEditor,
                        "-f": self.setFileManager, "-o": self.openProject,
                        "-h": self.help}
        # comment this out 
        # print(self.directories)
        # print()
        # print()
    
    def printVersion(self, *args):
        print("proman Project Manager version 1.0")

    def help(self, *args):
        helpstr = """
        proman 
        //////////////
        \[   ]--[   ]/
              L
            -----
        proman is a project manager. It helps you manage your
        projects from a terminal. The features are listed below.

        To UNINSTALL go to the cloned directory and run: bash uninstall.sh 

        Features
        ********

        Add your project directories 
        ----------------------------
        proman reads your project directories and imports all the absolute paths
        to your projects. 
        To add a project directory do this:
        proman -d /home/user/pythonProjects

        Access your projects from any directory instantly
        -------------------------------------------------
        Now all the directories under pythonProjects will be added to the
        ~/.proman/project-directories.json file. 

        Now you can open them using the terminal instantly with the editor of 
        your choice by typing:

        proman -p ProjectName

        or simply use:

        proman ProjectName

        Open your projects in an editor or file manager of choice
        ---------------------------------------------------------
        By default the editor is vim, to set the editor to something else
        use the name your editor uses to identify itself in the terminal. 
        Then run this command:
        proman -e EditorName

        Default FileManger is thunar set it to something else with:
        proman -f fileManagerName

        Open a project directory in the filemanager with:
        proman -o projectName

        Remove and list projects
        -------------------------
        To list all projects run:
        proman -s

        To remove a project run:
        proman -r ProjectName

        Generate ctags for your projects before opening
        -----------------------------------------------
        Pre-requiste: ctags

        proman -p ProjectName -t

        -t is to be used after specifying the project name not before.

        Use proman -v to see the version and -h to see the usage

        Contributing
        ************
        Pull requests are welcome. For major changes, please open an 
        issue first to discuss what you would like to change.
        Please make sure to update tests as appropriate.
        https://github.com/Arjun-Somvanshi/proman

        License
        *******
        [GNU GPL](https://www.gnu.org/licenses/)
        """
        print(helpstr)

    def write_directories(self):
        with open(self.project_dir_path, 'w') as f:
            json.dump(self.directories, f, indent=2)

    def write_editor(self):
        with open(self.editor_file_path, "w") as f:
            f.write(self.editor)

    def write_filemanager(self):
        with open(self.fm_file_path, "w") as f:
            f.write(self.filemanager)

    def refreshContainerDirectories(self):
        try: 
            with open(self.project_container_path, 'r') as f:
                self.container_directories = json.load(f)
        except:
            pass
        if self.container_directories["containers"]:
            for directory in self.container_directories["containers"]:
                self.parseProjectDirectory(directory)

    def parseProjectDirectory(self, projectdir):
        self.directories = {}
        if os.path.isdir(projectdir):
            contents = os.listdir(projectdir)
            for item in contents:
                item_absolute_path = os.path.join(projectdir, item)
                if os.path.isdir(item_absolute_path):
                    self.directories[item] = item_absolute_path
            self.write_directories()
            if not (projectdir in self.container_directories["containers"]):
                self.container_directories['containers'].append(projectdir)
                with open(self.project_container_path, 'w') as f:
                    json.dump(self.container_directories, f, indent=2)
        else:
            print("No such directory was found.")

    def showDirectories(self, *args):
        directory_keys = list(self.directories.keys())
        directory_keys = sorted(directory_keys)
        for key in directory_keys:
            directoryInfo = "Dirctory: " + self.directories[key]
            decorationLen = len(directoryInfo)
            for i in range(decorationLen):
                print("%", end="")
            print()
            print("Project Name: ", key)
            print(directoryInfo)
            for i in range(decorationLen):
                print("%", end="")
            print()
            print()

    def runProject(self, projectName):
        projectDir = None
        try:
            print("Running Project", projectName)
            projectDir = self.directories[projectName]
            projectDir = projectDir.replace(" ", "\ ")
        except Exception as e:
            print("No such project dirctory was found: ", e)
        else:
            try:
                subprocess.run('cd '+projectDir+' ; ' + self.editor + " .", shell=True)
            except Exception as e:
                print("Error while opening the project: ", e)
            else:
                try:
                    self.ctags_project_dir = projectDir
                except Exception as e:
                    print("Ctags Error occured: ", e)

    def openProject(self, projectName):
        try:
            print("Opening Project", projectName)
            projectDir = self.directories[projectName]
            projectDir = projectDir.replace(" ", "\ ")
            subprocess.run(self.filemanager + " " + projectDir, shell=True)
        except Exception as e:
            print("No such project dirctory was found: ", e)

    def addProject(self, *args):
        projectName = input("Enter the name of the project: ")
        invalidDirectory = True
        while(invalidDirectory):
            projectDir = input("Enter the absolute path of the project: ")
            invalidDirectory = not os.path.isdir(projectDir)
            if invalidDirectory:
                print("Not a valid directory!")
        self.directories[projectName] = projectDir
        self.write_directories()

    def deleteProject(self, projectName):
        try:
            del self.directories[projectName]
            self.write_directories()
        except Exception as e:
            print("Error Not a project: ", e)
    
    def setEditor(self, editor):
        self.editor = editor
        self.write_editor()

    def setFileManager(self, filemanager):
        self.filemanager = filemanager
        self.write_filemanager()
    

    def ctags(self, *args):
        if self.ctags_project_dir:
            subprocess.run('ctags -R ' + self.ctags_project_dir, shell=True)
            subprocess.run('mv tags ' + self.ctags_project_dir, shell=True)
        else:
            print("Need a project to generate tags for, enter a project name.")

    def run(self, opts):
        for option in opts:
            self.options[option[0]](option[1])

if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        opts, arg = getopt.getopt(args, 'vhp:ar:tsd:e:f:o:')
    except Exception as e:
        print("Wrong Usage\n", e)
    else:
        projectManager = ProjectManager()
        projectManager.refreshContainerDirectories()
        if len(args) == 1 and args[0] not in  ['-a', '-h', '-v', '-t', '-s']:
            projectManager.runProject(args[0])
        else: 
            projectManager.run(opts)
