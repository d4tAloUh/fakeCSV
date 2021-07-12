import csv
import random
import faker
import os


from celery import shared_task
from fakeCSV.models import Schema, DataSet, Column
from django.conf import settings


fake = faker.Faker(['en_US'])


def generate_random_data_for_column(column):
    if column.column_type == 'EMAIL':
        return fake.ascii_email()
    elif column.column_type == 'FULL_NAME':
        return fake.name_nonbinary()
    elif column.column_type == 'PHONE_NUMBER':
        return fake.phone_number()
    elif column.column_type == 'TEXT':
        return fake.paragraph(nb_sentences=column.column_to)
    elif column.column_type == 'INTEGER':
        return random.randrange(column.column_from, column.column_to, 1)
    elif column.column_type == 'DATE':
        return fake.date()
    else:
        raise ValueError('Bad column type')


def generate_row(columns):
    row = []
    for column in columns:
        row.append(generate_random_data_for_column(column))
    return row


@shared_task(bind=True)
def task_generate_data(self, schema_id, row_nums):
    schema = Schema.objects.get(id=schema_id)
    schema_columns = Column.objects.filter(schema_id=schema_id).order_by('column_order')
    dataset = DataSet.objects.create(schema=schema, id=self.request.id)

    file_name = f"Schema_{schema.schema_name}_{dataset.id}.csv"
    file_path = f"{settings.MEDIA_ROOT}/{file_name}"
    schema_headers = list(schema_columns.values_list('column_name', flat=True))

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file, delimiter=schema.column_separator,
                                quotechar=schema.string_character)
        csv_writer.writerow(schema_headers)

        for i in range(int(row_nums)):
            row = generate_row(schema_columns)
            csv_writer.writerow(row)

    blob = settings.bucket.blob(file_name)
    blob.upload_from_filename(file_path)
    blob.make_public()

    if os.path.exists(file_path):
        os.remove(file_path)

    dataset.file_path = blob.public_url
    dataset.save(update_fields=['file_path'])

    return dataset.id
