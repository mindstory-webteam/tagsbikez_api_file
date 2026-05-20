from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Wraps DRF errors:
    { "success": false, "error": { "detail": "..." } }
    """
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'success': False,
            'error': response.data,
        }

    return response
