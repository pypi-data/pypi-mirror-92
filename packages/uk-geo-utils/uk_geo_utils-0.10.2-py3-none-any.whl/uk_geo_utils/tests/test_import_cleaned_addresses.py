import os
from io import StringIO
from django.test import TestCase
from uk_geo_utils.models import Address
from uk_geo_utils.management.commands.import_cleaned_addresses import Command


class CleanedAddressImportTest(TestCase):
    def test_import_cleaned_addresses_valid(self):
        # check table is empty before we start
        self.assertEqual(0, Address.objects.count())

        # path to file we're going to import
        csv_path = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "../fixtures/cleaned_addresses",
            )
        )

        cmd = Command()

        # supress output
        cmd.stdout = StringIO()

        # import data
        opts = {"cleaned_ab_path": csv_path, "transaction": False}
        cmd.handle(**opts)

        # ensure all our tasty data has been imported
        self.assertEqual(4, Address.objects.count())

    def test_import_cleaned_addresses_file_not_found(self):
        csv_path = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "../fixtures/pathdoesnotexist",
            )
        )

        cmd = Command()

        # supress output
        cmd.stdout = StringIO()

        opts = {"cleaned_ab_path": csv_path, "transaction": False}
        with self.assertRaises(FileNotFoundError):
            cmd.handle(**opts)
