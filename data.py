from database import Database
from classes import *

class Data:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Data, cls).__new__(cls)
            cls._instance.db = None
            cls._instance.selectedDegree = None
        return cls._instance

    def set_db(self, db: Database) -> None:
        self.db = db

    def get_db(self) -> Database:
        return self.db

    def set_selected_degree(self, degree: Degree) -> None:
        self.selectedDegree = degree

    def get_selected_degree(self) -> Degree:
        return self.selectedDegree
