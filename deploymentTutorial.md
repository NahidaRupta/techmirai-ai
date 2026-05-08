# TechMirai AI - Full Stack Application Deploy

# 🚀 How to Launch a Free Landing Page (Frontend static file only)

This guide explains, step-by-step, how to launch your landing page for **FREE** using GitHub Pages. It is written for beginners and does not require a Visa or any bank card.

---

## 📋 What You Need Before Starting
* **Computer/Laptop** & Internet connection
* **Email Address**
* **Domain Name:** `techmirai-ai.com`
* **Landing Page Files:** At least an `index.html` file

---

## 🛠️ Step-by-Step Instructions

### Step 1: Create a Free GitHub Account
1. Open [GitHub.com](https://github.com) in your browser.
2. Click on **Sign Up**.
3. Follow the prompts to enter your email, create a username, and password.
4. Verify your email.
5. *Note: No credit card is required.*

### Step 2: Create a New Repository
1. After logging in, click the **+** button at the top-right and select **New repository**.
2. **Repository Name:** `techmirai-ai`
3. Set Visibility to **Public**.
4. Click **Create repository**.

### Step 3: Upload Your Landing Page
1. Inside the repository, click the **uploading an existing file** link.
2. Drag and drop your files (ensure `index.html` is in the root folder).
3. Click **Commit changes**.

### Step 4: Enable GitHub Pages
1. Click **Settings** at the top of your repository.
2. Select **Pages** from the left sidebar.
3. Under **Branch**, select `main` (or `master`) and click **Save**.
4. Your site will soon be live at: `https://<your-username>.github.io/techmirai-ai/`

### Step 5: Connect Your Domain (`techmirai-ai.com`)
1. Log in to your domain provider (e.g., Namecheap, GoDaddy).
2. Go to **DNS Management** or **Advanced DNS**.
3. Add the following **A Records** (Point to GitHub IPs):
   - `185.199.108.153`
   - `185.199.109.153`
   - `185.199.110.153`
   - `185.199.111.153`
4. Add a **CNAME Record**:
   - **Host/Name:** `www`
   - **Value:** `<your-username>.github.io`
5. Save changes.

### Step 6: Add Custom Domain to GitHub
1. Go back to your GitHub repository **Settings** > **Pages**.
2. Under **Custom domain**, enter `techmirai-ai.com`.
3. Click **Save**.
4. Check **Enforce HTTPS** (it may take a few minutes/hours to become available).

---

## ✅ Final Result
- Your website is live at your own domain.
- HTTPS is enabled automatically for security.
- Hosting is **100% Free**.
- No banking details were ever shared.

---

## 📈 Future Upgrade (Optional)
When your website grows and you need more power (like professional email or server-side databases), you can move to paid hosting like Hostinger for around **$2–4 per month**.



# 🗄️ Render Database & Backend Deployment Guide

This guide provides the exact steps to provision a PostgreSQL database on Render, retrieve your connection string, and link it to your FastAPI web service.

---

## 1. Create the Database on Render
1. Log in to your **Render Dashboard**.
2. Click the **New +** button in the top right corner and select **PostgreSQL**.
3. Fill in the following details:
   - **Name:** `techmirai-db`
   - **Database:** `techmirai_db`
   - **User:** `techmirai`
   - **Region:** Choose the region closest to your users (e.g., Singapore).
   - **PostgreSQL Version:** Select `15` or `16`.
   - **Plan:** Select the **Free** plan.
4. Click **Create Database**.

---

## 2. Retrieve Your Connection String
Once the database status is **Available**:
1. Scroll down to the **Connections** section on the database info page.
2. Look for the **External Connection String**.
3. Click the **Copy** icon. 
   > **Note:** Use the **External** string for connecting from your ThinkPad (local testing) or GitHub. Use the **Internal** string only if your Backend Service is also hosted on Render.

---

## 3. Deploy the Web Service
1. On the Render Dashboard, click **New +** and select **Web Service**.
2. Choose **Build and deploy from a Git repository**.
3. Connect your `techmirai-ai` repository.

### Service Configuration:
- **Name:** `techmirai-backend`
- **Region:** Use the **same region** as your database.
- **Branch:** `main`
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

---

## 4. Link the Database (Crucial Step)
Before finishing the setup, you must connect the backend to the database:
1. Scroll to the **Environment Variables** section.
2. Click **Add Environment Variable**.
3. **Key:** `DATABASE_URL`
4. **Value:** Paste the **External Connection String** you copied in Step 2.
5. Click **Create Web Service**.

---

## ⚠️ Important Notes
* **Free Tier Limits:** Render Free databases expire after **30 days**. Ensure you back up your data or upgrade if the project becomes permanent.
* **Spin-up Time:** Free services "spin down" after inactivity. The first request after a break may take 30+ seconds to process.

## Send  Enail nitification:
On Render: Go to your Web Service -> Environment tab.

Add these new keys (if you haven't yet):

SMTP_USER = nahida.rahaman37@gmail.com

SMTP_PASSWORD = rwjedgalrhxnqjth

ADMIN_EMAIL = nahida.rahaman37@gmail.com

SMTP_SERVER = smtp.gmail.com

SMTP_PORT = 587