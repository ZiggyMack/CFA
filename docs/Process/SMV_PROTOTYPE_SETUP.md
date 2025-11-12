# SMV Prototype Setup Guide

**Owner:** Process Claude
**Bootstrap Creator:** Doc Claude (2025-11-11)
**Version:** 1.0
**Purpose:** Step-by-step instructions for launching the SMV prototype dev server

---

## Overview

This guide documents the setup process for running the SMV (Symmetry Matrix Visualizer) prototype on a Windows machine using Git Bash (MINGW64). The prototype is a React + Vite application that visualizes adversarial auditing sessions with the Trinity Architecture.

**Key Learning:** WSL Ubuntu's default Node.js packages can have architecture compatibility issues. Using **nvm (Node Version Manager)** is the recommended approach for Git Bash/MINGW64 environments.

---

## Prerequisites

- **Git Bash** (MINGW64) installed on Windows
- **Internet connection** (for downloading nvm and Node.js)
- **CFA repository** cloned to local machine

---

## One-Time Setup

### Step 1: Install nvm (Node Version Manager)

Open Git Bash and run:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
```

**Expected Output:**
```
=> Downloading nvm from git to '/c/Users/YourUsername/.nvm'
=> Compressing and cleaning up git repository
=> nvm is ready to use
```

### Step 2: Load nvm into Current Session

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

**Verification:**
```bash
nvm --version
# Should output: 0.39.0 or similar
```

### Step 3: Install Node.js LTS via nvm

```bash
nvm install --lts
```

**Expected Output:**
```
Installing latest LTS version.
Downloading and installing node v24.11.1...
Now using node v24.11.1 (npm v11.6.2)
```

**Verify Installation:**
```bash
node --version  # v24.11.1
npm --version   # 11.6.2
```

### Step 4: Navigate to Prototype Directory

```bash
cd /d/Documents/CFA/ui/smv/prototype
```

**Note:** In Git Bash (MINGW64), Windows drives are mounted at `/d/` not `/mnt/d/` (unlike WSL Ubuntu).

### Step 5: Install npm Dependencies (One-Time)

```bash
npm install
```

**Expected Output:**
```
added 316 packages, and audited 317 packages in 2m
...
2 moderate severity vulnerabilities
```

**Note:** The security warnings are acceptable for a development prototype. If needed, run `npm audit fix` later.

---

## Daily Launch Process

Every time you want to run the SMV prototype:

### Quick Start Commands (Copy-Paste):

```bash
# 1. Load nvm
export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# 2. Navigate to prototype
cd /d/Documents/CFA/ui/smv/prototype

# 3. Start dev server
npm run dev
```

### Expected Output:

```
  VITE v5.4.21  ready in 1010 ms

  ➜  Local:   http://localhost:3001/
  ➜  Network: use --host to expose
```

### Access the Prototype:

Open your browser and go to: **http://localhost:3001/**

---

## Stopping the Server

Press `Ctrl+C` in the terminal running the dev server.

---

## Troubleshooting

### Issue: `npm: command not found`

**Cause:** nvm not loaded in current session.

**Solution:** Run the nvm load command:
```bash
export NVM_DIR="$HOME/.nvm" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

### Issue: `cannot execute binary file: Exec format error`

**Cause:** You installed Node.js via `apt install nodejs` in Git Bash or WSL, which can have architecture mismatches.

**Solution:** Remove incompatible Node.js and use nvm instead:
```bash
# If you accidentally installed via apt
sudo apt remove nodejs npm -y

# Then install via nvm (see Step 3 above)
nvm install --lts
```

### Issue: `Could not read package.json: ENOENT`

**Cause:** Not in the correct directory.

**Solution:** Ensure you're in `/d/Documents/CFA/ui/smv/prototype`:
```bash
pwd  # Should output: /d/Documents/CFA/ui/smv/prototype
```

### Issue: Port 3001 Already in Use

**Cause:** Previous dev server instance still running.

**Solution:** Kill the process using port 3001:
```bash
# Find process using port 3001
netstat -ano | findstr :3001

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

---

## Architecture Notes

### Why nvm Instead of System Node.js?

1. **Architecture Compatibility:** nvm downloads pre-built binaries matching your system architecture (win-x64)
2. **Version Management:** Easily switch between Node.js versions for different projects
3. **User-Level Installation:** No admin/sudo privileges needed
4. **Git Bash Compatible:** Works seamlessly in MINGW64 environment

### SMV Prototype Tech Stack

- **React 18.3** - UI framework
- **Vite 5.4** - Build tool and dev server
- **React Router** - Scenario navigation
- **D3.js** (future) - Advanced visualizations
- **Port:** 3001 (hardcoded in vite.config.js)

### Project Structure

```
ui/smv/prototype/
├── src/
│   ├── components/       # React components (SymmetryView, CalibrationDrawer, etc.)
│   ├── data/            # Mock scenario JSON files
│   ├── App.jsx          # Main app component
│   └── main.jsx         # Entry point
├── public/              # Static assets
├── index.html           # HTML template
├── package.json         # Dependencies
├── vite.config.js       # Vite configuration (port 3001)
└── README.md            # Prototype-specific docs
```

---

## Process Claude Maintenance Duties

1. **Pre-Launch Validation:** Verify nvm is installed before guiding users to launch prototype
2. **Dependency Updates:** Quarterly check for critical npm security updates (`npm audit`)
3. **Documentation Updates:** Update this guide when:
   - Node.js LTS version changes significantly
   - Vite/React major version upgrades occur
   - New troubleshooting issues are discovered
4. **Health Check:** Ensure prototype still launches successfully after CFA repo updates

---

## Related Documentation

- **SMV Mockup Scenarios:** [/relay/workshop/smv_mockups/README.md](../../relay/workshop/smv_mockups/README.md)
- **SMV Architecture:** [/docs/smv/README.md](../smv/README.md)
- **Trinity Architecture:** [/docs/architecture/TRINITY.md](../architecture/TRINITY.md)
- **VuDu Operations:** [/auditors/Mission/VUDU_Operations/README.md](../../auditors/Mission/VUDU_Operations/README.md)

---

## Changelog

- **v1.0** (2025-11-11): Initial setup guide created (Doc Claude)
  - Documented nvm installation process
  - Added troubleshooting for "Exec format error" issue
  - Clarified Git Bash vs WSL Ubuntu path differences (`/d/` vs `/mnt/d/`)
  - Established Process Claude ownership for maintenance

---

**Last Updated:** 2025-11-11
**Tested Environment:** Windows 11, Git Bash (MINGW64), Node.js v24.11.1
**Maintainer:** Process Claude
