# flow_system
流量检测模型系统
## Folders(flow_system)
* `data_cut/`存放按照五元组切割后的流量样本
* `data_raw/`存放流量收集来的原始样本
* `feature_extract/`存放特征提取后的训练和测试样本
* `flow_cut/`按照五元组切割流量样本模块
* `flow_collect/`采集流量模块
* `model_train/`模型训练模块
* `model_test/`模型测试模块
* `result_show/`结果展示模块
* `flow_system/`配置模块
* `home`主页模块
* `requirement.txt`配置要求
* `manage.py`django主要运行程序
## Data
* `data_raw`存放流量收集来的原始样本
* `data_cut`存放按照五元组切割后的流量样本，其中`flow/`存放普通流量,`tls/`存放加密流量
* `feature_extract/`存放特征提取后的特征，其中`image/`存放图片特征,`flow/`存放流级特征,`tls/`存放加密特征，详细命名规则请看每个文件夹中的readme.txt
## Model
* MGREL
## Model_save
* `model_save/`存放MGREL
## Settings
* `flow_system/settings`中，`DATABASES`设置数据库账号与密码，默认数据库为mysql
## Use
* `python manage.py migrate flow_cut`建立数据库标项
* `python manage.py migrate flow_collect`建立数据库标项
* `python manage.py migrate feature_extract`建立数据库标项
* `python manage.py migrate model_test`建立数据库标项
* `python manage.py makemigrations`保存数据库变动
* `python manage.py runserver`运行本地服务器
## Contributors
@xuxiaohaoer
@sunny778889
@ASUIDH
## Other
