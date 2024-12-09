def repository_for(model, base_class):
    def wrapper(cls):
        class WrappedRepository(cls, base_class):
            def __init__(self, session, *args, **kwargs):
                super().__init__(session, model)
                if hasattr(cls, '__init__'):
                    cls.__init__(self, session, *args, **kwargs)
        return WrappedRepository
    return wrapper

def crud_repository_for(model):
    from . import CRUDRepository
    return repository_for(model, CRUDRepository)


def extended_crud_repository_for(model):
    from . import ExtendedCRUDRepository
    return repository_for(model, ExtendedCRUDRepository)