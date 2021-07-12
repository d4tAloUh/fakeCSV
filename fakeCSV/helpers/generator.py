import csv
import random
import faker
import os
import firebase_admin

from celery import shared_task
from fakeCSV.models import Schema, DataSet, Column
from firebase_admin import storage, credentials
from django.conf import settings

PRIVATE_KEY = os.environ.get("private_key",
                             "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDAH1XtzFd4ZCPX\nsrSl+/QOHEPbJ955ASjo0FOAl1St8l6GwlRyODrk3cxZRxN4RPKkJ5+nBw4TNPky\nsaSaHJnG6tgSqdgiVAG7vS+647Zp4tV1dDNgBySFOyguk1FFyK3/3gLmBwpRxb7H\nw70JN8Jw/NsgwBY0TCCkafVqBmDLLOuZEaHpBYMGbwEedA/RFCqdUxtzrExe0DMn\n4tpU1Zo9aX5nfoHHcDbNlI8WP0mShZSi1B3eV64jEBcKDJT17TYstLlmHnT2O3Wi\nr+TqpIvCRMDTWlukbwoBFVXcGe85NyMQXleOZ2zGUPGupmXW4IJw9fSnuHKBYryJ\nvLQgApjnAgMBAAECggEACMkGCrnhir74Mp4DNmSHPE6c6Gcc0by0rFy7t3F0F6uH\nGLNx3XKRIt5k60oy644qPZ5q5bOOuGB06sAGeQjzcTio88WHfXOzoUGdQ/cIuYkm\ns1htHFLcn9OyL9sLCDK33i+T7gUxZXGHmqaVPNgrZd5Hfj+6ZDQno/e3wgbo+Ia7\niVH+qKzFLYWA4/jsSwjL07VPlqPP5KPa3zurC01LczhtnZmEURqgK/RFtSyUcQyG\n5pPqu560m94thiwpEDUrjR30lPaA1E8dAHdMuI4IQleWOMwVXPJa9Wx5PXrHEWFB\nUTDo3HRV289byd7Rk4Wg1XjDb6g6KlRY14Mnd7DigQKBgQDkdZ4hhvFj45jmcgqa\nqjj43NZBOAj1pe4BiNWBqmr954dhmZzvDHO9hJ+Krj7Uzkmk+/Ig1NZpAlkZIejL\nlvqPhWo5075+NQwHZSWFzJ2dBBMQSsz6JAKycfUGt0JmWZ6XgS8KVeU6aGiAxZI0\nsreCP9A5lOjlir4sO1EKFBiMgQKBgQDXSFZUxi/PuWiDa0OT/kljZZXXi9v1HZ6Q\n3GlH9CaT64NOcnd4VqWhp66r3o8stw2ZIyzg2B8HFv6oOb8GD7KW981V/eMmQHxF\nX2nlB/OzIMk2D2yUK2EzzLyQLwUh7LWSgv4X3wK7fNO0BQDR0n33fAbqO+n51LM9\n7WiFAA2RZwKBgQDHGcYNHAhlcGXBd+PL9Muf/v3uasJMKyaoSbMgxP9ndg7jPTeq\nkWSQ5vMPrlltprZBxZy3hiWx8Gzr3UR/oX2N9MylxuZ+IQbxrvGrkK5Pt8xRZ48J\n9LYxA+Vxy+ZfQn1XNitjy4XxiCqDBywrJxGMvsZeWGs8GNUxwSQYL3lRgQKBgF2n\n457nxV8KGxSpMnIMuyKZzBFEkAFXzGba7JZX+fx6Bdq344+fqljkWRH+Na1PSYQo\nkFqUyxLLhyfqT1c0tw4EafkSBaLbhPStKKVxyyxPhBmXpjXjlVryo8naGtKCZw+B\nG0eJRmgISxVS4+NkPlbPRzbZr9V3Gi9DvCe4OS7bAoGAIoGHEtye+Q/4FHFKxDv5\n/xK0ltiQHSqnezP0MqRk83k1EeiPvYpM+umdpoe7eoMTYaVZd993gbl91I+jU9KZ\nBk7fg4modwh2zRIlnqrCCnVR4r6BhDw0Z9cPZf9iFZqEo8/FvJ1lx0WoANbHZo9b\npq5F3ONJzZtlBxwtmFU9cJA=\n-----END PRIVATE KEY-----\n").replace(
    '\\n', '\n')
PRIVATE_KEY_ID = os.environ.get("private_key_id", "32a7264e24815e99a33e14c2743dac11f4d9f1e4")
CLIENT_EMAIL = os.environ.get('client_email',
                              "firebase-adminsdk-9fo2f@planeks-test-4227a.iam.gserviceaccount.com")
CLIENT_ID = os.environ.get('client_id', "108400431971091242931")

print("Private key is", PRIVATE_KEY, type(PRIVATE_KEY))
print("Private key id is", PRIVATE_KEY_ID, type(PRIVATE_KEY_ID))

credential = credentials.Certificate({
    "type": "service_account",
    "project_id": "planeks-test-4227a",
    "private_key_id": PRIVATE_KEY_ID,
    "private_key": PRIVATE_KEY,
    "client_email": CLIENT_EMAIL,
    "client_id": CLIENT_ID,
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-9fo2f%40planeks-test-4227a.iam.gserviceaccount.com"
})

firebase_app = firebase_admin.initialize_app(credential, {
    'storageBucket': "planeks-test-4227a.appspot.com"
})

bucket = storage.bucket(app=firebase_app)

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

    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_path)
    blob.make_public()

    if os.path.exists(file_path):
        os.remove(file_path)

    dataset.file_path = blob.public_url
    dataset.save(update_fields=['file_path'])

    return dataset.id
