from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.label import MDLabel

import csv
from datetime import date
from datetime import datetime


class TraxAll(MDApp):
    data = []
    vendors = []
    paymentMethods = []
    categories = []

    transactionsFile = "csvFiles/transactions.csv"
    vendorsFile = "csvFiles/vendors.csv"
    paymentMethodsFile = "csvFiles/paymentMethods.csv"
    categoriesFile = "csvFiles/categories.csv"

    dataTable = None
    dateLabel = None
    
    columnToSortBy = 0

    screen = MDScreen()

    def build(self):
        self.tableFromFile ("csvFiles/transactions.csv")
        self.listFromFile (self.vendors, self.vendorsFile)
        self.listFromFile (self.paymentMethods, self.paymentMethodsFile)
        self.listFromFile (self.categories, self.categoriesFile)

        dialOptions = {
            "Transaction" : [ 
                "icons/money.png",
                "on_release", lambda x : self.askForNewTransaction()
            ], 
            "Payment Method" : [
                "icons/creditCard.png",
                "on_release", lambda x : self.askForNewItem(self.paymentMethods, self.paymentMethodsFile, "Payment Method")
            ], 
            "Vendor" : [
                "icons/vendor.png",
                "on_release", lambda x : self.askForNewItem(self.vendors, self.vendorsFile, "Vendor/Service")
            ]
        }


        self.dataTable = MDDataTable (
            pos_hint = {"center_x" : 0.5, "center_y" : 0.5},
            size_hint = (1.0, 0.8),
            check = False,
            column_data = [("Date", dp(20)), ("Cost", dp(20)), ("Store/Service", dp(30)), ("Category", dp(30)), ("Payment Method", dp(30)), ("Description", dp(30))],
            row_data = self.data,
            rows_num = 1000,
            sorted_on = "Date",
        )

        # self.dateLabel = MDLabel()

        # addTransactionButtonBox = MDBoxLayout(
        #     pos_hint = {"center_x" : 0.5},
        #     adaptive_size = True,
        #     padding = "10dp",
        #     spacing = "10dp"
        # )

        # addTransactionButton = MDFillRoundFlatButton(
        #     text = "Add Transaction",
        #     on_release = lambda x: self.askForNewTransaction()
        # )

        addButton = MDFloatingActionButtonSpeedDial(
            data = dialOptions,
            root_button_anim = True,
            pos_hint = {"center_x" : 0.2}
        )

        calculateButton = MDFloatingActionButton(
            icon = "icons/reciept.png",
            on_release = lambda x : self.askForCalculationInfo(),
            #pos_hint = {"center_x" : 0.8}
        )


        layout = MDFloatLayout()
        
        #addTransactionButtonBox.add_widget(addButton)
        self.screen.add_widget(self.dataTable)
        self.screen.add_widget(
            MDBoxLayout(
                addButton,
                calculateButton,
                padding = "20dp",
                pos_hint = {"center_x" : -0.36}
            )
        )
        #self.addTransaction((date.fromisoformat("2022-03-11"),"This","os ","a","test","stub"))
        return self.screen

    def askForNewTransaction(self):
        dropDownItems = []

        # self.dateLabel.text = "Date"

        errorDialog = MDDialog(
            title = "Error",
            text = "Something's not right. Please review the transaction details and try again.",
            buttons = [
                MDFillRoundFlatButton(
                    text = "OK",
                    on_release = lambda x : errorDialog.dismiss()
                )
            ]
        )

        # datePicker = MDDatePicker()
        # datePicker.on_save = self.on_save and datePicker.dismiss

        dateTextField = MDTextField(
            hint_text = "Date",
            validator = "date",
            date_format = "yyyy/mm/dd",
            helper_text = "YYYY/MM/DD Format",
            required = True,
            text = str(datetime.now().year) + "/" + str(datetime.now().month) + "/" + str(datetime.now().day)
        )

        costTextField = MDTextField(
            hint_text = "Cost",
            input_filter = "float",
            required = True
        )

        descriptionTextField = MDTextField(
            hint_text = "Description"
        )

        paymentMethodListItems = [
            {
                "text" : item[0],
                "viewclass" : "OneLineListItem",
                "on_release" : lambda x = item : [dropDownItems.append(["P", x[0]]), paymentMethodDropItem.set_item(x[0]), paymentMethodMenu.dismiss()]
            } for item in self.paymentMethods
        ]

        vendorListItems = [
            {
                "text" : item[0],
                "viewclass" : "OneLineListItem",
                "on_release" : lambda x = item : [dropDownItems.append(["V", x[0]]), vendorDropItem.set_item(x[0]), vendorMenu.dismiss()]
            } for item in self.vendors
        ]

        categoryListItems = [
            {
                "text" : item [0],
                "viewclass" : "OneLineListItem",
                "on_release" : lambda x = item : [dropDownItems.append(["C", x[0]]), categoryDropItem.set_item(x[0]), categoryMenu.dismiss()] 
            } for item in self.categories
        ]

        vendorDropItem = MDDropDownItem()
        paymentMethodDropItem = MDDropDownItem()
        categoryDropItem = MDDropDownItem()

        vendorMenu = MDDropdownMenu(
            items = vendorListItems,
            position = "center",
            caller = vendorDropItem,
            width_mult = 4
        )

        paymentMethodMenu = MDDropdownMenu(
            items = paymentMethodListItems,
            position = "center",
            caller = paymentMethodDropItem,
            width_mult = 4
        )

        categoryMenu = MDDropdownMenu(
            items = categoryListItems,
            position = "center",
            caller = categoryDropItem,
            width_mult = 4
        )

        vendorDropItem.text = "Select"
        paymentMethodDropItem.text = "Select"
        categoryDropItem.text = "Select"

        vendorDropItem.on_release = vendorMenu.open
        paymentMethodDropItem.on_release = paymentMethodMenu.open
        categoryDropItem.on_release = categoryMenu.open

        dialog = MDDialog(
            title = "Add Transaction",
            type = "custom",
            content_cls = MDBoxLayout(
                dateTextField,
                costTextField,
                MDBoxLayout(
                    MDLabel(
                        text = "Vendor/Service"
                    ),
                    vendorDropItem,
                    padding = "12dp"
                ),
                MDBoxLayout(
                    MDLabel(
                        text = "Category"
                    ),
                    categoryDropItem,
                    padding = "12dp"
                ),
                MDBoxLayout(
                    MDLabel(
                        text = "Payment Method"
                    ),
                    paymentMethodDropItem,
                    padding = "12dp"
                ),                
                descriptionTextField,
                orientation = "vertical",
                spacing = "12dp",
                size_hint_y = None,
                height = "400dp"
            ),
            buttons = [
                MDFlatButton(
                    text = "CANCEL",
                    on_release = lambda x : dialog.dismiss()
                ),
                MDFillRoundFlatButton(
                    text = "ADD",
                    on_release = lambda x : dialog.dismiss() if self.addTransaction([dateTextField.text, costTextField.text, dropDownItems, descriptionTextField.text]) else errorDialog.open()   
                )
            ]
        )

        dialog.open()
        # datePicker.open()

    # def on_save(self, instance, value):
    #     print("gooby")
    #     self.dateLabel.text = str(value)

    def askForNewItem(self, itemList, filename, itemType):
        errorDialog = MDDialog(
            title = "Error",
            text = "This " + itemType.lower() + " is already in our records. Please try again.",
            buttons = [
                MDFillRoundFlatButton(
                    text = "OK",
                    on_release = lambda x : errorDialog.dismiss()
                )
            ]
        )

        textField = MDTextField(
            hint_text = itemType
        )

        dialog = MDDialog(
            title = "Add New " + itemType,
            type = "custom",
            content_cls = MDBoxLayout(
                textField,
                orientation = "vertical",
                size_hint_y = None
            ),
            buttons = [
                MDFlatButton(
                    text = "CANCEL",
                    on_release = lambda x : dialog.dismiss()
                ),
                MDFillRoundFlatButton(
                    text = "ADD",
                    on_release = lambda x : dialog.dismiss() if self.addToList([textField.text], itemList, filename) else errorDialog.open()   
                )
            ],
        )

        dialog.open()

    def askForCalculationInfo(self):
    
        errorDialog = MDDialog(
            title = "Error",
            text = "Something's not right. Please review your inputs and try again.",
            buttons = [
                MDFillRoundFlatButton(
                    text = "OK",
                    on_release = lambda x : errorDialog.dismiss()
                )
            ]
        )

        startDateTextField = MDTextField(
            hint_text = "Start Date",
            validator = "date",
            date_format = "yyyy/mm/dd",
            helper_text = "YYYY/MM/DD Format",
            required = True,
            text = str(datetime.now().year) + "/" + str(datetime.now().month) + "/" + str(datetime.now().day)
        )

        endDateTextField = MDTextField(
            hint_text = "End Date",
            validator = "date",
            date_format = "yyyy/mm/dd",
            helper_text = "YYYY/MM/DD Format",
            required = True,
            text = str(datetime.now().year) + "/" + str(datetime.now().month) + "/" + str(datetime.now().day)
        )

        dropDownItems = []

        paymentMethodListItems = [
            {
                "text" : item[0],
                "viewclass" : "OneLineListItem",
                "on_release" : lambda x = item : [dropDownItems.append(["P", x[0]]), paymentMethodDropItem.set_item(x[0]), paymentMethodMenu.dismiss()]
            } for item in self.paymentMethods
        ]

        vendorListItems = [
            {
                "text" : item[0],
                "viewclass" : "OneLineListItem",
                "on_release" : lambda x = item : [dropDownItems.append(["V", x[0]]), vendorDropItem.set_item(x[0]), vendorMenu.dismiss()]
            } for item in self.vendors
        ]

        categoryListItems = [
            {
                "text" : item [0],
                "viewclass" : "OneLineListItem",
                "on_release" : lambda x = item : [dropDownItems.append(["C", x[0]]), categoryDropItem.set_item(x[0]), categoryMenu.dismiss()] 
            } for item in self.categories
        ]

        vendorDropItem = MDDropDownItem()
        paymentMethodDropItem = MDDropDownItem()
        categoryDropItem = MDDropDownItem()

        vendorMenu = MDDropdownMenu(
            items = vendorListItems,
            position = "center",
            caller = vendorDropItem,
            width_mult = 4
        )

        paymentMethodMenu = MDDropdownMenu(
            items = paymentMethodListItems,
            position = "center",
            caller = paymentMethodDropItem,
            width_mult = 4
        )

        categoryMenu = MDDropdownMenu(
            items = categoryListItems,
            position = "center",
            caller = categoryDropItem,
            width_mult = 4
        )

        vendorDropItem.text = "All"
        paymentMethodDropItem.text = "All"
        categoryDropItem.text = "All"

        vendorDropItem.on_release = vendorMenu.open
        paymentMethodDropItem.on_release = paymentMethodMenu.open
        categoryDropItem.on_release = categoryMenu.open

        dialog = MDDialog(
            title = "Calculate Expenses",
            type = "custom",
            content_cls = MDBoxLayout(
                MDBoxLayout(
                    startDateTextField,
                    endDateTextField,
                    spacing = "30dp"
                ),
                MDBoxLayout(
                    MDLabel(
                        text = "Vendor/Service"
                    ),
                    vendorDropItem,
                    padding = "12dp"
                ),
                MDBoxLayout(
                    MDLabel(
                        text = "Category"
                    ),
                    categoryDropItem,
                    padding = "12dp"
                ),
                MDBoxLayout(
                    MDLabel(
                        text = "Payment Method"
                    ),
                    paymentMethodDropItem,
                    padding = "12dp"
                ),                
                orientation = "vertical",
                size_hint_y = None,
                spacing = "12dp",
                height = "250dp"
            ),
            buttons = [
                MDFlatButton(
                    text = "CANCEL",
                    on_release = lambda x : dialog.dismiss()
                ),
                MDFillRoundFlatButton(
                    text = "SEARCH",
                    on_release = lambda x : dialog.dismiss() if self.showResults(startDateTextField.text, endDateTextField.text, dropDownItems) else errorDialog.open()   
                )
            ]
        )

        dialog.open()

    def showResults(self, startDateString, endDateString, selections):

        startDate = date.fromisoformat(startDateString.replace("/", "-"))
        endDate = date.fromisoformat(endDateString.replace("/", "-"))

        if (startDate > endDate) or (startDate > date.today()) or (endDate > date.today()):
            return False

        paymentMethod = None
        category = None
        vendor = None

        for i in range (0, len(selections)):
            if (selections[i][0] == "P"):
                paymentMethod = selections[i][1]
            
            elif (selections[i][0] == "C"):
                category = selections[i][1]

            elif (selections[i][0] == "V"):
                vendor = selections[i][1]

        #filteredData = self.dataTable.row_data.copy()
        filteredData = []

        for rowData in self.dataTable.row_data:
            shouldBeAdded = True

            if rowData[0] > endDate or rowData[0] < startDate:
                shouldBeAdded = False
                #print(rowData)
                continue

            if paymentMethod != None:
                if paymentMethod != rowData[4]:
                    shouldBeAdded = False
                    #print(rowData)
                    continue
            
            if category != None:
                if category != rowData[3]:
                    shouldBeAdded = False
                    #print(rowData)
                    continue

            if vendor != None:
                if vendor != rowData[2]:
                    shouldBeAdded = False
                    #print(rowData)
                    continue

            if shouldBeAdded:
                filteredData.append(rowData)
            
        totalSpent = 0

        for rowData in filteredData:
            totalSpent = totalSpent + float(rowData[1].replace("$", ''))

        dialog = MDDialog (
            title = "[color=ff0000]Total $" + str(totalSpent) + " spent[/color]",
            type = "custom",
            content_cls = MDBoxLayout(
                MDDataTable (
                    size_hint = (1.0, 0.8),
                    check = False,
                    column_data = [("Date", dp(20)), ("Cost", dp(20)), ("Store/Service", dp(30)), ("Category", dp(30)), ("Payment Method", dp(30)), ("Description", dp(30))],
                    row_data = filteredData,
                    rows_num = 1000,
                    sorted_on = "Date",
                ),
                orientation = "vertical",
                size_hint_y = None,
                height = "600dp",
                width = "600dp"
            ),
            buttons = [
                MDFillRoundFlatButton(
                    text = "OK",
                    on_release = lambda x : dialog.dismiss()
                )
            ]
        )

        dialog.open()

        return True

    @staticmethod
    def readFromFile(filename):
        csvFilename = open(filename, encoding="utf-8-sig")
        csvFileReader = csv.reader(csvFilename)
        return csvFileReader

    def tableFromFile(self, filename):
        try:
            fileReader = self.readFromFile(filename)
        except IOError as err:
            print(filename)
            return

        for rowData in fileReader:
            self.data.append((date.fromisoformat(rowData[0]), rowData[1], rowData[2], rowData[3], rowData[4], rowData[5]))

        self.data.sort(key = lambda data: data[0], reverse = True)

    def listFromFile (self, itemList, filename):
        try:
            fileReader = self.readFromFile(filename)
        except IOError as err:
            print(filename)
            return

        for rowData in fileReader:
            itemList.append(rowData)

        itemList.sort()

    def saveToFile(self, itemList, filename):
        csvFilename = open(filename, 'w', newline = '')
        csvWriter = csv.writer(csvFilename)
        
        csvWriter.writerows(itemList)

    def addTransaction(self, newData):
        newTransaction = []
        
        newTransaction.append(date.fromisoformat(newData[0].replace('/', '-')))

        if newTransaction[0] > date.today():
            print ("Date")
            return False
        
        newTransaction.append("$" + newData[1])

        if newTransaction[1] == "$":
            print("Money")
            return False

        for i in range (0, 3):
            newTransaction.append(None)

        for i in range (0, len(newData[2])):
            if (newData[2][i][0] == "P"):
                newTransaction[4] = newData[2][i][1]
            
            elif (newData[2][i][0] == "C"):
                newTransaction[3] = newData[2][i][1]

            elif (newData[2][i][0] == "V"):
                newTransaction[2] = newData[2][i][1]

        for i in range(2, 5):
            if newTransaction[i] == None:
                return False

        newTransaction.append(newData[3])
        
        self.dataTable.add_row(newTransaction)
        self.dataTable.row_data.sort(key = lambda data: data[0], reverse = True)

        self.saveToFile(self.dataTable.row_data, self.transactionsFile)

        return True

    def addToList(self, newData, itemList, filename):
        for rowData in itemList:
            if newData == rowData:
                return False
        
        itemList.append(newData)
        print(itemList)
        itemList.sort()

        self.saveToFile(itemList, filename)
        
        return True

TraxAll().run()