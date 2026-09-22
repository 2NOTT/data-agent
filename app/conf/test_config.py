from dataclasses import dataclass
from pathlib import Path

import yaml
from omegaconf import OmegaConf


def load_yaml():
    # 定义yaml文件的路径
    yaml_path = Path(__file__).resolve().parents[2] / "conf" / "test_config.yaml"

    # 打开文件流
    with open(yaml_path, mode='r', encoding='utf-8') as file_stream:
        # 加载yaml文件
        yaml_data = yaml.safe_load(file_stream)
        print(yaml_data, type(yaml_data))
        print(yaml_data['name'])


# 问题：加载得到的数据是字典或字典列表，读取字典中的属性数据不方便：不能通过，属性名获取没有提示
# 解决：使用类来封装字典数据

# 定义yaml文件的路径
yaml_path = Path(__file__).resolve().parents[2] / "conf" / "test_config.yaml"
# 加载yaml文件
yaml_data = OmegaConf.load(yaml_path)
print(yaml_data, type(yaml_data))
print(yaml_data.name) #可以去属性值，但没有提示

#定义数据的模型
@dataclass
class PersonConfig:
    name:str
    age:int
    height:float

#将yaml_data转化为指定类型PersonConfig的对象
person_config=OmegaConf.to_object(OmegaConf.merge(PersonConfig, yaml_data))
print(person_config,type(person_config))
print(person_config.name)