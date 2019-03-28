import csv

from django.core.management.base import BaseCommand
from django.db import transaction

from candidates.models import PersonRedirect
from people.models import PersonIdentifier, Person


class Command(BaseCommand):
    help = (
        "Expects a two column CSV with the YNR ID as the first column "
        "and the identifier to add as the second. There must be no column"
        "headings in the CSV. This commands assumes a single ID of each type"
        "and will overwrite IDs if there are duplicate for a person."
    )

    def add_arguments(self, parser):
        parser.add_argument("--file", action="store", required=True)
        parser.add_argument("--id-type", action="store", required=True)
        parser.add_argument("--replace", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options):
        id_types = [
            x[0] for x in PersonIdentifier.objects.select_choices() if x[0]
        ]
        if options["id_type"] not in id_types:
            raise ValueError(
                "{} isn't a valid ID type. Options are {}".format(
                    options["id_type"], ", ".join(id_types)
                )
            )

        in_file = csv.reader(open(options["file"]))
        for line in in_file:
            person_id = line[0]
            person_qs = Person.objects.filter(id=person_id)
            if not person_qs.exists():
                redirect_qs = PersonRedirect.objects.filter(
                    old_person_id=person_id
                )
                if redirect_qs.exists():
                    person_id = redirect_qs.get().new_person_id
                else:
                    continue

            exists = False
            try:
                pi = PersonIdentifier.objects.get(
                    person_id=person_id, value_type=options["id_type"]
                )
                exists = True
            except PersonIdentifier.DoesNotExist:
                pi = PersonIdentifier(
                    person_id=person_id, value_type=options["id_type"]
                )

            if not exists or exists and options["replace"]:
                pi.value = line[1]
                pi.save()