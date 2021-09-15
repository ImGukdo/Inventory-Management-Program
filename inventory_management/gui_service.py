from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
import member as m
import board as b
from wcwidth import wcswidth
import tkinter.font
import product as p
import order as o


class cScreen:

    def __init__(self):
        self.__root = None
        self.__service = m.cMem_service()
        self.__vo = m.cMem_vo()
        self.__joininfo = [0] * 7
        self.__logininfo = [0, 0]
        self.__updateinfo = [0, 0]
        self.__writetext = [0, 0]
        self.__deltext = None
        self.__boardlst= None
        self.__boardsearch = [0, 0]
        self.__board_service = b.cBoardService()
        self.__prod_service = p.ProdService()
        self.__prodinput = [0, 0, 0]
        self.__prodsearchA = [0, 0]
        self.__prodsearchI = [0, 0]
        self.__product = None
        self.__prodlst = [0, 0]
        self.__prodvolst = None
        self.__order_service = o.OrderService()
        self.__inventorylst = None
        self.__inventory = None
        self.__ordersearch = [0, 0]
        self.__ordercount = None
        self.__order = None
        self.__orderlst = None
        self.__myorder = None
        self.__myorderlst = None


    def __Main(self):
        if self.__service.join(m.cMem_vo(self.__joininfo[0].get(), self.__joininfo[1].get(), self.__joininfo[2].get(),
                                         self.__joininfo[3].get(), self.__joininfo[4].get(),self.__joininfo[5].get(), self.__joininfo[6].get())) :
            msgbox.showinfo("알림", "회원가입완료")
            self.__joininfo = [0] * 7
        else :
            msgbox.showerror("에러", "입력사항을 확인해주세요.")
            return
        self.__root.destroy()
        self.Login_Output()
    def __Cancel(self) :
        self.__root.destroy()
        self.Login_Output()
    def __Check(self) :
        if self.__joininfo[0].get() == "" :
            msgbox.showerror("에러", "사용할 수 없는 아이디입니다.")
            return
        for i in self.__joininfo[0].get() :
            if i == " " :
                msgbox.showerror("에러", "사용할 수 없는 아이디입니다.")
                return

        if self.__service.Check_id(self.__joininfo[0].get()) :
            msgbox.showinfo("알림", "사용 가능한 아이디입니다.")
        else :
            msgbox.showerror("에러", "이미 사용중인 아이디입니다.")


    def __Login(self):
        if not self.__service.log_in(self.__logininfo[0].get(), self.__logininfo[1].get()) :
            msgbox.showerror("에러", "아이디 또는 비밀번호를 다시 확인하세요.")
            return
        self.__root.destroy()
        self.Inventory_Output(self.__prod_service.getAll())

    def __Join(self):
        self.__root.destroy()
        self.Join_Output()

    def __InventoryMode(self, lst = None):
        if lst == None :
            lst = self.__prod_service.getAll()
        self.__root.destroy()
        self.Inventory_Output(lst)

    def __OrderMode(self, lst = None) :
        if self.__service.print_id() == "admin" :
            if lst == None:
                lst = self.__order_service.getAll(state = "준비중")
        elif lst == None :
            lst = self.__order_service.getById(id = self.__service.print_id())
        self.__root.destroy()
        self.Order_Output(lst)

    def __BoardMode(self, vo_lst = None, mode = 0):
        if vo_lst == None :
            vo_lst = self.__board_service.GetAll()
        self.__root.destroy()
        self.Board_Output(vo_lst, mode)

    def __InfoMode(self):
        self.__root.destroy()
        self.Info_Output()

    def __AdminMode(self, lst = None):
        if lst == None :
            lst = self.__prod_service.getAll()

        if self.__service.print_id() == "admin" :
            self.__root.destroy()
            self.Admin_Output(lst)
        else :
            msgbox.showerror("에러", "관리자전용입니다.")

    def __Update(self):
        if self.__updateinfo[1].get() == "" :
            msgbox.showerror("에러", "정보변경실패")
            return
        if self.__service.edit_myinfo(self.__updateinfo[0].get(), self.__updateinfo[1].get()) :
            msgbox.showinfo("알림", "정보변경완료")
        else :
            msgbox.showerror("에러", "정보변경실패")
        self.__InfoMode()

    def __Uploadtext(self):
        if self.__writetext[0].get() == "제목" and self.__writetext[1].get("1.0", END) == "내용을 입력하세요\n" :
            return
        vo = b.cBoard_vo(id=self.__service.print_id(), title=self.__writetext[0].get(), content=self.__writetext[1].get("1.0", END))
        if self.__board_service.AddBoard(vo) :
            msgbox.showinfo("알림", "글게시완료")
            self.__writetext[0].delete(0, END)
            self.__writetext[1].delete("1.0", END)
            self.__writetext[0].insert(0, "제목")
            self.__writetext[1].insert(END, "내용을 입력하세요")
            self.__BoardMode(self.__board_service.GetAll())
        else :
            msgbox.showerror("에러", "글게시실패")

    def __Deletetext(self):
        if self.__deltext.curselection() == () :
            return
        if self.__deltext.curselection()[0] == 0 :
            return
        num = self.__boardlst[self.__deltext.curselection()[0] - 1].num
        id = self.__boardlst[self.__deltext.curselection()[0] - 1].id
        if self.__board_service.DelBoard(num, id, self.__service.print_id()) :
            msgbox.showinfo("알림", "글삭제완료")
            self.__BoardMode(self.__board_service.GetAll())
        else :
            msgbox.showerror("에러", "글삭제실패")

    def __Searchtext(self):
        option = self.__boardsearch[0].get()
        if option == "글번호" :
            vo = self.__board_service.GetByNum(self.__boardsearch[1].get())
            if vo == None :
                msgbox.showerror("알림", "해당글이 없습니다.")
            else :
                self.__deltext.delete(0, END)
                lst = [vo]
                self.__BoardMode(lst)
        elif option == "작성자" :
            vo = self.__board_service.GetByWriter(self.__boardsearch[1].get())
            if vo == None:
                msgbox.showerror("알림", "해당 사용자가 작성한 글이 없습니다.")
            else :
                self.__deltext.delete(0, END)
                self.__BoardMode(vo)
        elif option == "제목" :
            if self.__boardsearch[1].get() == "" :
                msgbox.showerror("알림", "해당 제목의 글이 없습니다.")
                return
            vo = self.__board_service.GetBytitle(self.__boardsearch[1].get())
            if vo == None:
                msgbox.showerror("알림", "해당 제목의 글이 없습니다.")
            else:
                self.__deltext.delete(0, END)
                self.__BoardMode(vo)

    def __Seetext(self):
        if self.__deltext.curselection() == () :
            return
        if self.__deltext.curselection()[0] == 0 :
            return
        num = self.__boardlst[self.__deltext.curselection()[0] - 1].num
        vo = self.__board_service.GetByNum(num)
        lst = [vo]
        self.__deltext.delete(0, END)
        self.__BoardMode(lst, 1)

    def String_format(self, str, width, fill=" "):
        s_width = wcswidth(str)
        f_width = width - s_width
        if f_width < 0 :
            f_width = 0
        fill = (fill * f_width)[:f_width]
        return str + fill

    def __Insertprod(self):
        if self.__prodinput[0].get() == "" or self.__prodinput[1].get() == "" or self.__prodinput[2].get() == "" :
            return
        if self.__prod_service.addProd(p.ProdVo(prodname=self.__prodinput[0].get(),
                                       count=self.__prodinput[1].get(), price=self.__prodinput[2].get())) :
            msgbox.showinfo("알림", "재고등록완료")
            self.__AdminMode()
        else :
            msgbox.showerror("알림", "재고등록에 실패했습니다.")

    def __SearchprodA(self) :
        option = self.__prodsearchA[0].get()
        val = self.__prodsearchA[1].get()
        if option == "" or val == "" :
            return
        if option == "제품번호" :
            vo = self.__prod_service.getByNum(val)
            if vo :
                lst = [vo]
                self.__AdminMode(lst)
            else :
                msgbox.showerror("알림", "해당 제품번호은 등록되어있지 않습니다.")

        elif option == "제품명" :
            lst = self.__prod_service.getByProdname(val)
            if lst != None :
                self.__AdminMode(lst)
            else :
                msgbox.showerror("알림", "해당 제품명은 등록되어있지 않습니다.")
    def __SearchprodI(self) :
        option = self.__prodsearchI[0].get()
        val = self.__prodsearchI[1].get()
        if option == "" or val == "" :
            return
        if option == "제품번호" :
            vo = self.__prod_service.getByNum(val)
            if vo :
                lst = [vo]
                self.__InventoryMode(lst)
            else :
                msgbox.showerror("에러", "해당 제품번호은 등록되어있지 않습니다.")

        elif option == "제품명" :
            lst = self.__prod_service.getByProdname(val)
            if lst != None :
                self.__InventoryMode(lst)
            else :
                msgbox.showerror("알림", "해당 제품명은 등록되어있지 않습니다.")

    def __Updateprod(self) :
        if self.__product.curselection() == () or self.__prodlst[1].get() == "" :
            return

        num = self.__prodvolst[self.__product.curselection()[0] - 1].num
        option = self.__prodlst[0].get()
        val = self.__prodlst[1].get()

        if option == "수량" :
            option = 'count'
        elif option == "가격" :
            option = 'price'
        elif option == "제품명" :
            option = 'prodname'

        if self.__prod_service.editProd(num, option, val) :
            msgbox.showinfo("알림", "재고가 수정되었습니다.")
            self.__AdminMode()
        else :
            msgbox.showerror("알림", "재고 수정에 실패했습니다..")

    def __Deleteprod(self) :
        if self.__product.curselection() == () :
            return

        num = self.__prodvolst[self.__product.curselection()[0] - 1].num
        if self.__prod_service.delProd(num) :
            msgbox.showinfo("알림", "재고가 삭제되었습니다.")
            self.__AdminMode()
        else :
            msgbox.showerror("알림", "재고 삭제에 실패했습니다..")

    def __Insertoder(self) :
        if self.__inventory.curselection() == () :
            return
        if self.__service.print_id() == "admin" :
            return

        id = self.__service.print_id()
        vo = self.__inventorylst[self.__inventory.curselection()[0] - 1]
        if self.__order_service.addOrder(id, vo.num, vo.prodname) :
            msgbox.showinfo("알림", "출고리스트에 추가되었습니다.")
        else :
            msgbox.showerror("알림", "출고리스트에 추가를 실패했습니다..")

    def __Searchorder(self) :
        if self.__ordersearch[1].get() == "" :
            return
        id = self.__service.print_id()
        option = self.__ordersearch[0].get()
        val = self.__ordersearch[1].get()

        if option == "제품명" :
            lst = self.__order_service.getByName(id, val)
            if lst == None :
                msgbox.showerror("알림", "해당 제품이 없습니다.")
            else :
                self.__OrderMode(lst)
        elif option == "제품번호" :
            lst = self.__order_service.getByNum(id, val)
            if lst == None :
                msgbox.showerror("알림", "해당 제품번호의 제품이 없습니다.")
            else:
                self.__OrderMode(lst)
        elif option == "아이디" :
            if id != "admin" :
                msgbox.showerror("에러", "관리자전용입니다.")
                return
            else :
                lst = self.__order_service.getById(id = id, state = "준비중", val = val)
                if lst == None :
                    msgbox.showerror("알림", "해당 아이디가 요청한 출고가 없습니다.")
                else:
                    self.__OrderMode(lst)

    def __Updateorder(self) :
        if self.__ordercount.get() == "" or self.__order.curselection() == () :
            return
        id = self.__orderlst[self.__order.curselection()[0] - 1].id
        num = self.__orderlst[self.__order.curselection()[0] - 1].ordernum
        val = self.__ordercount.get()
        if self.__order_service.editOrder(id, num, val) :
            msgbox.showinfo("알림", "수량이 변경되었습니다.")
            self.__OrderMode()
        else :
            msgbox.showerror("알림", "수량 변경을 실패했습니다.")

    def __Deleteorder(self) :
        if self.__order.curselection() == () :
            return
        id = self.__service.print_id()
        num = self.__orderlst[self.__order.curselection()[0] - 1].ordernum
        if self.__order_service.delOrder(id, num) :
            msgbox.showinfo("알림", "제품이 삭제되었습니다.")
            self.__OrderMode()
        else :
            msgbox.showerror("알림", "제품 삭제를 실패했습니다.")

    def __Outputorder(self) :
        if self.__order.curselection() == () :
            return
        id = self.__service.print_id()
        num = self.__orderlst[self.__order.curselection()[0] - 1].ordernum
        order = self.__orderlst[self.__order.curselection()[0] - 1].amount
        count = self.__prod_service.getByNum(num).count
        if order == 0 or order > count :
            msgbox.showerror("에러", "제품 출고 요청에 실패했습니다.")
            return

        if self.__order_service.editState(id, num, "준비중") :
            msgbox.showinfo("알림", "제품을 출고요청했습니다.")
            self.__OrderMode()

        else :
            msgbox.showerror("에러", "제품 출고 요청에 실패했습니다.")

    def __Adminoutput(self) :
        if self.__order.curselection() == () :
            return
        id = self.__orderlst[self.__order.curselection()[0] - 1].id
        num = self.__orderlst[self.__order.curselection()[0] - 1].prodnum
        ordernum = self.__orderlst[self.__order.curselection()[0] - 1].ordernum
        order = self.__orderlst[self.__order.curselection()[0] - 1].amount
        count = self.__prod_service.getByNum(num).count
        if order == 0 or order > count :
            msgbox.showerror("에러", "제품 출고 요청에 실패했습니다.")
            return

        if self.__order_service.editState(id, ordernum, "출고") :
            if self.__prod_service.editProd(num, "count", str(count - order)) :
                msgbox.showinfo("알림", "제품을 출고했습니다.")
                self.__OrderMode()
            else :
                msgbox.showerror("에러", "제품 출고에 실패했습니다.")
        else :
            msgbox.showerror("에러", "제품 출고에 실패했습니다.")


    def __Cancelorder(self) :
        if self.__myorder.curselection() == () or self.__myorder.curselection()[0] == 0 :
            return
        if self.__myorderlst[self.__myorder.curselection()[0] - 1].state == "출고" :
            return
        id = self.__service.print_id()
        num = self.__myorderlst[self.__myorder.curselection()[0] - 1].ordernum
        if self.__order_service.editState(id, num, "대기") :
            msgbox.showinfo("알림", "출고요청을 취소했습니다.")
            self.__InfoMode()
        else :
            msgbox.showerror("에러", "출고요청 취소를 실패했습니다.")

    def __Admincancel(self) :
        if self.__myorder.curselection() == () or self.__myorder.curselection()[0] == 0 :
            return
        id = self.__myorderlst[self.__myorder.curselection()[0] - 1].id
        num = self.__myorderlst[self.__myorder.curselection()[0] - 1].prodnum
        ordernum = self.__myorderlst[self.__myorder.curselection()[0] - 1].ordernum
        count = self.__prod_service.getByNum(num).count
        order = self.__myorderlst[self.__myorder.curselection()[0] - 1].amount
        if self.__order_service.editState(id, ordernum, "준비중") :
            msgbox.showinfo("알림", "출고를 취소했습니다.")
            self.__prod_service.editProd(num, "count", str(count + order))
            self.__InfoMode()
        else :
            msgbox.showerror("에러", "출고 취소를 실패했습니다.")

    def __Mode(self):
        self.__root = Tk()
        self.__root.title("Inventory")
        self.__root.geometry("640x480+400+150")
        self.__root.resizable(False, False)

        frame_menu = Frame(self.__root)
        frame_menu.pack(side="top", fill="x")

        lstbtn = Button(frame_menu, width=22, height=1, text="재고리스트", command=self.__InventoryMode)
        lstbtn.pack(side="left")

        orderbtn = Button(frame_menu, width=22, height=1, text="출고하기", command=self.__OrderMode)
        orderbtn.pack(side="left")

        infobtn = Button(frame_menu, width=22, height=1, text="게시판", command=self.__BoardMode)
        infobtn.pack(side="left")

        closebtn = Button(frame_menu, width=22, height=1, text="내정보", command=self.__InfoMode)
        closebtn.pack(side="left")

    def Login_Output(self):
        self.__root = Tk()
        self.__root.title("Inventory")
        self.__root.geometry("640x480+400+150")
        self.__root.resizable(False, False)

        main_photo = PhotoImage(file="./images/mainImage.png")
        label1 = Label(self.__root, image=main_photo)
        label1.pack(pady=5)

        main_logo = PhotoImage(file="./images/mainlogo.png")
        label2 = Label(self.__root, image=main_logo)
        label2.pack(pady=5)

        self.__logininfo[0] = Entry(self.__root, width=30)
        self.__logininfo[0].insert(0, "아이디")
        self.__logininfo[0].pack(pady=10)

        self.__logininfo[1] = Entry(self.__root, width=30)
        self.__logininfo[1].insert(0, "비밀번호")
        self.__logininfo[1].pack()

        loginbtn = Button(self.__root, width=30, height=2, text="로그인", command=self.__Login)
        loginbtn.pack(pady=5)
        joinbtn = Button(self.__root, text="회원가입", command=self.__Join)
        joinbtn.pack()

        self.__root.mainloop()

    def Join_Output(self):
        self.__root = Tk()
        self.__root.title("Inventory")
        self.__root.geometry("640x480+400+150")
        self.__root.resizable(False, False)

        join_photo = PhotoImage(file="./images/joinlogo.png")
        label = Label(self.__root, image=join_photo)
        label.pack(side="top")

        frame1 = Frame(self.__root)
        frame1.pack(side="top", pady=5)
        label1 = Label(frame1, text="                 * 아 이 디  ")
        label1.pack(side="left")
        self.__joininfo[0] = Entry(frame1, width=20)
        self.__joininfo[0].pack(side="left")

        checkbtn = Button(frame1, text = "중복확인", command = self.__Check)
        checkbtn.pack(side = "right", padx = 5)

        frame2 = Frame(self.__root)
        frame2.pack(side="top", pady=5)
        label2 = Label(frame2, text="* 비밀번호 ")
        label2.pack(side="left")
        self.__joininfo[1] = Entry(frame2, width=20)
        self.__joininfo[1].pack(side="left")

        frame3 = Frame(self.__root)
        frame3.pack(side="top", pady=5)
        label3 = Label(frame3, text="* 이     름  ")
        label3.pack(side="left")
        self.__joininfo[2] = Entry(frame3, width=20)
        self.__joininfo[2].pack(side="left")

        frame4 = Frame(self.__root)
        frame4.pack(side="top", pady=5)
        label4 = Label(frame4, text="* 회     사  ")
        label4.pack(side="left")
        self.__joininfo[3] = Entry(frame4, width=20)
        self.__joininfo[3].pack(side="left")

        frame5 = Frame(self.__root)
        frame5.pack(side="top", pady=5)
        label5 = Label(frame5, text="* 주     소  ")
        label5.pack(side="left")
        self.__joininfo[4] = Entry(frame5, width=20)
        self.__joininfo[4].pack(side="left")

        frame6 = Frame(self.__root)
        frame6.pack(side="top", pady=5)
        label6 = Label(frame6, text="* 핸 드 폰  ")
        label6.pack(side="left")
        self.__joininfo[5] = Entry(frame6, width=20)
        self.__joininfo[5].pack(side="left")

        frame7 = Frame(self.__root)
        frame7.pack(side="top", pady=5)
        label7 = Label(frame7, text="  이 메 일  ")
        label7.pack(side="left")
        self.__joininfo[6] = Entry(frame7, width=20)
        self.__joininfo[6].pack(side="left")

        joinbtn = Button(self.__root, text="가입완료", width=15, height=2, command=self.__Main)
        joinbtn.pack(pady=20)

        cancelbtn = Button(self.__root, text = "취소", command = self.__Cancel)
        cancelbtn.pack()

        self.__root.mainloop()

    def Inventory_Output(self, lst):
        self.__Mode()
        font = tkinter.font.Font(family="D2Coding", size=10)
        frame_lst = Frame(self.__root)
        frame_lst.pack(side="top", fill="x", pady=10, padx=5)

        scrollbar = Scrollbar(frame_lst)
        scrollbar.pack(side="right", fill="y")

        self.__inventory = Listbox(frame_lst, selectmode="extended", height=18, yscrollcommand=scrollbar.set, font = font)
        self.__inventory.insert(END, self.String_format("  제품번호", 8) + " " * 20 + self.String_format("제품명", 6) +
                       " " * 24 + self.String_format("재고", 6) + " " * 11 + self.String_format("가격", 6))
        self.__inventorylst = lst
        for vo in lst:
            self.__inventory.insert(END, " " * 5 + self.String_format(str(vo.num), 10) + " " * 14 + self.String_format(vo.prodname, 31) +
                                 self.String_format(str(vo.count), 16) + self.String_format(str(vo.price), 20))

        self.__inventory.pack(side="left", fill="x", expand=True)
        scrollbar.config(command=self.__inventory.yview)

        frame_search = LabelFrame(self.__root, text="검색")
        frame_search.pack(side="top", fill="x", pady=10, padx=5)
        label1 = Label(frame_search, text="검색옵션")
        label1.pack(side="left", padx=10, pady=10)

        values = ["제품번호", "제품명"]
        self.__prodsearchI[0] = ttk.Combobox(frame_search, width=15, height=10, values=values, state="readonly")
        self.__prodsearchI[0].pack(side="left", padx=10)
        self.__prodsearchI[0].current(0)
        label2 = Label(frame_search, text="검색")
        label2.pack(side="left", padx=10, pady=10)
        self.__prodsearchI[1] = Entry(frame_search, width=20)
        self.__prodsearchI[1].pack(side="left", padx=10)

        searchbtn = Button(frame_search, text="검색하기", width=20, command = self.__SearchprodI)
        searchbtn.pack(side="left", padx=20)

        putbtn = Button(self.__root, width=22, height=2, text="출고리스트에 담기", command = self.__Insertoder)
        putbtn.pack(side="right", padx=10, pady=10)

        adminbtn = Button(self.__root, width=22, height=2, text="재고관리", command=self.__AdminMode)
        adminbtn.pack(side="right", padx=10, pady=10)

        self.__root.mainloop()

    def Admin_Output(self, lst):
        self.__Mode()
        font = tkinter.font.Font(family="D2Coding", size=10)
        frame_lst = Frame(self.__root)
        frame_lst.pack(side="top", fill="x", pady=10, padx=5)

        scrollbar = Scrollbar(frame_lst)
        scrollbar.pack(side="right", fill="y")

        self.__product = Listbox(frame_lst, selectmode="single", height=10, yscrollcommand=scrollbar.set, font = font)
        self.__product.insert(END, self.String_format("  제품번호", 8) + " " * 20 + self.String_format("제품명", 6) +
                       " " * 24 + self.String_format("수량", 6) + " " * 11 + self.String_format("가격", 6))
        self.__prodvolst = lst
        for vo in lst :
            self.__product.insert(END, " " * 5 + self.String_format(str(vo.num), 10) + " " * 14 + self.String_format(vo.prodname, 31) +
                                 self.String_format(str(vo.count), 16) + self.String_format(str(vo.price), 20))

        self.__product.pack(side="left", fill="x", expand=True)
        scrollbar.config(command=self.__product.yview)

        frame_search = LabelFrame(self.__root, text="검색")
        frame_search.pack(side="top", fill="x", pady=10, padx=5)
        label1 = Label(frame_search, text="검색옵션")
        label1.pack(side="left", padx=10, pady=10)

        values = ["제품번호", "제품명"]
        self.__prodsearchA[0] = ttk.Combobox(frame_search, width=15, height=10, values=values, state="readonly")
        self.__prodsearchA[0].pack(side="left", padx=10)
        self.__prodsearchA[0].current(0)
        label2 = Label(frame_search, text="검색")
        label2.pack(side="left", padx=10, pady=10)
        self.__prodsearchA[1] = Entry(frame_search, width=20)
        self.__prodsearchA[1].pack(side="left", padx=10)

        searchbtn = Button(frame_search, text="검색하기", width=20, command = self.__SearchprodA)
        searchbtn.pack(side="left", padx=20)

        frame_update = LabelFrame(self.__root, text="재고수정")
        frame_update.pack(side="top", fill="x", pady=5, padx=5)
        label1 = Label(frame_update, text="수정항목")
        label1.pack(side="left", padx=10, pady=10)

        values = ["수량", "가격", "제품명"]
        self.__prodlst[0] = ttk.Combobox(frame_update, width=20, height=10, values=values, state="readonly")
        self.__prodlst[0].pack(side="left", padx=10)
        self.__prodlst[0].current(0)
        self.__prodlst[1] = Entry(frame_update, width=25)
        self.__prodlst[1].pack(side="left", padx=10)
        updatebtn = Button(frame_update, text="변경하기", width=25, command = self.__Updateprod)
        updatebtn.pack(side="left", padx=20)

        frame_input = LabelFrame(self.__root, text="재고등록")
        frame_input.pack(side="top", fill="x", pady=5, padx=5)

        frame_insert = Frame(frame_input)
        frame_insert.pack(side="top", fill="x")

        label1 = Label(frame_insert, text="제품명")
        label1.pack(side="left", padx=10, pady=10)

        self.__prodinput[0] = Entry(frame_insert, width=18)
        self.__prodinput[0].pack(side="left", padx=10, pady=10)

        label2 = Label(frame_insert, text="수량")
        label2.pack(side="left", padx=10, pady=10)

        self.__prodinput[1] = Entry(frame_insert, width=18)
        self.__prodinput[1].pack(side="left", padx=10, pady=10)

        label3 = Label(frame_insert, text="가격")
        label3.pack(side="left", padx=10, pady=10)

        self.__prodinput[2] = Entry(frame_insert, width=18)
        self.__prodinput[2].pack(side="left", padx=10, pady=10)

        frame_btn = Frame(self.__root)
        frame_btn.pack(side="top", fill="x")
        inputbtn = Button(frame_btn, width=22, height=2, text="등록하기", command = self.__Insertprod)
        inputbtn.pack(side="right", padx=10, pady=10)

        deletebtn = Button(frame_btn, width=22, height=2, text="삭제하기", command = self.__Deleteprod)
        deletebtn.pack(side="right", padx=10, pady=10)

        self.__root.mainloop()

    def Order_Output(self, lst):
        self.__Mode()
        font = tkinter.font.Font(family="D2Coding", size=10)
        frame_lst = Frame(self.__root)
        frame_lst.pack(side="top", fill="x", pady=10, padx=5)

        scrollbar = Scrollbar(frame_lst)
        scrollbar.pack(side="right", fill="y")

        self.__order = Listbox(frame_lst, selectmode="single", height=13, yscrollcommand=scrollbar.set, font = font)
        self.__order.insert(END, self.String_format("  제품번호", 8) + " " * 20 + self.String_format("제품명", 6) +
        " " * 18 + self.String_format("재고", 6) + "      " + self.String_format("수량", 6) + " " * 5 + self.String_format("아이디", 6))
        self.__orderlst = lst

        for vo in lst :
            self.__order.insert(END, " " * 5 + self.String_format(str(vo.prodnum), 10) + " " * 14 + self.String_format(vo.prodname, 25) +
            self.String_format(str(self.__prod_service.getByNum(vo.prodnum).count), 13) + self.String_format(str(vo.amount), 10) + " " + self.String_format(str(vo.id), 20))

        self.__order.pack(side="left", fill="x", expand=True)
        scrollbar.config(command=self.__order.yview)

        frame_search = LabelFrame(self.__root, text="조회")
        frame_search.pack(side="top", fill="x", pady=10, padx=10)
        label3 = Label(frame_search, text="조회옵션")
        label3.pack(side="left", padx=10, pady=10)

        values = ["제품명", "제품번호", "아이디"]
        self.__ordersearch[0] = ttk.Combobox(frame_search, width=15, height=10, values=values, state="readonly")
        self.__ordersearch[0].pack(side="left", padx=10)
        self.__ordersearch[0].current(0)

        label4 = Label(frame_search, text="조회")
        label4.pack(side="left", padx=10, pady=10)
        self.__ordersearch[1] = Entry(frame_search, width=20)
        self.__ordersearch[1].pack(side="left", padx=10)
        searchbtn = Button(frame_search, text="조회하기", width=20, command = self.__Searchorder)
        searchbtn.pack(side="left", padx=20)

        frame_middle = Frame(self.__root)
        frame_middle.pack(side = "top", fill = "x", pady=10, padx=10)
        frame_order = LabelFrame(frame_middle, text="출고옵션")
        frame_order.pack(side="right")

        applybtn = Button(frame_order, text="적용하기", width=19, command = self.__Updateorder)
        applybtn.pack(side="right", padx=20)
        self.__ordercount = Entry(frame_order, width=20)
        self.__ordercount.pack(side="right", padx=10)
        label2 = Label(frame_order, text="수량")
        label2.pack(side="right", padx=10, pady=10)

        if self.__service.print_id() == "admin" :
            putbtn = Button(self.__root, width=22, height=2, text="출고하기", command=self.__Adminoutput)
            putbtn.pack(side="right", padx=10, pady=10)
        else :
            putbtn = Button(self.__root, width=22, height=2, text="출고하기", command = self.__Outputorder)
            putbtn.pack(side="right", padx=10, pady=10)
        deletebtn = Button(self.__root, width=22, height=2, text="삭제하기", command = self.__Deleteorder)
        deletebtn.pack(side="right", padx=10, pady=10)

        self.__root.mainloop()

    def Board_Output(self, vo_lst, mode = 0):
        self.__Mode()
        font = tkinter.font.Font(family="D2Coding", size=10)
        frame_lst = Frame(self.__root)
        frame_lst.pack(side="top", fill="x", pady=10, padx=5)

        scrollbar = Scrollbar(frame_lst)
        scrollbar.pack(side="right", fill="y")

        self.__deltext = Listbox(frame_lst, selectmode="single", height=10, yscrollcommand=scrollbar.set, font = font)
        if mode == 0 :
            self.__deltext.insert(END, self.String_format("  번호", 5) + " " * 25 + self.String_format("제목", 5) +
                       " " * 24 + self.String_format("작성자", 6) + " " * 11 + self.String_format("작성일", 6))

            self.__boardlst = vo_lst
            for vo in self.__boardlst :
                self.__deltext.insert(END, "   " + self.String_format(str(vo.num), 10) + " " * 10 + self.String_format(vo.title, 36) +
                "  " + self.String_format(vo.id, 14) + self.String_format(str(vo.w_date), 20))

        elif mode == 1 :
            lst = []
            index = 0
            for idx, i in enumerate(vo_lst[0].content) :
                if i == "\n" :
                    lst.append(vo_lst[0].content[index:idx])
                    index = idx + 1
            for i in lst :
                self.__deltext.insert(END, i)

        self.__deltext.pack(side="left", fill="x", expand=True)
        scrollbar.config(command=self.__deltext.yview)

        frame_search = LabelFrame(self.__root, text="검색")
        frame_search.pack(side="top", fill="x", pady=10, padx=5)
        label1 = Label(frame_search, text="검색옵션")
        label1.pack(side="left", padx=10, pady=10)

        values = ["글번호", "작성자", "제목"]
        self.__boardsearch[0] = ttk.Combobox(frame_search, width=15, height=10, values=values, state="readonly")
        self.__boardsearch[0].pack(side="left", padx=10)
        self.__boardsearch[0].current(0)
        label2 = Label(frame_search, text="검색")
        label2.pack(side="left", padx=10, pady=10)
        self.__boardsearch[1] = Entry(frame_search, width=20)
        self.__boardsearch[1].pack(side="left", padx=10)

        searchbtn = Button(frame_search, text="검색하기", width=20, command=self.__Searchtext)
        searchbtn.pack(side="left", padx=20)

        frame_board = LabelFrame(self.__root, text="글쓰기")
        frame_board.pack(side="left", padx=5, pady=10)

        self.__writetext[0] = Entry(frame_board, width=60)
        self.__writetext[0].pack(side="top", padx=10, pady=5)
        self.__writetext[0].insert(0, "제목")

        self.__writetext[1] = Text(frame_board, width=60, height=10)
        self.__writetext[1].pack(side="top", padx=10, pady=5)
        self.__writetext[1].insert(END, "내용을 입력하세요")

        frame_btn = Frame(self.__root)
        frame_btn.pack(side="right")

        if mode == 0 :
            deletebtn = Button(frame_btn, width=22, height=2, text="게시글 삭제", command=self.__Deletetext)
            seebtn = Button(frame_btn, width=22, height=2, text="게시글 보기", command=self.__Seetext)
        elif mode == 1 :
            deletebtn = Button(frame_btn, width=22, height=2, text="게시글 삭제")
            seebtn = Button(frame_btn, width=22, height=2, text="게시글 보기")

        seebtn.pack(side="top", padx=10, pady=10)
        deletebtn.pack(side="top", padx=10, pady=10)

        putbtn = Button(frame_btn, width=22, height=2, text="글올리기", command=self.__Uploadtext)
        putbtn.pack(side="top", padx=10, pady=10)

        self.__root.mainloop()

    def Info_Output(self):
        self.__Mode()
        font = tkinter.font.Font(family="D2Coding", size=10)
        frame_info = LabelFrame(self.__root, text="내정보")
        frame_info.pack(side="top", fill="x", padx=10, pady=10)

        info = self.__service.output_myinfo()
        frame_id = Frame(frame_info)
        frame_id.pack(side="top", fill="x", padx=10, pady=5)
        id = Label(frame_id, text="아   이   디   :    " + info.id)
        id.pack(side="left", padx=30)

        frame_name = Frame(frame_info)
        frame_name.pack(side="top", fill="x", padx=10, pady=5)
        name = Label(frame_name, text="이         름   :    " + info.name)
        name.pack(side="left", padx=30)

        frame_company = Frame(frame_info)
        frame_company.pack(side="top", fill="x", padx=10, pady=5)
        company = Label(frame_company, text="회         사   :    " + info.company)
        company.pack(side="left", padx=30)

        frame_address = Frame(frame_info)
        frame_address.pack(side="top", fill="x", padx=10, pady=5)
        address = Label(frame_address, text="주         소   :    " + info.addr)
        address.pack(side="left", padx=30)

        frame_phone = Frame(frame_info)
        frame_phone.pack(side="top", fill="x", padx=10, pady=5)
        phone = Label(frame_phone, text="핸드폰번호   :    " + info.mobile)
        phone.pack(side="left", padx=30)

        frame_email = Frame(frame_info)
        frame_email.pack(side="top", fill="x", padx=10, pady=5)
        if str(info.email) == 'None' :
            info.email = ""
        email = Label(frame_email, text="이   메   일   :    " + str(info.email))
        email.pack(side="left", padx=30)

        frame_update = LabelFrame(self.__root, text="정보수정")
        frame_update.pack(side="top", fill="x", pady=10, padx=10)
        label1 = Label(frame_update, text="수정항목")
        label1.pack(side="left", padx=10, pady=10)

        values = ["이름", "회사", "주소", "핸드폰번호", "이메일", "비밀번호"]
        self.__updateinfo[0] = ttk.Combobox(frame_update, width=15, height=10, values=values, state="readonly")
        self.__updateinfo[0].pack(side="left", padx=10)
        self.__updateinfo[0].current(0)
        self.__updateinfo[1] = Entry(frame_update, width=35)
        self.__updateinfo[1].pack(side="left", padx=10)
        applybtn = Button(frame_update, text="변경하기", width=30, command=self.__Update)
        applybtn.pack(side="left", padx=10)
        if self.__service.print_id() == "admin" :
            frame_output = LabelFrame(self.__root, text="출고목록")
            frame_output.pack(side="left", fill="both", expand=True, pady=10, padx=10)
        else :
            frame_output = LabelFrame(self.__root, text="출고신청목록")
            frame_output.pack(side="left", fill="both", expand=True, pady=10, padx=10)

        frame_lst = Frame(frame_output)
        frame_lst.pack(side="top", fill="x", expand=True, pady=10, padx=5)

        scrollbar = Scrollbar(frame_lst)
        scrollbar.pack(side="right", fill="y")

        if self.__service.print_id() == "admin" :
            self.__myorderlst = self.__order_service.getAll("출고")
            self.__myorder = Listbox(frame_lst, selectmode="extended", height=10, yscrollcommand=scrollbar.set,
                                     font=font)

            self.__myorder.insert(END, self.String_format("  아이디", 8) + "   " + self.String_format("제품번호", 8) + " " * 10 + self.String_format("제품명", 6) +
                                  " " * 10 + self.String_format("수량", 6) + " " * 6 + self.String_format("상태", 10))

            for vo in self.__myorderlst:
                self.__myorder.insert(END, " " * 3 + self.String_format(str(vo.id), 10) + " " +self.String_format(str(vo.prodnum), 10) + " " * 4 +
                self.String_format(vo.prodname, 15) + "   " + self.String_format(str(vo.amount), 10) + self.String_format(vo.state, 10))

            self.__myorder.pack(side="left", fill="x", expand=True)
            scrollbar.config(command=self.__myorder.yview)
        else :
            self.__myorderlst = self.__order_service.getById(id = self.__service.print_id(), state = "준비중")
            self.__myorder = Listbox(frame_lst, selectmode="extended", height=10, yscrollcommand=scrollbar.set, font = font)
            self.__myorder.insert(END, self.String_format("  제품번호", 8) + " " * 14 + self.String_format("제품명", 6) +
                               " " * 15 + self.String_format("수량", 6) + " " * 6 + self.String_format("상태", 10))

            for vo in self.__myorderlst:
                self.__myorder.insert(END, " " * 5 + self.String_format(str(vo.prodnum), 10) + " " * 8 + self.String_format(vo.prodname,20)
                + "   " + self.String_format(str(vo.amount), 10) + self.String_format(vo.state, 10))

            self.__myorder.pack(side="left", fill="x", expand=True)
            scrollbar.config(command=self.__myorder.yview)

        if self.__service.print_id() == "admin" :
            cancelbtn = Button(self.__root, width=15, height=2, text="출고취소", command=self.__Admincancel)
            cancelbtn.pack(side="bottom", padx=10, pady=10)
        else :
            cancelbtn = Button(self.__root, width=15, height=2, text="출고취소", command = self.__Cancelorder)
            cancelbtn.pack(side="bottom", padx=10, pady=10)

        self.__root.mainloop()


