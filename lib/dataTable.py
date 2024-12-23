import inflect
from snipeInstance import *

class dataTable:
    def __init__(self, db, table_name):
        self.db = db
        self.table_name = table_name
        self.search_key = None
        self.search_key_index = -1
        self.inflector = inflect.engine()
        self.records = []
        self.relations = {}
        self.column_names = []
        self.column_info = []
        self.discover()
        self.debug = 0

    def info(self):
        print()
        print("Table: {}".format(self.get_table_name()))

        print(" Relations:")
        for relation in self.relations:
            print("  {:20}: {}".format(relation, self.relations[relation].get_table_name()))

    def get_table_name(self):
        return self.db.config["database"] + "." + self.table_name

    def set_search_key(self, key):
        if key in self.column_names:
            self.search_key = key
            self.search_key_index = self.column_names.index(key)

    def add_relation(self, field_name, table_name):
        if not field_name in self.relations:
            # print("Adding relation '{}' from '{}'".format(field_name, self.table_name))
            self.relations[field_name] = self.db[table_name]

    def add_extra_relations(self):
        pass

    def is_relation(self, field_name):
        return field_name in self.relations

    def discover(self):
        if not self.db.has_table(self.table_name):
            raise Exception("No table called '{}' found in {}".format(self.table_name, self.db.config['database']))

        self.column_names = []
        self.column_info = {}
        rst = self.db.describe_table(self.table_name)
        for row in rst:
            key = row["Field"]
            self.column_names += [key,]
            self.column_info[key] = row
            # print(key)

    def discover_relations(self):
        # print("\nDiscovering relations for '{}.{}'".format(self.db.config['database'], self.table_name))
        self.add_extra_relations()

        for column in self.column_names:
            # print("..", column)
            if column.endswith("_id"):
                name = column[:-3]

                # The relation may already have been setup by the 'add_extra_relations()' function
                if not column in self.relations:
                    table_name = self.inflector.plural(name)
                    # print("Table name:", table_name)
                    if self.db.has_table(table_name):
                        self.add_relation(column, table_name)
                    else:
                        print("Can't figure out relation '{}' in table '{}'".format(name, self.table_name))


    def read_all(self, debug=False):
        if self.debug or debug:
            print("read_all() called on {}".format(self.get_table_name()))

        rst = self.db.query("SELECT * FROM {}".format(self.table_name))

        if self.debug or debug:
            rst.dump()

        return rst

    def find(self, value, search_field=None, columns="*"):
        if search_field == None:
            search_field = self.search_key

        if isinstance(columns, list):
            columns = ",".join(columns)
            
        if self.debug:
            print("find({}, '{}', {}) called on table {}".format(value, search_field, columns, self.get_table_name()))
            
        sql = "SELECT {} FROM {} WHERE {}='{}'".format(
            columns, self.table_name, search_field, value)

        rst = self.db.query(sql)

        if self.debug:
            print("# records returned:", rst.record_count)

        return rst

    def find_single(self, value, search_field=None, columns="*"):
        rst = self.find(value, search_field, columns)
        num_records = rst.record_count
        
        if num_records > 1 or num_records < 0:
            raise Exception("Unexpected count - should have been 0 or 1")

        return rst

    def record_exists(self, value, search_field=None):
        rst = self.find_single(value, search_field=None, columns=["id",])

        return rst.record_count != 0

    def create(self, columns):
        if self.debug:
            print("Create:", columns)

        values = []
        placeholders = []
        cols = []
        for col in columns:
            val = columns[col]

            if val != None:
                # print(col, "->", val)

                placeholders += ["%s",]
                values += [val,]
                cols += [col,]

        sql = "INSERT INTO {} ({}) VALUES({})".format(
            self.table_name,
            ", ".join(cols),
            ", ".join(placeholders)
        )

        if self.debug:
            print("SQL:", sql)
            
        new_id = self.db.insert(sql, values)
        # print("New id=", new_id)

        return new_id
