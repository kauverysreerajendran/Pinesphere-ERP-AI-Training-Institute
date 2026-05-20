# core/roles.py
from enum import Enum

class UserRole(str, Enum):
    SUPER_ADMIN    = "super_admin"
    BRANCH_ADMIN   = "branch_admin"
    COUNSELLOR     = "counsellor"
    TRAINER        = "trainer"
    STUDENT        = "student"
    PARENT         = "parent"
    HR             = "hr"
    FINANCE        = "finance"
    FRANCHISE_OWNER = "franchise_owner"

# Permission matrix — which roles can access which sections
ROLE_PERMISSIONS = {
    UserRole.SUPER_ADMIN:    ["users", "branches", "finance", "reports", "lms", "hr", "leads"],
    UserRole.BRANCH_ADMIN:   ["students", "batches", "attendance", "reports", "lms"],
    UserRole.COUNSELLOR:     ["leads", "admissions"],
    UserRole.TRAINER:        ["batches", "attendance", "lms", "assignments"],
    UserRole.STUDENT:        ["lms", "assignments", "profile"],
    UserRole.PARENT:         ["reports", "fees", "attendance"],
    UserRole.HR:             ["employees", "payroll", "leaves"],
    UserRole.FINANCE:        ["fees", "invoices", "reports", "finance"],
    UserRole.FRANCHISE_OWNER: ["branches", "reports"],
}