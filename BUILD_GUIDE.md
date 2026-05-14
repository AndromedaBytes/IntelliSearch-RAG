# IntelliSearch V2 — Build & Distribution Guide

## Build Sequence

Execute these commands in order to produce the final distributable .exe:

### 1. Environment Setup

```powershell
# Activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt

# Verify installation
python scripts/doctor.py
```

### 2. Testing

```powershell
# Run unit tests
pytest tests/ -v --asyncio-mode=auto

# Run integration tests (requires backend running)
python run.py  # In another terminal
python scripts/integration_test.py
```

### 3. Frontend Build

```powershell
cd frontend
npm install
npm run build
npm run export
cd ..
```

### 4. .EXE Build

```powershell
# Build Windows .exe
python build_exe.py

# Output: dist\IntelliSearch-V2.exe
```

### 5. Release

```powershell
# Tag release
git tag v2.0.0
git push origin v2.0.0

# GitHub Actions automatically:
# - Builds .exe on Windows runner
# - Creates GitHub Release
# - Uploads IntelliSearch-V2.exe as asset
```

## Automated GitHub Actions Build

When you push a tag matching `v*.*.*`, the `.github/workflows/build-exe.yml` workflow:

1. Checks out code on Windows runner
2. Sets up Python 3.10 + Node.js 20
3. Installs dependencies
4. Builds Next.js frontend
5. Runs PyInstaller
6. Creates GitHub Release with .exe attached

## White-Label Customization

To sell IntelliSearch V2 as a custom product:

### 1. Branding
```bash
# Replace in these files:
backend/app/config.py        # CHROMA_COLLECTION_NAME
frontend/app/layout.tsx      # metadata.title, brand colors
README.md                    # Project name, description
```

### 2. Colors
```bash
# tailwind.config.ts
# Modify gold and accent color schemes
```

### 3. Security
```bash
# Generate strong production client key:
python -c "import secrets; print(secrets.token_hex(64))"

# Set as CLIENT_KEY in production .env
```

### 4. Configuration Tuning
```python
# backend/app/config.py
SIMILARITY_THRESHOLD = 0.65  # Lower = more permissive
CHUNK_SIZE = 512             # Adjust for domain
TOP_K_RETRIEVAL = 15         # More results = slower
```

### 5. Build & Deliver
```bash
# Build custom .exe
python build_exe.py

# Deliver to client:
# - dist/ClientName-Intelligence.exe
# - Setup guide (see below)
# - .env.example with their tokens pre-configured
```

## First-Run User Experience

When user double-clicks IntelliSearch-V2.exe:

1. **Setup Window** appears (if .env doesn't exist)
   - Collects GitHub Token A (GPT-4o)
   - Collects GitHub Token B (Llama 3.1 405B)
   - Allows client key generation or entry

2. **Auto-generate** button creates random key

3. **Save & Continue** writes .env next to .exe

4. **Backend launches** in background thread

5. **Browser opens** to http://127.0.0.1:8000

6. **Sidebar shows** health status, corpus size

## Troubleshooting Build Issues

### Build fails with "PyInstaller not found"
```bash
pip install pyinstaller==6.8.0
```

### Frontend build errors
```bash
cd frontend
rm -r node_modules package-lock.json
npm install
npm run build
```

### Port 8000 already in use
```powershell
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Missing ffmpeg
```bash
# Windows
choco install ffmpeg
# Or download from https://ffmpeg.org/download.html
```

## Distribution Checklist

- [ ] All tests pass (`pytest tests/ -v`)
- [ ] Integration tests pass (`scripts/integration_test.py`)
- [ ] Doctor script shows ✓ PASS (`python scripts/doctor.py`)
- [ ] .exe file built and tested on clean Windows machine
- [ ] File size < 200MB (flag if larger)
- [ ] First-run setup window works
- [ ] Dark theme renders correctly
- [ ] Sidebar health check updates every 15s
- [ ] Chat input sends messages (with dummy backend)
- [ ] Upload drag-drop works
- [ ] Settings modal saves client key
- [ ] All toasts display without errors
- [ ] Markdown rendering works in responses
- [ ] Citation pills display correctly
- [ ] Gate-blocked messages show warning style
- [ ] No console errors in browser DevTools

## Performance Targets

- Query latency: < 5 seconds total
  - ChromaDB search: < 500ms
  - Llama inference: < 4.5s
  
- Ingest latency: < 10 seconds per file
  - File reading: < 100ms
  - GPT-4o extraction: < 9s (depends on file size)
  - ChromaDB storage: < 100ms

- Memory usage: < 200MB idle

## Security Best Practices for Production

1. **Client Key** - Use `secrets.token_hex(64)` for production
2. **HTTPS** - Deploy behind reverse proxy with SSL
3. **CORS** - Restrict to known origins in production
4. **Rate Limiting** - Implement at proxy level
5. **Logging** - Store logs securely
6. **Backup** - Regular backups of ChromaDB storage

## Support & Documentation

- **Installation**: See README.md Quick Start
- **API Reference**: See README.md API Reference
- **Architecture**: See README.md Architecture Deep Dive
- **GitHub Issues**: Report bugs and feature requests
- **GitHub Discussions**: Ask questions and share ideas

---

**Built for MakersGroup** | IntelliSearch V2 | GPT-4o · Llama 3.1 405B · ChromaDB · FastAPI · PyInstaller
