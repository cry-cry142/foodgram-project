from csv import DictReader
import os
from django.core.management import BaseCommand
from django.conf import settings

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        base = settings.BASE_DIR
        for row in DictReader(
            open(os.path.join(
                base, '..', 'data', 'ingredients.csv'), encoding="utf8"
            ),
            fieldnames=('name', 'unit')
        ):
            ingredient = Ingredient(
                name=row['name'], measurement_unit=row['unit']
            )
            ingredient.save()
