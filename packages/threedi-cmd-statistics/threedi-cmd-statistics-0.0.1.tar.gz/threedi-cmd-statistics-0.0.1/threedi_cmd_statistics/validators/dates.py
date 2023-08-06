from datetime import datetime
from typing import List
import re

from threedi_cmd_statistics.validators import ValidationError


def validate_year(input_year: str) -> None:
    """
    :raises ValidationError if the input_year is not of format
        2yyy or the year lays in the future
    """
    pattern = r"(2)(\d){3}"
    m = re.fullmatch(pattern, input_year)
    if not m:
        raise ValidationError("Invalid year input, must be <2yyy>")
    if int(input_year) > datetime.utcnow().year:
        raise ValidationError("Invalid year input, must not be in the future")


def validate_dates(dates: List[datetime]) -> None:
    """
    :raises ValidationError if the list contains more than 2 values
        or the start_date (that is, the first date in the list) is after
        the end_date (that is, the second date in the list)
    """
    if len(dates) > 2:
        raise ValidationError(
            "At most two dates, e.g. <start date> <end date>"
        )
    try:
        start_date, end_date = dates
    except ValueError:
        return
    if start_date >= end_date:
        raise ValidationError(
            "The first date option must be before the second, e.g. <start date> <end date>"
        )
