from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.button import MDFlatButton
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

        self.dateLabel = MDLabel()

        addTransactionButtonBox = MDBoxLayout(
            pos_hint = {"center_x" : 0.5},
            adaptive_size = True,
            padding = "10dp",
            spacing = "10dp"
        )

        addTransactionButton = MDFillRoundFlatButton(
            text = "Add Transaction",
            on_release = lambda x: self.askForNewTransaction()
        )

        addButton = MDFloatingActionButtonSpeedDial(
            data = dialOptions,
            root_button_anim = True,
            pos_hint = {"center_x" : 0.5}
        )


        layout = MDFloatLayout()
        
        #addTransactionButtonBox.add_widget(addButton)
        self.screen.add_widget(self.dataTable)
        self.screen.add_widget(addButton)
        self.addTransaction((date.fromisoformat("2022-03-11"),"This","os ","a","test","stub"))
        return self.screen

    def askForNewTransaction(self):

        transaction = []

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

        paymentMethodListItems = [
            {
                "text" : item[0],
                "viewclass" : "OneLineListItem",
                "on_release" : lambda x = item : [paymentMethodDropItem.set_item(x[0]), paymentMethodMenu.dismiss()]
            } for item in self.paymentMethods
        ]

        vendorListItems = [
            {
                "text" : item[0],
                "viewclass" : "OneLineListItem",
                "on_release" : lambda x = item : [vendorDropItem.set_item(x[0]), vendorMenu.dismiss()]
            } for item in self.vendors
        ]

        categoryListItems = [
            {
                "text" : item [0],
                "viewclass" : "OneLineListItem",
                "on_release" : lambda x = item : [categoryDropItem.set_item(x[0]), categoryMenu.dismiss()] 
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
                MDTextField(
                    hint_text = "Date",
                    validator = "date",
                    date_format = "yyyy/mm/dd",
                    helper_text = "YYYY/MM/DD Format",
                    required = True,
                    text = str(datetime.now().year) + "/" + str(datetime.now().month) + "/" + str(datetime.now().day)
                ),
                MDTextField(
                    hint_text = "Cost",
                    input_filter = "float",
                    required = True
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
                MDTextField(
                    hint_text = "Description"
                ),
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
                    on_release = lambda x : dialog.dismiss() if self.addTransaction() else errorDialog.open()   
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
        self.dataTable.add_row(newData)
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