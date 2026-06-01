# Amul Stock Monitor Bot

Checks an Amul product page every 5 minutes and emails you when it's back in stock. Runs free on GitHub Actions — no server needed.

## Setup (5 minutes)

### 1. Fork this repo
Click **Fork** at the top right of this page.

### 2. Get a Gmail App Password
1. Enable 2-Step Verification on your Google account
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Create an app password (name it anything, e.g. "amul bot")
4. Copy the 16-character password shown

### 3. Add GitHub Secrets
Go to your forked repo → **Settings → Secrets and variables → Actions → New repository secret**

Add these 3 secrets:

| Secret name | Value |
|---|---|
| `AMUL_SENDER_EMAIL` | Your Gmail address (e.g. `you@gmail.com`) |
| `AMUL_SENDER_PASSWORD` | The 16-char App Password from step 2 |
| `AMUL_RECEIVER_EMAIL` | Where to send alerts (can be any email) |

### 4. Enable Actions
Go to the **Actions** tab → click **Enable GitHub Actions**.

That's it. The bot checks every 5 minutes automatically.

---

## Changing the product

By default it monitors:
```
https://shop.amul.com/en/product/amul-chocolate-whey-protein-34-g-or-pack-of-60-sachets
```

To monitor a different product, add a 4th secret:

| Secret name | Value |
|---|---|
| `AMUL_PRODUCT_URL` | Full URL of the Amul product page you want |

---

## Stopping the bot

Once you've placed your order, go to **Actions → Amul Stock Check → ⋯ → Disable workflow** to stop checks.
