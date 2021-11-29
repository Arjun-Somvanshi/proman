import getopt
import sys
import json
import os
import subprocess

class ProjectManager:
    def __init__(self):
        self.directories = {}
        self.ctags_project_dir = ""
        self.project_dir_path = os.path.expanduser("~/.proman/project-directories.json")
        try:
            with open(self.project_dir_path, 'r') as f:
                self.directories = json.load(f)
        except Exception as e:
            pass
        self.options = {"-p": self.runProject, "-a": self.addProject, 
                        "-r": self.deleteProject, "-t": self.ctags,
                        "-d": self.parseProjectDirectory, "-s": self.showDirectories,
                        "-v": self.printVersion}
    
    def printVersion(self, *args):
        print("proman Project Manager version 1.0")

    def write_directories(self):
        with open(self.project_dir_path, 'w') as f:
            json.dump(self.directories, f, indent=2)

    def parseProjectDirectory(self, projectdir):
        if os.path.isdir(projectdir):
            contents = os.listdir(projectdir)
        for item in contents:
            item_absolute_path = os.path.join(projectdir, item)
            if os.path.isdir(item_absolute_path):
                self.directories[item] = item_absolute_path
        self.write_directories()

    def showDirectories(self, *args):
        for key in self.directories:
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
        try:
            print("Running Project", projectName)
            projectDir = self.directories[projectName]
            subprocess.run('cd '+projectDir+' ; vim .', shell=True)
            self.ctags_project_dir = projectDir
        except Exception as e:
            print("Project Directory Not found", e)

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
            print(e)

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
        opts, arg = getopt.getopt(args, 'vp:ar:tsd:')
    except Exception as e:
        print("Wrong Usage\n", e)
    else:
        projectManager = ProjectManager()
        projectManager.run(opts)
