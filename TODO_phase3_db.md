# Phase 3 – Database & Migrations (Tracker)

## Steps
- [ ] Confirm migrations history: migrations/versions contains existing migration files (or none)
- [ ] Ensure Alembic env.py autogenerate can see model metadata (import models if required)
- [ ] Ensure Flask-Migrate is initialized (db + migrate)
- [ ] Run: flask db init (only if migrations are missing)
- [ ] Run: flask db migrate -m "Initial tables"
- [ ] Run: flask db upgrade
- [ ] Verify with verify_db.py
- [ ] Verify table creation + schema constraints (PK/NOT NULL/UNIQUE/indexes/timestamps)
- [ ] Rollback test: flask db downgrade (one revision)
- [ ] Rollback recovery: flask db upgrade back to latest
- [ ] Final verification: frontend files unchanged
- [ ] Prepare deliverables summary

