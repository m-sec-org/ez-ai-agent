FROM php:7.4-apache

# 安装 mysqli 扩展
RUN docker-php-ext-install mysqli

# 启用 Apache rewrite 模块
RUN a2enmod rewrite

COPY . /var/www/html

# 设置工作目录
WORKDIR /var/www/html

# 设置目录权限
RUN chown -R www-data:www-data /var/www/html