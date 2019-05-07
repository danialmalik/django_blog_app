"""Basic settings for REST API"""

DEFAULT_PAGE_SIZE = 10
DEFAULT_MAX_PAGE_SIZE = 50
DEFAULT_DATE_TIME_FORMAT = '%d-%m-%Y %I:%M%p'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),

    # e.g. 25-10-2018 12:12AM
    'DATETIME_FORMAT': DEFAULT_DATE_TIME_FORMAT,

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': DEFAULT_PAGE_SIZE,
    'MAX_PAGE_SIZE': DEFAULT_MAX_PAGE_SIZE
}
