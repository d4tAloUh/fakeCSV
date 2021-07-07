import csv
import random

from planeks.celery import app
from fakeCSV.models import Schema, DataSet, Column
from django.conf import settings
import uuid
import faker

fake = faker.Faker()


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


@app.task
def task_generate_data(schema_id, row_nums):
    schema = Schema.objects.get(id=schema_id)
    schema_columns = Column.objects.filter(schema_id=schema_id).order_by('column_order')
    dataset = DataSet.objects.create(schema=schema)

    file_name = f"{settings.MEDIA_ROOT}Schema_{schema.schema_name}_{schema_id}.csv"

    with open(file_name, 'w', newline='') as file:
        csv_writer = csv.writer(file, delimeter=schema.column_separator, quotechar=schema.string_character)
        for _ in range(row_nums):
            row = generate_row(schema_columns)
            csv_writer.writerow(row)

    dataset.file_path = file_name
    dataset.save(update_fields='file_path')
