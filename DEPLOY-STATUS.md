# Deployment status

## Done (automated)

- Site built at `C:\Users\tonyv\glittercloud-website`
- Pushed to https://github.com/Tvalc/glittercloud-website
- GitHub Pages enabled (branch `main`, custom domain `glittercloud.solutions`)
- Build status: **built** (verified on GitHub)

## One step left: GoDaddy DNS

The domain still points to **Vercel** (old Web3 site). Until DNS changes, visitors see the old site.

In GoDaddy → **DNS** for `glittercloud.solutions`:

### Remove

- Any **A** records pointing to `76.76.21.21` or other Vercel IPs
- Any **CNAME** for `www` pointing to `cname.vercel-dns.com`

### Add

| Type  | Name | Value                |
|-------|------|----------------------|
| A     | @    | 185.199.108.153      |
| A     | @    | 185.199.109.153      |
| A     | @    | 185.199.110.153      |
| A     | @    | 185.199.111.153      |
| CNAME | www  | tvalc.github.io      |

After saving, wait 5–30 minutes, then open https://glittercloud.solutions — you should see the new Tony-led site.

In GitHub → repo **Settings → Pages**, enable **Enforce HTTPS** once the domain verifies.

## Replace headshot (optional)

Save your photo as `assets/tony-headshot.jpg`, update `index.html` `src` to that path, commit and push. A gold SVG placeholder is live until then.
