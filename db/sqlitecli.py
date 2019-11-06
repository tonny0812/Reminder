# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     sqliteutil
   Description :
   Author :       guodongqing
   date：          2019/11/6
-------------------------------------------------
"""
import json
import sqlite3


#
# 连接数据库帮助类
# 链接：https://www.jb51.net/article/140903.htm
# eg:
#  db = database()
#  count,listRes = db.executeQueryPage("select * from student where id=? and name like ? ", 2, 10, "id01", "%name%")
#  listRes = db.executeQuery("select * from student where id=? and name like ? ", "id01", "%name%")
#  db.execute("delete from student where id=? ", "id01")
#  count = db.getCount("select * from student ")
#  db.close()


#
class SqliteDataBase(object):
    dbfile = "sqlite.db"
    memory = ":memory:"
    conn = None
    showsql = True

    def __init__(self):
        self.conn = self._getConn()

    # 输出工具
    def _out(self, outStr, *args):
        if (self.showsql):
            for var in args:
                if (var):
                    outStr = outStr + ", " + str(var)
            print("db. " + outStr)
        return

    # 获取连接
    def _getConn(self):
        if (self.conn is None):
            conn = sqlite3.connect(self.dbfile)
            if (conn is None):
                conn = sqlite3.connect(self.memory)
            if (conn is None):
                print("dbfile : " + self.dbfile + " is not found && the memory connect error ! ")
            else:
                conn.row_factory = self._dict_factory  # 字典解决方案
                self.conn = conn
            self._out("db init conn ok ! ")
        else:
            conn = self.conn
        return conn

    # 字典解决方案
    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    # 关闭连接
    def close(self, conn=None):
        res = 2
        if (not conn is None):
            conn.close()
            res = res - 1
        if (not self.conn is None):
            self.conn.close()
            res = res - 1
        self._out("db close res : " + str(res))
        return res

    # 加工参数tuple or list 获取合理参数list
    # 把动态参数集合tuple转为list 并把单独的传递动态参数list从tuple中取出作为参数
    def _turnArray(self, args):
        # args (1, 2, 3) 直接调用型 exe("select x x", 1, 2, 3)
        # return [1, 2, 3] <- list(args)
        # args ([1, 2, 3], ) list传入型 exe("select x x",[ 1, 2, 3]) len(args)=1 && type(args[0])=list
        # return [1, 2, 3]
        if (args and len(args) == 1 and (type(args[0]) is list)):
            res = args[0]
        else:
            res = list(args)
        return res

    # 分页查询 查询page页 每页num条 返回 分页前总条数 和 当前页的数据列表 count,listR = db.executeQueryPage("select x x",1,10,(args))
    def _executeQueryPage(self, sql, page, num, *args):
        args = self._turnArray(args)
        count = self.getCount(sql, args)
        pageSql = "select * from ( " + sql + " ) limit 5 offset 0 "
        # args.append(num)
        # args.append(int(num) * (int(page) - 1) )
        self._out(pageSql, args)
        conn = self._getConn()
        cursor = conn.cursor()
        listRes = cursor.execute(sql, args).fetchall()
        return (count, listRes)

    # 查询列表array[map] eg: [{'id': u'id02', 'birth': u'birth01', 'name': u'name02'}, {'id': u'id03', 'birth': u'birth01', 'name': u'name03'}]
    def _executeQuery(self, sql, *args):
        args = self._turnArray(args)
        self._out(sql, args)
        conn = self._getConn()
        cursor = conn.cursor()
        res = cursor.execute(sql, args).fetchall()
        return res

    # 执行sql或者查询列表 并提交
    def _execute(self, sql, *args):
        args = self._turnArray(args)
        self._out(sql, args)
        conn = self._getConn()
        cursor = conn.cursor()
        # sql占位符 填充args 可以是tuple(1, 2)(动态参数数组) 也可以是list[1, 2] list(tuple) tuple(list)
        res = cursor.execute(sql, args).fetchall()
        conn.commit()
        # self.close(conn)
        return res

    # 查询列名列表array[str] eg: ['id', 'name', 'birth']
    def _getColumnNames(self, sql, *args):
        args = self._turnArray(args)
        self._out(sql, args)
        conn = self._getConn()
        if (not conn is None):
            cursor = conn.cursor()
            cursor.execute(sql, args)
            res = [tuple[0] for tuple in cursor.description]
        return res

    # 查询结果为单str eg: 'xxxx'
    def _getString(self, sql, *args):
        args = self._turnArray(args)
        self._out(sql, args)
        conn = self._getConn()
        cursor = conn.cursor()
        listRes = cursor.execute(sql, args).fetchall()
        columnNames = [tuple[0] for tuple in cursor.description]
        # print(columnNames)
        res = ""
        if (listRes and len(listRes) >= 1):
            res = listRes[0][columnNames[0]]
        return res

    # 查询记录数量 自动附加count(*) eg: 3
    def _getCount(self, sql, *args):
        args = self._turnArray(args)
        sql = "select count(*) cc from ( " + sql + " ) "
        resString = self._getString(sql, args)
        res = 0
        if (resString):
            res = int(resString)
        return res


class User(object):
    def __init__(self, account, name, tel, email, order):
        self.account = account
        self.name = name
        self.tel = tel
        self.email = email
        self.isValid = 1
        self.order = order


class SqliteUserDB(SqliteDataBase):
    def __init__(self):
        self.meeting_user_path = 'meetinguser.json'
        self.mis_user_path = 'misuser.json'

    def __del__(self):
        self.close()

    def __createTable(self):
        misuser_create_sql = ''' 
                                create table if not exists misuser(
                                  account   text primary key,
                                  name  text not null,
                                  tel  text not null,
                                  email text not null,
                                  is_valid int not null default 1,
                                  order_n int not null
                                )
                                '''
        meetinguser_create_sql = ''' 
                                create table if not exists meetinguser(
                                  account   text primary key,
                                  name  text not null,
                                  tel  text not null,
                                  email text not null,
                                  is_valid int not null default 1,
                                  order_n int not null
                                )
                                '''
        self._execute(misuser_create_sql)
        self._execute(meetinguser_create_sql)

    def initMeetingUsers(self):
        self.__createTable()
        userlist = []
        with open(self.meeting_user_path, 'rb') as meetingfile:
            content = meetingfile.read()
            userlist_json = json.loads(content, encoding='utf-8')
            for user_json in userlist_json:
                user = User(**user_json)
                userlist.append(user)
        try:
            self.insert_meetingusers(userlist)
        except Exception as e:
            print(e)

    def initMisUsers(self):
        self.__createTable()
        userlist = []
        with open(self.mis_user_path, 'rb') as misfile:
            content = misfile.read()
            userlist_json = json.loads(content, encoding='utf-8')
            for user_json in userlist_json:
                user = User(**user_json)
                userlist.append(user)
        try:
            self.insert_misusers(userlist)
        except Exception as e:
            print(e)

    def insert_meetingusers(self, users):
        insert_sql = "insert into meetinguser values "
        values = []
        for user in users:
            user_info = []
            user_info.append('"{0}"'.format(user.account))
            user_info.append('"{0}"'.format(user.name))
            user_info.append('"{0}"'.format(user.tel))
            user_info.append('"{0}"'.format(user.email))
            user_info.append(str(user.isValid))
            user_info.append(str(user.order))
            value = ",".join(user_info)
            value = "(" + value + ")"
            values.append(value)
        insert_sql += ",".join(values)
        result = self._execute(insert_sql)

    def insert_misusers(self, users):
        insert_sql = "insert into misuser values "
        values = []
        for user in users:
            user_info = []
            user_info.append('"{0}"'.format(user.account))
            user_info.append('"{0}"'.format(user.name))
            user_info.append('"{0}"'.format(user.tel))
            user_info.append('"{0}"'.format(user.email))
            user_info.append(str(user.isValid))
            user_info.append(str(user.order))
            value = ",".join(user_info)
            value = "(" + value + ")"
            values.append(value)
        insert_sql += ",".join(values)
        result = self._execute(insert_sql)

    def update_meetinguser(self, user):
        update_sql = "update meetinguser set tel = ?, email = ?, is_valid = ? where account = ?"
        result = self._execute(update_sql, user.tel, user.email, user.isValid, user.account)

    def disable_meetinguser(self, account):
        update_sql = "update meetinguser set is_valid = 0 where account = ?"
        result = self._execute(update_sql, account)

    def able_meetinguser(self, account):
        update_sql = "update meetinguser set is_valid = 1 where account = ?"
        result = self._execute(update_sql, account)

    def query_meetinguser_by_account(self, account):
        query_sql = "select * from meetinguser where account = ?"
        return self._executeQuery(query_sql, account)

    def get_meetinguser_all(self):
        query_sql = "select * from meetinguser where 1=1"
        return self._executeQuery(query_sql)

    def get_meetinguser_all_count(self):
        query_sql = "select * from meetinguser where 1=1"
        return self._getCount(query_sql)

    def get_meetinguser_all_valid(self):
        query_sql = "select * from meetinguser where is_valid = 1"
        return self._executeQuery(query_sql)

    def get_meetinguser_all_count_valid(self):
        query_sql = "select * from meetinguser where is_valid = 1"
        return self._getCount(query_sql)


################初始化####################
def init():
    userdb = SqliteUserDB()
    userdb.initMeetingUsers()
    userdb.initMisUsers()
    userdb.close()


if __name__ == '__main__':
    init()
