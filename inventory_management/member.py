import pymysql

class cMem_vo :
    def __init__(self, id = None, pwd = None, name = None, company = None, addr = None, mobile = None, email = None) :
        self.id = id
        self.pwd = pwd
        self.name = name
        self.company = company
        self.addr = addr
        self.mobile = mobile
        self.email = email

class cMem_dao :
    def __init__(self) :
        self.__conn = None
        self.__cur = None

    def __connect(self) :
        self.__conn = pymysql.connect(host = '127.0.0.1', user = 'root', password = '1234',
                                      db = 'projectdb', charset = 'utf8')
        self.__cur = self.__conn.cursor()

    def __disconnect(self) :
        self.__cur = None
        self.__conn.close()

    def insert(self, vo) :
        self.__connect()
        sql = 'insert into membertbl values(%s, %s, %s, %s, %s, %s, %s)'
        val = (vo.id, vo.pwd, vo.name, vo.company, vo.addr, vo.mobile, vo.email)
        self.__cur.execute(sql, val)
        self.__conn.commit()
        self.__disconnect()

    def select(self, id) :
        self.__connect()
        sql = 'select * from membertbl where id = %s'
        val = (id, )
        self.__cur.execute(sql, val)
        row = self.__cur.fetchone()
        self.__disconnect()
        if row != None :
            vo = cMem_vo(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            return vo


    def update(self, id, option, new_info):
        self.__connect()
        if option == "이름" :
            option = "name"
        elif option == "회사" :
            option = "company"
        elif option == "주소" :
            option = "address"
        elif option == "핸드폰번호" :
            option = "mobile"
        elif option == "이메일" :
            option = "email"
        elif option == "비밀번호" :
            option = "password"

        sql = 'update membertbl set ' + option + ' = %s where id = %s'
        val = (new_info, id)
        self.__cur.execute(sql, val)
        self.__conn.commit()
        self.__disconnect()


class cMem_service :
    __login_state = None
    def __init__(self) :
        self.dao = cMem_dao()

    def print_id(self) :
        return cMem_service.__login_state

    def join(self, vo) :
        try :
            if vo.id == "" or vo.pwd == "" or vo.name == "" or \
                vo.company == "" or vo.addr == "" or vo.mobile == "" :
                return False
            self.dao.insert(vo)
        except :
            return False
        else :
            return True

    def log_in(self, id, pwd) :
        vo = self.dao.select(id)
        if vo == None :
            return False
        else :
            if vo.pwd == pwd :
                cMem_service.__login_state = vo.id
                return True
            else :
                return False

    def output_myinfo(self):
        vo = self.dao.select(cMem_service.__login_state)
        return vo

    def edit_myinfo(self, option, newinfo) :
        try :
            self.dao.update(cMem_service.__login_state, option, newinfo)
        except :
            return False
        else :
            return True

    def Check_id(self, id) :
        if self.dao.select(id) == None :
            return True
        else :
            return False
