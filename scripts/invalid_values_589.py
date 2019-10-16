from typing import TypedDict

class Movie(TypedDict):
    name: str
    year: int

def f(m: Movie):
    return m['year']

f({'year': 'wrong type', 'name': 12})