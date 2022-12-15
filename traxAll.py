from kivy.metrics import dp

from kivymd.app import App
from kivymd.uix.datatables import DataTable
from kivymd.uix.screen import Screen

import csv
from datetime import date


class TraxAll(App):
    data = []

    def build(self):
        self.addToList ("csvFiles/december2021.csv")
        print(self.data)
        self.dataTable = DataTable (
            check = False,
            column_data = [("Date", dp(20)), ("Cost", dp(20)), ("Store/Service", dp(30)), ("Category", dp(30)), ("Description", dp(30)), ("Payment Method", dp(30))],
            row_data = self.data,
            rows_num = 1000
        )

        screen = Screen()
        screen.add_widget(self.dataTable)
        return screen

    @staticmethod
    def readFromFile(filename):
        csvFilename = open(filename, encoding="utf-8-sig")
        csvFileReader = csv.reader(csvFilename)
        return csvFileReader

    def addToList(self, filename):
        try:
            fileReader = self.readFromFile(filename)
        except IOError as err:
            return -1

        for rowData in fileReader:
            self.data.append((int (rowData[0]), rowData[1], rowData[2], rowData[3], rowData[4], rowData[5]))

TraxAll().run()