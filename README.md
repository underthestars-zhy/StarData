# StarData
> 一个现代的云数据系统

## 安装
1. 下载最新版本源代码
2. 按照必要的库: `pip install fastapi`和`pip install uvicorn`
3. 请确保`./config/data.json`内容为**空**
4. 编辑`./data.json`，请按照对应格式
5. 使用`uvicorn app:app`运行
6. 愉快玩耍

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
* 