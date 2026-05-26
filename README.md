# Glittercloud Solutions — placeholder site

Static site for GitHub Pages + GoDaddy DNS (same pattern as sectorscavengers.com).

## 1. Add your headshot

Save the photo you shared as:

```
assets/tony-headshot.jpg
```

Until then, the page shows a "TV" fallback circle.

## 2. Push to GitHub

```bash
cd glittercloud-website
git init
git add .
git commit -m "Placeholder site: Tony-led GTM, ops, and AI positioning"
```

Create a new repo on GitHub (e.g. `glittercloud-website`), then:

```bash
git remote add origin https://github.com/YOUR_USER/glittercloud-website.git
git branch -M main
git push -u origin main
```

## 3. Enable GitHub Pages

1. Repo **Settings → Pages**
2. Source: **Deploy from branch** → `main` / `/ (root)`
3. Custom domain: `glittercloud.solutions`
4. Enable **Enforce HTTPS** when available

The `CNAME` file is already in the repo root.

## 4. GoDaddy DNS (replace Vercel)

Remove existing Vercel A/CNAME records, then add:

| Type | Name | Value |
|------|------|--------|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | YOUR_USER.github.io |

If using a **project** repo Pages URL, use the CNAME GitHub shows in Pages settings instead of `github.io` root.

## 5. Verify

- https://glittercloud.solutions loads this site
- Headshot displays
- Mailto links work on mobile/desktop
