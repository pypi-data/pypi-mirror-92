import typing

def validate(request, schema, data, mode=None, **kw) -> typing.Optional[dict]:
    """ Validate data 

    return None if valid
    return dictionary with following structure if invalid::

       {'field': '<field_name>',
        'message': '<error_message>'}
    """
    return None
