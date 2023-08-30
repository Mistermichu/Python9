import sys
import csv
import os
import json
import pickle


class MainProcess:
    def __init__(self, input_file_name, output_file_name):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.changes = []
        self.input_file_data = []

    def read_input_file(self):
        _, extension = os.path.splitext(self.input_file_name)
        if extension == ".csv":
            with open(self.input_file_name, "r") as input_file:
                file_reader = csv.reader(input_file)
                for row_data in file_reader:
                    self.input_file_data.append(row_data)
        elif extension == ".json":
            with open(self.input_file_name, "r") as input_file:
                self.input_file_data = json.load(input_file)
        elif extension == ".txt":
            with open(self.input_file_name, "r") as input_file:
                for line in input_file:
                    self.input_file_data.append(line.strip.split(","))
        elif extension == ".pickle":
            with open(self.input_file_name, "rb") as input_file:
                self.input_file_name = pickle.load(input_file)
        else:
            print("Unsupported file extension.")
            sys.exit(1)

    def edit_data(self):
        for new_value in self.changes:
            try:
                column, row, value = new_value.split(",")
                column, row = int(column), int(row)
                self.input_file_data[row][column] = value
            except IndexError:
                print(f"WARNING! An incorrect data has been detected: \"{new_value}\".")
                print(f"Check if expected column and row exist in input file. \nStep skipped")
                continue






input_file_data = []

def bad_input_data(value_type, argv_number):
    print(f"Argv number: {argv_number}. Value provided in argv for {value_type} is incorrect.")
    print("Try again.")

def read_file():
    with open(sys.argv[1], "r") as input_file:
        file_reader = csv.reader(input_file)
        for row_data in file_reader:
            input_file_data.append(row_data)

def edit_data():
    global changes, input_file_data, output_file_data
    for new_value in changes:
        try:
            column, row, value = new_value.split(",")
            column, row = int(column), int(row)
            input_file_data[row][column] = value
        except IndexError:
            print(f"WARNING! An incorrect data has been detected: \"{new_value}\".")
            print(f"Check if expected column and row exist in input file. \nStep skipped")
            continue
    output_file_data = input_file_data
    
def write_data():
    global output_file_data
    with open(sys.argv[2], "w", newline="") as output_file:
        file_writer = csv.writer(output_file)
        for new_row_value in output_file_data:
            file_writer.writerow(new_row_value)

def input_file():
    input_file_name = sys.argv[1]
    if os.path.exists(input_file_name):
        return True
    else:
        return False

def argv_check():
    if not input_file():
        print(f"File {sys.argv[1]} not found.")
        return False
    else:
        print("Input file detected.")
        changes = sys.argv[3:]
        for change_number, requested_change in enumerate(changes):
            if "," not in requested_change:
                print("Error. Wrong argv format.")
                return False
            column_row_value = requested_change.split(",")
            if len(column_row_value) != 3:
                print("Error. Wrong argv format.")
                return False
            column = column_row_value[0]
            row = column_row_value[1]
            new_value = column_row_value[2]
            try:
                int(column)
            except ValueError:
                bad_input_data("column", change_number + 3)
                return False
            try:
                int(row)
            except ValueError:
                bad_input_data("row", change_number + 3)
                return False
            print(f"Requested change {change_number + 1}. In column {column}, row {row}, new value: {new_value}")
        return True
    
#RUN APP
if len(sys.argv) < 4:
    print("FATAL ERROR")
    print("NOT ENOUGH DATA")
else:
    if not argv_check():
        pass
    else:
        output_file_name = sys.argv[2]
        read_file()
        changes = sys.argv[3:]
        edit_data()
        write_data()
