import pymysql, sys, json, csv
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import *
import sys, datetime

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
        sql = "SELECT orders.orderNo, orders.orderDate, orders.requiredDate, orders.shippedDate, orders.status , customers.name as customer, orders.comments " \
              "FROM customers " \
              "JOIN orders " \
              "ON customers.customerId = orders.customerId " \
              "ORDER BY orders.orderNo"

        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def selectCustomers(self):
        sql = "SELECT DISTINCT name as customer FROM customers ORDER BY name ASC "
        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def searchSelectCustomers(self, value):

        if value == 'ALL':
            sql = "SELECT orders.orderNo, orders.orderDate, orders.requiredDate, orders.shippedDate, orders.status , customers.name as customer, orders.comments " \
                  "FROM customers " \
                  "JOIN orders " \
                  "ON customers.customerId = orders.customerId " \
                  "ORDER BY orders.orderNo"
            params = ()
        else:
            sql = "SELECT orders.orderNo, orders.orderDate, orders.requiredDate, orders.shippedDate, orders.status , customers.name as customer, orders.comments " \
                  "FROM customers " \
                  "JOIN orders " \
                  "ON customers.customerId = orders.customerId " \
                  "WHERE name = %s" \
                  "ORDER BY orders.orderNo"
            params = (value)  # SQL문의 실제 파라미터 값의 튜플

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows


    def selectCountry(self):
        sql = "SELECT DISTINCT country FROM customers ORDER BY country ASC"
        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def searchSelectCountry(self, value):

        if value == 'ALL':
            sql = "SELECT orders.orderNo, orders.orderDate, orders.requiredDate, orders.shippedDate, orders.status , customers.name as customer, orders.comments " \
                  "FROM customers " \
                  "JOIN orders " \
                  "ON customers.customerId = orders.customerId " \
                  "ORDER BY orders.orderNo"
            params = ()
        else:
            sql = "SELECT orders.orderNo, orders.orderDate, orders.requiredDate, orders.shippedDate, orders.status , customers.name as customer, orders.comments " \
                  "FROM customers " \
                  "JOIN orders " \
                  "ON customers.customerId = orders.customerId " \
                  "WHERE country = %s" \
                  "ORDER BY orders.orderNo"
            params = (value)  # SQL문의 실제 파라미터 값의 튜플

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def selectCity(self):
        sql = "SELECT DISTINCT city FROM customers ORDER BY city ASC"
        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    # 국가 기준의 도시만 콤보박스 만들기
    def selectCityFromCountry(self, country):
        self.country = country
        if self.country == "ALL" :
            sql = "SELECT DISTINCT city FROM customers ORDER BY city ASC"
        else:
            sql = "SELECT DISTINCT city FROM customers WHERE country = '" + self.country+"' ORDER BY city ASC"
        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def searchSelectCity(self, value):

        if value == 'ALL':
            sql = "SELECT orders.orderNo, orders.orderDate, orders.requiredDate, orders.shippedDate, orders.status , customers.name as customer, orders.comments " \
                  "FROM customers " \
                  "JOIN orders " \
                  "ON customers.customerId = orders.customerId " \
                  "ORDER BY orders.orderNo"
            params = ()
        else:
            sql = "SELECT orders.orderNo, orders.orderDate, orders.requiredDate, orders.shippedDate, orders.status , customers.name as customer, orders.comments " \
                  "FROM customers " \
                  "JOIN orders " \
                  "ON customers.customerId = orders.customerId " \
                  "WHERE city = %s" \
                  "ORDER BY orders.orderNo"
            params = (value)  # SQL문의 실제 파라미터 값의 튜플

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows

    def orderDetail(self, value):
        sql = "SELECT od.orderLineNo, od.productCode, p.name as productName , od.quantity, od.priceEach, od.quantity * od.priceEach as 상품주문액 " \
              "FROM orderDetails od INNER JOIN orders o USING(orderNo) " \
              "INNER JOIN products p " \
              "USING (productCode) " \
              "WHERE orderNo = %s " \
              "ORDER BY od.orderLineNo"

        params = (str(value))
        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows



class SaveMyData:
    def __init__(self, data, orderNumber):
        self.data = data
        self.orderNumber = orderNumber

    # csv로 출력
    def CSV(self):
        with open(str(self.orderNumber) + '.csv', 'w', encoding='utf-8') as f:
            w = csv.writer(f)
            w.writerow(self.data[0].keys())
            for item in self.data:
                w.writerow(item.values())

    # json으로 출력
    def JSON(self):
        for i in self.data:
            i['priceEach'] = str(i['priceEach']) # 문자형으로 변환하여 저장
            i['상품주문액'] = str(i['상품주문액']) # 문자형으로 변환하여 저장

        with open(str(self.orderNumber)+'.json', 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii = False)

    # xml로 출력
    def XML(self):
        rootElement = ET.Element('TABLE')

        for r in self.data:
            rowElement = ET.Element('ROW')
            rootElement.append(rowElement)

            for v in list(r.keys()):
                if r[v] == None:
                    rowElement.attrib[v] = ''
                else:
                    rowElement.attrib[v] = str(r[v])

        ET.ElementTree(rootElement).write(str(self.orderNumber)+'.xml', encoding='utf-8', xml_declaration=True)


# 주문의 상세 내역을 보여주는 창
class SubWindow(QWidget):
    def __init__(self, orderNumber):
        super().__init__()
        self.dbManager = DB_Utils()
        self.orderNumber = orderNumber
        self.setupUI()


    def setupUI(self):

        query = DB_Queries()
        self.orderdetail = query.orderDetail(self.orderNumber)

        self.setWindowTitle("서브 페이지")
        self.setGeometry(100, 100, 800, 600)

        # 타이틀 설정
        self.title = QGroupBox('주문 상세 내역', self)
        self.topSubLayout = QVBoxLayout()
        self.topSubLayout.addWidget(self.title)

        # 주문번호
        self.orderNumBox = QHBoxLayout()
        self.orderNum = QLabel("주문번호: ", self)
        self.orderNumT = QLabel(str(self.orderNumber), self)
        self.orderNumBox.addWidget(self.orderNum)
        self.orderNumBox.addWidget(self.orderNumT)

        # 상품개수
        self.orderCntBox = QHBoxLayout()
        self.orderCnt = QLabel("상품개수: ", self)
        self.orderCntT = QLabel(str(len(self.orderdetail)) + " 개", self)
        self.orderCntBox.addWidget(self.orderCnt)
        self.orderCntBox.addWidget(self.orderCntT)

        # 주문금액
        self.orderAmountBox = QHBoxLayout()
        self.orderAmount = QLabel("주문금액: ", self)
        total = 0
        for rowIDX, customer in enumerate(self.orderdetail):
            for columnIDX, (k, v) in enumerate(customer.items()):
                if k =="상품주문액":
                    total+=v
        self.orderAmountT = QLabel(str(total)+" 원", self)
        self.orderAmountBox.addWidget(self.orderAmount)
        self.orderAmountBox.addWidget(self.orderAmountT)

        self.infoLayout = QHBoxLayout()
        self.infoLayout.addLayout(self.orderNumBox)
        self.infoLayout.addLayout(self.orderCntBox)
        self.infoLayout.addLayout(self.orderAmountBox)


        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(self.orderdetail))
        self.tableWidget.setColumnCount(len(self.orderdetail[0]))
        self.tableLayout = QVBoxLayout()
        self.tableLayout.addWidget(self.tableWidget)

        columnNames = list(self.orderdetail[0].keys())
        self.tableWidget.setHorizontalHeaderLabels(columnNames)

        for rowIDX, customer in enumerate(self.orderdetail):  # customer는 딕셔너리
            for columnIDX, (k, v) in enumerate(customer.items()):
                if v == None:  # 파이썬이 DB의 널값을 None으로 변환함.
                    continue  # QTableWidgetItem 객체를 생성하지 않음
                elif isinstance(v, datetime.date):  # QTableWidgetItem 객체 생성
                    item = QTableWidgetItem(v.strftime('%Y-%m-%d'))
                else:
                    item = QTableWidgetItem(str(v))

                self.tableWidget.setItem(rowIDX, columnIDX, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()


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
        self.saveBtn.clicked.connect(self.saveData)

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

    def saveData(self):

        save = SaveMyData(self.orderdetail, self.orderNumber)

        fileType = self.fileTypeBox
        type = ''

        if fileType['csv'].isChecked():
            save.CSV()
            type = 'csv'
        elif fileType['json'].isChecked():
            save.JSON()
            type = 'json'
        else:
            save.XML()
            type = 'xml'


        QMessageBox.about(self, type ,'파일을 저장했습니다.')


# 메인 화면
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

        # 가장 마지막으로 선택한 콤보박스를 확인하기 위한 변수
        self.nowSelect = ''

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
        self.customerCombo.activated.connect(self.customerComboBoxActivated)

        # 국가 부분 셀렉트 박스
        self.country = QLabel("국가: ", self)
        self.countryCombo = QComboBox(self)
        columnName2 = list(country[0].keys())[0]
        items2 = ['없음' if row[columnName2] == None else row[columnName2] for row in country]
        self.countryCombo.addItems(['ALL'])
        self.countryCombo.addItems(items2)
        self.countryCombo.activated.connect(self.countryComboBoxActivated)


        # 도시 부분 셀렉트 박스
        self.city = QLabel("도시: ", self)
        self.cityCombo = QComboBox(self)
        columnName3 = list(city[0].keys())[0]
        items3 = ['없음' if row[columnName3] == None else row[columnName3] for row in city]
        self.cityCombo.addItems(['ALL'])
        self.cityCombo.addItems(items3)
        self.cityCombo.activated.connect(self.cityComboBoxActivated)


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
        self.cntResult = QGroupBox('검색된 주문의 개수: '+ str(len(init)), self)
        self.countResult = QVBoxLayout()
        self.countResult.addWidget(self.cntResult)
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(init))
        self.tableWidget.setColumnCount(len(init[0]))
        self.tableLayout = QVBoxLayout()
        self.tableLayout.addWidget(self.tableWidget)
        self.tableWidget.cellClicked.connect(self.clickedSellInfo)
        columnNames = list(init[0].keys())
        self.tableWidget.setHorizontalHeaderLabels(columnNames)

        for rowIDX, customer in enumerate(init):  # customer는 딕셔너리
            for columnIDX, (k, v) in enumerate(customer.items()):
                if v == None:  # 파이썬이 DB의 널값을 None으로 변환함.
                    continue  # QTableWidgetItem 객체를 생성하지 않음
                elif isinstance(v, datetime.date):  # QTableWidgetItem 객체 생성
                    item = QTableWidgetItem(v.strftime('%Y-%m-%d'))
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


    def clickedSellInfo(self):
        if self.tableWidget.item(self.tableWidget.currentRow() , 0) == None:
            return ;
        else :
            self.orderNum = self.tableWidget.item(self.tableWidget.currentRow() , 0).text()
            self.secondWindow()

    # customer 콤보박스를 선택했다면
    def customerComboBoxActivated(self):
        self.customerActive = self.customerCombo.currentText()
        self.nowSelect = 'customer'
        # country와 city 콤보박스의 값을 초기화 시킨다
        self.countryCombo.setCurrentText('ALL')
        self.cityCombo.setCurrentText('ALL')


    # country 콤보박스를 선택했다면
    def countryComboBoxActivated(self):
        self.countryActive = self.countryCombo.currentText()
        self.nowSelect = 'country'
        # customer 와 city 콤보박스의 값을 초기화 시킨다
        self.customerCombo.setCurrentText('ALL')
        self.cityCombo.setCurrentText('ALL')
        query = DB_Queries()
        city = query.selectCityFromCountry(self.countryActive)
        columnName3 = list(city[0].keys())[0]
        items3 = ['없음' if row[columnName3] == None else row[columnName3] for row in city]
        self.cityCombo.clear()
        self.cityCombo.addItems(['ALL'])
        self.cityCombo.addItems(items3)


    # city 콤보박스를 선택했다면
    def cityComboBoxActivated(self):
        self.cityActive = self.cityCombo.currentText()
        self.nowSelect = 'city'
        # country 콤보박스의 값을 초기화 시킨다
        self.customerCombo.setCurrentText('ALL')
        if self.cityActive == "ALL" :
            self.countryCombo.setCurrentText('ALL')


    # 검색 버튼 클릭
    def searchButtonClicked(self):
        query = DB_Queries()

        # 초반에 아무것도 선택 안하고 바로 검색 누르면 기본 화면만 보여지도록
        if self.nowSelect == '':
            return ;
        # self.showWhat은 어떤 콤보박스 기준으로 검색하여 보여줄지 설정

        # customer 콤보박스를 기준으로 검색
        if self.nowSelect == 'customer':
            self.showWhat = query.searchSelectCustomers(self.customerActive)
        # country 콤보박스를 기준으로 검색
        elif self.nowSelect == 'country':
            self.showWhat = query.searchSelectCountry(self.countryActive)
        # city 콤보박스를 기준으로 검색
        else:
            self.showWhat = query.searchSelectCity(self.cityActive)


        if len(self.showWhat) == 0:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            self.cntResult.setTitle('검색된 주문의 개수: ' + str(0))
            return ;
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(self.showWhat))
        self.tableWidget.setColumnCount(len(self.showWhat[0]))
        self.tableWidget.setHorizontalHeaderLabels(self.showWhat[0])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.cntResult.setTitle('검색된 주문의 개수: '+ str(len(self.showWhat)))

        for rowIDX, ctm in enumerate(self.showWhat):
            for columnIDX, (k, v) in enumerate(ctm.items()):
                if v == None:
                    continue
                elif isinstance(v, datetime.date):
                    item = QTableWidgetItem(v.strftime('%Y-%m-%d'))
                else:
                    item = QTableWidgetItem(str(v))

                self.tableWidget.setItem(rowIDX, columnIDX, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()


    # 초기화 버튼 클릭
    def initButtonClicked(self):
        self.nowSelect = 'customer'
        self.customerActive = "ALL"

        self.tableWidget.clearContents()
        self.customerCombo.setCurrentText('ALL')
        self.countryCombo.setCurrentText('ALL')
        self.cityCombo.setCurrentText('ALL')
        self.cntResult.setTitle('검색된 주문의 개수: ' + str(0))

        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)



    # 주문 상세 내역 윈도우 띄우기
    def secondWindow(self):
        self.subLayout = SubWindow(self.orderNum)
        self.subLayout.show()



def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

main()
