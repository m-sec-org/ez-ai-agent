# EZ 工具存放目录

## EZ 自动化渗透工具

将 EZ 工具下载放置于该文件夹下，注意要下载证书。

### 项目地址
https://github.com/m-sec-org/EZ

### 下载地址
https://github.com/m-sec-org/EZ/releases/tag/1.9.2

### 证书申请地址
https://msec.nsfocus.com/

### 本项目推荐使用命令(被动扫描)
```bash
./ez webscan --listen 0.0.0.0:9999 --disable-pocs web-brute --pocs beta-common-fileupload,php-path-disclosure,sqldet,beta-sqldet,php-realpath-leak
```

