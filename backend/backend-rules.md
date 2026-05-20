# Pinesphere ERP Backend Rules

---

# 1. Purpose

This document defines the backend engineering standards for the Pinesphere ERP platform.

The backend architecture must remain:

- Scalable
- Secure
- Predictable
- Modular
- AI-agent-friendly
- Enterprise-ready

The backend stack is based on:

- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Redis
- FastAPI for AI services

Source reference: :contentReference[oaicite:0]{index=0}

---

# 2. Backend Engineering Philosophy

The backend must prioritize:

- Clean architecture
- Service isolation
- Secure APIs
- Predictable response formats
- Modular business logic
- Long-term maintainability

---

## Backend Must Never Become

```text id="v7mpx2"
❌ Massive monolithic chaos
❌ Business logic inside views
❌ Inconsistent API responses
❌ Random database access
❌ Security bypass system


Recommended Backend Structure

backend/
│
├── apps/
├── core/
├── config/
├── services/
├── shared/
├── middleware/
├── utils/
├── requirements/
├── scripts/
├── tests/
└── manage.py

Django App Structure Rules

Each domain must be isolated as an app.

apps/
├── authentication/
├── students/
├── attendance/
├── courses/
├── lms/
├── finance/
├── notifications/
├── ai_engine/
└── analytics/


Django App Internal Structure

Every app should follow:

students/
│
├── models/
├── serializers/
├── services/
├── views/
├── urls/
├── permissions/
├── selectors/
├── tasks/
├── validators/
├── tests/
└── admin/

Backend Architecture Rules
Mandatory
Thin views
Service-based business logic
Selector-based read queries
Reusable serializers
Clear permission system
Isolated app domains
Forbidden
❌ Fat views
❌ Business logic in serializers
❌ Raw SQL everywhere
❌ Shared global state
❌ Cross-module dependency chaos
7. Django Models Rules
Mandatory
One model per responsibility
Explicit relationships
Use UUID where required
Timestamps everywhere
Soft delete preferred