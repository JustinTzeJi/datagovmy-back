import environ
from django.core.management.base import BaseCommand

from data_gov_my.catalog_utils import catalog_builder
from data_gov_my.utils import cron_utils
from data_gov_my.utils.DataBuilder import GeneralDataBuilder


env = environ.Env()
environ.Env.read_env()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "operation", nargs="+", type=str, help="States what the operation should be"
        )

    def handle(self, *args, **kwargs):
        category = kwargs["operation"][0]
        operation = kwargs["operation"][1]
        command = operation

        if len(kwargs["operation"]) > 2:
            files = kwargs["operation"][2]
            command = operation + " " + files
            files = files.split(",")
        else:
            files = []

        rebuild = operation == "REBUILD"

        """
        CATEGORIES :
        1. DATA_CATALOG
        2. DASHBOARD

        OPERATIONS :
        1. UPDATE
            - Updates the db, by updating values of pre-existing records

        2. REBUILD
            - Rebuilds the db, by clearing existing values, and inputting new ones

        SAMPLE COMMAND :
        - python manage.py loader DATA_CATALOG REBUILD
        - python manage.py loader DASHBOARDS UPDATE meta_1,meta_2
        """
        if category in [
            "DATA_CATALOG",
            "DASHBOARDS",
            "I18N",
            "FORMS",
        ] and operation in [
            "UPDATE",
            "REBUILD",
        ]:
            # Delete all file src
            # os.remove("repo.zip")
            # shutil.rmtree("DATAGOVMY_SRC/")
            cron_utils.remove_src_folders()
            if category == "DATA_CATALOG":
                catalog_builder.catalog_operation(command, "MANUAL")

            GeneralDataBuilder.build_operation_by_category(
                manual=True, category=category, rebuild=rebuild, meta_files=files
            )
