from coreSQL import *

from snipeCategories import *
from snipeCompanies import *
from snipeLocations import *
from snipeManufacturers import *
from snipeStatusLabels import *

class snipeSQL(coreSQL):
    def __init__(self, config):
        super(snipeSQL, self).__init__(config)
        self.table_objects = {}

    def __getitem__(self, key):
        # print("Get reference to '{}' table. Known tables:".format(key), self.table_objects)
        if key in self.table_objects:
            return self.table_objects[key]

        return None

    def __setitem__(self, key, val):
        # print("Adding table '{}' ('{}')".format(key, val.table_name))
        self.table_objects[key] = val

    def discover_relations(self):
        for table in self.table_objects:
            self.table_objects[table].discover_relations()
