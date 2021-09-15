import pymysql

class OrderVo:
    def __init__(self, id=None, prodnum=None, prodname=None, amount=None, state=None, ordernum = None):
        self.id = id                #출고요청자 id
        self.prodnum= prodnum       #제품번호
        self.prodname = prodname    #제품명
        self.amount = amount        #수량
        self.state = state          #출고처리상태
        self.ordernum = ordernum


class OrderDao: #member 테이블과 관련된 db 작업만 구현
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
        sql = 'insert into ordertbl(id, prodnum, prodname) values(%s, %s, %s)'
        vals = (vo.id, str(vo.prodnum), vo.prodname)
        try:
            cur.execute(sql, vals)
            self.conn.commit()
            self.disconnect()
            return True
        except :
            self.disconnect()
            return False


    def selectAll(self, state):
        ordertbls = []
        self.connect()
        cur = self.conn.cursor()
        sql = 'select * from ordertbl where state = %s'
        val = (state, )
        try:
            cur.execute(sql, val)
            for row in cur:
                ordertbls.append(OrderVo(row[0], row[1], row[2], row[3], row[4], row[5]))
            self.disconnect()
            return ordertbls
        except :
            self.disconnect()
            return None

    def selectByNum(self, id, prodnum):
        ordertbls = []
        self.connect()
        cur = self.conn.cursor()
        if id == "admin" :
            sql = 'select * from ordertbl where prodnum = ' + str(prodnum) + ' and state = %s'
            vals = ("준비중", )
        else :
            sql = 'select * from ordertbl where prodnum = ' + str(prodnum) + ' and id = %s and state = %s'
            vals = (id, "대기")
        try:
            cur.execute(sql, vals)#읽기동작은 검색 결과를 커서에 담는다
            for row in cur:
                ordertbls.append(OrderVo(row[0], row[1], row[2], row[3], row[4], row[5]))
            self.disconnect()
            return ordertbls
        except Exception as err:
            print(err)
            self.disconnect()
            return None

    def selectById(self, id, state, val):#검색결과는 여러행. 리스트에 담아서 반환.
        ordertbls = []
        self.connect()
        cur = self.conn.cursor()
        if id == "admin" :
            sql = 'select * from ordertbl where id like %s and state = %s'
            vals = ('%' + val + '%', state)
        else :
            if state == "대기" :
                sql = 'select * from ordertbl where id = %s and state = %s'
                vals = (id, state)
            else :
                sql = 'select * from ordertbl where id=%s and state != %s'
                vals = (id, "대기")
        try:
            cur.execute(sql, vals)
            for row in cur:
                ordertbls.append(OrderVo(row[0], row[1], row[2], row[3], row[4], row[5]))
            self.disconnect()
            return ordertbls
        except :
            self.disconnect()
            return None

    def selectByName(self, id, prodname):
        ordertbls = []
        self.connect()
        cur = self.conn.cursor()
        prodname = '%'+prodname+'%'
        if id == "admin" :
            sql = 'select * from ordertbl where prodname like %s and state = %s'
            vals = (prodname, "준비중")
        else :
            sql = 'select * from ordertbl where prodname like %s and id = %s and state = %s'
            vals = (prodname, id, "대기")
        try:
            cur.execute(sql, vals)
            for row in cur:
                ordertbls.append(OrderVo(row[0], row[1], row[2], row[3], row[4], row[5]))
            self.disconnect()
            return ordertbls
        except :
            self.disconnect()
            return None

    def editOrder(self, id, num, val):
        self.connect()
        cur = self.conn.cursor()
        sql = 'update ordertbl set amount = ' + str(val) + ' where ordernum = ' + str(num) + ' and id = %s'
        vals = (id, )
        try:
            cur.execute(sql, vals) #execute() 쓰기작업(insert, update, delete)하면 적용된 줄수를 반환
            self.conn.commit()
            self.disconnect()
            return True
        except :
            self.disconnect()
            return False

    def editState(self, id, num, state):
        self.connect()
        cur = self.conn.cursor()
        sql = 'update ordertbl set state = %s where ordernum = ' + str(num) + ' and id = %s'
        vals = (state, id)
        try:
            cur.execute(sql, vals) #execute() 쓰기작업(insert, update, delete)하면 적용된 줄수를 반환
            self.conn.commit()
            self.disconnect()
            return True
        except Exception as err:
            print(err)
            self.disconnect()
            return False



    def delOrder(self, id, num):
        self.connect()
        cur = self.conn.cursor()
        sql = 'delete from ordertbl where ordernum = ' + str(num) + ' and id = %s'
        vals = (id,)
        try:
            cur.execute(sql, vals)
            self.conn.commit()
            self.disconnect()
            return True
        except :
            self.disconnect()
            return False


class OrderService:
    def __init__(self):
        self.dao = OrderDao()

    def addOrder(self, id, num, name):
        if self.dao.insert(OrderVo(id = id, prodname = name, prodnum = num)) :
            return True
        else :
            return False


    def getAll(self, state = "대기"):
        Ordertbls = self.dao.selectAll(state)
        if Ordertbls == None :
            return None
        else :
            return Ordertbls

    def getByNum(self, id, num):
        vo_list = self.dao.selectByNum(id, num)
        if vo_list == None :
            return None
        else :
            return vo_list


    def getById(self, id, state = "대기", val = None):
        vo_list = self.dao.selectById(id, state, val)
        if vo_list == None :
            return None
        else :
            return vo_list


    def getByName(self, id, val):
        vo_list = self.dao.selectByName(id, val)
        if vo_list == None :
            return None
        else :
            return vo_list

    def editOrder(self, id, num, val):
        if self.dao.editOrder(id, num, val) :
            return True
        else :
            return False

    def editState(self, id, num, state) :
        if self.dao.editState(id, num, state) :
            return True
        else :
            return False

    def delOrder(self, id, num):
        if self.dao.delOrder(id, num) :
            return True
        else :
            return False
