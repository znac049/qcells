#!/usr/bin/env python3

import sys
sys.path.insert(0, '../lib')

import inspect
import dataclasses

from configparser import ConfigParser
from dataclasses import dataclass, field

from coreSQL import *

@dataclass
class UserRecord():
    name: str
    email: str
    id: int = 0 #field(repr=False, default=0)


parser = ConfigParser()
found = parser.read("../qcells.cfg")

if not parser.has_section("mysql"):
    print("No target section present")
    exit(42)

for option in ["host", "user", "password", "database"]:
    if not parser.has_option("mysql", option):
        raise Exception("mysql is missing some items")

db = coreSQL(
    database=parser.get("mysql", "database"), 
    user=parser.get("mysql", "user"), 
    password=parser.get("mysql", "password"),
    host=parser.get("mysql", "host") 
    )

print(db.tables)

bob = UserRecord(name="bob", email="bob@chippers.org.uk")
# print(dataclasses.fields(bob))

db.create_table("fred", UserRecord)
db.create_table("fred", bob)
