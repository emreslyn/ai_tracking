import paramiko

def connect_ssh(host,port,username,password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    return ssh

def upload_file(ssh, local_path, filename):
    ftp_client = ssh.open_sftp()
    ftp_client.put(local_path, "/itu/s06d03/user_home/isleyen16/ai_tracking/" + filename)
    ftp_client.close()

def check_file(filename, allowed_extensions):
    if not "." in filename:
        return False
    extension = filename.rsplit(".",1)[1]
    if extension.upper() in allowed_extensions:
        return True
    else:
        return False