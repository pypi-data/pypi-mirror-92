# scrapy-appauth

## 安裝方法

使用 pip 安裝

    $ pip install scrapy-appleauth

或者使用 pipenv 安装

    $ pipenv install scrapy-appleauth

## 配置

1. 在 Scrapy 中的 settings.py 加入：

        APPLE_SECURE = 'YOUR_AUTHKEY.p8'
        APPLE_KEY = 'YOUR_KEY'
        APPLE_ISS = 'YOUR_ISS'
        APPLE_EXPIRE = 20

2. 在 Scrapy 中的 settings.py 配置中间件：

        DOWNLOADER_MIDDLEWARES = {
            'scrapy-appleauth.appleauth.AppleAuthDownloaderMiddleware': 555
        }

    或者在 Spider 的 custom_settings 中配置：

        custom_settings = {
            'DOWNLOADER_MIDDLEWARES': {
                'scrapy-appleauth.appleauth.AppleAuthDownloaderMiddleware': 555
            }
        }

3. 配置完成，可以使用 Apple Restful API 抓取数据了

## 备注

Develop Apple：[https://developer.apple.com/documentation/](https://developer.apple.com/documentation/)