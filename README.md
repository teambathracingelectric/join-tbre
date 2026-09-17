# TBRe 27 sign-up page: handoff

Static sign-up page for TBRe 27 recruitment. One HTML file plus images. No build step, no framework, no server. Works on phones, tablets and laptops.

Flow: QR code -> sign-up form -> thank-you page (WhatsApp link, Intro Talk, taster sessions, about the team, FAQ).

Live at **join.teambathracingelectric.com**.

## What's in the repo

```
join-tbre/
  index.html      the whole page (HTML, CSS, JS in one file)
  img/
    hero.jpg          desktop hero (Hockenheim wide shot)
    hero_mobile.jpg   phone hero (portrait crop of the panning shot)
    team.jpg          team photo, about section
    redbull.jpg       car next to the Red Bull F1 car, about section
    logo.png          colour logo (favicon)
    logo_white.png    white logo (hero and footer)
  README.md                       this file (not served)
  wrangler.jsonc                  Cloudflare config (not served)
  .assetsignore                   what Cloudflare leaves off the site
  .github/workflows/deploy.yaml   deploys on every push to main
```

Companion file, kept in the TBRe Teams channel: `TBRe27 Signups.xlsx`. The page writes into it via Power Automate (see step 2).

## Everything you might need to change

Open `index.html`. The `CONFIG` block near the top holds every value that changes:

| Key | What it is | Current state |
|---|---|---|
| `endpoint` | Power Automate HTTP trigger URL | empty until step 2 is done. While empty the form skips saving and goes straight to the thank-you page |
| `whatsapp` | TBRe 27 community invite link | set |
| `intro.date` `intro.time` `intro.room` | Intro Talk as shown on the page | Thu 1 Oct 2026, 18:15 to 19:15, CB 1.10 |
| `intro.startISO` `intro.endISO` | same event in UTC for the calendar file (BST = UTC+1) | 20261001T171500Z / 20261001T181500Z |
| `sessions` | the five tasters: label, title, room, date, start, end (UK local time) | set |
| `website` `instagram` `linkedin` `email` | footer links | check the Instagram and LinkedIn URLs are right before going live |

Everything else (headline, FAQ answers, about text) is plain text in the HTML. Search for it and edit.

Open item: the hero headline "Build the car. Race the car." is to be replaced. Vince has options to pick from.

## Step 1: hosting

Deployed the same way as the website and Log Studio: GitHub Actions runs `wrangler deploy` on every push to `main`, and Cloudflare serves the repo root as a static Worker at join.teambathracingelectric.com. Wrangler creates the DNS record on the first deploy. Nothing is set up in the Cloudflare dashboard.

The full team process is in GitLab: `tbre-ai/team-knowledge/processes` → `Web Development/Deploying with Cloudflare.md`. Follow that if it and this summary ever differ.

One-off: the repo must be on the repository list of the organisation secrets `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` (GitHub org → Settings → Secrets and variables → Actions). Without that, the Actions run goes green but prints a notice that nothing was deployed.

To update the page: branch, edit, open a pull request, merge. The merge deploys it.

## Step 2: connect the Excel (Power Automate)

Do this after hosting, then redeploy with the URL filled in.

1. Put `TBRe27 Signups.xlsx` in the TBRe Teams channel (Files tab). Don't rename the sheet `Signups`, the table `Signups`, or the seven column headers. The flow maps by name.
2. Go to make.powerautomate.com with a Bath account.
3. Create > Instant cloud flow > skip the name prompt > trigger **When an HTTP request is received**.
   - Who can trigger the flow: **Anyone**.
   - Request body JSON schema:
     ```json
     {"type":"object","properties":{
       "name":{"type":"string"},"email":{"type":"string"},"course":{"type":"string"},
       "year":{"type":"string"},"interest":{"type":"string"},
       "submitted":{"type":"string"},"source":{"type":"string"}}}
     ```
4. New step > **Excel Online (Business)** > **Add a row into a table**.
   - Location: the SharePoint site behind the Teams channel. Document library: Documents. File: `TBRe27 Signups.xlsx`. Table: `Signups`.
   - Map each column to the field of the same name from the trigger (dynamic content).
5. Save. Reopen the trigger; it now shows the **HTTP POST URL**. Copy it.
6. Paste it into `CONFIG.endpoint` in `index.html` (inside the quotes). Merge to `main`; it redeploys.

If the tenant blocks the HTTP trigger as a premium connector, tell Vince: fallback is a Microsoft Form behind the page.

The page sends one JSON object per sign-up:

```json
{"name":"Sam Taylor","email":"st123@bath.ac.uk","course":"Mechanical Engineering",
 "year":"1st year","interest":"Mechanical, Software","submitted":"2026-09-25T13:02:11.000Z","source":"qr"}
```

`interest` is a comma-separated list (multi-select) or empty. `source` is `qr` unless the link had `?src=...` on it (e.g. `?src=insta` for the Instagram bio link), so you can see where sign-ups came from. The `Summary` sheet in the workbook counts by year, interest and source automatically.

## Step 3: test end to end

1. Open the live URL on a phone.
2. Submit a test entry. Confirm it lands as a row in the Excel within a few seconds.
3. Tap the WhatsApp button, confirm it opens the TBRe 27 community.
4. Tap "Add to calendar" on the Intro Talk and on one taster. Confirm times show as 18:15 and the right taster time in the phone's calendar.
5. Delete the test row from the Excel.

## Step 4: QR code

Only once the URL is final. The QR encodes the exact address, so a change means reprinting. Ask Vince or generate one from the final URL; print the short URL under it for people whose camera won't scan.

## Useful URLs on the page

- `.../#welcome` opens the thank-you page directly without submitting. Pin this in the WhatsApp for people already signed up.
- `.../?src=insta`, `.../?src=poster` etc. tag the sign-up's source.
- "Already signed up? Skip to the info page" under the form does the same as `#welcome`.

## Notes

- The page loads one font (IBM Plex Sans) from Google Fonts; everything else is local.
- If the form fails to save it retries once, then tells the person to join the WhatsApp instead. It never blocks them.
- Calendar files are one-way: changing the room on the page does not update calendars people already imported. Room changes go via WhatsApp and an Outlook invite to the emails in the Excel.
- All images are under 300 KB each. Total page weight is about 1.2 MB on first load.
