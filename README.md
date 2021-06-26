# StarData
> 一个现代的云数据系统

## 安装
1. 下载最新版本源代码
2. 按照必要的库: `pip install fastapi`和`pip install uvicorn`
3. 请确保`./config/data.json`内容为**空**
4. 编辑`./data.json`，请按照对应格式
5. 编译`./info.py`，请按照下面教程**验证**
6. 使用`uvicorn app:app`运行
7. 愉快玩耍

## 格式
### 数据集
整个`./data.json`包含了与数据有关的所有信息。 我们将其成为**数据集**。
```json
{
  "data_version": 1.0,
  "db": []
}
```
* `db_version`表示数据集的版本，每次更新数据集内的任何内容都需要更新这个版本。
* `db`内是所有的数据库信息。
### 数据库
一个数据集允许拥有多个**数据库**，每个数据库是单独的一个`.db`文件。
```json
{
  "db_name": "star",
  "db_table": []
}
```
* `db_name`是这个数据库的名称
* `db_table`储存这个数据库的所有**表**
* 将数据库放入数据集的`db`数组中
### 表
一个数据库拥有多个**表**，表可以看作是编程语言中的一个类的定义。
```json
{
  "table_name": "main",
  "table_parameter": []
}
```
* `table_name`是这个表的名称
* `table_parameter`存放表的**参数**，可以看作类中的属性
* 将表防暑数据库的`db_table`中
### 参数
一个表可以定义多个**参数**，我们建议将参数名称大写(当然也会自动转换)。
```json
{
  "parameter_name": "id",
  "is_primary": true,
  "not_null": true,
  "parameter_type": "uuid"
}
```
* `parameter_name`这个参数的名称
* `is_primary`告知此参数是否为**主键**，一个表只能有一个
* `not_null`告知该参数是否可以赋值**NULL**
* `parameter_type`告知该参数的类型，请详见下面教程**类型**
* 将参数放入表的`table_parameter`中
## 验证
为了保护数据安全，我们在每次操作都需要验证。验证有`./info.py`控制
* `api_key`是URL参数中需要携带的验证字符串，如`https://xxx.xxx/xxx?api=xxx`
* `private_key`是在post请求中需要的密钥
* `salt`使用跟随在`private_key`后的盐

在每个**post**请求中，`key`应该是`private_key`+`salt`的MD5(不区分大小写)。
## 类型
### uuid
* 单字节字符串
* 默认值为`uuid1()`的生成值
* 在where等操作中应该使用`''`包裹值
* 在SQL中对应`TEXT`
### string
* 双字节字符串，支持中文/英文等
* 默认值为`'this is a null value'`
* 在where等操作中应该使用`''`包裹值
* 在SQL中对应`NTEXT`
### int
* 有符号整数，位数由SQLite自身决定
* 默认值为`0`
* 在where等操作中可以直接输入整数
* 在SQL中对应`INTEGER`
### double
* 64位有符号小数
* 默认值为`0.0`
* 在where等操作中可以直接输入小数
* 在SQL中对应`DOUBLE`
### en-str
* 单字节字符串
* 默认值为`'this is a null value'`
* 在where等操作中应该使用`''`包裹值
* 在SQL中对应`TEXT`
### null
* null，不可加入`not_null`为`true`的参数中
* 默认值位`NULL`
* 在where等操作中可以直接输入
* 在SQL中对应`NULL`
## API
> 为了演示所有URL由`http://127.0.0.1:8000`代替

我们基于`fastapi`完整所有网络操作。
### 获取数据库信息
* 请求方式`get`
* 需要api
```http request
GET /db_info?api=ahdi1e3 HTTP/1.1
Host: 127.0.0.1:8000
Connection: close
User-Agent: Paw/3.2.2 (Macintosh; OS X/12.0.0) GCDHTTPRequest
```
### 插入数据
* 请求方式`get`
* 需要api和key
* 使用json发生post数据
* 对于没有给出的参数会自动填充默认值
```json
{
  "db_name": "数据库名称",
  "table_name": "表名称",
  "insert_data": {
    "参数名称": "值"
  },
  "key": "md5加盐密钥"
}
```
```http request
POST /insert?api=ahdi1e3 HTTP/1.1
Content-Type: text/plain; charset=utf-8
Host: 127.0.0.1:8000
Connection: close
User-Agent: Paw/3.2.2 (Macintosh; OS X/12.0.0) GCDHTTPRequest

{
  "db_name": "star",
  "table_name": "main",
  "insert_data": {
    "name": "这是中文"
  },
  "key": "03CE1890B3456B7D09FF56C981659189"
}
```
### 更新数据
* 请求方式`get`
* 需要api和key
* 使用json发生post数据
* 每个数据更新组的标识符要在`conditions`中有对应值
```json
{
  "key": "md5加盐密钥",
  "db_name": "数据库名",
  "table_name": "表名",
  "conditions": {
    "标识符1": "where条件语句",
    "标识符2": "where条件语句"
  },
  "new_data": {
    "标识符1": {
      "参数名称": "新的参数值"
    },
    "标识符2": {
      "参数名称": "新的参数值"
    }
  }
}
```
```http request
POST /update?api=ahdi1e3 HTTP/1.1
Content-Type: text/plain; charset=utf-8
Host: 127.0.0.1:8000
Connection: close
User-Agent: Paw/3.2.2 (Macintosh; OS X/12.0.0) GCDHTTPRequest

{
  "key": "03CE1890B3456B7D09FF56C981659189",
  "db_name": "star",
  "table_name": "main",
  "conditions": {
    "name": "name = 'cc'",
    "t": "name = 'ee'"
  },
  "new_data": {
    "name": {
      "name": "ddddddddd"
    },
    "t": {
      "name": "dd"
    }
  }
}
```
### 删除数据
* 请求方式`get`
* 需要api和key
* 使用json发生post数据
```json
{
  "key": "md5加盐密钥",
  "db_name": "数据库名",
  "table_name": "表名",
  "condition": "查询条件"
}
```
```http request
POST /delete?api=ahdi1e3 HTTP/1.1
Content-Type: text/plain; charset=utf-8
Host: 127.0.0.1:8000
Connection: close
User-Agent: Paw/3.2.2 (Macintosh; OS X/12.0.0) GCDHTTPRequest

{
  "key": "03CE1890B3456B7D09FF56C981659189",
  "db_name": "star",
  "table_name": "main",
  "condition": "name = 'dd'"
}
```
### 搜索数据
* 请求方式`get`
* 需要api和key
* 使用json发生post数据
* 返回值有`value_dict`即以dict组成的数据，类似于`[{}]`
* 返回值有`value_list`即以list组成的数据，类似与`[[]]`
```json
{
  "key": "md5加盐密钥",
  "db_name": "数据库名称",
  "table_name": "表名称",
  "select_parameter": [
    "搜索值"
  ],
  "other": "附加语句，可以没有这个参数，即可选"
}
```
```http request
POST /select?api=ahdi1e3 HTTP/1.1
Content-Type: text/plain; charset=utf-8
Host: 127.0.0.1:8000
Connection: close
User-Agent: Paw/3.2.2 (Macintosh; OS X/12.0.0) GCDHTTPRequest

{
  "key": "03CE1890B3456B7D09FF56C981659189",
  "db_name": "star",
  "table_name": "main",
  "select_parameter": [
    "NAME"
  ],
  "other": "where ID='0affdf9e-d681-11eb-a421-acde48001122'"
}
```
返回值:
```json
{
  "type": "select",
  "message": "Successful search",
  "value_dict": [
    {
      "NAME": "ddddddddd"
    }
  ],
  "value_list": [
    [
      "ddddddddd"
    ]
  ]
}
```
## TODO
- [ ] 完成数据集更新
- [ ] 完成更新映射
- [ ] 完成文件等储存
- [ ] 完成python和swift库