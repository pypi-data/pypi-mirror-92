import enum


class Formats(enum.Enum):
    JSON = 'json'
    TABLE = 'table'


class ApiOperation(enum.Enum):
    LIST = 'list'
    FETCH = 'fetch'
    CREATE = 'create'
    DELETE = 'delete'
    UPDATE = 'update'


class Profile(enum.Enum):
    API_KEY = 'api_key'
    ACCOUNT = 'account'


class Export_Formats(enum.Enum):
    CSV = 'csv'
    EXCEL = 'excel'
    HTML = 'html'


class Export_Formats_Extensions(enum.Enum):
    CSV = '.csv'
    EXCEL = '.xlsx'
    HTML = '.html'


ERROR_HEADER = ["message",
                "type",
                "api_error_code",
                "error_code",
                "error_msg",
                "http_status_code"
                ]
