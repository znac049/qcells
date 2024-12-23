#!/usr/bin/env python3

import sys
sys.path.insert(0, '../lib')

from dataclasses import dataclass, field

from coreSQL import *

@dataclass
class UserRecord():
    name: str
    email: str
    id: int = 0 #field(repr=False, default=0)

db = coreSQL({'host': "snowflake.aad.resillion.com", 'database': "bob", 'user': "bob", 'password': "beanbagz"})

bob = UserRecord(name="bob", email="bob@chippers.org.uk")
print(bob)