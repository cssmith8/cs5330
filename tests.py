from database import Database
from classes import *

def tests(db: Database) -> None:
    db.create_tables()
    db.clear_tables()
    
    d1: Degree = Degree("Computer Science", "BS")
    db.insert_degree(d1)

    d2: Degree = db.get_degree("Computer Science", "BS")

    assert d2 != None, "Failed: Degree is None."
    assert d1 == d2, "Failed: Degrees do not match."