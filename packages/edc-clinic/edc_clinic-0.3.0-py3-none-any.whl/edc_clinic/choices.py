from edc_constants.constants import NEVER, NOT_APPLICABLE
from edc_reportable import (
    MICROMOLES_PER_LITER,
    MICROMOLES_PER_LITER_DISPLAY,
    MILLIGRAMS_PER_DECILITER,
    MILLIMOLES_PER_LITER,
    MILLIMOLES_PER_LITER_DISPLAY,
)

GLUCOSE_UNITS = (
    (MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_DECILITER),
    (MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER_DISPLAY),
)

GLUCOSE_UNITS_NA = (
    (MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_DECILITER),
    (MILLIMOLES_PER_LITER, MILLIMOLES_PER_LITER_DISPLAY),
    (NOT_APPLICABLE, "Not applicable"),
)
SERUM_CREATININE_UNITS = (
    (MILLIGRAMS_PER_DECILITER, MILLIGRAMS_PER_DECILITER),
    (MICROMOLES_PER_LITER, MICROMOLES_PER_LITER_DISPLAY),
)


MISSED_PILLS = (
    ("today", "today"),
    ("yesterday", "yesterday"),
    ("earlier_this_week", "earlier this week"),
    ("last_week", "last week"),
    ("lt_month_ago", "less than a month ago"),
    ("gt_month_ago", "more than a month ago"),
    (NEVER, "have never missed taking my study pills"),
)
