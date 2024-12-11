from functools import wraps

from robust_library_api.db.dao.exc import CommonRepositoryError

def model_row_to_dict(author_row) -> dict:
    formatted_row = dict(author_row.__dict__)
    formatted_row.pop('_sa_instance_state', None)
    return formatted_row

def repository_fallback(custom_exception: Exception, 
                        repository_error: Exception = CommonRepositoryError):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except repository_error as e:
                raise custom_exception
        return wrapper
    return decorator