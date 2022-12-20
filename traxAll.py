from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu

import csv
from datetime import date


class TraxAll(MDApp):
    data = []
    dataTable = None
    columnToSortBy = 0
    screen = MDScreen()

    def build(self):
        self.listFromFile ("csvFiles/transactions.csv")

        self.dataTable = MDDataTable (
            pos_hint = {"center_x" : 0.5, "center_y" : 0.5},
            size_hint = (1.0, 0.85),
            check = False,
            column_data = [("Date", dp(20)), ("Cost", dp(20)), ("Store/Service", dp(30)), ("Category", dp(30)), ("Payment Method", dp(30)), ("Description", dp(30))],
            row_data = self.data,
            rows_num = 1000,
            sorted_on = "Date",
        )

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

        layout = MDFloatLayout()
        
        addTransactionButtonBox.add_widget(addTransactionButton)
        self.screen.add_widget(self.dataTable)
        self.screen.add_widget(addTransactionButtonBox)
        self.addToList((date.fromisoformat("2022-03-11"),"This","os ","a","test","stub"))
        return self.screen

    @staticmethod
    def askForNewTransaction():
        datePicker = MDDatePicker(
            on_cancel = lambda x: print("Daniel")
        )

        dialog = MDDialog(
            title = "Add Transaction",
            type = "custom",
            content_cls = MDBoxLayout(
                MDTextField(
                    hint_text = "Cost",
                    input_filter = "float",
                ),
                MDTextField(
                    hint_text = "Store/Service",
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
                    text = "ADD"
                )
            ]
        )

        dialog.open()
        datePicker.open()



    @staticmethod
    def readFromFile(filename):
        csvFilename = open(filename, encoding="utf-8-sig")
        csvFileReader = csv.reader(csvFilename)
        return csvFileReader

    def listFromFile(self, filename):
        try:
            fileReader = self.readFromFile(filename)
        except IOError as err:
            print(filename)
            return

        for rowData in fileReader:
            self.data.append((date.fromisoformat(rowData[0]), rowData[1], rowData[2], rowData[3], rowData[4], rowData[5]))

        self.data.sort(key = lambda data: data[0], reverse = True)

    def saveToFile(self, filename):
        csvFilename = open(filename, 'w', newline = '')
        csvWriter = csv.writer(csvFilename)
        
        for rowData in self.dataTable.row_data:
            csvWriter.writerow(rowData)

    def addToList(self, newData):
        self.dataTable.add_row(newData)
        self.dataTable.row_data.sort(key = lambda data: data[0], reverse = True)

        self.saveToFile("csvFiles/transactions.csv")


TraxAll().run()