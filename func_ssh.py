import sys
import subprocess

try:
    import time
    import paramiko

except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '-r', 'requirements.txt'])

import config

class Ssh():
    def __init__(self):
        pass

    # 컴퍼니 브랜치 repo 시 사용
    def ssh_cmd(ip, port, user, pw, cmds):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(ip, port, user, pw)

        stdin, stdout, stderr = ssh.exec_command(";".join(cmds))

        lines = stdout.read()
        res = ''.join(str(lines))

        return res

    def ssh_cmd_backup(ip, port, user, pw, cmds):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(ip, port, user, pw)

        stdin, stdout, stderr = ssh.exec_command(";".join(cmds))
        #ch = ssh.get_transport().open_session()
        #res = ch.recv_exit_status()
        #stdin.write(cmd+'\n')
        #stdin.flush()
        #stdout._set_mode('b')

        lines = stdout.read()
        res = ''.join(str(lines))

        '''
        for line in lines:
            re = str(line).replace('\n', '')
            print(re)
            if str(re) in "fin":
                print("fin")
                break;
        '''

        return res


    def wait_stems(ch):
        time.sleep(1)
        outdata = errdata = ""

        while ch.recv_ready():
            outdata += str(ch.recv(1024))

        while ch.recv_stderr_ready():
            errdata += str(ch.recv_stderr(1024))

        return outdata, errdata


    def ssh_connection(ip, port, user, pw):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh.connect(ip, port, user, pw)

            console = ssh.invoke_shell()
            console.settimeout(9999)
            console.keep_this = ssh
            time.sleep(3)

            return console

        except Exception as err:
            print(err)


    # 원격으로 관리 대상 서버의 프로퍼티를 체크하여 이상 유무를 파악
    def ssh_onenet_property_check(cmd):
        servers = config.ssh_servers

        for server in servers:
            print(server["ip"], server["port"], server["id"], server["pw"], cmd)


if __name__ == '__main__':
    ssh = Ssh()
    print("ssh")
