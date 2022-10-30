import pymysql
from PyQt5.QtWidgets import *
import sys

class DB_Utils:

    def queryExecutor(self, db, sql, params):
        conn = pymysql.connect(host='localhost', user='guest', password='bemyguest', db='classicmodels', charset='utf8')

        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:     # dictionary based cursor
                cursor.execute(sql, params)
                rows = cursor.fetchall()
                return rows
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            conn.close()

class DB_Queries:
    # 모든 검색문은 여기에 각각 하나의 메소드로 정의

    def initTable(self):  # 초기에는 고객의 “ALL”이 선택된 것으로 가정하고, 검색 결과를 출력
        # sql = "SELECT * FROM customers ORDER BY name ASC "
        sql = "SELECT orders.orderNo, orders.orderDate, orders.requiredDate, orders.shippedDate, orders.status , customers.name, orders.comments " \
              "FROM customers " \
              "JOIN orders " \
              "ON customers.customerId = orders.customerId "

        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def selectCustomers(self):
        sql = "SELECT DISTINCT name FROM customers ORDER BY name ASC "
        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def searchSelectCustomers(self, value):
        if value == 'ALL':
            sql = "SELECT * FROM customers WHERE name"
            params = ()
        else:
            sql = "SELECT * FROM customers WHERE name = %s"
            params = (value)         # SQL문의 실제 파라미터 값의 튜플

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def selectCountry(self):
        sql = "SELECT DISTINCT country FROM customers ORDER BY country ASC"
        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def selectCity(self):
        sql = "SELECT DISTINCT city FROM customers ORDER BY city ASC"
        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows


class SubWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):

        self.setWindowTitle("서브 페이지")
        self.setGeometry(100, 100, 800, 600)


        # 타이틀 설정
        self.title = QGroupBox('주문 상세 내역', self)
        self.topSubLayout = QVBoxLayout()
        self.topSubLayout.addWidget(self.title)

        # 주문번호
        self.orderNumBox = QHBoxLayout()
        self.orderNum = QLabel("주문번호: ", self)
        self.orderNumT = QLabel(str(0), self)
        self.orderNumBox.addWidget(self.orderNum)
        self.orderNumBox.addWidget(self.orderNumT)

        # 상품개수
        self.orderCntBox = QHBoxLayout()
        self.orderCnt = QLabel("상품개수: ", self)
        self.orderCntT = QLabel(str(0), self)
        self.orderCntBox.addWidget(self.orderCnt)
        self.orderCntBox.addWidget(self.orderCntT)
        # 주문금액
        self.orderAmountBox = QHBoxLayout()
        self.orderAmount = QLabel("주문금액: ", self)
        self.orderAmountT = QLabel(str(0), self)
        self.orderAmountBox.addWidget(self.orderAmount)
        self.orderAmountBox.addWidget(self.orderAmountT)

        self.infoLayout = QHBoxLayout()
        self.infoLayout.addLayout(self.orderNumBox)
        self.infoLayout.addLayout(self.orderCntBox)
        self.infoLayout.addLayout(self.orderAmountBox)

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(20)
        self.tableLayout = QVBoxLayout()
        self.tableLayout.addWidget(self.tableWidget)


        # 파일 다운로드
        self.fileTypeBox = {
            'csv': QRadioButton('CSV'),
            'json': QRadioButton('JSON'),
            'xml': QRadioButton('XML'),
        }
        self.fileTypeBox['csv'].setChecked(True)

        self.saveAsGroup = QGroupBox('파일 출력')
        self.saveBtn = QPushButton('저장')
        self.saveBtn.setMaximumWidth(200)

        self.saveAsLayout = QHBoxLayout()
        self.saveAsLayout.addWidget(self.fileTypeBox['csv'])
        self.saveAsLayout.addWidget(self.fileTypeBox['json'])
        self.saveAsLayout.addWidget(self.fileTypeBox['xml'])
        self.saveAsLayout.addWidget(self.saveBtn)
        self.saveAsGroup.setLayout(self.saveAsLayout)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.topSubLayout)
        self.layout.addLayout(self.infoLayout)
        self.layout.addLayout(self.tableLayout)
        self.layout.addWidget(self.saveAsGroup)
        self.setLayout(self.layout)



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        query = DB_Queries()

        init = query.initTable()  # 초기에는 고객의 “ALL”이 선택된 것으로 가정하고, 검색 결과를 출력
        customers = query.selectCustomers()  # 고객
        country = query.selectCountry()  # 국가
        city = query.selectCity()  # 도시


        self.setWindowTitle("주문 검색 페이지")
        self.setGeometry(0, 0, 800, 600)

        # 타이틀 설정
        self.title = QGroupBox('주문검색', self)
        self.topSubLayout = QVBoxLayout()
        self.topSubLayout.addWidget(self.title)

        # 고객 부분 셀렉트 박스
        self.customer = QLabel("고객: ", self)
        self.customerCombo = QComboBox(self)
        columnName = list(customers[0].keys())[0]
        items = ['없음' if row[columnName] == None else row[columnName] for row in customers]
        self.customerCombo.addItems(['ALL'])
        self.customerCombo.addItems(items)

        # 국가 부분 셀렉트 박스
        self.country = QLabel("국가: ", self)
        self.countryCombo = QComboBox(self)
        columnName2 = list(country[0].keys())[0]
        items2 = ['없음' if row[columnName2] == None else row[columnName2] for row in country]
        self.countryCombo.addItems(['ALL'])
        self.countryCombo.addItems(items2)


        # 도시 부분 셀렉트 박스
        self.city = QLabel("도시: ", self)
        self.cityCombo = QComboBox(self)
        columnName3 = list(city[0].keys())[0]
        items3 = ['없음' if row[columnName3] == None else row[columnName3] for row in city]
        self.cityCombo.addItems(['ALL'])
        self.cityCombo.addItems(items3)

        # 검색 버튼
        self.searchBtn = QPushButton('검색', self)
        self.searchBtn.setMaximumWidth(200)
        self.searchBtn.clicked.connect(self.searchButtonClicked)

        # 초기화 버튼
        self.initBtn = QPushButton('초기화', self)
        self.initBtn.setMaximumWidth(200)
        self.initBtn.clicked.connect(self.initButtonClicked)

        self.buttonLayout = QVBoxLayout()
        self.buttonLayout.addWidget(self.searchBtn)
        self.buttonLayout.addWidget(self.initBtn)

        self.Top = QHBoxLayout()
        self.Top.addLayout(self.topSubLayout)
        self.Top.addLayout(self.buttonLayout)

        self.searchLayout = QHBoxLayout()
        self.searchLayout.addWidget(self.customer)
        self.searchLayout.addWidget(self.customerCombo)
        self.searchLayout.addWidget(self.country)
        self.searchLayout.addWidget(self.countryCombo)
        self.searchLayout.addWidget(self.city)
        self.searchLayout.addWidget(self.cityCombo)
        self.searchLayout.addWidget(self.searchBtn)
        self.searchLayout.addWidget(self.initBtn)
        self.title.setLayout(self.searchLayout)


        # 검색 주문 수
        self.cntResult = QGroupBox('검색된 주문의 개수: ', self)
        self.countResult = QVBoxLayout()
        self.countResult.addWidget(self.cntResult)
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(init))
        self.tableWidget.setColumnCount(len(init[0]))
        self.tableLayout = QVBoxLayout()
        self.tableLayout.addWidget(self.tableWidget)
        self.tableWidget.cellClicked.connect(self.secondWindow)
        columnNames = list(init[0].keys())
        self.tableWidget.setHorizontalHeaderLabels(columnNames)

        for rowIDX, customer in enumerate(init):  # customer는 딕셔너리
            for columnIDX, (k, v) in enumerate(customer.items()):
                if v == None:  # 파이썬이 DB의 널값을 None으로 변환함.
                    continue  # QTableWidgetItem 객체를 생성하지 않음
                else:
                    item = QTableWidgetItem(str(v))

                self.tableWidget.setItem(rowIDX, columnIDX, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()


        self.layout = QVBoxLayout()
        self.layout.addLayout(self.Top)
        self.layout.addLayout(self.countResult)
        self.layout.addLayout(self.tableLayout)
        self.setLayout(self.layout)

    # 검색 버튼 클릭
    def searchButtonClicked(self):
        print('search button clicked')

    # 초기화 버튼 클릭
    def initButtonClicked(self):
        # 초기에는 고객의 “ALL”이 선택된 것으로 가정하고, 검색 결과를 출력
        query = DB_Queries()
        init = query.initTable()

        columnNames = list(init[0].keys())
        self.tableWidget.setHorizontalHeaderLabels(columnNames)

        for rowIDX, customer in enumerate(init):  # customer는 딕셔너리
            for columnIDX, (k, v) in enumerate(customer.items()):
                if v == None:  # 파이썬이 DB의 널값을 None으로 변환함.
                    continue  # QTableWidgetItem 객체를 생성하지 않음
                else:
                    item = QTableWidgetItem(str(v))

                self.tableWidget.setItem(rowIDX, columnIDX, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()


    # 주문 상세 내역 윈도우 띄우기
    def secondWindow(self):
        self.subLayout = SubWindow()
        self.subLayout.show()



def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

main()
