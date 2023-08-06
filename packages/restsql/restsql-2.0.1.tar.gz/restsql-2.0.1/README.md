# RestSQL

## query流程

1. 预处理query_dict: 将子select全部拆出。
2. 从主select开始，到所有子select完成，执行查询并获得一个个dataframe。
3. 删除子dataframe中非export的字段与不在on的字段
4. 将子dataframe join进主dataframe。
5. 根据fields删除多余字段，并执行计算

## 测试

* [x] Gen data
  * [x] pgsql
  * [x] mysql
* [x] Model测试
* [ ] Engine测试
  * [x] SqlEngine
    * [x] pgsql
    * [x] mysql
  * [ ] EsEngine
* [ ] Query测试
  * [x] pgsql
  * [x] mysql
  * [ ] impala
  * [ ] es
