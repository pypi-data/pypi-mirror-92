IUpdatable
=======================

封装常用函数

详细文档：https://www.cnblogs.com/IUpdatable/articles/12500039.html

Installation
-----

首次安装：

```bash
pip install iupdatable
```

更新安装：

```bash
pip install --upgrade iupdatable
```


-----

### 更新日志：

* v 0.2.4: 增加  WeiXinCrawler 类, 用于抓取微信公众号历史消息。

* v 0.2.2: 增加 Timer 类

> Timer 主要函数：
> * 获取 Unix 时间戳（精确到秒）：timestamp、unix、unix10
> * 获取 Unix 时间戳（精确到毫秒）：timestamp13、unix13
> * 随机等待若干秒：sleep_range、sleep_range_async
> * Unix 时间戳转换成 datetime：unix_to_datetime、timestamp_to_datetime
> * Unix 时间戳转换成 datetime 字符串：unix_to_datetime_str、timestamp_to_datetime_str

* v 0.2.0: 修复多进程下写入日志报错问题
> * 多进程下操作日志会报错：[WinError 32] 另一个程序正在使用此文件，进程无法访问。
>   这里通过添加 concurrent_log_handler 模块 替换掉系统内置的 TimedRotatingFileHandler 解决。

* v 0.1.9: 添加 Status 类
> * 详细说明文章：[[Python] iupdatable包：Status 模块使用介绍](https://www.cnblogs.com/IUpdatable/p/14140258.html)


### 文件 - File
- read： 读取文件
- write： 写入文件
- append：追加写入文件
- append_new_line：新建一行，然后追加写入文件
- read_lines： 按行一次性读取文件
- write_lines：按行一次性写入文件
- write_csv：写入CSV文件
- read_csv：读取CSV文件
- exist_within_extensions: 检查一个文件是否存在（在指定的几种格式中）
- get_file_path_within_extensions: 获取一个文件的路径（在指定的几种格式中）

简单实例:

```python
from iupdatable.system.io.File import File


sample_text = 'this is sample text.'
sample_texts = ['123', 'abc', 'ABC']
append_text = 'this is append text.'

# 写入
File.write('1.txt', sample_text)
File.write_lines('2.txt', sample_texts)

File.append('1.txt', append_text)
File.append_new_line('2.txt', append_text)

# 读取
read_text1 = File.read('1.txt')
read_text2 = File.read_lines('2.txt')

# 打印输出
print(read_text1)
print(read_text2)
```

### 日志 - logging

简单实例：

```python
from iupdatable.logging.Logger import Logger
from iupdatable.logging.LogLevel import LogLevel


def test_logging():
    # 日志等级：
    # CRITICAL  同：FATEL，下同
    # ERROR
    # WARNING
    # INFO
    # DEBUG
    # NOTSET    按照 WARNING 级别输出

    # 设置为 DEBUG，输出所有信息
    # 设置为 WARNING, INFO、DEBUG 级别的日志就不会输出
    Logger.get_instance().config(log_level=LogLevel.DEBUG)

    Logger.get_instance().debug('debug message1')
    Logger.get_instance().info('info message1')
    Logger.get_instance().warning('warning message1')
    Logger.get_instance().error('error message1')
    Logger.get_instance().debug('debug message1', is_with_debug_info=True)  # 要想输出具体的调试信息
    Logger.get_instance().fatal('fatal message1')
    Logger.get_instance().critical('critical message1')  # fatal = critical

    # 也可以输出变量
    abc = [1, 2, 4]
    Logger.get_instance().info(abc)


test_logging()
```

### Base64
- encode：base64编码
- decode：base64解码
- encode_multilines：base64多行解码
- decode_multilines：base64多行解码

### CSProduct

```python
from iupdatable.system.hardware import CSProduct

# 一次性获取所有的CSProduct信息
cs_product = CSProduct.get()
print("CSProduct: " + str(cs_product))
print(cs_product["Caption"])

# 或者
# 使用各项函数单独获取
print("Caption: " + CSProduct.get_caption())
print("Description: " + CSProduct.get_description())
print("IdentifyingNumber: " + CSProduct.get_identifying_number())
print("Name: " + CSProduct.get_name())
print("SKUNumber: " + CSProduct.get_sku_number())
print("UUID: " + CSProduct.get_uuid())
print("Vendor: " + CSProduct.get_vendor())
print("Version: " + CSProduct.get_version())

```

### UMeng

友盟统计

这里使用了自定义事件统计的功能

创建网站类型的统计，第一个参数是统计代码中的id

```python
UMeng.log_stat(1211111111, '来源页面', '目录', '行为', '标签')
```

License
-------
MIT