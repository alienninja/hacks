# Deployment Guide

## Quick Setup with GitHub Pages

### 1. Create GitHub Repository

```bash
cd /home/nano/carcrash
git init
git add .
git commit -m "Initial commit - Car Crash Simulator hack"
git branch -M main
```

Create a new repository on GitHub (e.g., `game-hacks`), then:

```bash
git remote add origin https://github.com/YOUR-USERNAME/game-hacks.git
git push -u origin main
```

### 2. Enable GitHub Pages

1. Go to your repository settings
2. Navigate to "Pages" in the sidebar
3. Under "Source", select `main` branch
4. Click "Save"

Your site will be live at: `https://YOUR-USERNAME.github.io/game-hacks/`

### 3. Add Custom Domain (Optional)

If you want to use `hacks.bithash.cc`:

**In GitHub:**
1. Go to repository Settings → Pages
2. Under "Custom domain", enter `hacks.bithash.cc`
3. Save

**In Your DNS Provider:**
Add a CNAME record:
```
Type: CNAME
Name: hacks
Value: YOUR-USERNAME.github.io
TTL: Auto or 3600
```

Wait 10-60 minutes for DNS propagation.

### 4. Enable HTTPS (Recommended)

After DNS is configured:
1. Go to Settings → Pages
2. Check "Enforce HTTPS"

## Alternative: Netlify Drop

Even simpler:

1. Go to https://app.netlify.com/drop
2. Drag the `/home/nano/carcrash` folder
3. Get instant URL
4. Add custom domain in Netlify settings

## Alternative: Cloudflare Pages

1. Push to GitHub (steps 1 above)
2. Go to Cloudflare Pages
3. Connect your repository
4. Auto-deploys on every push

## File Structure

```
/
├── index.html              (Main landing page)
├── README.md              (GitHub readme)
├── car-crash-simulator/   (First game)
│   ├── index.html         (Game-specific write-up)
│   ├── modify_game_config.py
│   ├── reset_dailies.sh
│   └── writeup.md
└── [future-games]/        (Add more games here)
```

## Testing Locally

```bash
# Simple HTTP server
cd /home/nano/carcrash
python3 -m http.server 8000

# Then visit: http://localhost:8000
```

## Updating Content

```bash
# Make changes to files
git add .
git commit -m "Update: description of changes"
git push

# GitHub Pages will auto-update in 1-2 minutes
```
