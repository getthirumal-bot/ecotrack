# Point ecotrack.ltd to Railway

You have the domain **ecotrack.ltd** at GoDaddy. Use one of the options below so it opens your Ecotrack app on Railway.

---

## Step 0: Add the domain in Railway (do this first)

1. Go to **https://railway.app** → your project → your **web service**.
2. Open **Settings** → **Networking** → **Public Networking**.
3. Under **Custom Domains**, click **Add custom domain**.
4. Enter **ecotrack.ltd** and add it. Add **www.ecotrack.ltd** as well (so both work).
5. Railway will show the **CNAME target** (e.g. `web-production-b5c33.up.railway.app`). You will use this in DNS.

---

## Option A: GoDaddy only (www only, then redirect root to www)

GoDaddy does **not** allow a CNAME on the root (@), so you can only point **www.ecotrack.ltd** directly to Railway. Then use GoDaddy forwarding so **ecotrack.ltd** redirects to **www.ecotrack.ltd**.

### In GoDaddy DNS

1. Go to **https://dcc.godaddy.com** → **My Products** → **ecotrack.ltd** → **DNS** (or **Manage DNS**).
2. **Add a CNAME record:**
   - **Type:** CNAME  
   - **Name:** `www`  
   - **Value:** (paste the Railway CNAME target, e.g. `web-production-b5c33.up.railway.app`)  
   - **TTL:** 600 or 1 hour  
   - Save.

### Forward root to www (optional)

1. In GoDaddy, go to **ecotrack.ltd** → **Forwarding** (or **Domain Forwarding**).
2. Add forwarding: **ecotrack.ltd** → **https://www.ecotrack.ltd** (301 permanent).
3. Save. After DNS propagates, visiting **ecotrack.ltd** will redirect to **www.ecotrack.ltd**, which loads your app.

### In Railway

- Add custom domains **ecotrack.ltd** and **www.ecotrack.ltd** (Step 0).  
- For **ecotrack.ltd**, Railway may show “needs CNAME” — with Option A you’re only giving Railway **www** via CNAME; root is handled by GoDaddy forwarding. If Railway doesn’t verify **ecotrack.ltd**, you can leave only **www.ecotrack.ltd** in Railway and rely on forwarding for the root.

---

## Option B: Use Cloudflare DNS (both ecotrack.ltd and www.ecotrack.ltd)

You keep the domain **registered** at GoDaddy but use **Cloudflare** for DNS. Then you can point both **ecotrack.ltd** and **www.ecotrack.ltd** to Railway.

### 1. Add site in Cloudflare

1. Go to **https://dash.cloudflare.com** → **Add a site** → enter **ecotrack.ltd**.
2. Choose the **Free** plan.
3. Cloudflare will show **two nameservers** (e.g. `ada.ns.cloudflare.com` and `bob.ns.cloudflare.com`). Copy them.

### 2. Change nameservers at GoDaddy

1. Go to **GoDaddy** → **My Products** → **ecotrack.ltd** → **Manage** → **Nameservers**.
2. Choose **Change** / **Custom** and replace with Cloudflare’s two nameservers.
3. Save. Propagation can take from a few minutes up to 24–48 hours.

### 3. In Cloudflare DNS

1. In Cloudflare, open **ecotrack.ltd** → **DNS** → **Records**.
2. Remove any conflicting A or CNAME for `@` if present.
3. **Add CNAME for root:**
   - **Type:** CNAME  
   - **Name:** `@`  
   - **Target:** (Railway CNAME target, e.g. `web-production-b5c33.up.railway.app`)  
   - **Proxy status:** DNS only (gray cloud) — recommended so Railway can issue SSL.
4. **Add CNAME for www:**
   - **Type:** CNAME  
   - **Name:** `www`  
   - **Target:** (same Railway CNAME target)  
   - **Proxy status:** DNS only (gray cloud).
5. Save.

### 4. In Railway

- Add custom domains **ecotrack.ltd** and **www.ecotrack.ltd** (Step 0).  
- After DNS propagates, Railway will see the CNAMEs and issue SSL. Both **https://ecotrack.ltd** and **https://www.ecotrack.ltd** will open your app.

---

## After DNS is set

- Propagation can take from a few minutes to 24–48 hours (sometimes up to 72).
- Railway will issue HTTPS automatically (Let’s Encrypt). If it stays “Validating”, wait for DNS and ensure no proxy (or use “DNS only” in Cloudflare).
- Test: **https://www.ecotrack.ltd** (and **https://ecotrack.ltd** if you used Option B or forwarding).

---

## Quick reference

| Goal                         | Where        | What to do |
|-----------------------------|-------------|------------|
| Add domain in Railway       | Railway → Service → Settings → Networking | Add **ecotrack.ltd** and **www.ecotrack.ltd** |
| CNAME for www (GoDaddy)     | GoDaddy DNS | CNAME **www** → Railway target |
| Forward root to www         | GoDaddy     | Forward **ecotrack.ltd** → **https://www.ecotrack.ltd** |
| Both @ and www (no redirect)| Cloudflare  | Use Cloudflare DNS; CNAME **@** and **www** → Railway target |

Your Railway CNAME target is the one shown in Railway after you add the custom domain (e.g. **web-production-b5c33.up.railway.app** — no `https://`, no path).
