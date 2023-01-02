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
    mostRecent = None

    transactionsFile = "csvFiles/transactions.csv"
    vendorsFile = "csvFiles/vendors.csv"
    paymentMethodsFile = "csvFiles/paymentMethods.csv"
    categoriesFile = "csvFiles/categories.csv"

    dataTable = None
    dateLabel = None
    
    columnToSortBy = 0

    screen = MDScreen()

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"

        self.tableFromFile (self.transactionsFile)
        self.listFromFile (self.vendors, self.vendorsFile)
        self.listFromFile (self.paymentMethods, self.paymentMethodsFile)
        self.listFromFile (self.categories, self.categoriesFile)

        ## Initializing the array containing dial options. Is used when speed dial is created        
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
            ],
            "Category" : [
                "icons/category.png",
                "on_release", lambda x: self.askForNewItem(self.categories, self.categoriesFile, "Category")
            ]
        }

        ## Creation of data tab;e
        self.dataTable = MDDataTable (
            pos_hint = {"center_x" : 0.5, "center_y" : 0.5},
            size_hint = (1.0, 0.8),
            check = False,
            column_data = [("Date", dp(20)), ("Cost", dp(20)), ("Store/Service", dp(30)), ("Category", dp(30)), ("Payment Method", dp(30)), ("Description", dp(30))],
            row_data = self.data,
            rows_num = 1000,
            sorted_on = "Date",
        )

        ## Button for adding a transaction
        addButton = MDFloatingActionButtonSpeedDial(
            data = dialOptions,
            root_button_anim = True,
            pos_hint = {"center_x" : 0.2}
        )

        ## Button for open the 'Calculate Expenses' menu
        calculateButton = MDFloatingActionButton(
            icon = "icons/reciept.png",
            on_release = lambda x : self.askForCalculationInfo(),
        )

        ## Button for undoing the previous transaction 
        deleteButton = MDFloatingActionButton(
            icon = "icons/delete.png",
            on_release = lambda x : self.deleteConfirmation()
        )

        self.screen.add_widget(self.dataTable)
        self.screen.add_widget(
            MDBoxLayout(
                addButton,
                deleteButton,
                calculateButton,
                padding = "20dp",
                spacing = "250dp",
                pos_hint = {"center_x" : 0.1}
            )
        )

        return self.screen

    ## This method generates a menu that asks the user for the details of the
    ## transaction they wish to add
    def askForNewTransaction(self):
        dropDownItems = []

        ## Error dialog (Note for next revision, there are many of these in the code, 
        ## next time, just make the dialog get generated from a function
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

        ## Code was originally going to use the MDDatePicker library to pick dates. Did not work.
        ## Might be implemented in a revision
        # datePicker = MDDatePicker()
        # datePicker.on_save = self.on_save and datePicker.dismiss

        ## Date Text Field
        dateTextField = MDTextField(
            hint_text = "Date",
            validator = "date",
            date_format = "yyyy/mm/dd",
            helper_text = "YYYY/MM/DD Format",
            required = True,
            text = str(datetime.now().year) + "/" + str(datetime.now().month) + "/" + str(datetime.now().day)
        )

        ## Cost Text Field
        costTextField = MDTextField(
            hint_text = "Cost",
            input_filter = "float",
            required = True
        )

        ## Description Text Field
        descriptionTextField = MDTextField(
            hint_text = "Description (Optional)"
        )

        ## Data to be put into the drop down lists. Each time an option is selected in the dropdown menu, it is appended to
        ## the dropDownItems array. Where the last instances of "P", "V" and "C" are checked and implemented accordingly.

        ## Payment Method Dropdown Items
        paymentMethodListItems = [
            {
                "text" : item[0],
                "viewclass" : "OneLineListItem",
                "on_release" : lambda x = item : [dropDownItems.append(["P", x[0]]), paymentMethodDropItem.set_item(x[0]), paymentMethodMenu.dismiss()]
            } for item in self.paymentMethods
        ]

        ## Vendor Dropdown Items
        vendorListItems = [
            {
                "text" : item[0],
                "viewclass" : "OneLineListItem",
                "on_release" : lambda x = item : [dropDownItems.append(["V", x[0]]), vendorDropItem.set_item(x[0]), vendorMenu.dismiss()]
            } for item in self.vendors
        ]

        ## Category Dropdown Items
        categoryListItems = [
            {
                "text" : item [0],
                "viewclass" : "OneLineListItem",
                "on_release" : lambda x = item : [dropDownItems.append(["C", x[0]]), categoryDropItem.set_item(x[0]), categoryMenu.dismiss()] 
            } for item in self.categories
        ]

        ## Drop Items and elements are modified separately due to errors being returned when traditionally handling a KivyMD element

        vendorDropItem = MDDropDownItem()
        paymentMethodDropItem = MDDropDownItem()
        categoryDropItem = MDDropDownItem()
  
        ## Creation of Dropdown Menus
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

        ## Setting the drop items to open the dropdown menus upon getting clicked
        vendorDropItem.on_release = vendorMenu.open
        paymentMethodDropItem.on_release = paymentMethodMenu.open
        categoryDropItem.on_release = categoryMenu.open

        ## Method's main dialog
        dialog = MDDialog(
            title = "Add Transaction",
            type = "custom",
            content_cls = MDBoxLayout(
                dateTextField,
                costTextField,

                ## BoxLayouts for each Dropdown menu, each including the DropItem and its label
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

        ## More MDDatePicker Code, keep for possible revisions
        # datePicker.open()

    # def on_save(self, instance, value):
    #     print("gooby")
    #     self.dateLabel.text = str(value)

    ## Asks the user for the name of the new item they wish to add to the appropriate list, whether that be a vendor or payment method.
    def askForNewItem(self, itemList, filename, itemType):

        ## Error Dialog
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

        ## Main User-input text field. This text field's hint is named based on the itemType value 
        ## passed into the method. Will be displayed followed by "Add New" in the dialog box
        textField = MDTextField(
            hint_text = itemType
        )

        dialog = MDDialog(
            
            ## Title is changed based on the string stored in itemType
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

    ## Creates a dialog box that asks for what kinds of transactions the user wants to search for
    def askForCalculationInfo(self):
    
        ## Error Dialog Box
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

        ## Text field for the start date (note for next revision, these can easily be done in a function)
        startDateTextField = MDTextField(
            hint_text = "Start Date",
            validator = "date",
            date_format = "yyyy/mm/dd",
            helper_text = "YYYY/MM/DD Format",
            required = True,

            ## Intializing the contents of the text field as the current date
            text = str(datetime.now().year) + "/" + str(datetime.now().month) + "/" + str(datetime.now().day)
        )

        ## Text field for the start date
        endDateTextField = MDTextField(
            hint_text = "End Date",
            validator = "date",
            date_format = "yyyy/mm/dd",
            helper_text = "YYYY/MM/DD Format",
            required = True,

            ## Initializing the content of the text field as the current date
            text = str(datetime.now().year) + "/" + str(datetime.now().month) + "/" + str(datetime.now().day)
        )

        ## Same logic with askForNewTransactions used with this function
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

        ## Method's main dialog
        dialog = MDDialog(
            title = "Calculate Expenses",
            type = "custom",
            content_cls = MDBoxLayout(

                ## BoxLayout for text fields
                MDBoxLayout(
                    startDateTextField,
                    endDateTextField,
                    spacing = "30dp"
                ),
                ## BoxLayout is created for each dropdown item
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

    ## Asks the user if they wish to undo the last transaction they added, temporary function until a more
    ## viable solution is developed for deleting a transaction in future revision
    def deleteConfirmation(self):
        ## Method's main dialog
        dialog = MDDialog(
            title = "Undo",
            text = "Would you like to undo your last transaction?",
            buttons = [
                MDFlatButton(
                    text = "No",
                    on_release = lambda x : dialog.dismiss()
                ),
                MDFillRoundFlatButton(
                    text = "Yes",
                    on_release = lambda x : [self.deleteTransaction(), dialog.dismiss()]  
                )
            ]
        )

        ## Error dialog
        errorDialog = MDDialog(
            title = "Error",
            text = "There is no transaction to redo.",
            buttons = [
                MDFillRoundFlatButton(
                    text = "OK",
                    on_release = lambda x : errorDialog.dismiss()
                )
            ]
        )

        ## When a new transaction is created, it is set as the most recent transaction,
        ## this resets every time the app is turned on. If it is found that no transaction has been made
        ## during runtime, the error dialog opens
        if self.mostRecent == None:
            errorDialog.open()
        else:
            dialog.open()
        
    ## Deletes the most recent transaction
    def deleteTransaction(self):
        self.dataTable.row_data.remove(self.mostRecent)
        self.mostRecent = None

    ## Shows a new dialog box that shows the results of a user's search
    def showResults(self, startDateString, endDateString, selections):

        ## Tries to get convert the two dates to datetime format. Function will shut down
        ## if that fails
        try:    
            startDate = date.fromisoformat(startDateString.replace("/", "-"))
            endDate = date.fromisoformat(endDateString.replace("/", "-"))
        except:
            return False

        ## Check to see if the date range is valid
        if (startDate > endDate) or (startDate > date.today()) or (endDate > date.today()):
            return False

        ## Initialization and setting of dropdown selections to be used in search
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

        filteredData = []

        ## Search begins, for loop goes through the existing list and checks whether or not each
        ## list element is one of the elements the user is searching for. If so, the element is added
        ## to a new list with the searched elements at the end of each iteration
        for rowData in self.dataTable.row_data:
            shouldBeAdded = True

            ## Check if date is in range
            if rowData[0] > endDate or rowData[0] < startDate:
                shouldBeAdded = False
                continue

            ## Check for each dropdown item
            if paymentMethod != None:
                if paymentMethod != rowData[4]:
                    shouldBeAdded = False
                    continue
            
            if category != None:
                if category != rowData[3]:
                    shouldBeAdded = False
                    continue

            if vendor != None:
                if vendor != rowData[2]:
                    shouldBeAdded = False
                    continue

            if shouldBeAdded:
                filteredData.append(rowData)

        ## Initialization and adding up of total money spent from elements within search
        totalSpent = 0

        for rowData in filteredData:
            totalSpent = totalSpent + float(rowData[1].replace("$", ''))

        ## Main dialog
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

    ## Opens a CSV file
    @staticmethod
    def readFromFile(filename):
        csvFilename = open(filename, encoding="utf-8-sig")
        csvFileReader = csv.reader(csvFilename)
        return csvFileReader

    ## Creates a 2D array of data from a file
    def tableFromFile(self, filename):
        try:
            fileReader = self.readFromFile(filename)
        except IOError as err:
            return

        for rowData in fileReader:
            self.data.append((date.fromisoformat(rowData[0]), rowData[1], rowData[2], rowData[3], rowData[4], rowData[5]))

        self.data.sort(key = lambda data: data[0], reverse = True)

    ## Creates an array of data to a given list from a given file
    def listFromFile (self, itemList, filename):
        try:
            fileReader = self.readFromFile(filename)
        except IOError as err:
            print(filename)
            return

        for rowData in fileReader:
            itemList.append(rowData)

        itemList.sort()

    ## Saves from a given list to a given file
    def saveToFile(self, itemList, filename):
        csvFilename = open(filename, 'w', newline = '')
        csvWriter = csv.writer(csvFilename)
        
        csvWriter.writerows(itemList)

    ## Checks validity of and adds a transaction to the data table
    def addTransaction(self, newData):
        newTransaction = []
        
        ## Check to see if date/format is valid
        try:
            newTransaction.append(date.fromisoformat(newData[0].replace('/', '-')))
        except:
            return False

        ## Date cannot be from later than the current day
        if newTransaction[0] > date.today():
            print ("Date")
            return False

        ## Adding a dollar sign to the cost string
        newTransaction.append("$" + newData[1])

        ## Check to see if cost text field is empty
        if newTransaction[1] == "$":
            print("Money")
            return False

        ## Intialization/addition of drop item selections
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

        ## Addition of description
        newTransaction.append(newData[3])
        
        ## If the method makes it to this point, the new transaction is added to the data table and the data is sorted
        self.dataTable.add_row(newTransaction)
        self.dataTable.row_data.sort(key = lambda data: data[0], reverse = True)

        ## mostRecent is set to the new transaction so that it can be undone if the user wishes
        self.mostRecent = newTransaction

        ## Current data on data table is saved to the transactions file
        self.saveToFile(self.dataTable.row_data, self.transactionsFile)

        return True

    ## Adds a given element to a given list
    def addToList(self, newData, itemList, filename):
        ## Check to see if element is already in the list
        for rowData in itemList:
            if newData == rowData:
                return False
        
        ## New element is added to the list and the list is sorted
        itemList.append(newData)
        itemList.sort()

        ## New list is saved to the given file
        self.saveToFile(itemList, filename)
        
        return True

TraxAll().run()