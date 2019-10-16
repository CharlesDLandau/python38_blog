from typing import TypedDict

class Movie(TypedDict):
    name: str
    year: int
        
# Cannonical assignment of Movie
movie: Movie = {'name': 'Wally 2: Rise of the Garbage Bots', 'year': 2055}