# Trevor Adair Photography

A complete, original 19-page static photography website, built around Trevor's photographs. Warm ivory, botanical olive, restrained brass, editorial typography, and deliberately varied image compositions. No production framework or package installation is required.

## View locally

From this folder, with Python 3.12 or later:

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000. Use a web server rather than double-clicking HTML files because the site uses root-relative links.

## Deploy to GitHub Pages

1. Create your GitHub repository and upload this folder's **contents**, including `.github/workflows/deploy.yml` and `dist/assets/`. Do not upload the enclosing ZIP.
2. Use `main` as the branch. In repository Settings → Pages, choose **GitHub Actions** as the build source.
3. Run the Deploy photography site workflow, or push a commit to `main`.
4. The workflow discovers the actual Pages origin and repository subpath automatically. Its default output is a review site with search indexing disabled. A public review URL is still publicly accessible; noindex is not access control.
5. After approving the package details and launch content, add repository Actions variable `PUBLISH_READY` with value `true`, then rerun the workflow. This enables indexing and removes preview notices and the unapproved testimonial.

No GitHub account was connected and no repository was created during this build. The deployment workflow is supplied, not a claim of a completed public deployment.

## Your future domain

When purchased and connected, configure `trevoradairphotography.com` in GitHub Pages and complete DNS verification following GitHub's current instructions. Enforce HTTPS. Rerun the workflow after domain setup; canonical URLs and sitemap will use the actual configured Pages origin. Do not set the future domain as canonical before it resolves to this website.

For another host, the output directory is `dist`. Example production build:

```sh
SITE_URL=https://trevoradairphotography.com PUBLISH_READY=true python3 scripts/build.py
python3 scripts/check.py
```

## Editing

| Location | Purpose |
|---|---|
| `src/config.json` | Contact details, social URLs, prices, testimonial approval |
| `scripts/build.py` | Page copy, service terms, layout templates and journal articles |
| `src/style.css` | OKLCH colors, spacing, responsive layouts and type |
| `src/app.js` | Mobile menu, gallery filters, accessible dialog and inquiry draft |
| `src/images.json` | Image descriptions, categories and available widths |
| `dist/assets/` | Committed optimized photography and self-hosted fonts |
| `docs/pricing-research.md` | Ten-photographer comparison and exact calculations |
| `docs/launch-and-seo.md` | Decisions to confirm and search growth roadmap |

Edit source, then rebuild. Do not hand-edit generated HTML. Image processing is optional and uses Pillow; `scripts/prepare_assets.py` records the original export process and requires the original source-photo paths to be updated on another computer. All optimized assets are already included, so it is not part of deployment.

## Inquiry behavior

GitHub Pages cannot send email by itself. The contact form validates details and prepares a real email draft addressed to Trevor. The visitor explicitly opens their email application and sends it, or copies the draft. It never shows a false “message sent” confirmation. Email and telephone links also work directly. A hosted form service can be integrated later after choosing its account and privacy terms. No secret belongs in this repository.

## Pages

Home; portfolio; families; couples and proposals; seniors and graduates; portraits and missionaries; events; investment; experience; about; contact; journal; three useful planning guides; privacy; 404.

All photography remains Trevor Adair's. Font redistribution is governed by the included SIL Open Font Licenses. This package is intended for Trevor's business, not resale of the photography.
