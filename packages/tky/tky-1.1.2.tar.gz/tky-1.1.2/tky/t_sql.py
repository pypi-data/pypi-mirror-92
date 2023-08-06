# _*_ coding:utf-8 _*_
"""
常用SQL类集合
\n 目前支持的有：
\n Oracle(names/set_one/set_all/upd_del) （Oracle类，依赖cx_Oracle）
\n Es(read_es) （ES类，依赖elasticsearch）
\n @author: 'TangKaiYue'
"""


# Oracle数据相关集合
class Oracle:
    """
    【Oracle数据相关集合】\n
    \n 目前已支持方法：
    \n 1、names | 数据库连接配置(依赖cx_Oracle)
    \n 2、set_one | 查询数据表的第一条数据
    \n 3、set_all | 查询数据表的所有数据
    \n 4、upd_del | 修改/删除数据表的数据
    """

    # 数据库连接配置
    def names(self: str = 'null', pwd: str = 'null', url: str = 'null'):
        """
        【Oracle数据库连接方法】\n
        :param self :  str 用户名；
        :param pwd :  str 密码；
        :param url :  str  数据库连接(包含服务名)；
        :return: 输出数据库连接结果；
        """
        try:
            # 判断必要入参
            if self == 'null' or pwd == 'null' or url == 'null':
                return print("异常：数据库的 账号、密码、URL 都不能为空...")
            else:
                import cx_Oracle  # 模块引用
                cs = cx_Oracle.connect(str(self), str(pwd), str(url), encoding="UTF-8")
                return cs
        except EnvironmentError as err:
            return '发生异常：%s' % err

    # 查询数据表的第一条数据
    def set_one(self: str = 'null', conn: str = 'null'):
        """
        【查询数据表的第一条数据】\n
        :param self :  str sql语句；
        :param conn: str 数据库连接,如：oracle.names()；
        :return:  输出结果；
        """
        try:
            # 判断必要入参
            if conn == 'null' or self == 'null':
                return print("异常：SQL语句、数据库连接值 不能为空！！！（PS:连接值可参考连接方法oracle.names()）")
            else:
                if self:
                    # 获取游标
                    with conn.cursor() as cursor:
                        try:
                            cursor.execute(self)
                        except Exception as e:
                            cursor.close()  # 关闭游标
                            return print('发生异常:%s \n传入的SQL：%s; 数据连接：%s' % (e, self, conn))
                        else:
                            val_one = cursor.fetchone()
                            return val_one
        except EnvironmentError as err:
            return '发生异常：%s' % err

    # 查询数据表的所有数据
    def set_all(self: str = 'null', conn: str = 'null'):
        """
        【查询数据表的所有数据】\n
        使用注意：大量数据查询不建议使用此项功能；\n
        :param self :  str sql语句；
        :param conn: str 数据库连接,如：oracle.names()；
        :return:  输出结果；
        """
        try:
            # 判断必要入参
            if conn == 'null' or self == 'null':
                return "异常：SQL语句、数据库连接值 不能为空！！！（PS:连接值可参考连接方法oracle.names()）"
            else:
                if self:
                    # 获取游标
                    with conn.cursor() as cursor:
                        try:
                            cursor.execute(self)
                        except Exception as e:
                            cursor.close()  # 关闭游标
                            return print('发生异常:%s \n传入的SQL：%s; 数据连接：%s' % (e, self, conn))
                        else:
                            val_one = cursor.fetchall()
                            v_list = list(val_one)
                            return v_list
        except EnvironmentError as err:
            return '发生异常：%s' % err

    # 修改/删除数据表的数据
    def upd_del(self: str = 'null', conn: str = 'null'):
        """
        【修改数据表的数据】\n
        :param self :  str sql语句；
        :param conn: str 数据库连接,如：oracle.names()；
        :return:  输出结果；
        """
        try:
            # 判断必要入参
            if self == 'null' or conn == 'null':
                return "异常：SQL语句、数据库连接值 都不能为空！！！（PS:连接值可参考连接方法oracle.names()）"
            else:
                if self:
                    # 获取游标
                    with conn.cursor() as cursor:
                        try:
                            cursor.execute(self)
                        except Exception as e:
                            conn.rollback()  # 事务回滚
                            cursor.close()  # 关闭游标
                            return print('发生异常:%s \n传入的SQL：%s; 数据连接：%s' % (e, self, conn))
                        else:
                            conn.commit()  # 事务提交
                            update_nums = cursor.rowcount
                            return print('执行成功：', update_nums)
        except EnvironmentError as err:
            return '发生异常：%s' % err


# ES数据相关集合
class Es:
    """
    【ES数据相关集合】\n
    \n 目前已支持方法：
    \n 1、read_es | 链接ES数据并查询(依赖elasticsearch)
    """

    # 链接ES并查询
    def read_es(self, port, index, querys: str = '{ "query": { "match_all": {} } }'):
        """
        【连接es数据】\n
        :param self: es的host；
        :param port: 连接端口；
        :param index: 索引名；
        :param querys: 查询条件；
        :return: 查询结果
        """
        try:
            from elasticsearch import Elasticsearch, helpers
            url = {"host": self, "port": port, "timeout": 150}
            es = Elasticsearch([url])
            if es.ping():
                print("Successfully connect!")
                query = querys
                res = helpers.scan(es, index=index, scroll="20m", query=query)
                return res
            else:
                print("Failed.....")
                exit()
        except EnvironmentError as err:
            return '发生异常：%s' % err
