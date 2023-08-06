# shopex_dingding_note_2.x
消息推送到钉钉

安装方式
    
    一、
        1、git clone https://github.com/magic119/shopex-dingding-notify-2.x.git

        2、切换到文件夹下，找到setup.py，在终端执行 python setup.py install 会自动将项目安装到第三方库中
        在执行命令之前，选择好对应的python版本，2.7.x

    二、推荐使用
        pip install -i https://pypi.org/simple/ 

使用方式
    
    注意！
    创建客户端时，已经启动发送消息的线程，因此程序不会有异常信息抛出，会在控制台打印出可能产生的异常。发送消息时，请传入正确格式的字典数据
    {"time": 事件产生时间, "main": "事件产生主体", "service": "所属服务", "message": 消息内容}

    1、控制台打印的信息可以在安装好库中的conf文件夹的config.py中配置(不建议修改)，其他配置作用的详细信息请参考config.py中的
    注释。

    2、导入客户端，创建实例
    from dingding_client.notice_client import NoticeClient
    app_key = "xxx"
    app_secret = "xxx"
    api_url = "xxx"

    client = NoticeClient(app_key=self.app_key, app_secret=self.app_secret, api_url=self.api_url)
    
    # 第一个参数是一个列表，表示要发送给谁
    # 第二个参数也是一个列表， 表示mq消息队列
    client.send(["s4261"], ["dingding"])