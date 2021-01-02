from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
import sys
from os import path
from PyQt5.uic import loadUiType  # imports the UI from Qtdesign
import sqlite3

FORM_CLASS, _ = loadUiType(path.join(path.dirname('__file__'), "design.ui"))


class Main(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()
        self.navigation()

    def Handle_Buttons(self):
        self.refresh_button.clicked.connect(self.GET_DATA)
        self.search_button.clicked.connect(self.search)
        self.check_button.clicked.connect(self.check)
        self.update_button.clicked.connect(self.update)
        self.delete_button.clicked.connect(self.delete)
        self.add_button.clicked.connect(self.add)
        self.next_button.clicked.connect(self.next)
        self.prev_button.clicked.connect(self.prev)
        self.first_button.clicked.connect(self.first)
        self.last_button.clicked.connect(self.last)

    def check(self):
        db = sqlite3.connect("parts_database.db")
        cursor = db.cursor()
        command = '''SELECT Reference, Part_Name, Count from parts_table order by Count asc LIMIT 3'''
        result = cursor.execute(command)
        self.table2.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table2.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def search(self):
        db = sqlite3.connect("parts_database.db")
        cursor = db.cursor()
        nbr = int(self.count_filter.text())
        command = '''SELECT * from parts_table WHERE Count<=?'''
        result = cursor.execute(command, [nbr])
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def GET_DATA(self):
        # connect with sqlite database and display data from database
        db = sqlite3.connect("parts_database.db")
        cursor = db.cursor()
        command = '''SELECT * from parts_table'''
        result = cursor.execute(command)
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        # display the reference number and type in statistics tab
        cursor2 = db.cursor()
        cursor3 = db.cursor()
        part_name = '''SELECT COUNT(DISTINCT Part_Name) from parts_table'''
        ref_name = '''SELECT COUNT (DISTINCT Reference) from parts_table'''
        result_parts = cursor2.execute(part_name)
        result_ref = cursor3.execute(ref_name)
        self.label_ref.setText(str(result_ref.fetchone()[0]))
        self.label_parts.setText(str(result_parts.fetchone()[0]))

        # display number of holes min, max and their references
        cursor4 = db.cursor()
        cursor5 = db.cursor()
        min_hole = '''SELECT MIN(Number_of_holes), Reference from parts_table'''
        max_hole = '''SELECT MAX(Number_of_holes), Reference from parts_table'''
        result_minhole = cursor4.execute(min_hole)
        result_maxhole = cursor5.execute(max_hole)
        r1 = result_minhole.fetchone()
        r2 = result_maxhole.fetchone()
        self.label_min_holes.setText(str(r1[0]))
        self.label_max_holes.setText(str(r2[0]))
        self.label_min_holes2.setText(str(r1[1]))
        self.label_max_holes2.setText(str(r2[1]))

    def navigation(self):
        db = sqlite3.connect("parts_database.db")
        cursor = db.cursor()

        command = '''SELECT * from parts_table'''
        result = cursor.execute(command)
        val = result.fetchone()

        self.id.setText(str(val[0]))
        self.Reference.setText(str(val[1]))
        self.Part_Name.setText(str(val[2]))
        self.Min_Area.setText(str(val[3]))
        self.Max_Area.setText(str(val[4]))
        self.Number_of_holes.setText(str(val[5]))
        self.Min_diameter.setText(str(val[6]))
        self.Max_diameter.setText(str(val[7]))
        self.Count.setValue(val[8])

    def update(self):
        db = sqlite3.connect("parts_database.db")
        cursor = db.cursor()

        id_ = int(self.id.text())
        reference_ = self.Reference.text()
        part_name_ = self.Part_Name.text()
        min_area_ = self.Min_Area.text()
        max_area_ = self.Max_Area.text()
        number_of_holes_ = self.Number_of_holes.text()
        min_diameter_ = self.Min_diameter.text()
        max_diameter_ = self.Max_diameter.text()
        count_ = str(self.Count.value())

        row = (
            reference_, part_name_, min_area_, max_area_, number_of_holes_, min_diameter_, max_diameter_, count_, id_)
        command = '''UPDATE parts_table SET Reference=?, Part_Name=?, Min_Area=?, Max_area=?, Number_of_holes=?, Min_diameter=?, 
        Max_diameter=?, Count=? WHERE ID=?'''

        cursor.execute(command, row)
        db.commit()

    def delete(self):
        db = sqlite3.connect("parts_database.db")
        cursor = db.cursor()
        d = self.id.text()
        command = '''DELETE from parts_table WHERE ID=? '''
        cursor.execute(command, d)
        db.commit()

    def add(self):
        db = sqlite3.connect("parts_database.db")
        cursor = db.cursor()

        reference_ = self.Reference.text()
        part_name_ = self.Part_Name.text()
        min_area_ = self.Min_Area.text()
        max_area_ = self.Max_Area.text()
        number_of_holes_ = self.Number_of_holes.text()
        min_diameter_ = self.Min_diameter.text()
        max_diameter_ = self.Max_diameter.text()
        count_ = str(self.Count.value())

        row = (
            reference_, part_name_, min_area_, max_area_, number_of_holes_, min_diameter_, max_diameter_, count_)
        command = '''INSERT INTO  parts_table (Reference, Part_Name, Min_Area, Max_area, Number_of_holes, Min_diameter, 
                Max_diameter, Count) VALUES(?,?,?,?,?,?,?,?)'''

        cursor.execute(command, row)
        db.commit()

    def next(self):
        db = sqlite3.connect("parts_database.db")
        cursor = db.cursor()
        idd = int(self.id.text())

        command = '''SELECT * from parts_table WHERE ID=?'''
        result = cursor.execute(command, str(idd + 1))
        val = result.fetchone()

        self.id.setText(str(val[0]))
        self.Reference.setText(str(val[1]))
        self.Part_Name.setText(str(val[2]))
        self.Min_Area.setText(str(val[3]))
        self.Max_Area.setText(str(val[4]))
        self.Number_of_holes.setText(str(val[5]))
        self.Min_diameter.setText(str(val[6]))
        self.Max_diameter.setText(str(val[7]))
        self.Count.setValue(val[8])
        db.commit()

    def prev(self):
        db = sqlite3.connect("parts_database.db")
        cursor = db.cursor()
        idd = int(self.id.text())

        command = '''SELECT * from parts_table WHERE ID=?'''
        result = cursor.execute(command, str(idd - 1))
        val = result.fetchone()

        self.id.setText(str(val[0]))
        self.Reference.setText(str(val[1]))
        self.Part_Name.setText(str(val[2]))
        self.Min_Area.setText(str(val[3]))
        self.Max_Area.setText(str(val[4]))
        self.Number_of_holes.setText(str(val[5]))
        self.Min_diameter.setText(str(val[6]))
        self.Max_diameter.setText(str(val[7]))
        self.Count.setValue(val[8])


    def first(self):
        db = sqlite3.connect("parts_database.db")
        cursor = db.cursor()

        command = '''SELECT * from parts_table'''
        result = cursor.execute(command)
        val = result.fetchone()

        self.id.setText(str(val[0]))
        self.Reference.setText(str(val[1]))
        self.Part_Name.setText(str(val[2]))
        self.Min_Area.setText(str(val[3]))
        self.Max_Area.setText(str(val[4]))
        self.Number_of_holes.setText(str(val[5]))
        self.Min_diameter.setText(str(val[6]))
        self.Max_diameter.setText(str(val[7]))
        self.Count.setValue(val[8])

    def last(self):
        db = sqlite3.connect("parts_database.db")
        cursor = db.cursor()

        command = '''SELECT * from parts_table WHERE ID=(SELECT MAX(ID) from parts_table) '''
        result = cursor.execute(command)
        val = result.fetchone()

        self.id.setText(str(val[0]))
        self.Reference.setText(str(val[1]))
        self.Part_Name.setText(str(val[2]))
        self.Min_Area.setText(str(val[3]))
        self.Max_Area.setText(str(val[4]))
        self.Number_of_holes.setText(str(val[5]))
        self.Min_diameter.setText(str(val[6]))
        self.Max_diameter.setText(str(val[7]))
        self.Count.setValue(val[8])


def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
