from enum import Enum

class ProductStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    flagged = "flagged"
    rejected = "rejected"

class UserRole(str, Enum):
    user = "user"
    admin = "admin" 