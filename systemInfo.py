class SystemInfo:
    sys_name = ""
    boot_time = ""
    cpu_usage = ""
    current_freq = 0.0
    def __init__(self,sys_name,boot_time,cpu_usage,current_freq):
        self.sys_name = sys_name
        self.boot_time = boot_time
        self.cpu_usage = cpu_usage
        self.current_freq = current_freq