# Korena Pharmacy PharmaLedger — Universal Installable PWA

## What this is
Installable PWA for Windows, macOS, Android phones/tablets, and iPhone/iPad, using the **same Flask backend and PostgreSQL database**. No GitHub required. It is not a native APK, EXE or iOS IPA. Accounting actions require connectivity.

## Option A: Local demonstration, same Wi-Fi
1. Install Docker Desktop on Windows. Open the `Korena_JLT` folder.
2. Copy `.env.server.example` to `.env`; replace all placeholders with **new** strong secrets. Set `KORENA_HTTPS=0` for local HTTP testing only.
3. Run `docker compose up --build -d` in the `Korena_JLT` folder.
4. On the server laptop, visit `http://localhost:8000` and sign in using configured administrator account. Data is retained in the named `korena_postgres` Docker volume.
5. For testing from other devices, edit `compose.yaml` app ports from `127.0.0.1:8000:8000` to `8000:8000`, configure Windows firewall to permit TCP 8000 on **private network only**, and open `http://<laptop-LAN-IP>:8000`.
6. **Note**: HTTP on a LAN IP is not a secure context, so PWA installation/service workers will typically NOT work on mobile using that address. The app remains usable as a web page for demos. For actual installation you need HTTPS with a trusted certificate.

## Option B: Public HTTPS installation, no GitHub
1. Use a Linux VPS or hosting provider that supports Docker, persistent storage, and HTTPS. Deploy by uploading the `Korena_JLT` folder using SFTP/SCP rather than GitHub (e.g. `scp -r Korena_JLT user@server:/opt/`).
2. Use a real domain (e.g. a pharmacy-owned subdomain) and a reverse proxy (Caddy/nginx) that terminates HTTPS using a trusted certificate. Do NOT expose PostgreSQL to the internet.
3. Copy `.env.server.example` to `.env` on the server, set strong credentials, `KORENA_HTTPS=1`, and configure `compose.yaml` to keep HTTP app internal to the reverse proxy (for example, bind port 8000 to 127.0.0.1 and proxy to it). Run `docker compose up --build -d`. PostgreSQL lives in a persistent Docker named volume.
4. Check `https://YOUR-DOMAIN/health` then log in, test debit/credit, ledger, trial balance and audit integrity, and set up PostgreSQL backups and update procedures before entering real pharmacy data.
5. On Android / supported desktop Chrome/Edge: visit the HTTPS URL, use **Install app** prompt or browser Install option.
6. On iPhone/iPad: open the HTTPS address in Safari, tap **Share → Add to Home Screen** then **Add**.
7. Installed apps connect to the same server; internet access is required for accounting operations. This PWA does not synchronize offline edits.

## Data security and migration
- This deployment initializes a NEW central PostgreSQL database; the previous offline SQLite records are NOT automatically imported.
- Never publish `.env`, real credentials, or live pharmacy financial data. Rotate any password previously shared in chat.
- `INITIAL_ADMIN_PASSWORD` creates the first administrator on an empty database; it will not reset an existing account.
- PostgreSQL access and HTTPS setup must be reviewed before production use. Set firewall, backups, strong passwords, secure cookies and access controls.
- A PWA installed on multiple devices is one shared application, not multiple separate local databases.
