
import pymysql

#num, prodname, count, price
class ProdVo:
    def __init__(self, num=None, prodname=None, count=None, price=None):
        self.num= num
        self.prodname = prodname
        self.count = count
        self.price = price


class ProdDao:
    def __init__(self):
        self.conn = None    #커넥션 객체 담을 멤버 변수

    #db연결함수. db 사용전 로그인하는 작업을 수행
    def connect(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1234', db='projectdb', charset='utf8')

    #db 닫는 함수
    def disconnect(self):
        self.conn.close()

    def insert(self, vo):
        self.connect()
        cur = self.conn.cursor()
        sql = 'insert into prodtbl(prodname, count, price) values(%s, %s, %s)'
        vals = (vo.prodname, vo.count, vo.price)
        try:
            cur.execute(sql, vals)
            self.conn.commit()
        except :
            self.disconnect()
            return False
        else :
            self.disconnect()
            return True


    def selectAll(self):
        prodtbls = []
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from prodtbl'
        try:
            cur.execute(sql)
            for row in cur:
                prodtbls.append(ProdVo(row[0], row[1], row[2], row[3]))
            self.disconnect()
            return prodtbls
        except :
            return None


    def selectByNum(self, num):
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from prodtbl where num=%s'
        vals = (num,)
        try:
            cur.execute(sql, vals)#읽기동작은 검색 결과를 커서에 담는다
            row = cur.fetchone()  #검색결과 한줄 추출. 한줄은 여러개의 컬럼으로 구성됨
            self.disconnect()
            if row != None:
                return ProdVo(row[0], row[1], row[2], row[3])
        except :
            self.disconnect()
            return None


    def selectByProdname(self, prodname):#검색결과는 여러행. 리스트에 담아서 반환.
        prodtbls = []
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from prodtbl where prodname like %s'
        vals = ("%" + prodname + "%")
        try:
            cur.execute(sql, vals)
            for row in cur:
                prodtbls.append(ProdVo(row[0], row[1], row[2], row[3]))
            self.disconnect()
            return prodtbls
        except :
            self.disconnect()
            return None

    def editProd(self, num, option, val):
        self.connect()
        cur = self.conn.cursor()
        if option == "prodname" :
            sql = 'update prodtbl set ' + option + ' = ' + "'" + val  + "'" + ' where num = ' + str(num)
        else :
            sql = 'update prodtbl set ' + option + ' = ' + val + ' where num = ' + str(num)
        try:
            cur.execute(sql) #execute() 쓰기작업(insert, update, delete)하면 적용된 줄수를 반환
            self.conn.commit()
            self.disconnect()
            return True
        except :
            self.disconnect()
            return False

    def delProd(self, num):
        self.connect()
        cur = self.conn.cursor()
        sql = 'delete from prodtbl where num=%s'
        vals = (num,)
        try:
            line = cur.execute(sql, vals)
            self.conn.commit()
            self.disconnect()
            return True
        except :
            self.disconnect()
            return False


class ProdService:
    def __init__(self):
        self.dao = ProdDao()

    def addProd(self, vo):
        if self.dao.insert(vo) :
            return True
        else :
            return False

    def getAll(self):
        prodtbls = self.dao.selectAll()
        return prodtbls

    def getByNum(self, num):
        vo = self.dao.selectByNum(num)
        if vo==None:
            return None
        else:
            return vo

    def getByProdname(self, name):
        vo_list = self.dao.selectByProdname(name)
        return vo_list

    def editProd(self, num, option, val):
        if self.dao.editProd(num, option, val) :
            return True
        else :
            return False

    def delProd(self, num):
        if self.dao.delProd(num) :
            return True
        else :
            return False
