# FastAPI Backend Deployment on Railway

This guide provides a complete step-by-step checklist for deploying this FastAPI backend to Railway, connecting it to the custom subdomain `api.learnenglishzero.io.vn`, and configuring it for use with a frontend.

## Deployment Checklist

### **Phase 1: Local Testing**

Before deploying, always test your changes locally.

1.  **Activate your virtual environment:**
    ```bash
    source venv/bin/activate
    ```

2.  **Run the local server:**
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```

3.  **Test the new endpoint:**
    Open your browser or use a tool like `curl` to access `http://127.0.0.1:8000/items/hello`.
    ```bash
    curl http://127.0.0.1:8000/items/hello
    ```
    You should see the following JSON response, confirming the endpoint works:
    ```json
    {"message":"Hello from learnenglishzero API!"}
    ```

### **Phase 2: Commit and Push to GitHub**

Railway deploys directly from your GitHub repository. Ensure your latest changes are pushed.

1.  **Stage your changes:**
    ```bash
    git add .
    ```

2.  **Commit the changes:**
    ```bash
    git commit -m "feat: add /hello endpoint and CORS configuration"
    ```

3.  **Push to your main branch:**
    ```bash
    git push origin main
    ```

### **Phase 3: Railway Deployment and Configuration**

Now, let's set up the project on Railway.

1.  **Create a New Project on Railway:**
    *   Log in to [railway.app](https://railway.app).
    *   Click **New Project** and select **Deploy from GitHub repo**.
    *   Choose your repository. Railway will automatically create a service.

2.  **Set Environment Variables:**
    Your application needs secrets and configuration to run properly. **Never hardcode secrets in your source code.**
    *   In your Railway service, go to the **Variables** tab.
    *   Add your secrets as new variables. It's good practice to add placeholders even if you don't have the final values yet.
        *   `DATABASE_URL`: `postgresql://user:pass@host:port/db`
        *   `SECRET_KEY`: `your-super-secret-key-that-is-very-long`
        *   `OPENAI_API_KEY`: `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
    *   *Description*: The variables page in Railway is a simple key-value store. You type the name on the left and the value on the right.

3.  **Verify the Start Command:**
    Railway uses the `Procfile` to determine how to run your app.
    *   Go to the **Settings** tab in your service.
    *   Under the **Deploy** section, confirm the **Start Command** is being read from the `Procfile`: `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`.

4.  **Configure the Custom Subdomain (`api.learnenglishzero.io.vn`):**
    This is how you make your API accessible from a clean, professional URL.
    *   **Step A: Generate a Public Domain on Railway**
        *   In your service's **Settings** tab, under the **Networking** section, click **Generate Domain**. Railway will give you a temporary public URL like `my-app-production.up.railway.app`.
    *   **Step B: Add Your Custom Subdomain on Railway**
        *   In the same **Networking** section, find **Custom Domains**.
        *   Enter `api.learnenglishzero.io.vn` and click **Add Domain**.
        *   Railway will show you a **CNAME** record value to use. It will look similar to the public domain you just generated. **Copy this value.**
    *   **Step C: Create a CNAME Record at Your Domain Registrar**
        *   Log in to the control panel where you manage your `io.vn` domain.
        *   Navigate to the DNS management or DNS records section.
        *   Create a **new CNAME record** with the following details:
            *   **Type:** `CNAME`
            *   **Host** (or **Name**): `api` (This represents the `api.` part of your subdomain)
            *   **Value** (or **Points to**): Paste the CNAME value you copied from Railway (e.g., `my-app-production.up.railway.app`).
            *   **TTL (Time to Live):** You can usually leave this at the default setting (e.g., 1 hour or "Automatic").
        *   Save the new DNS record.

### **Phase 4: Verify Deployment**

1.  **Check Deployment Status:**
    *   Wait for Railway to complete the deployment. You can monitor the progress in the **Deployments** tab.
    *   Check the deployment logs for any errors.

2.  **Test the API Endpoint:**
    *   Once DNS propagation is complete (this can take from a few minutes to a few hours), open your browser or use `curl` to test your new live endpoint:
        ```bash
        curl https://api.learnenglishzero.io.vn/items/hello
        ```
    *   **Success!** You should see the same JSON response as you did locally:
        ```json
        {"message":"Hello from learnenglishzero API!"}
        ```
    *   This also confirms your frontend at `https://learnenglishzero.io.vn` will be able to call this API without CORS errors.

### **Phase 5: Future Updates and Best Practices**

1.  **Updating the Backend:**
    Your project is set up for continuous deployment. To update the app, simply push new commits to your `main` branch on GitHub. Railway will automatically detect the changes and redeploy your application.
    ```bash
    git add .
    git commit -m "feat: add new user endpoint"
    git push origin main
    ```

2.  **Best Practices for Railway's Free Tier:**
    *   **Sleep Mode:** Services on the free "Starter" plan will sleep after a period of inactivity. The first request after a sleep period will be slower as the service wakes up. This is generally fine for development and hobby projects.
    *   **Connection Limits:** Be mindful of database connection limits. Ensure your code properly closes database connections after use.
    *   **Logging:** Use the **Deployments** tab in Railway to view logs. If you encounter issues (like CORS errors), the logs are the first place to look for clues. `print()` statements in your Python code will also appear here.

---
This checklist provides everything you need to get your backend live.