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

    def write_data(self):
        _, extension = os.path.splitext(self.output_file_name)
        if extension == ".csv":
            with open(self.output_file_name, "w", newline="") as output_file:
                file_writer = csv.writer(output_file)
                for row in self.input_file_data:
                    file_writer.writerow(row)
        elif extension == ".json":
            with open(self.output_file_name, "w") as output_file:
                json.dump(self.input_file_data, output_file, indent=4)
        elif extension == ".txt":
            with open(self.output_file_name, "w") as output_file:
                for row in self.input_file_data:
                    output_file.write(".".join(row) + "\n")
        elif extension == ".pickle":
            with open(self.output_file_name, "wb") as output_file:
                pickle.dump(self.input_file_data, output_file):
        else:
            print("Unsupported file extension.")
            sys.exit(1)

    def process_changes(self):
        if not os.path.exists(self.input_file_name):
            print(f"Error. File {self.input_file_name} not found.")
            sys.exit(1)
        self.read_input_file()
        for change_number, requested_change in enumerate(self.changes):
            column, row, value = requested_change.split(",")
            try:
                int(column)
                int(row)
            except ValueError:
                print(f"WARNING! An incorrect data has been detected for change number: \"{change_number}\".")
                print(f"Check if expected column and row exist in input file. \nStep skipped")
                continue
        self.edit_data()
        self.write_data()

class Reader(MainProcess):
    def __init__(self, input_file_name, output_file_name, *changes):
        super().__init__(input_file_name, output_file_name)
        self.changes = changes

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("FATAL ERROR\n NOT ENOUGH DATA")
    else:
        input_file_name = sys.argv[1]
        output_file_name = sys.argv[2]
        changes = sys.argv[3:]
        reader = Reader(input_file_name, output_file_name, *changes)
        reader.process_changes()