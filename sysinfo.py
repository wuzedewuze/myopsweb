#!/usr/bin/python
# coding:utf-8
# author: rongjunfeng

import json
import subprocess
import psutil
import socket
import time
import re
import platform
import requests

device_white = ['eth0', 'eth1', 'eth2', 'eth3', 'bond0', 'bond1']

# 获取主机名
def get_hostname():
    return socket.gethostname()

# 获取ip地址信息和mac地址信息
def get_innerIp(ipinfo):
    inner_device = ["eth1", "bond0","eth0"]
    ret = {}
    for info in ipinfo:
        if info.get("ip", None) and info.get('device', None) in inner_device:
            ret['inner_ip'] = info['ip']
            ret['mac_address'] = info['mac']
            return ret
    return {}


def get_device_info():
    ret = []
    for device, info in psutil.net_if_addrs().items():
        if device in device_white:
            device_info = {'device': device}
            for snic in info:
                if snic.family == 2:
                    device_info['ip'] = snic.address
                elif snic.family == 17:
                    device_info['mac'] = snic.address
            ret.append(device_info)
    return ret

# 获取cpu信息
def get_cpuinfo():
    ret = {"cpu": '', 'num': 0}
    with open('/proc/cpuinfo') as f:
        for line in f:
            line_list = line.strip().split(':')
            key = line_list[0].rstrip()
            if key == "model name":
                ret['cpu'] = line_list[1].lstrip()
            if key == "processor":
                ret['num'] += 1
    return ret

# 获取磁盘信息
def get_disk():
    cmd = """/sbin/fdisk -l 2>>/dev/null|egrep "Disk|Platte"|egrep -v 'identifier|mapper|Disklabel'"""
    disk_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    partition_size = []
    for dev in disk_data.stdout.readlines():
        #size = int(dev.strip().split(', ')[1].split()[0]) / 1024 / 1024 / 1024
        size = int(dev.strip().decode().split(', ')[1].split()[0]) / 1024 / 1024 / 1024
        partition_size.append(str(size))
    return " + ".join(partition_size)

# 获取内测信息
def _get_total_mem():
    with open('/proc/meminfo') as f:
        for line in f:
            if "MemTotal" in line:
                return int(line.split()[1])

def get_mem():
    total = _get_total_mem()
    m_total = total / 1024.0
    if len(str(int(m_total))) < 4:
        return "{} MB".format(round(m_total, 2))
    else:
        return "{} GB".format(round(m_total / 1024.0, 2))


#

# 获取操作系统信息，服务器类型  sn  uuid信息
def get_Manufacturer():
    cmd = """/usr/sbin/dmidecode | grep -A6 'System Information'"""
    ret = {}
    manufacturer_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in manufacturer_data.stdout.readlines():
        str_line = line.decode().strip()
        if "Manufacturer" in str_line:
            ret['manufacturers'] = str_line.split(': ')[1]
        elif "Product Name" in str_line:
            ret['server_type'] = str_line.split(': ')[1].strip()
        elif "Serial Number" in str_line:
            ret['sn'] = str_line.split(': ')[1].strip().replace(' ','')
        elif "UUID" in str_line:
            ret['uuid'] = str_line.split(': ')[1].strip()
    return ret

# 获取
def get_rel_date():
    cmd = """/usr/sbin/dmidecode | grep -i release"""
    data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    date = data.stdout.readline().decode().split(': ')[1].strip()
    return re.sub(r'(\d+)/(\d+)/(\d+)',r'\3-\1-\2',date)

def get_os_version():
    return " ".join(platform.linux_distribution())




def run():
    data = {}
    data['hostname'] = get_hostname()
    data.update(get_innerIp(get_device_info()))
    cpuinfo = get_cpuinfo()
    data['server_cpu'] = "{cpu} {num}".format(**cpuinfo)
    data['server_disk'] = get_disk()
    data['server_mem'] = get_mem()
    data.update( get_Manufacturer())
    data['manufacture_date'] = get_rel_date()
    data['os'] = get_os_version()
    try:
        if "VMware" in data['manufacturers']:
            data['vm_status'] = 0
        else:
            data['vm_status'] = 1
    except KeyError:
        raise Exception("run as root")
    send(data)


def send(data):
    url = "http://192.168.0.201:8000/resource/server/report/"
    r = requests.post(url, data=data)
    print(r.status_code)
    print(r.content)
    print(data)


if __name__ == "__main__":
    run()
