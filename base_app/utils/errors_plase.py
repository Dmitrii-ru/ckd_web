

def create_error(
        name = 'Нет данных',
        path = 'Нет данных',
        error = 'Нет данных',
        ):

    from base_app.models import ErrorData
    error = ErrorData.objects.create(
        name=name,
        path=path,
        error= error
    )
    error.save()