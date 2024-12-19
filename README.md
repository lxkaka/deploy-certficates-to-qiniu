# 上传证书到七牛云

这个项目的主要功能是定期更新 SSL 证书并将证书上传到七牛云。

## 安装

首先，你需要安装项目的依赖。你可以使用以下命令来安装：

```bash
pip install -r requirements.txt
```

## 使用   
你可以使用以下命令来运行这个项目：
```
python upload_cert.py
```
在运行这个命令之前，你需要确保你的证书文件已经放在了正确的位置，并且你已经设置了正确的环境变量。
包含如下环境变量
**QINIU_ACCESS_KEY**  
**QINIU_ACCESS_SECRET**  
**QINIU_DOMAIN** 

### 证书生成
#### 安装 acme   
`curl https://get.acme.sh | sh`
#### 阿里云 ak 和 as 写入配置文件  
vim ～/.acme.sh/acme.sh.env     
修改后acme.sh.env文件变成:    
```bash
export LE_WORKING_DIR="/${用户目录}/.acme.sh"  
alias acme.sh="/${用户目录}/.acme.sh/acme.sh"  
export Ali_Key="*****“
export Ali_Secret=”*******"
```
#### 生成
``` bash
mkdir -p ~/certs/${domain}
acme.sh --issue --dns dns_ali -d ${domain} \
          --key-file ~/certs/${domain}/privkey.pem --fullchain-file ~/certs/${domain}/fullchain.pem
```

## 自动化
这个项目使用GitHub Actions来自动化证书的更新和部署。GitHub Actions会在每两个月的第二十天自动执行这个任务。

你可以在.github/workflows/action.yml文件中查看详细的配置。

update...
