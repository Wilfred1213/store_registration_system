import datetime
from django.core.exceptions import ValidationError


def validate_date_is_past(date):
    if date >= datetime.date.today():
        raise ValidationError("La fecha no puede ser en el futuro.")
