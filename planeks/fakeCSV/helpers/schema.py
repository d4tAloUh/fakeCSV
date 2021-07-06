from fakeCSV.models import Schema, Column


def update_or_create_schema(request, pk):
    try:
        schema = Schema.objects.get(id=pk)
        schema.schema_name = request.POST['schema_name']
        schema.string_character = request.POST['string_character']
        schema.column_separator = request.POST['column_separator']
        schema.save(update_fields=['schema_name', 'string_character', 'column_separator', 'date_edit'])
    except Schema.DoesNotExist:
        schema = Schema.objects.create(
            schema_name=request.POST['schema_name'],
            string_character=request.POST['string_character'],
            column_separator=request.POST['column_separator'],
            user=request.user
        )
    return schema


def update_or_create_schema_columns(request, schema):
    columns = {}
    # Group data into dict by pk
    for key, value in request.POST.items():
        key_pk = key.split('.')
        if len(key_pk) > 1:
            if value == '' or key_pk[0] == 'schema':
                continue
            if key_pk[1] in columns:
                columns[key_pk[1]][key_pk[0]] = value
            else:
                columns[key_pk[1]] = {
                    key_pk[0]: value
                }
    # Update or create
    for column_pk in columns:
        try:
            column = Column.objects.get(id=column_pk)
            for value in columns[column_pk]:
                setattr(column, value, columns[column_pk][value])
            column.save(update_fields=columns[column_pk].keys())
        except (Column.DoesNotExist, ValueError, TypeError):
            Column.objects.create(
                **columns[column_pk],
                schema=schema
            )

        Column.objects.filter(schema=schema).exclude(id__in=[key for key in columns.keys() if key.isnumeric()]).delete()
