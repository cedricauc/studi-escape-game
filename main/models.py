from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

ROLES = [
    (0, "Admin"),
    (1, "Employee"),
    (2, "Client"),
]


class User(AbstractUser):
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    email = models.EmailField('email address', unique=True)
    role = models.IntegerField(choices=ROLES, null=True, blank=True)

    @property
    def full_name(self):
        "Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        db_table = "user"


class Level(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "level"


class Image(models.Model):
    title = models.CharField(max_length=255)
    alt = models.CharField(max_length=255)
    img = models.ImageField(upload_to='img', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "image"


class Room(models.Model):
    num = models.CharField(max_length=255)

    def __str__(self):
        return self.num

    class Meta:
        db_table = "room"


class Scenario(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    min_participant = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    max_participant = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    price_participant = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    slug = models.SlugField(null=True)
    level = models.ForeignKey(
        Level,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="scenarios",
    )
    images = models.ManyToManyField(Image, blank=True)
    rooms = models.ManyToManyField(Room, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def clean(self):
        if self.max_participant < self.min_participant:
            raise ValidationError("The max number of participants must be greater than the min number of participants")

    class Meta:
        db_table = "scenario"


class Game(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name="games")

    def __str__(self):
        return f"{self.start_time} : {self.end_time}"

    class Meta:
        db_table = "game"


class Cart(models.Model):
    participant = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    created_date = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True,
                             )

    def __str__(self):
        return f"{self.id} : {self.created_date}"

    class Meta:
        db_table = "cart"


class Booking(models.Model):
    booking_number = models.CharField(max_length=255)
    participant = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    created_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.IntegerField()
    is_canceled = models.BooleanField(default=False)
    in_progress = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    start_hour = models.IntegerField(blank=True, null=True)
    start_minutes = models.IntegerField(blank=True, null=True)
    end_hour = models.IntegerField(blank=True, null=True)
    end_minutes = models.IntegerField(blank=True, null=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="booking")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.booking_number

    class Meta:
        db_table = "booking"


class Discount(models.Model):
    step = models.IntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_percentage = models.BooleanField(default=False)
    scenarios = models.ManyToManyField(Scenario, blank=True)

    def __str__(self):
        return f"{self.id} : {self.discount}"

    class Meta:
        db_table = "discount"


class ScenarioRoomClue(models.Model):
    clue = models.TextField()
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} : {self.scenario.title} - {self.room.num}"

    class Meta:
        db_table = "clue"


class TicketCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "ticket_category"
        verbose_name_plural = "Ticket Categories"


class TicketQuestion(models.Model):
    author = models.CharField(max_length=255)
    question = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(TicketCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id} : {self.category.title}"

    class Meta:
        db_table = "ticket_question"


class TicketAnswer(models.Model):
    answer = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(TicketQuestion, on_delete=models.CASCADE, related_name="ticket_answer")

    def __str__(self):
        return f"{self.id} : {self.question.category.title}"

    class Meta:
        db_table = "ticket_answer"
