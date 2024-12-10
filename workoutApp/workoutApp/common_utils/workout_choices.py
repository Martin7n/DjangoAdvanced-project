from django.db import models


class ExrxCategory(models.TextChoices):
    BASIC = "Basic", "Basic"
    AUXILIARY = "Auxiliary", "Auxiliary"
    ASSISTANCE = "Assistance", "Assistance"


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


class MealChoice(models.TextChoices):
    BREAKFAST = "Breakfast", "Breakfast"
    DINNER = "Dinner", "Dinner"
    LUNCH = "Lunch", "Lunch"
    OTHER = "Other", "Other"


class ComplexType(models.TextChoices):
    AMRAP = ("AMRAP", "AMRAP")
    DBY = ("Death By", "Death By")
    EMOM = ("EMOM", "EMOM")
    FT = ("For time", "For time")


class Load(models.TextChoices):
    BW = ("BW", "BW")
    HBW = ("Half BW", "Half BW")
    QU = (".75 BW", ".75 BW")
