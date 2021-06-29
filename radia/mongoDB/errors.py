class MongoError(Exception):
    """Base Exception"""
    pass


class TeamNoFoundError(MongoError):
    """Team Not Found"""
    pass


class CaptainNotFound(MongoError):
    pass


class RoleNotFound(MongoError):
    pass
