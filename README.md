# Learn English From Zero Backend

This is a FastAPI backend project structured with best practices to provide a robust and scalable API for a "Learn English From Zero" application.

## Project Structure

The project follows a modular structure to separate concerns and improve maintainability:

```
.
├── app/                  # Main application module
│   ├── __init__.py       # Makes 'app' a Python package
│   ├── main.py           # FastAPI application entry point, includes routers
│   ├── dependencies.py   # For shared dependencies (e.g., database connection)
│   └── routers/          # Contains API route definitions
│       ├── __init__.py
│       └── items.py      # Example router for '/items' endpoints
├── tests/                # Unit and integration tests
│   ├── __init__.py
│   └── test_items.py     # Tests for the 'items' router
├── .gitignore            # Specifies intentionally untracked files to ignore
├── Procfile              # Declares process types for platforms like Railway
├── requirements.txt      # Lists Python project dependencies
└── README.md             # Project documentation (this file)
```

## Getting Started

Follow these steps to set up and run the project locally.

### 1. Local Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-github-repo-url>
    cd learn_english_from_zero_for_vietnamese_backend
    ```
    *(Replace `<your-github-repo-url>` with the actual URL of your GitHub repository)*

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 2. Running Locally

Once your environment is set up, you can run the FastAPI application:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The application will be accessible at `http://127.0.0.1:8000`. You can test the API endpoints:
*   `http://127.0.0.1:8000/`
*   `http://127.0.0.1:8000/items/`
*   `http://127.0.0.1:8000/docs` (for interactive API documentation)

## Deployment to Railway

This section guides you through deploying your FastAPI project to Railway with a custom domain.

### 1. Commit and Push Changes to GitHub

Before deploying, ensure your latest code is pushed to your GitHub repository.

1.  **Add all changes to staging:**
    ```bash
    git add .
    ```
2.  **Commit your changes:**
    ```bash
    git commit -m "feat: setup initial FastAPI project structure"
    ```
    *(Use descriptive commit messages following conventional commits if possible)*
3.  **Push to GitHub:**
    ```bash
    git push origin main
    ```
    *(Assuming your main branch is named `main`)*

### 2. Create a Railway Project

1.  **Log in to Railway:** Go to [railway.app](https://railway.app) and log in.
2.  **New Project:** Click "New Project" from your dashboard.
3.  **Deploy from GitHub Repo:** Select this option.
4.  **Configure GitHub App:** Grant Railway access to your `learn_english_from_zero_for_vietnamese_backend` repository.
5.  **Select Repository:** Choose your repository from the list. Railway will automatically detect it and suggest a service.

### 3. Configure the Service on Railway

Railway uses the `Procfile` and `requirements.txt` to deploy your application.

*   **Start Command:** Railway should automatically pick up the `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT` command from your `Procfile`. You can verify this in your service's **Settings** tab under the **Deploy** section.

### 4. Environment Variables (Optional but Recommended)

For production applications, store sensitive data and configurations in environment variables.

1.  Navigate to your service in Railway.
2.  Go to the **Variables** tab.
3.  Add any necessary variables (e.g., `DATABASE_URL`, `SECRET_KEY`).

### 5. Expose Application and Set Custom Domain (`learnenglishzero.io.vn`)

1.  **Generate Public Domain:** In your service's **Settings** tab, under **Networking**, click "Generate Domain" to get a free `.up.railway.app` URL.
2.  **Add Custom Domain:**
    *   In the **Settings** tab, scroll to **Custom Domains**.
    *   Enter `learnenglishzero.io.vn` and click "Add Domain".
    *   Railway will provide a **CNAME** record value (e.g., `my-service-xyz.up.railway.app`).
3.  **Configure DNS with Your Domain Provider:**
    *   Log in to your domain registrar (where you purchased `learnenglishzero.io.vn`).
    *   Go to the DNS management settings.
    *   Create a new **CNAME** record:
        *   **Host/Name**: `learnenglishzero` (or your subdomain prefix)
        *   **Value/Points to**: The CNAME value provided by Railway (e.g., `my-service-xyz.up.railway.app`).
    *   DNS propagation can take a few minutes to several hours. Once complete, your domain will show as "Connected" on Railway.

### 6. Testing the Deployment

1.  Once deployment completes on Railway, click on the generated Railway domain or your custom domain (`https://learnenglishzero.io.vn`).
2.  You should see the expected JSON response: `{"message": "Welcome to the Learn English API"}`.
3.  Check the **Deployments** tab in Railway for real-time logs and status updates.

### 7. Updating the Application

Railway is integrated with GitHub for continuous deployment.

1.  Make changes to your code locally.
2.  Commit and push your changes to the `main` branch of your GitHub repository:
    ```bash
    git add .
    git commit -m "feat: improve API endpoint X"
    git push origin main
    ```
3.  Railway will automatically detect the new commit and trigger a fresh deployment.

## Running Tests

To run the unit and integration tests for your project:

1.  Activate your virtual environment (if not already active).
2.  Run `pytest` from the project root:
    ```bash
    pytest
    ```

---

This `README.md` provides a complete guide for your project.
