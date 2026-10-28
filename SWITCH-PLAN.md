# Switch plan: point morticeandtenon.us at the new site (GitHub Pages)

**Status: NOT started.** The new site is only on the preview URL, https://jeclass.github.io/mortice-tenon-site/. The live domain still serves the Base44 site. Do nothing below until Josh approves the preview and says to switch. Do not cancel Base44 until the new site has run cleanly on the domain for 1–2 weeks.

## Current DNS (checked 2026-10-27 21:07 MDT with `dig`)

| Record | Value now | Notes |
|---|---|---|
| NS | ns-cloud-b1…b4.googledomains.com | Squarespace Domains (ex-Google Domains). Edit DNS in Squarespace → Domains → morticeandtenon.us → DNS. |
| `@` ALIAS | base44.onrender.com | Resolves to A 216.24.57.16 and 216.24.57.18 (Render, Base44's host) |
| `www` CNAME | base44.onrender.com | |
| `@` MX | none | Email to @morticeandtenon.us does not work yet (see "Email" below) |
| `@` TXT | `v=spf1 -all` | Leave alone here; the Google Workspace setup replaces it |

GitHub Pages addresses, confirmed in the GitHub Docs page "Managing a custom domain for your GitHub Pages site" on 2026-10-27:

- A: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
- AAAA (optional, IPv6): `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
- `www` CNAME target: `jeclass.github.io`. Use the user domain only, **without** the repo name.

## Before you start

1. **Josh approves** the preview and answers the open questions (see the final report / brain note).
2. **Screenshot the current Squarespace DNS records**, so rollback can restore them exactly.
3. **Email is separate.** `sales@morticeandtenon.us` (shown on the site) only works after the Google Workspace setup adds the MX record, the new SPF TXT, and a `sales@` alias or group. When you change the web records below, **don't touch the MX, TXT or Google verification records.**
4. **Recommended: verify the domain with GitHub** (blocks domain takeover). Go to github.com → avatar → Settings → Pages → "Add a domain" → `morticeandtenon.us`. GitHub shows a TXT record named `_github-pages-challenge-jeclass` with a value. Add it in Squarespace DNS, wait a few minutes, then click Verify. This is safe to do any time, because it doesn't affect the live site.

## Switch steps (do steps 1 and 2 back to back)

Once step 1 is done, the preview URL redirects to morticeandtenon.us, which still shows Base44 until step 2 has propagated.

### 1. Add the custom domain on GitHub

The site publishes from the `main` branch, `/docs` folder, so the CNAME file belongs in `docs/`:

```bash
cd ~/mortice-tenon-site
echo "morticeandtenon.us" > docs/CNAME
git add docs/CNAME && git commit -m "Add custom domain morticeandtenon.us" && git push
gh api -X PUT repos/jeclass/mortice-tenon-site/pages -f cname=morticeandtenon.us
gh api repos/jeclass/mortice-tenon-site/pages   # expect "cname": "morticeandtenon.us"
```

You can also use Settings → Pages → Custom domain → Save. If you use the UI, GitHub commits `docs/CNAME` itself, so run `git pull` afterwards.

### 2. Change the DNS records in Squarespace

Squarespace → Domains → morticeandtenon.us → DNS → Custom records:

| Action | Type | Host | Value |
|---|---|---|---|
| **Delete** | ALIAS | @ | base44.onrender.com |
| **Delete** | CNAME | www | base44.onrender.com |
| Add | A | @ | 185.199.108.153 |
| Add | A | @ | 185.199.109.153 |
| Add | A | @ | 185.199.110.153 |
| Add | A | @ | 185.199.111.153 |
| Add (optional) | AAAA | @ | 2606:50c0:8000::153 (and 8001, 8002, 8003) |
| Add | CNAME | www | jeclass.github.io |
| **Keep** | MX / TXT / Google records | — | do not touch |

Don't use wildcard (`*`) records. If Squarespace shows "Squarespace Defaults" web records pointing @ or www elsewhere, remove those web records only.

### 3. Wait for DNS, then enforce HTTPS

```bash
dig morticeandtenon.us +noall +answer -t A        # expect the four 185.199.x.153
dig www.morticeandtenon.us +noall +answer         # expect CNAME jeclass.github.io
gh api repos/jeclass/mortice-tenon-site/pages      # wait for "https_certificate": {"state": "approved"}
gh api -X PUT repos/jeclass/mortice-tenon-site/pages -F https_enforced=true
```

DNS usually updates within an hour, though GitHub says it can take up to 24 hours. The certificate can take a while after DNS is correct. Until it is issued, "Enforce HTTPS" can't be ticked.

### 4. Verify

- `curl -sI https://morticeandtenon.us/` returns `200` with `server: GitHub.com`.
- `curl -sI http://morticeandtenon.us/` returns a `301` to https.
- `https://www.morticeandtenon.us/` redirects to `https://morticeandtenon.us/`.
- All pages load: `/`, `/products/`, `/install/`, `/wholesale/`, `/about/`, `/contact/`, `/privacy/`, `/downloads/mortice-and-tenon-line-card.pdf`.
- An old Base44 path, such as `/docs/pricing-availability.xlsx`, shows the custom 404 page.
- Spot-check on a phone. Re-run Lighthouse on the live domain.
- Record the change in the brand brain (`inbox/YYYY-MM-DD-mtagent-change-website-domain-switch.md`), with the before → after records.

### 5. Afterwards

- Keep Base44 active for 1–2 weeks as the rollback target, then Josh decides on cancelling it.
- Optional: add the site to Google Search Console and submit `https://morticeandtenon.us/sitemap.xml`.

## Rollback (any time, takes effect as DNS propagates)

1. In Squarespace DNS, delete the four `A` @ records (and any `AAAA` records) and the `CNAME www → jeclass.github.io`.
2. Re-add `ALIAS @ → base44.onrender.com` and `CNAME www → base44.onrender.com`, exactly as in the "before" screenshot.
3. On GitHub, remove the custom domain so the preview URL works again: `git rm docs/CNAME && git commit -m "Remove custom domain" && git push`, then Settings → Pages → Custom domain → Remove. Alternatively: `gh api -X PUT repos/jeclass/mortice-tenon-site/pages -F cname=null`.
4. Check that `curl -sI https://morticeandtenon.us/` shows the Render/Base44 headers (`rndr-id`) again.

Rollback depends on Base44 still being paid for and still having the domain attached. That is why Base44 stays active until the new site is proven.
