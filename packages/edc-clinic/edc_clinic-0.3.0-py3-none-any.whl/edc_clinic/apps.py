from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = "edc_clinic"
    verbose_name = "Edc Clinic"
    has_exportable_data = False
    include_in_administration_section = False
