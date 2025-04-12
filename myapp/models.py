from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, age, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            age=age
        )
        user.set_password(password)  # Hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, age, password=None):
        user = self.create_user(
            email=email,
            name=name,
            age=age,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Password will be hashed
    age = models.IntegerField()
    # Many-to-Many relationship to Golfer
    #favorite_golfers = models.ManyToManyField("Golfer", related_name="fans", blank=True)
        # Many-to-Many relationship to Golfer with a custom intermediary table
    favorite_golfers = models.ManyToManyField(
        "Golfer", 
        related_name="fans", 
        blank=True,
        through="AllUsersFavoriteGolfers"
    )


    # User authentication-related fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # The following are necessary for Django's auth system
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'age']  # Fields required when creating superuser

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "all_users"



# class Golfer(models.Model):
#     name = models.CharField(max_length=100)
#     day_1_score = models.IntegerField()
#     day_2_score = models.IntegerField()
#     day_3_score = models.IntegerField()
#     day_4_score = models.IntegerField()
#     average_scores_dayoverday = models.FloatField(null=True, blank=True)
#     tier = models.IntegerField()

#     def __str__(self):
#         return self.name

#     # def calculate_average(self):
#     #     # Collect all the scores into a list
#     #     scores = [self.day_1_score, self.day_2_score, self.day_3_score, self.day_4_score]
        
#     #     # Filter out the None values and calculate the average
#     #     valid_scores = [score for score in scores if score is not None]
#     #     if valid_scores:
#     #         # If there are valid scores, calculate the average
#     #         return sum(valid_scores) / len(valid_scores)
#     #     else:
#     #         # If there are no valid scores, return None
#     #         return None

#     # def save(self, *args, **kwargs):
#     #     # Automatically calculate the average when saving the golfer
#     #     self.average_scores_dayoverday = self.calculate_average()
#     #     super().save(*args, **kwargs)

#     class Meta:
#         db_table = "all_golfers"
class Golfer(models.Model):
    name = models.CharField(max_length=100)
    day_1_score = models.IntegerField()
    day_2_score = models.IntegerField()
    day_3_score = models.IntegerField()
    day_4_score = models.IntegerField()
    average_scores_dayoverday = models.FloatField(null=True, blank=True)
    tier = models.IntegerField()

    def __str__(self):
        return self.name

    def calculate_average_over_par(self):
        # Assuming par is 72 for each round
        par = 72

        # Get the scores for each day
        scores = [self.day_1_score, self.day_2_score, self.day_3_score, self.day_4_score]

        # Calculate over par for each score
        over_par_scores = [score - par for score in scores if score is not None]

        # Calculate the average over par
        if over_par_scores:
            return sum(over_par_scores) / len(over_par_scores)
        else:
            return None

    class Meta:
        db_table = "all_golfers"
#added
class AllUsersFavoriteGolfers(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # Linking to User
    golfer = models.ForeignKey('Golfer', on_delete=models.CASCADE)  # Linking to Golfer

    class Meta:
        db_table = 'all_users_favorite_golfers'  # Specify table name if needed


class UserAverage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    overall_avg_over_par = models.FloatField(null=True, blank=True)

    # def __str__(self):
    #     return f"{self.user.username} - {self.overall_avg_over_par}"
    class Meta:
        managed = False  # tells Django not to create/migrate this table
        db_table = 'useraverage'  # this must match your MariaDB table name exactly