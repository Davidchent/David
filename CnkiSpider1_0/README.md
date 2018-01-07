
使用前，请务必认真研读并遵守此文，严禁用于非法用途！！！

//知网爬虫（python3.x）

#需安装的库：scrapy、urllib、configparser、copy、sqlite3

#使用方法
1.在config.conf文件中修改搜索关键字--keyword、最大获取页数--maxpage
2.打开cmd、cd至CnkiSpider1_0、输入scrapy crawl cnki即可
（推荐使用pycharm）

#注意事项
1.此代码采用搜索引擎接口为http://search.cnki.net/
2.爬取条目为“题目、发表时间、来源、机构、引用/下载次数、关键词、摘要、下载链接”（因页面不同，爬取内容会有变化）
3.爬到的内容存放在cnki.sqlite数据库中，可自行导出到文件
***此项目/代码仅供个人学习交流使用，严禁用于任何商业用途；请务必遵守相关法律法规，严禁给党和国家添麻烦***
***对于任何使用此代码产生的违法犯罪行为，所产生的后果由代码执行者承担***
如需交流，欢迎来件  chendaton@foxmail。com

                   ---作者保留个人权利---