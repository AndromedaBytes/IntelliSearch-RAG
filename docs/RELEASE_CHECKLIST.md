# IntelliSearch V2 Release Checklist

## Pre-Release (Development Phase)

### Code Quality & Security
- [ ] All UI emojis removed (no unicode in production)
- [ ] No plaintext secrets in repository (`.env` excluded from git)
- [ ] `.env.example` provided with all required keys documented
- [ ] Client key validation implemented (`X-IntelliSearch-Client-Key` header)
- [ ] GitHub token validation in place (models:read permission required)
- [ ] Similarity gate enabled (default 0.70 cosine similarity)
- [ ] Citation deduplication working correctly
- [ ] Error messages sanitized (no internal stack traces exposed)

### Feature Completeness
- [ ] Backend RAG pipeline functional (ingestion → retrieval → synthesis → citations)
- [ ] Frontend UI complete with Settings modal (client key, endpoint, similarity threshold)
- [ ] Similarity threshold toggle implemented and persisted to localStorage
- [ ] Chat interface responsive and accessible
- [ ] File upload working (PDF, images, audio formats)
- [ ] Health endpoint available (`GET /health`)
- [ ] Ingestion endpoint protected with client key (`POST /ingest/`)
- [ ] Query endpoint protected with client key (`POST /query/`)

### Testing & Validation
- [ ] Backend health check script passes: `python scripts/health_check.py`
- [ ] GitHub Models authentication verified: `python scripts/verify_foundry_inference.py`
- [ ] Query endpoint tested: `python scripts/run_query_xeno.py`
- [ ] Model parity checked: `python scripts/ask_models.py`
- [ ] Frontend builds without errors: `npm run build`
- [ ] UI tested in browser (localhost:8000 after EXE launch)
- [ ] File ingestion tested with PDF, image, audio files
- [ ] Similarity gate blocks low-relevance queries correctly
- [ ] Citations properly deduplicated and ranked by similarity

### Documentation
- [ ] README.md updated with setup instructions
- [ ] `.env.example` includes all required environment variables
- [ ] API endpoint documentation available (docstrings in routers)
- [ ] Architecture documented (GPT-4o ingestion, Llama synthesis, similarity gate)
- [ ] Troubleshooting guide included (common errors, GitHub token setup)

---

## Build & Packaging

### Build Process
- [ ] Run `python build_exe.py` successfully
  - Next.js frontend builds without errors
  - PyInstaller bundles backend and frontend
  - No critical warnings in build log
- [ ] Resulting EXE at `dist/IntelliSearch-V2/IntelliSearch-V2.exe`
- [ ] Size reasonable (~600-800 MB for full bundle)
- [ ] Executable launches without errors on clean system

### Package Verification
- [ ] EXE starts server on port 8000 automatically
- [ ] UI loads at http://localhost:8000
- [ ] Health check passes when running EXE
- [ ] Can ingest files and query corpus
- [ ] Settings persist across restarts

### Sign & Notarize (Windows)
- [ ] Code signing certificate obtained (Sectigo, DigiCert, etc.)
- [ ] Executable signed: `signtool sign /f cert.pfx IntelliSearch-V2.exe`
- [ ] Signature verified: `signtool verify /pa IntelliSearch-V2.exe`
- [ ] Optional: Submit to Microsoft SmartScreen for whitelisting

---

## Pre-Distribution

### Token & Security Hardening
- [ ] Rotate GitHub PAT (generate new token, update locally)
- [ ] Verify `.env` NOT committed to repo (check `.gitignore`)
- [ ] `.env` bundled in EXE with safe defaults (randomized CLIENT_KEY)
- [ ] Remove any hardcoded credentials from source files
- [ ] Secrets scanning passed (e.g., `git-secrets`, `truffleHog`)

### Final Testing on Clean System
- [ ] Test on Windows 11 machine without dev tools installed
- [ ] No dependency on Python installation or virtual environment
- [ ] EXE runs independently (self-contained bundle)
- [ ] Can ingest large files (>100 MB) without crashing
- [ ] Query latency acceptable (< 15 seconds for synthesis)
- [ ] No console errors or warnings visible to user
- [ ] Task manager shows reasonable memory usage (< 1 GB)

### Release Notes & Communication
- [ ] Release notes written (features, bug fixes, known issues)
- [ ] Version bumped (e.g., `2.0.0` in `package.json`, `VERSION` file)
- [ ] Changelog updated
- [ ] GitHub release created with notes and EXE attached
- [ ] Users notified via email/Slack (if applicable)

---

## Post-Release (Monitoring)

### Issue Tracking & Support
- [ ] GitHub Issues enabled for bug reports
- [ ] Support email configured and monitored
- [ ] Common issues documented in FAQ
- [ ] User feedback collected and triaged

### Telemetry & Analytics (Optional)
- [ ] Basic usage telemetry enabled (if user consents)
- [ ] Error reporting to sentry.io or similar (optional)
- [ ] No sensitive data sent in telemetry

### Maintenance Cycle
- [ ] Plan for regular token rotation (quarterly)
- [ ] Monitor model API deprecations (GitHub Models, Azure AI Inference)
- [ ] Plan updates for security patches
- [ ] Document feedback for next version

---

## Rollback Plan

- [ ] Previous version backed up
- [ ] Instructions for reverting to prior build
- [ ] User communication plan if critical bug found post-release

---

## Quick Sanity Check Before Release

Run the following before shipping:

```bash
# 1. Health check
python scripts/health_check.py

# 2. Verify foundry inference
python scripts/verify_foundry_inference.py

# 3. Test query
python scripts/run_query_xeno.py

# 4. Test model parity
python scripts/ask_models.py

# 5. Build EXE
python build_exe.py

# 6. Launch and verify UI
Start-Process "dist\IntelliSearch-V2\IntelliSearch-V2.exe"
# Visit http://localhost:8000 in browser
# Upload a test file, query corpus, adjust similarity threshold
```

If all pass, ready to release! 🚀

---

**Release Date**: _______________  
**Version**: _______________  
**Approved By**: _______________  
**Notes**: 

