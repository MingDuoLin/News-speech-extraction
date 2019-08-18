import pymysql
import sys
sys.path.append('../')

from utils.tools import token, cut


class DatabaseHandle(object):
    """
    定义Mysql操作类
    """

    def __init__(self, host, username, password, database, port):
        """
        初始化创建数据
        """
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.db = pymysql.connect(
            self.host, self.username, self.password,
            self.database, self.port,
        )

    def select(self, sql):
        """
        数据库查询
        :param sql: 查询语句
        :return: 表的内容
        """
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
        except Exception as e:
            print('error:{}\n'.format(e))
            return
        data = cursor.fetchall()  # 返回所有的内容
        with open('news-sql.txt', 'w', encoding='utf-8') as fp:
            for i in range(len(data)):
                if not data[i][0]:
                    print(data[i][0])
                    continue
                res = cut(token(''.join(data[i][0].split('\\n'))))
                print('Finished {}\n'.format(i))
                fp.write(res)

    def close(self):
        """
        关闭数据库链接
        """
        self.db.close()


if __name__ == "__main__":
    host = 'rm-8vbwj6507z6465505ro.mysql.zhangbei.rds.aliyuncs.com'
    username = 'root'
    password = 'AI@2019@ai'
    database = 'stu_db'
    port = 3306
    lite = 'news_chinese'

    db = DatabaseHandle(
        host, username, password, database, port,
    )

    print('db connect success\n')

    sql = 'select content from news_chinese'
    db.select(sql)
    db.close()
