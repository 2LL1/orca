t以下是一些胡乱的想法，大家有想法尽管往里添加意见。某条达成一致我们就实现他。

基本架构
-------------

### settings.py ###
一个配置文件，用来配置所有的内容，而不用XML配置。各个用户可以根据自己的需求
在自己的PYTHONPATH或别的地方保留自己私有的settings.py。在工程文件夹下有一个
全局的settings.py文件，作为例子和范本。


### [orca] ###
最主要的folder，主要的code都在此。是一个python package。


#### orca.db ####
数据库的实现

#### orca.sim ####
模拟过程的实现

#### orca.alpha ####
alpha的实现

### orca-man.py ###
一个程序的入口点，所有常用功能可以通过他在命令行完成。比如建库，更新数据，
预测，作图，复盘等等。

### [db] ###
SQLITE3的数据库文件保存的folder，在settings.py中由变量DB_PATH指定。用户可以
在settings.py中自由修改。但由于数据库通常都比较大，所有大家还是保留一份完整
的数据库在一个公用folder中。


数据库和数据结构
-------------------


### Ocean ###
Ocean是最主要的数据库模型。凡是符合以下模型的数据都归为Ocean。
1. 数据有一个时间点（可以是对应一天或者一分钟）
2. 数据对应一个股票或者一种指数
3. 数据是一组实数，比如K线图的开票收盘等十二条数据。

Ocean可以有很多种，通过一个全局函数 *ocean(name)* 获取一个ocean的实例，然后该实例
获取对应的frames。以下是一段使用的例子：

    from orca.db import ocean
    k05 = ocean('K05') # K05代表5min K线图。该句获取k05实例

    # 从K05 获取5个DataFrame，包含从14年1月1号到14年9月9号的数据。
    # data.open 代表开票价的DataFrame
    # data.high 代表最高价的DataFrame
    # 以此类推
    data = k05.frames(['open', 'high', 'low', 'close', 'amount'], 140101, 140909)


frames是Ocean最主要的函数。
    def frames(self, names, t1=None, t2=None, cat=None):
该函数包括4个参数，其中
* names是一个字符串列表，表面需要取这个Ocean种的那些数据
* t1是开始时间，如果不给的话默认从最早开始
* t2是结束时间，如果不给的话默认到最后为止
* cat表面股票的种类，是一个字符串。如果不给默认所有股票，给的话则只选择给定的种类，
比如"HS300"代表HS300给定的股票，"Industry"表明工业类的股票，等等等等。


Ocean还应该包括
* init功能，用来初始化数据库（从原始文件或是数据库中导入所有数据）。
* refresh功能，用于更新数据库（从原始数据中读入上次更新以后的数据）。

全局的ocean函数用来获得ocean的实例，我们应该对需要的ocean的名称达成一致。
比如：
* K05，表示5分钟K线的数据
* K01，表示1分钟K线的数据
* KDAY，表示日K线的数据
等等等。
