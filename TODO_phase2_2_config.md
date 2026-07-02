# TODO - Phase 2 (Configuration)

## Backups (mandatory)
- [x] app.py.backup created earlier
- [x] config.py.backup created earlier
- [x] extensions.py.backup created earlier
- [x] models.py.backup created earlier
- [x] routes/wishes.py.backup created earlier
- [x] api/health.py.backup created earlier

## Deliverables checklist
- [x] DevelopmentConfig / ProductionConfig / TestingConfig created (in `app/config.py`)
- [x] Config factory implemented (in `app/config_factory.py`)
- [x] Connection pool settings: pool_pre_ping True, pool_recycle 280
- [x] SQLALCHEMY_TRACK_MODIFICATIONS False
- [ ] No db.create_all() in config (later phase)
- [x] Logging configured with Python logging (in `app/logging_config.py`)
- [x] Debug controlled by environment only
- [x] .env.example exists with placeholders
- [x] Frontend unchanged

## Verification
- [x] Flask imports successfully (create_app)
- [x] Config loads successfully in this environment
- [x] Environment variables detected OR safe dev defaults used
- [x] SQLAlchemy initializes successfully (health depends on DB availability)
- [x] No frontend files modified

## Notes / Current limitations
- `/api/health` returns 503 when MySQL is unreachable (expected, not a regression)
- Production strict env validation is implemented via `validate_or_raise()` but not called yet.

