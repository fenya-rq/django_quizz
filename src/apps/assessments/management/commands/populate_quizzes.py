import csv

from django.core.management.base import BaseCommand, CommandError
from apps.assessments.models import Quizz, Question


class Command(BaseCommand):
    help = 'Fill quizzes with questions from a given CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        file_path = options['csv_file']
        created_quizzes = 0
        created_questions = 0

        try:
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:

                    # Checking required fields
                    try:
                        quizz_name = row['quizz_name'].strip()
                        item = row['item'].strip()
                        item_type = row['item_type'].strip()
                        correct_answer = row['correct_answer'].strip()
                    except KeyError as e:
                        raise CommandError(f"Missing column in CSV: {e}")

                    # Get or create a Quizz
                    quizz, created = Quizz.objects.get_or_create(name=quizz_name)
                    if created:
                        created_quizzes += 1

                    # Create a question
                    Question.objects.create(
                        quizz=quizz,
                        item=item,
                        item_type=item_type,
                        correct_answer=correct_answer
                    )
                    created_questions += 1

        except FileNotFoundError:
            raise CommandError(f'File not found: {file_path}')
        except Exception as e:
            raise CommandError(f'Error processing file: {e}')

        self.stdout.write(self.style.SUCCESS(
            f'Imported {created_questions} questions. '
            f'{created_quizzes} new quizzes created.'
        ))
