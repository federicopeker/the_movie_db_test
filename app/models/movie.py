class Movie:
    """Represents a Movie object."""

    def __init__(self, id: int, title: str, release_date: str, rating):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.rating = rating

    def to_dict(self):
        """Returns a dictionary representation of the movie."""
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "rating": self.rating,
        }
