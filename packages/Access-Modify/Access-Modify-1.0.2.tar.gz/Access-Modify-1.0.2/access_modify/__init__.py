from access_modify.access_modify import access, public, private, protected

__all__ = list(map(
    lambda x: x.__name__,
    [ access, public, private, protected ]
))
