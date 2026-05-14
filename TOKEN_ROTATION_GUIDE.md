# Token Rotation & Security Guide

## Overview

This guide covers secure token management for IntelliSearch V2, including:
- GitHub Personal Access Token (PAT) rotation
- Client key generation & rotation
- `.env` file security
- Secrets scanning

---

## 1. GitHub Personal Access Token (PAT) Rotation

### Why Rotate?
- Security best practice (tokens are like passwords)
- Reduces impact of accidental exposure
- Complies with SOC 2 / enterprise security policies
- Recommended quarterly or when team changes

### Current Token Permissions Required

Your GitHub PAT must have **`models:read`** permission to access:
- `https://models.github.ai/inference` (OpenAI models, Llama models)

### Steps to Rotate

#### Step 1: Generate New Token
1. Visit: https://github.com/settings/tokens
2. Click **Generate new token** → **Generate new token (classic)**
3. Fill in:
   - **Token name**: `IntelliSearch-V2-Prod` (or your naming convention)
   - **Expiration**: 30 days (recommended) or 90 days
   - **Select scopes**: 
     - ✅ Check **`models:read`**
     - ✅ (Optional) Check **`repo`** if needed for file storage
4. Click **Generate token**
5. **Copy the token** (only visible once!)

#### Step 2: Verify New Token Works
Replace the old token in your test environment first:

```bash
# Windows PowerShell
$Env:GITHUB_TOKEN = "ghp_your_new_token_here"
python scripts/verify_foundry_inference.py
```

Expected output: `AUTH_SUCCESS model=openai/gpt-4.1`

#### Step 3: Update .env
Edit `.env` (or `.env.production`):

```bash
# Old token
GITHUB_TOKEN=ghp_old_token_xxxxxxxxxxxx

# New token
GITHUB_TOKEN=ghp_new_token_xxxxxxxxxxxx
```

#### Step 4: Rebuild & Test

```bash
# Rebuild the packaged EXE
python build_exe.py

# Test
python scripts/health_check.py
```

All checks should pass with green `[OK]` status.

#### Step 5: Deploy
- Replace old EXE with new build
- Update `.env` on production machine (if applicable)
- Test queries on production

#### Step 6: Revoke Old Token
Once confirmed new token works everywhere:
1. Visit: https://github.com/settings/tokens
2. Find the old token
3. Click **Delete**
4. Confirm

---

## 2. Client Key Management

### What is CLIENT_KEY?
- A shared secret between frontend and backend
- Validates requests: `X-IntelliSearch-Client-Key` header
- Prevents unauthorized access to query/ingest endpoints

### Current Client Key
Check `.env`:

```bash
CLIENT_KEY=sk-intellisearch-xxxxxxxxxxxxxxxxxxx
```

### Rotate Client Key

#### Option A: Generate New Random Key (Recommended)

```python
import secrets
import string

# Generate 32 random alphanumeric chars
random_key = "sk-intellisearch-" + secrets.token_hex(16)
print(random_key)
# Example: sk-intellisearch-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

#### Option B: Use Python Secrets Module

```bash
python -c "import secrets; print('sk-intellisearch-' + secrets.token_hex(16))"
```

#### Steps

1. Generate new key (use Option A or B above)
2. Update `.env`:
   ```bash
   CLIENT_KEY=sk-intellisearch-<new_random_key>
   ```
3. Rebuild EXE:
   ```bash
   python build_exe.py
   ```
4. Test:
   ```bash
   python scripts/health_check.py
   ```
5. Replace old EXE with new build

### Note on Frontend
- Frontend reads `CLIENT_KEY` from `.env` during build
- Users can override in Settings modal
- Value persisted to browser localStorage

---

## 3. .env File Security

### Best Practices

#### ✅ DO:
- ✅ Add `.env` to `.gitignore` (already configured)
- ✅ Never commit `.env` to version control
- ✅ Keep `.env` on secure machines only
- ✅ Restrict file permissions: `chmod 600 .env` (Linux/Mac)
- ✅ Use `.env.example` with placeholder values in repo
- ✅ Rotate tokens regularly
- ✅ Use environment variables in production (not .env files)

#### ❌ DON'T:
- ❌ Commit `.env` to GitHub
- ❌ Share `.env` in emails or Slack
- ❌ Hardcode secrets in source code
- ❌ Log secrets to console
- ❌ Include `.env` in EXE distributable (except default non-sensitive values)

### File Permissions (Linux/Mac)

```bash
chmod 600 .env
ls -la .env
# Should show: -rw------- 1 user group ... .env
```

### Verify .env is Ignored

```bash
git status
# Should NOT show .env

git check-ignore .env
# Should print: .env
```

---

## 4. Secrets Scanning

### Before Committing Code

Run secrets scanner to detect accidentally hardcoded secrets:

```bash
# Install (if not already)
pip install truffleHog

# Scan repository
trufflehog filesystem . --only-verified
```

Or use GitHub's built-in secret scanning:
- Go to: https://github.com/YOUR_ORG/YOUR_REPO/settings/security
- Enable: "Secret scanning"
- Enable: "Push protection" (blocks commits with detected secrets)

### What to Look For

Common patterns to avoid in code:
```python
# ❌ BAD
GITHUB_TOKEN = "ghp_xxxxxxxxxxxxxxxxxxxx"
CLIENT_KEY = "sk-intellisearch-xxxxxx"
api_key = "sk_live_xxxxxx"

# ✅ GOOD
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
CLIENT_KEY = settings.CLIENT_KEY
api_key = config.get_secret("api_key")
```

---

## 5. Token Rotation Schedule

### Recommended Calendar

```
Q1 (Jan-Mar):  GitHub PAT rotation
Q2 (Apr-Jun):  Client key rotation + GitHub PAT
Q3 (Jul-Sep):  GitHub PAT rotation
Q4 (Oct-Dec):  Audit all secrets + rotation
```

### After Team Changes
- If team member with access leaves: **rotate immediately**
- If PAT compromised: **rotate immediately**
- If repo exposed publicly: **rotate immediately**

---

## 6. Emergency Token Revocation

If PAT is compromised or leaked:

### Immediate Action
```bash
# 1. Revoke old token
#    Visit: https://github.com/settings/tokens → Delete

# 2. Generate new token (fast!)
#    Follow "Generate New Token" steps above

# 3. Update .env and rebuild
GITHUB_TOKEN=ghp_new_emergency_token

# 4. Rebuild EXE
python build_exe.py

# 5. Test
python scripts/verify_foundry_inference.py

# 6. Redeploy to all instances
```

### Notification
- Notify users that new version is available
- Include security note in release
- Consider forcing update if possible

---

## 7. Secrets Management for Production

If deploying to cloud:

### Option A: Environment Variables (Recommended)
```bash
# On Windows Server / cloud VM
setx GITHUB_TOKEN "ghp_xxxxxxxxxxxx"
setx CLIENT_KEY "sk-intellisearch-xxxx"

# Restart application
```

### Option B: Secret Manager
- **Azure Key Vault**: Fetch secrets at runtime
- **AWS Secrets Manager**: Similar pattern
- **Kubernetes Secrets**: For containerized deployments

Example Azure Key Vault integration:
```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://myvault.vault.azure.net/", credential=credential)

github_token = client.get_secret("GITHUB-TOKEN").value
```

### Option C: Config Files (Less Secure)
- Store `.env.production` in restricted location
- File permissions: `0600` (read/write owner only)
- Not in version control
- Backed up separately

---

## 8. Audit Log

Keep a record of token rotations:

```
Date         | Token Type    | Reason        | Status
-------------|---------------|---------------|----------
2026-05-03   | GitHub PAT    | Routine       | COMPLETE
2026-05-10   | Client Key    | Routine       | COMPLETE
2026-06-01   | GitHub PAT    | Team change   | PENDING
```

---

## Quick Reference

### Verify Current Token Works
```bash
python scripts/verify_foundry_inference.py
```

### Run Full Health Check
```bash
python scripts/health_check.py
```

### Generate New Keys
```bash
# GitHub PAT: Visit https://github.com/settings/tokens
# Client Key: python -c "import secrets; print('sk-intellisearch-' + secrets.token_hex(16))"
```

### Rebuild & Test
```bash
python build_exe.py
python scripts/health_check.py
```

---

## Support & Questions

- **Token won't work?** Ensure `models:read` permission in GitHub PAT settings
- **EXE not starting?** Check `.env` format and tokens are valid
- **Queries failing after rotation?** Restart EXE and clear browser cache
- **Locked out?** Generate new CLIENT_KEY and restart backend

---

**Last Updated**: 2026-05-03  
**Reviewed By**: _____________  
**Next Review**: _____________  
