import socket
import fcntl
import struct
import subprocess


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(
        fcntl.ioctl(
            s.fileno(),
            0x8915,
            struct.pack('256s', bytes(ifname[:15], 'utf-8'))
        )[20:24]
    )


def get_interfaces():
    out = subprocess.Popen(['cat', '/proc/net/dev'],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = out.communicate()
    stdout = stdout.decode('utf-8')
    l = stdout.split('\n')

    interfaces = []
    for interface in l[2:]:
        iface = interface.split(":")[0]
        if iface != "":
            interfaces.append(iface.strip())

    return interfaces
