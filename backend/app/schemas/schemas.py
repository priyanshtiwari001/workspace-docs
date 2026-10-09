from enum import Enum

class Roles(str,Enum):
    OWNER="owner"
    VIEWER="viewer"
    EDITOR="editor"