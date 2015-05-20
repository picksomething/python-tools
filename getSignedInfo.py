#!/usr/bin/python
import os
import sys


def check_args():
    if len(sys.argv) == 3:
        file1 = str(sys.argv[1]).split(os.sep)[-1]
        file2 = str(sys.argv[2]).split(os.sep)[-1]
        if not file1.endswith("apk") or not file2.endswith("apk"):
            print("not a apk file")
            exit(0)
        return [file1, file2]
    elif len(sys.argv) == 2:
        file1 = str(sys.argv[1]).split(os.sep)[-1]
        if not file1.endswith("apk"):
            print("not a apk file")
            exit(0)
        return file1


def check_exist(input_apk):
    if not os.path.exists(input_apk):
        print(input_apk + " file does not exist")
        exit(0)


def exec_cmd(cmd):
    r = os.popen(cmd)
    text = r.readline()
    r.close()
    return text


def get_signed_info(apk):
    cmd1 = "jar tf " + apk + " | grep RSA"
    result1 = exec_cmd(cmd1)
    result1 = result1.strip()
    cmd2 = "jar xf " + apk + " " + result1
    os.system(cmd2)
    cmd3 = "keytool -printcert -file " + result1 + "| grep MD5"
    md5 = exec_cmd(cmd3)
    md5 = md5.strip()
    return md5


def diff_md5(apk1, apk2):
    apk1_md5 = get_signed_info(apk1)
    apk2_md5 = get_signed_info(apk2)
    if apk1_md5 == apk2_md5:
        print(apk1 + "md5 == " + apk2 + "md5")
    else:
        print(apk1 + " md5 != " + apk2 + " md5")
        print(apk1 + ' \t' + apk1_md5)
        print(apk2 + ' \t' + apk2_md5)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage:./getSignedInfo.py xxx.apk to get singed info or")
        print("usage:./getSignedInfo.py one.apk two.apk to compare their signed info")
        exit(0)
    elif len(sys.argv) == 2:
        apk_file1 = check_args()
        check_exist(apk_file1)
        apk_file1_md5 = get_signed_info(apk_file1)
        print("APK:" + apk_file1)
        print(apk_file1_md5)
    elif len(sys.argv) == 3:
        apk_list = check_args()
        apk_file1 = apk_list[0]
        check_exist(apk_file1)
        apk_file2 = apk_list[1]
        check_exist(apk_file2)
        diff_md5(apk_file1, apk_file2)
