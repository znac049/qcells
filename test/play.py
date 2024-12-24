#!/usr/bin/env python3

import sys
sys.path.insert(0, '../lib')

import inspect
import dataclasses
from dataclasses import dataclass, field

from coreSQL import *

@dataclass
class UserRecord():
    name: str
    email: str
    id: int = 0 #field(repr=False, default=0)

db = coreSQL(database='bob', user='bob', password='fishfac3')
print(db.tables)

bob = UserRecord(name="bob", email="bob@chippers.org.uk")
print(dataclasses.fields(bob))