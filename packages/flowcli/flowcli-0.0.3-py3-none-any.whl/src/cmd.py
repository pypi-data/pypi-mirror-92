import fire
from src import initTool, pull, download, common, upload, config, logout, run, login, push, project


class Cmd(object):
    """Command line tool\n
    Mainly used for flow hub platform file and tool transfer. If you encounter any problems during use, please report related problems to flowhub@163.com, and we will reply to your message as soon as possible.
    login:
        The user login, the user needs to complete the login first before performing other operations of ft
        --k key 
        Need to get password from webpage personal center
        E.g:ft login --k=a18607940dd611eb9d6e024255358b77

    logout:
        The user logout. After completing the ft tool operation, perform this operation to exit to prevent others from embezzling and fraudulent use
        E.g:ft logout

    upload:
        Upload files or folders to the platform account
        --s source 
        The path of the file or folder to be uploaded under the current computer or cluster
        --t target 
        Upload to the directory path under the platform account
        E.g:ft upload --s=./data.txt --t=/data/

    download:
        File or folder download
        --s source 
        Files or folders that need to be downloaded from the platform
        --t target 
        Download to the specified directory
        E.g:ft download --s /output/venn/data.txt --t ./

    push:
        Upload the tool to the platform account
        --f 
        Optionally specify the location of tool.json, if not set, look for the tool.json file in the current folder
        E.g:ft push --f=./tool.json

    pull:
        Pull online mirror, pull tool mirror from platform to local further development
        --id 
        Get the ID of the tool version from the web
        E.g:ft pull --id=263347730d3311ebb63c024255358b77

    initTool:
        The initialization tool will generate the tool template tool.json file in the current directory. The user needs to configure the tool.json file according to the local development tool image
        E.g:ft initTool demo

    run:
        Test the locally developed tool image and upload it to the platform after normal operation. Find the tool.json file in the current folder by default, please run it in the tool folder
        E.g:ft run

    project:
        List the user's project, and can switch the current project
        
    version:
        View the version of the ft command line tool
        E.g:ft version
    """
    def login(self, k=None, env=None):
        """

        """
        login.login(k=k, env=env)
    def logout(self):
        """

        """
        logout.logout()
    def upload(self, s=None, t=None):
        """

        """
        common.checkToken()
        project.checkProject()
        upload.upload(s=s, t=t)
    def download(self, s=None, t=None):
        """

        """
        common.checkToken()
        project.checkProject()
        download.download(s=s, t=t)
    def push(self, f=None):
        """

        """
        common.checkToken()
        project.checkProject()
        push.push(file=f)
    def pull(self, id):
        """

        """
        common.checkToken()
        project.checkProject()
        pull.pull(toolVersionId=id)
    def initTool(self, name):
        """

        """
        common.checkToken()
        initTool.initTool(name)

    def run(self):
        """

        """
        common.checkToken()
        run.run()
    def project(self):
        common.checkToken()
        project.view()

    def version(self):
        """

        """
        return config.version

def init():
    fire.Fire(Cmd)