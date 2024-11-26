from django.db import models

class DayOfWeek(models.TextChoices):
    MONDAY = 'Monday', 'Monday'
    TUESDAY = 'Tuesday', 'Tuesday'
    WEDNESDAY = 'Wednesday', 'Wednesday'
    THURSDAY = 'Thursday', 'Thursday'
    FRIDAY = 'Friday', 'Friday'
    SATURDAY = 'Saturday', 'Saturday'
    SUNDAY = 'Sunday', 'Sunday'

# Not used as the category and type will be user added
class ExrxCategory(models.TextChoices):
    BASIC = "Basic", "Basic"
    AUXILIARY = "Auxiliary", "Auxiliary"
    ASSISTANCE = "Assistance", "Assistance"
#
class ExrxType(models.TextChoices):

    PUSH = "Push", "Push"
    PULL = "Pull", "Pull"
    LOWER = "Legs", "Legs"
    OTHER = "Other", "Other"


class WorkoutType(models.TextChoices):

    PUSH = "Push", "Push"
    PULL = "Pull", "Pull"
    LEGS = "Legs", "Legs"
    TBT = "TBT", "TBT"
    OTHER = "Other", "Other"


class GoodDayChoice(models.TextChoices):
    EXCELLENT = "Excellent", "Excellent"
    ABOVE = "Above expectations", "Above expectations"
    AVERAGE = "Average", "Average"
    NOTBAD = "Not bad, not terrible", "Not bad, not terrible"
    BAD = "There will be a better days", "There will be a better days"


class IngredientsChoice(models.TextChoices):
    CHICKEN = 'Chicken', 'Chicken'
    BEAF = 'Beaf', 'Beaf'
    PIG = 'Pig', 'Pig'
    FISH = 'Fish', "Fish"
    EGGS = 'Eggs', "Eggs"
    POTATOES = 'Potatoes', "Potatoes"
    BREAD = "Bread", "Bread"
    RICE = "Rice", "Rice"


class MealChoice(models.TextChoices):
    BREAKFAST = "Breakfast", "Breakfast"
    DINNER = "Dinner", "Dinner"
    LUNCH = "Lunch", "Lunch"
    OTHER = "Other", "Other"


