from dataRow import *

class recordSet:
    def __init__(self, cursor):
        self.rows = []
        self.record_number = -1
        self.record_count = 0

        columns = []
        for column in cursor.description:
            columns += [column[0],]

        self.columns = columns
        self.number_of_columns = len(columns)

        for row in cursor:
            self.rows += [dataRow(columns, row),]
            self.record_count += 1
        cursor.close()

    def __iter__(self):
        self.record_number = -1
        return self

    def __next__(self):
        self.record_number += 1
        if self.record_number >= self.record_count:
            raise StopIteration

        return self.rows[self.record_number]

    def __getitem__(self, key):
        if key >= 0 and key < self.record_count:
            return self.rows[key]

        return None

    def dump(self):
        print("Number of records:", self.record_count)
        for row in self.rows:
            print("  ", row)
        
    def rewind(self):
        self.record_number = -1

    def indexOf(self, column_name):
        if column_name in self.columns:
            return self.columns.index(column_name)

        return None

    def nameOf(self, column_index):
        if 0 <= column_index and column_index < self.number_of_columns:
            return self.columns[column_index]

        return None
    