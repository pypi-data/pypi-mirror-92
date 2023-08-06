from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum
from threedi_cmd_statistics.validators.dates import validate_dates, validate_year
from threedi_cmd_statistics.validators import ValidationError


@dataclass
class OptionsValidator:
    month: Optional[Enum]
    year: Optional[str]
    dates: Optional[List[datetime]]
    user_filter: Optional[str]
    organisation_filter: Optional[str]

    def validate(self) -> None:
        """
        :raises ValidationError if the input data is invalid
        """
        if self.year:
            validate_year(self.year)
        if all((self.dates, any((self.year, self.month)))):
            raise ValidationError("Either use year/month or date")

        if self.dates:
            validate_dates(self.dates)
