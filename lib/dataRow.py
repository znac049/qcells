class dataRow:
    def __init__(self, columns, data):
        row = {}
        i = 0
        for  idx in columns:
            row[idx] = data[i]
            i += 1

        self.row = row

    def __getitem__(self, key):
        if key in self.row:
            return self.row[key]

        return None

    def __repr__(self):
        result = "dataRow: "
        num_cols = len(self.row)
        print_cols = min(num_cols, 6)

        items = []
        for col in self.row:
            if print_cols > 0:
                items += ["'{}': '{}'".format(col, self.row[col]),]

            print_cols = print_cols - 1

        result += ", ".join(items)
        if num_cols >= 6:
            result += ", ..."

        return result

    def as_string(self):
        result = "dataRow: "
        num_cols = len(self.row)

        items = []
        for col in self.row:
            items += ["'{}': '{}'".format(col, self.row[col]),]

        result += ", ".join(items)

        return result

    def keys(self):
        return self.row.keys()
