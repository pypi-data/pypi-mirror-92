# -*- coding: utf-8 -*-
'''ssh远程主机执行shell
'''
import pexpect


def ssh_cmd(ip, uname, passwd, cmd):
    ret = -1
    ssh = pexpect.spawn('ssh %s@%s "%s"' % (uname, ip, cmd))
    try:
        i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=5)
        if i == 0 :
            ssh.sendline(passwd)
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('password: ')
            ssh.sendline(passwd)
        ssh.sendline(cmd)
        r = ssh.read()
        print(r)
        ret = 0
    except pexpect.EOF:
        print "EOF"
        ssh.close()
        ret = -1
    except pexpect.TIMEOUT:
        print "TIMEOUT"
        ssh.close()
        ret = -2
    return ret, r


if __name__ == '__main__':
    ssh_cmd("192.168.0.100", "bi", "12345667980", "ls /")