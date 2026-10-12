
from .user import User
from .workspace import WorkSpace
from .workspace_member import WorkspaceMember
from .refresh_token import RefreshToken
from .note import Note
# This tells Python: "When someone imports models, load all of these classes."
__all__ = [
    "Note",
    "RefreshToken",
    "User",
    "WorkSpace",
    "WorkspaceMember",
]

'''
Q. How does SQLAlchemy resolve circular relationships in a modular codebase?
SQLAlchemy uses a string-based class registry. By passing the class name as a string to relationship(), it defers evaluation. To ensure all classes are registered in SQLAlchemy's mapper registry before configuration happens, I centralize all model imports in the models/__init__.py file and trigger it at startup."
'''
