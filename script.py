from systemInfo import SystemInfo
class Script:
    file_name = ""
    server = ""
    condition = ""
    sysInfo = ""
    def __init__(self,file_name,server,condition):
        self.file_name = file_name
        self.server = server
        self.condition = condition
