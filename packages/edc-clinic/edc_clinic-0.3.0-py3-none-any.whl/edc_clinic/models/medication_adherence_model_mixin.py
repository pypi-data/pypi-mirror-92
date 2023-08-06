from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from edc_model import models as edc_models

from ..constants import MISSED_PILLS


class MedicationAdherenceModelMixin(models.Model):

    visual_score_slider = models.CharField(
        verbose_name="Visual score", max_length=3, help_text="%"
    )

    visual_score_confirmed = models.IntegerField(
        verbose_name=mark_safe(
            "<B><font color='orange'>Interviewer</font></B>: "
            "please confirm the score indicated from above."
        ),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="%",
    )

    last_missed_pill = models.CharField(
        verbose_name="When was the last time you missed your study pill?",
        max_length=25,
        choices=MISSED_PILLS,
    )

    pill_count = models.IntegerField(verbose_name="Number of pills left in the bottle")

    missed_pill_reason = models.ManyToManyField(
        f"{settings.LIST_MODEL_APP_LABEL}.NonAdherenceReasons",
        verbose_name="Reasons for missing study pills",
        blank=True,
    )

    other_missed_pill_reason = edc_models.OtherCharField()

    class Meta:
        abstract = True
        verbose_name = "Medication Adherence"
        verbose_name_plural = "Medication Adherence"
