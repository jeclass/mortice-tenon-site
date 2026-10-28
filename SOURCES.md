# Sources for every claim on the site

Rule: nothing goes on the site unless it is in one of these sources. No prices (they change), no ratings or review counts, no sales or customer counts, no "USA" or "aerospace" wording.

Checked 2026-10-27 by Reggie (Mortice & Tenon agent).

## Source key

| Key | Source |
|---|---|
| ZIP-LABEL | Approved zip anchor labels, `~/mt-data/labels/FINAL2-2026-10-13/Zip Anchor {10,25,50,100}pk.pdf` (sent to supplier 2026-10-13 on Josh's "send"). Text extracted with PyMuPDF. |
| EA-LABEL | Approved Easy Anchor labels, `~/mt-data/labels/EA-RESIZE-2026-10-27/v2/Easy Anchor {2,5,10,20}pk.pdf` (wording identical to FINAL2). |
| BRAIN-ZIP | Brand brain `pages/products/zip-anchors-nylon66.md` (status: canonical) |
| BRAIN-EA | Brand brain `pages/products/easy-anchor-toggles.md` (status: canonical) |
| BRAIN-BRAND | Brand brain `pages/brand-overview.md` (status: canonical): Amazon US, FBA |
| UPC-REG | `~/mt-data/brand-docs/barcode-registry.csv`, cross-checked with the decoded barcodes in the two label manifests (`FINAL2-2026-10-13/manifest.csv`, `EA-RESIZE-2026-10-27/v2/manifest.csv`): all 8 match |
| AMZ-TITLE | Our own live Amazon listing titles, read 2026-10-27 (all 8 ASINs returned HTTP 200, "In Stock") |
| BRIEF | Josh's request as relayed by the main agent, 2026-10-27 (email address, no phone, Class Sales LLC, Amazon store URL) |
| GH-DOCS | GitHub Docs (Pages hosting, IP logging) |

## Claims

| Claim on the site | Where | Source |
|---|---|---|
| Zip anchors are "Reinforced Nylon 66" | Home, Products, Install, Line card | BRAIN-ZIP; AMZ-TITLE |
| Zip anchors are self-drilling ("Self drilling zip drywall anchors") | all | ZIP-LABEL heading |
| Zip anchors hold up to 90 lb in 1/2 in drywall | all | ZIP-LABEL "Will hold up to 90 pounds in 1/2" drywall"; BRAIN-ZIP "rated 90 lb". Basis: Josh's own weight test (held over 120 lb), see brain inbox `2026-10-21-mtagent-change-josh-decisions-insurance-label-claims.md` |
| Zip: use on drywall, hollow walls, sheet rock and plastered walls | Home, Products, Install, Line card | ZIP-LABEL band |
| Zip install steps 1–4 (exact wording) | Install | ZIP-LABEL 50pk/100pk (the 10/25pk labels say the same steps in 3–4 panels) |
| Items required: screwdriver or drill, #2 Phillips | all | ZIP-LABEL and EA-LABEL "ITEMS REQUIRED" |
| Zip packs: 10, 25, 50, 100; anchors with screws | Products, Line card | BRAIN-ZIP ("with screws", 4 packs); AMZ-TITLE (10/25/50: "N anchors and N screws") |
| Easy Anchor is a self-drilling toggle anchor | all | EA-LABEL "SELF-DRILLING TOGGLE ANCHORS" |
| Easy Anchor holds up to 100 lb in 1/2 in drywall | all | EA-LABEL "Holds up to 100 lb in 1/2 in drywall"; BRAIN-EA "holds 100 lb" |
| Easy Anchor: anchor 2-1/2 in, screws #8 × 2-1/8 in | Home, Products, Install, Line card | EA-LABEL icon ring "Anchor: 2-1/2 in · Screws: #8 × 2-1/8 in"; listing image `New Easy Anchor/01-04-23.jpg` (2-1/2" anchor, 2-1/8" screw). See open question: listing titles say "#8 x 2-1/2"" |
| Easy Anchor packs: 2, 5, 10, 20; "N anchors + N screws" | Products, Line card | EA-LABEL "2 ANCHORS + 2 SCREWS" etc.; BRAIN-EA |
| Toggle opens behind the wall when the screw pops forward | Home, Products, Install | EA-LABEL step 3 |
| Easy Anchor install steps 1–4 (exact wording) | Install | EA-LABEL |
| Avoid studs and wires | Products, Install | EA-LABEL step 1 |
| Made in China | Products, About, Line card | ZIP-LABEL and EA-LABEL distributor block |
| ASINs (8) | Products, Wholesale, Line card | BRAIN-ZIP, BRAIN-EA, UPC-REG; AMZ-TITLE (all live) |
| UPCs (8) | Wholesale, Line card | UPC-REG = label manifests (see open question on EA 10pk) |
| Every retail pack carries a UPC barcode | Wholesale | ZIP-LABEL, EA-LABEL (barcodes decode to the UPCs) |
| Sold on Amazon and fulfilled by Amazon; Amazon ships orders and handles delivery and returns | Home, Products, About, Contact | BRAIN-BRAND ("Amazon US, FBA") |
| Screws in every pack | Home | BRAIN-ZIP, EA-LABEL |
| Email sales@morticeandtenon.us; no phone | all | BRIEF |
| Brand of Class Sales LLC | footer, About, Privacy, Line card | BRIEF; brain inbox `2026-10-07-mtagent-brand-identity.md` (unverified) — **confirm with Josh** |
| Hosted on GitHub Pages; GitHub logs visitor IPs for security | Privacy | GH-DOCS ("About GitHub Pages" / GitHub Privacy Statement) |
| No cookies, analytics, trackers, forms; fonts/images self-hosted | Privacy | The site code itself (verify: `grep -ri "script\|iframe\|http" docs/*.html`) |
| A mortice and tenon is a woodworking joint | About | General knowledge (definition) |

## Images

| File(s) in `docs/assets/img/` | Source (all owned by Mortice & Tenon) |
|---|---|
| `products/zip-10-*`, `zip-25-*`, `zip-50-*` | `Amazon Pics/Zip Anchors/Zip Anchor {10,25,50} Pack/ZipSelfDrillingAnchor N Hero Image - jpg 1500x1500 px.jpg` = the live Amazon main images |
| `products/zip-100-*` | `Amazon Pics/Zip Anchors/updated 100 pack hero.jpg` = live main image |
| `products/ea-5-*`, `ea-10-*` | `Amazon Pics/New Easy Anchor/01-02-24 (1).jpg`, `01-01-27 (1).jpg` = live main images |
| `products/ea-2-*`, `ea-20-*` | `Amazon Pics/New Easy Anchor/ChatGPT Image Jul 17, 2026, 12_26_48 PM.png` / `01_59_33 PM.png` = live main images (AI-generated for M&T) |
| `install/zip-step-*.webp` | Cropped from ZIP-LABEL 100pk (our own label art) |
| `install/ea-step-*.webp` | Cropped from EA-LABEL 20pk v2 (our own label art) |
| `logo.svg`, `mark.svg`, favicons, `icon-512.png` | `logos/logo-pdf 1b.pdf` (vector primary logo) |
| `og-card.jpg` | Composed from the logo and two of the main images above |

Not used: `Website pics/` and `Shutterstock/` (license unknown), listing infographics with unverifiable claims ("100,000 homes", "100,000+ sold", "15 lbs more", "60 seconds"), A+ images ("USA BRAND", "Aerospace Grade").

Fonts: Arvo Bold and Outfit (variable), both SIL Open Font License 1.1, served unmodified as WOFF2; licenses in `docs/assets/fonts/OFL-*.txt`.
