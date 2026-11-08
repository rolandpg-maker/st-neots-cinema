# St Neots Cineworld: phone-friendly listings

An unofficial, personal, mobile-friendly web app showing **all Cineworld St Neots films and screening times**, organised into cinema weeks from **Friday to Thursday**.

## What it does
- Opens on today's date, with a full Friday-to-Thursday day picker.
- Displays all films and times on one page, either alphabetically by film or by earliest showing.
- Retains previously collected dates within the current cinema week, even after those dates disappear from the live rolling listings.
- Collects new showtimes automatically four times a day through GitHub Actions and publishes updates to GitHub Pages.
- No login is needed to view the finished app on a phone.

**Limitations:** The source publishes all film showtimes, but not which physical screen (1 to 6) each film uses. Listings are provided by GoFilm, not directly by Cineworld. They can be corrected or altered; check Cineworld before travelling. Scheduled GitHub workflows are not guaranteed to run exactly on time. The scraper relies on the source website's headings and may need adjusting if its structure changes.

## Put it on your phone via GitHub Pages

1. On GitHub, make a new **public** repository, e.g. `st-neots-cinema`. Unzip this project, then upload all files and directories **including `.github/workflows/update.yml`** to that repository. Ensure hidden `.github` folder is included.
2. Under **Settings → Pages**, choose **Source: GitHub Actions** (not “Deploy from a branch”).
3. Under **Settings → Actions → General → Workflow permissions**, ensure GitHub Actions can write to the repository. Workflow permissions are also declared in the YAML, but organisation policies may override them.
4. Under **Actions → Refresh St Neots listings**, choose **Run workflow** once. When the workflow succeeds, visit `https://YOUR-GITHUB-USERNAME.github.io/st-neots-cinema/` (substitute your own account and repo names). GitHub also displays the exact deployment URL under **Settings → Pages**.
5. Open that URL on your phone. On iPhone, Share → Add to Home Screen. On Android, browser menu → Add to Home Screen / Install app.

The initial `docs/showtimes.json` contains a sourced snapshot of **6–12 November 2026**. Running the workflow fetches the latest available dates. The weekly Friday-to-Thursday view changes automatically. The scraper collects future/past accessible dates as the source publishes them and keeps recent dates in its JSON file.

## Project files

- `docs/index.html` - mobile web application
- `docs/showtimes.json` - data cache, updated by automation
- `scripts/update_listings.py` - source parser
- `.github/workflows/update.yml` - automatic refresh and GitHub Pages deployment

Data source: https://gofilm.uk/towns/st-neots . Cineworld confirmation: https://www.cineworld.co.uk/cinemas/x0tvc-cineworld-cinema-st-neots/

This project is not affiliated with Cineworld or GoFilm.
