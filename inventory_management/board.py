import pymysql

class cBoard_vo :
    def __init__(self, num = None, id = None, title = None, content = None, w_date = None) :
        self.num = num
        self.id = id
        self.title = title
        self.content = content
        self.w_date = w_date

class cBoard_dao :
    def __init__(self) :
        self.__conn = None
        self.__cur = None

    def __Connect(self) :
        self.__conn = pymysql.connect(host = '127.0.0.1', user = 'root', password = '1234',
                                      db = 'projectdb', charset = 'utf8')
        self.__cur = self.__conn.cursor()

    def __Disconnnect(self) :
        self.__cur = None
        self.__conn.close()

    def Insert(self, vo) :
        self.__Connect()
        sql = 'insert into boardtbl(id, title, content, w_date) values(%s, %s, %s, now())'
        val = (vo.id, vo.title, vo.content)
        self.__cur.execute(sql, val)
        self.__conn.commit()
        self.__Disconnnect()

    def SelectAll(self) :
        boards = []
        self.__Connect()
        sql = 'select * from boardtbl order by num desc'
        self.__cur.execute(sql)
        for row in self.__cur :
            boards.append(cBoard_vo(row[0], row[1], row[2], row[3], row[4]))
        self.__Disconnnect()
        return boards

    def SelectByNum(self, num) :
        self.__Connect()
        try :
            sql = 'select * from boardtbl where num = ' + str(num)
            self.__cur.execute(sql)
        except :
            self.__Disconnnect()
            return None
        row = self.__cur.fetchone()
        self.__Disconnnect()
        if row != None :
            return cBoard_vo(row[0], row[1], row[2], row[3], row[4])


    def SelectByWriter(self, writer) :
        boards = []
        self.__Connect()
        sql = 'select * from boardtbl where id = %s'
        val = (writer, )

        self.__cur.execute(sql, val)
        for row in self.__cur :
            if row != None :
                boards.append(cBoard_vo(row[0], row[1], row[2], row[3], row[4]))
        self.__Disconnnect()
        return boards

    def SelectBytitle(self, word) :
        boards = []
        self.__Connect()
        sql = 'select * from boardtbl where title like %s'
        val = ('%' + word + '%', )

        self.__cur.execute(sql, val)
        for row in self.__cur :
            if row != None :
                boards.append(cBoard_vo(row[0], row[1], row[2], row[3], row[4]))
        self.__Disconnnect()
        return boards

    def DelBoard(self, num) :
        self.__Connect()
        sql = 'delete from boardtbl where num = ' + str(num)
        self.__cur.execute(sql)
        self.__conn.commit()
        self.__Disconnnect()

class cBoardService :
    def __init__(self) :
        self.__dao = cBoard_dao()

    def AddBoard(self, vo) :
        try :
            self.__dao.Insert(vo)
        except :
            return False
        else :
            return True

    def GetAll(self) :
        board = self.__dao.SelectAll()
        return board

    def DelBoard(self, num, id, current_id):
        try :
            if id == current_id or current_id == "admin":
                self.__dao.DelBoard(num)
            else :
                return False
        except :
            return False
        else :
            return True


    def GetByNum(self, num) :
        vo = self.__dao.SelectByNum(num)
        if vo == None :
            return None
        else :
            return vo

    def GetByWriter(self, id) :
        vo_lst = self.__dao.SelectByWriter(id)
        if len(vo_lst) == 0 :
            return None
        else :
            return vo_lst

    def GetBytitle(self, title) :
        vo_lst = self.__dao.SelectBytitle(title)
        if len(vo_lst) == 0 :
            return None
        else :
            return vo_lst
