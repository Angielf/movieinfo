from django.db import models
from datetime import date


class Category(models.Model):
    name = models.CharField("Category", max_length=150)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Actor(models.Model):
    """Actors and Directors"""
    name = models.CharField("Name", max_length=100)
    age = models.PositiveSmallIntegerField("Age", default=0)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="actors/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Actors and Directors"
        verbose_name_plural = "Actors and Directors"


class Genre(models.Model):
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Movie(models.Model):
    title = models.CharField("Title", max_length=100)
    tagline = models.CharField("Tagline", max_length=100, default="")
    description = models.TextField("Description")
    poster = models.ImageField("Poster", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Release Year", default=2019)
    country = models.CharField("Country", max_length=30)
    directors = models.ManyToManyField(Actor,
                                       verbose_name="Director",
                                       related_name="film_director")
    actors = models.ManyToManyField(Actor,
                                    verbose_name="Actors",
                                    related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="Genres")
    world_premiere = models.DateField("In Theaters", default=date.today)
    budget = models.PositiveIntegerField("Budget", default=0, help_text="Sum in dollars")
    fees_in_usa = models.PositiveIntegerField("Gross USA", default=0, help_text="Sum in dollars")
    fees_in_world = models.PositiveIntegerField("Worldwide Gross", default=0, help_text="Sum in dollars")
    category = models.ForeignKey(Category,
                                 verbose_name="Category",
                                 on_delete=models.SET_NULL,
                                 null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField("Draft", default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"


class MovieShots(models.Model):
    title = models.CharField("Title", max_length=100)
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie,
                              verbose_name="Film",
                              # when you delete a movie all related images will also be deleted
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Movie Image"
        verbose_name_plural = "Movie Images"


class RatingStar(models.Model):
    value = models.SmallIntegerField("Value", default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Rating Star"
        verbose_name_plural = "Rating Stars"


class Rating(models.Model):
    ip = models.CharField("IP", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Star")
    movie = models.ForeignKey(Movie, on_delete=models.CharField, verbose_name="Movie")

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField("Name", max_length=100)
    text = models.TextField("Text", max_length=5000)
    parent = models.ForeignKey('self',  # the record will refer to the record in the same table
                               verbose_name="Parent",
                               on_delete=models.SET_NULL,
                               blank=True,  # optional field
                               null=True)
    movie = models.ForeignKey(Movie, verbose_name="Movie", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
