from database import Database
from classes import *

def tests(db: Database) -> None:
    print("Running tests...")
    db.create_tables()
    db.clear_tables()
    
    d1: Degree = Degree("Computer Science", "BS")
    db.insert_degree(d1)

    d2: Degree = db.get_degree("Computer Science", "BS")

    assert d2 != None, "Failed: Did not get degree from table."
    # assert d1 == d2, "Failed: Degrees do not match."

    # Test for Foreign Key Constraint Integrity
    c1: Course = Course("cs5330", "Databases")
    db.insert_course(c1)
    print("\n")

    s1: Section = Section("101", "cs5330", "Spring", "2024", "60", "5678")
    print("Exception \"Error inserting section\" should print to console: ")
    assert not db.insert_section(s1), "Failed: Section inserted despite violating foreign key constraints."
    print("\n")

    i1: Instructor = Instructor("5678", "Dr. Lin")
    db.insert_instructor(i1)
    db.insert_section(s1)
    assert db.get_section("101", "cs5330", "Spring", "2024"), "Failed: Expected insert section to now succeed."


    
