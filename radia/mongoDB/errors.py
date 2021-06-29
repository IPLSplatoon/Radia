class MongoError(Exception):
    """Base Exception"""
    pass


class TeamNoFoundError(MongoError):
    """Team Not Found"""
    pass


class CaptainNotFound(MongoError):
    """Captain not Found"""
    pass


class RoleNotFound(MongoError):
    """Role not Found"""
    pass
