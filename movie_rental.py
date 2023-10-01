from typing import List, Dict, Tuple
from enum import Enum
from datetime import datetime, timedelta

class RentStatus(int, Enum):
    AVAILABLE = 0
    RENTED = 1

class Movie:
    def __init__(self, _id: int) -> None:
        # other attributes may be added like, director, genre etc
        self._id = _id

    def __repr__(self) -> str:
        return f"Movie {self._id}"

class Store:
    def __init__(self, _id: int,) -> None:
        self._id = _id

    def __repr__(self) -> str:
        return f"Store {self._id}"

class MovieCopy:
    def __init__(self, _id: int, movie_id: int, store_id: int, price: float, ) -> None:
        self.is_available = True
        self._id = _id
        self.movie_id = movie_id
        self.store_id = store_id
        self.price= price

    def mark_movie_unavailable(self):
        self.is_available = False

    def mark_movie_available(self):
        self.is_available = True

    def __lt__(self, other):
        if self.price == other.price:
            return self.store._id < other.store._id
        return self.price < other.price 
    
    def __repr__(self) -> str:
        return f"MovieCopy of {self.movie_id} from store {self.store_id} with price {self.price}"


class Rental:
    def __init__(self, _id: Tuple, movie_copy_id: int,) -> None:
        self._id = _id
        self.movie_copy_id = movie_copy_id
        self.rented_at = datetime.now()
        self.status = RentStatus.RENTED
        self.rent = None
        self.returned_at = None

    def return_movie(self, movie_copy: MovieCopy):
        self.status = RentStatus.AVAILABLE
        from random import randint
        # Some random delay to simulate a rented time delay
        self.returned_at = datetime.now() + timedelta(randint(1, 10))
        self.fare = (self.returned_at - self.rented_at).days * movie_copy.price


    def mark_movie_available(self):
        self.status = RentStatus.AVAILABLE




class MovieRentalSystem:

    RESULT_SET_SIZE = 5

    def __init__(self) -> None:
        self._stores: Dict[int, Store] = {}
        self._rentals: Dict[Tuple, Rental] = {}
        self._movie_copies: Dict[int, MovieCopy] = {}

    def is_movie_rented(self, store_id, movie_id):
        key = (store_id, movie_id)
        if key not in self._rentals:
            return False
        return self._rentals[key].status == RentStatus.RENTED
    
    def _find_movie_in_store(self, store_id: int, movie_id: int):
        return next(
            (
                movie_copy
                for movie_copy in self._movie_copies.values()
                if movie_copy.store_id == store_id
                and movie_copy.movie_id == movie_id
            ),
            None,
        )

    def search(self, movie_id: str):
        # TODO: Consider heap here
        result = [
            movie_copy
            for movie_copy in self._movie_copies.values()
            if movie_copy.movie_id == movie_id and movie_copy.is_available
        ]
        return sorted(result, key=lambda movie_copy: movie_copy.price)[:self.RESULT_SET_SIZE]
    
    def rent_movie(self, store_id: int, movie_id: int):
        movie_copy = self._find_movie_in_store(store_id, movie_id)
        if not movie_copy:
            raise ValueError("Movie not available")
        if not movie_copy.is_available:
            raise ValueError("Movie already rented")
        key = (store_id, movie_id)
        rental = Rental(key, movie_copy._id)
        self._rentals[key] = rental
        movie_copy.mark_movie_unavailable()

    def return_movie(self, store_id, movie_id):
        movie_copy = self._find_movie_in_store(store_id, movie_id)
        if not movie_copy:
            raise ValueError("Invalid Input")
        if movie_copy.is_available:
            raise ValueError("Movie not rented")
        rental = self._rentals[(store_id, movie_id)]
        rental.return_movie(movie_copy)
        movie_copy.mark_movie_available()
        print(f"movie {movie_id} returned to store {store_id} successfully with rent is {rental.fare}")

    def add_movie_to_store(self, _id: int, movie_id: int, store_id: int, price: float):
        movie_copy = MovieCopy(_id, movie_id, store_id, price)
        self._movie_copies[movie_copy._id] = movie_copy

    def report(self, report_type: str):
        report = Report()
        return report.get_report_mapping(report_type)(report, self._movie_copies, self._rentals.values(), 5)

        
class Report:


    @classmethod
    def get_report_mapping(cls, report_type: str):
        REPORT_TYPES_TO_REPORT_MAPPING = {
            "cheap_movies": cls.cheapest_movie,
            "most_rented": cls.most_rented_movies,
        }
        return REPORT_TYPES_TO_REPORT_MAPPING[report_type]


    def _add_movies_from_rentals(self, movie_copies: Dict[int, MovieCopy], rentals: List[Rental]):
        movies = []
        for rental in rentals:
            movie_copy = movie_copies[rental.movie_copy_id]
            movies.append(movie_copy.movie_id)
        return movies

    def cheapest_movie(self, movie_copies: Dict[int, MovieCopy], rentals: List[Rental], _limit: int,):
        cheapest_rentals = sorted(rentals, key=lambda x: x.fare)[: _limit]
        print("cheapest movies", self._add_movies_from_rentals(movie_copies, cheapest_rentals))



    def most_rented_movies(self, movie_copies: Dict[int, MovieCopy], rentals: List[Rental], _limit: int,):
        movies_count = {}
        for rental in rentals:
            movie_id = movie_copies[rental.movie_copy_id].movie_id
            movies_count[movie_id] = movies_count.get(movie_id, 0) + 1
        most_rented_movies = sorted(movies_count, key=lambda x: movies_count[x], reverse=True)[:_limit]
        print("most rented movies", most_rented_movies)
        

def driver():
    store1 = Store(1)
    store2 = Store(2)
    store3 = Store(3)
    movie1 = Movie(1)
    movie2 = Movie(2)
    movie3 = Movie(3)
    movie5 = Movie(5)
    movie4 = Movie(4)

    rental_system = MovieRentalSystem()
    rental_system._stores = {store1._id: store1, store2._id: store2, store3._id: store3}
    rental_system.add_movie_to_store(1, movie1._id, store1._id, 10)
    rental_system.add_movie_to_store(2, movie1._id, store2._id, 15)
    rental_system.add_movie_to_store(3, movie1._id, store3._id, 12)
    rental_system.add_movie_to_store(4, movie2._id, store1._id, 20)
    rental_system.add_movie_to_store(5, movie2._id, store2._id, 40)
    rental_system.add_movie_to_store(6, movie3._id, store1._id, 30)
    rental_system.add_movie_to_store(7, movie4._id, store2._id, 25)
    rental_system.add_movie_to_store(8, movie5._id, store3._id, 35)

    # Test the search method
    print(rental_system.search(4))  
    print(rental_system.search(1)) 
    print(rental_system.search(2)) 

    # Test the rent_movie method
    rental_system.rent_movie(1, 2)
    rental_system.rent_movie(2, 4)
    rental_system.rent_movie(1, 1)  
    rental_system.rent_movie(2, 1)  


    # Test the return_movie method
    rental_system.return_movie(2, 4)
    rental_system.return_movie(1, 1)
    rental_system.return_movie(1, 2)
    rental_system.return_movie(2, 1)  


    # # Test the report method
    rental_system.report('cheap_movies')
    rental_system.report('most_rented')



if __name__ == '__main__':
    driver()