from pathlib import Path

import yaml

#定义yaml文件的路径
yaml_path = Path(__file__).resolve().parents[2] / "conf" / "test_config.yaml"

#打开文件流
with open(yaml_path, mode='r', encoding='utf-8') as file_stream:
    #加载yaml文件
    yaml_data=yaml.safe_load(file_stream)
    print(yaml_data,type(yaml_data))
    print(yaml_data['name'])

#问题：加载得到的数据是字典或字典列表，读取字典中的属性数据不方便：不能通过，属性名获取没有提示
#解决：使用类来封装字典数据

#加载yaml文件
# yaml.safe_load()