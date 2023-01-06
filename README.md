# TraxAll


## Using on Mobile

At the moment, the app is only available on Android. Pulling the repo and running it on your machine will have the app work normally but if you wish to use the app on android, the google drive with the APK can be found at: traxall.maximossamuel.com

## Getting started

### Python
* Ensure you have the latest version of python installed

### KivyMD
* This app was made using the KivyMD library, which is an extension of the Kivy library.
* Install Kivy by going to your terminal and inputting the following into your command line:

```
python -m pip install "kivy[full]" kivy_examples
```
* Then install KivyMD by inputting the following into the command line:

```
pip install kivymd
```

### Running the program
* On a terminal, navigate to the folder where main.py is located and input the following into the command line:

```
python main.py
```
* Do NOT run traxAll.py. That is an old version of main.py and is there for version control purposes

## About the Author

Maximos Samuel
maximos@uoguelph.ca

## Things to Note for Future Revisions

### Functionality
* Many widgets and blocks of code are repeated and could have been easily returned by methods
* Add a way to remove unwanted categories, payment methods and vendors
* Add an easier way to delete a transaction
* Add a way to edit a transaction

### UI Design
* The buttons are not centered, as of writing this, I haven't found a way to fix that
* when using the app on mobile, the keyboard will go over the description text field, making it so that the user cannot see what they are typing
* When selecting an item from a dropmenu, the size of the selected item may distort the dropmenu's label
