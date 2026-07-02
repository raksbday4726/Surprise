# TODO - Phase 1 (Architecture Refactor Only)

## Step 0: Backup (mandatory)
- [ ] Backup app.py -> app.py.backup
- [ ] Backup config.py -> config.py.backup
- [ ] Backup extensions.py -> extensions.py.backup
- [ ] Backup models.py -> models.py.backup
- [ ] Backup routes/wishes.py -> routes/wishes.py.backup
- [ ] Backup api/health.py -> api/health.py.backup

## Step 1: Create new modular package structure
- [ ] Create: app/__init__.py (app factory) 
- [ ] Create: app/config.py (Config)
- [ ] Create: app/extensions.py (db, migrate)
- [ ] Create: app/models/__init__.py (imports for Wish, Upload)
- [ ] Create: app/models.py logic moved under app/models/wish.py or __init__.py
- [ ] Create: app/routes/__init__.py
- [ ] Create: app/routes/wishes.py blueprint (existing logic copied verbatim)
- [ ] Create: app/routes/health.py blueprint (existing logic copied verbatim)

## Step 2: Wiring / Entrypoints
- [ ] Create: run.py (Gunicorn-ready) with create_app import
- [ ] Update: app.py to re-export create_app or become thin compatibility shim

## Step 3: Preserve external behavior
- [ ] Ensure endpoints remain: /api/wishes, /api/health
- [ ] Ensure uploads remain accessible exactly as before (route + photo_url format)
- [ ] Ensure JSON keys + wish to_dict output unchanged

## Step 4: Verification
- [ ] Run server locally (python run.py) and check /api/health
- [ ] Call /api/wishes GET to validate response shape
- [ ] Manual smoke test: POST /api/wishes with/without photo (curl) 

## Step 5: Report
- [ ] Document folder structure, moved/created/removed files, and rationale
- [ ] Provide verification report

