#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# 脚本功能：上传从Let"s Encrypt申请的 cdn.xxxx.com 的SSL证书到七牛云存储并启用。
# 使用方法: python qiniu_letssl.py
#
# pip install qiniu

import qiniu
from qiniu import DomainManager
import os
import time

def main():
    # 七牛云API相关的AccessKey和SecretKey.
    # access_key = os.getenv("ACCESS_KEY", "")
    access_key = os.getenv("QINIU_ACCESS_KEY")
    secret_key = os.getenv("QINIU_ACCESS_SECRET")
    if not access_key or not secret_key:
        raise Exception("请设置七牛云的AccessKey和SecretKey")
    # 操作的域名
    domain = os.getenv("QINIU_DOMAIN")

    auth = qiniu.Auth(access_key=access_key, secret_key=secret_key)
    domain_manager = DomainManager(auth)

    # Let"s Encrypt申请的证书公钥和私钥文件所在的目录.
    ca = f"~/certs/{domain}/fullchain.pem"
    ca = os.path.expanduser(ca)
    privatekey = f"~/certs/{domain}/privkey.pem"
    privatekey = os.path.expanduser(privatekey)

    with open(privatekey, "r") as f:
        privatekey_str = f.read()

    with open(ca, "r") as f:
        ca_str = f.read()

    ret, info = domain_manager.create_sslcert("{}/{}".format(domain, time.strftime("%Y%m%d_%M%S", time.localtime())),
                                            domain, privatekey_str, ca_str)
    print(ret["certID"])

    if domain.startswith("*"):
        domain = domain[1:]
    ret, info = domain_manager.put_httpsconf(domain, ret["certID"], False)
    print(info)


if __name__ == "__main__":
    main()