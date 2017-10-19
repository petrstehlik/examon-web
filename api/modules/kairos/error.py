from muapi.error import ApiException

class JobsError(ApiException):
    status_code = 500
