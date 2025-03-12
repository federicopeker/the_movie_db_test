from app.models.movie import Movie


def test_create_movie():
    movie = Movie(id=132, title="The Gorge", release_date="2025-02-13", rating=0)
    assert movie.id == 132
    assert movie.title == "The Gorge"
    assert movie.release_date == "2025-02-13"
