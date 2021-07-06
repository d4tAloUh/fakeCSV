from planeks.celery import app

from fakeCSV.models import Schema, DataSet


@app.task
def generate_data_task(schema_id, user_id, nums_row):
    exist_schema, _schema = __get_schema_from_db(pk=schema_id, user__pk=user_id)
    if not exist_schema:
        return _schema
    if not nums_row:
        logging.error("There is no number of lines in the parameters.")
        return {'status': 'error', 'message': 'There is no number of lines in the parameters.'}
    fields = __fill_fields(columns=_schema.schema_columns.all())
    url = 'https://www.mockaroo.com/api/generate.csv'
    payload = {'key': '2ef5da30', 'count': nums_row, }
    response = requests.post(url=url, params=payload, json=fields)
    if response.ok:
        content_b64 = __convertBytesToB64(content_bytes=response.content,
                                          delimiter=_schema.get_column_separator_char(),
                                          quote_char=_schema.get_string_character_char())
        dataset = DataSet.objects.create(schema=_schema, file_content=content_b64)
        if dataset:
            return {'status': 'ok', 'message': f'{dataset.pk}'}
        else:
            logging.error(f"Received incorrect CSV format")
            return {'status': 'error', 'message': 'Received incorrect CSV format.'}
    else:
        logging.error(f"Error while receiving data from the mockaroo")
        return {'status': 'error', 'message': 'Error while receiving data from the mockaroo.'}
