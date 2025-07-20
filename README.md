# Full-Stack Django + React Template

This is a powerful, production-ready template for building modern web applications. It features a Django and Django REST Framework backend with a decoupled React frontend built with Vite and Mantine. The entire application is containerized with Docker and ready for automated deployment with GitHub Actions.

The architecture is designed to be a self-contained monorepo where the React frontend is built and then served as static files by the Django backend, simplifying deployment to a single server instance.

## Features

- **Backend (Django):**

  - Django 4+ with a production-ready settings structure.
  - Django REST Framework for building powerful APIs.
  - JWT Authentication using `djangorestframework-simplejwt` with access and refresh tokens.
  - Custom User model using **email as the primary identifier**.
  - Production-grade web server setup with Gunicorn.
  - Efficient static file serving in production using WhiteNoise.
  - Environment variable management with `django-environ`.
  - Automatic code formatting with **Black** and **isort**.

- **Frontend (React):**

  - Modern frontend stack with **React 18** and **Vite**.
  - **Mantine UI** component library for rapid, beautiful UI development.
  - **Axios** instance with interceptors for automatically handling API requests and JWT refresh logic.
  - Global authentication state management via React Context.
  - Protected routes for authenticated users.
  - Automatic code formatting with **Prettier** and **ESLint**.

- **DevOps & Workflow:**
  - **Dockerized** multi-stage build for a small, secure production image.
  - **Docker Compose** for easy local development and production orchestration.
  - **GitHub Actions** CI/CD pipeline for automated builds and deployments on push to `main`.
  - **Nginx** configured as a high-performance reverse proxy.
  - **VS Code Settings** pre-configured for automatic formatting on save for both Python and JavaScript/React.

## Getting Started (Local Development)

Follow these steps to get a local development environment up and running.

### Prerequisites

- Python 3.11+ and `pip`
- Node.js 22+ and `npm`
- Docker and Docker Compose (Optional, but recommended for mirroring production)

### 1. Initial Setup

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd <your-project-directory>
    ```

2.  **Set up the Backend:**

    ```bash
    # Navigate to the backend directory
    cd backend

    # Create and activate a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

    # Install Python dependencies
    pip install -r requirements.txt

    # Run database migrations
    python manage.py migrate
    ```

3.  **Set up the Frontend:**

    ```bash
    # Navigate to the frontend directory
    cd ../frontend

    # Install Node.js dependencies
    npm install
    ```

### 2. Running the Development Servers

If you want to test the Docker container, you will need to go through the following steps.

- **Run the Django Backend Server:**

  ```bash
  # From the backend/ directory, with your venv activated
  python manage.py runserver
  # Backend will be available at http://127.0.0.1:8000
  ```

- **Run the React Frontend Server:**
  ```bash
  # From the frontend/ directory
  npm run dev
  # Frontend will be available at http://127.0.0.1:5173
  ```
  The Vite dev server is already configured to proxy API requests to `http://127.0.0.1:8000`.

### 3. Running the Docker Container

You will need to run two separate servers for local development to enjoy hot-reloading.

```bash
# Navigate to the backend diretory and copy the .env.example file. Configure variables as needed
cp .env.example .env

# Navigate to the root directory and build the Docker image
docker-compose build

# Run the database migrations
docker-compose run --rm web python manage.py migrate

# Start the container
docker-compose up -d

# (Optional) Check the process and monitor logs
docker-compose ps
docker-compose logs -f web

# Cleanup
docker-compose down -v
```

## New Project Configuration

When you use this template to start a new project, you should configure the following:

1.  **Backend Environment (`backend/.env`):**

    - **`SECRET_KEY`**: Generate a new secret key. You can use an online generator or Django's `get_random_secret_key()` function.
    - **`DEBUG`**: Should be `True` for development.
    - **`DJANGO_SETTINGS_MODULE`**: Should be `backend.settings.development`.

2.  **Frontend Environment (`frontend/.env.development`):**

    - **`VITE_APP_API_URL`**: Ensure this is set to your Django development server URL (`http://localhost:8000/api`).

3.  **`ALLOWED_HOSTS`:** In `backend/backend/settings/development.py`, ensure `127.0.0.1` and `localhost` are present.

## Production Deployment

This template is designed for automated deployment to a single Linux server.

### Prerequisites

- A server with SSH access (e.g., an Ubuntu 22.04 VPS).
- Docker and Docker Compose installed on the server.
- Nginx installed on the server.
- A domain name pointed at your server's IP address.

### Step 1: GitHub & Docker Hub Setup

1.  **Create GitHub Repository:** Push your new project to its own GitHub repository.

2.  **Create Docker Hub Repository:** Create a new public or private repository on [hub.docker.com](https://hub.docker.com/).

3.  **Set GitHub Secrets:** In your GitHub repository settings under `Settings > Secrets and variables > Actions`, add the following repository secrets:
    - `DOCKER_USERNAME`: Your Docker Hub username.
    - `DOCKER_PASSWORD`: Your Docker Hub password or access token.
    - `SSH_HOST`: Your server's domain name or IP address.
    - `SSH_USERNAME`: The user to log in as on your server (e.g., `ubuntu`).
    - `SSH_PRIVATE_KEY`: The private SSH key for accessing your server.

### Step 2: Server-Side Setup

1.  **Clone the Project on the Server:**

    ```bash
    git clone <your-repository-url>
    cd <your-project-directory>
    ```

2.  **Create Production Environment File:** On your server, inside the `backend/` directory, create the production `.env` file. **DO NOT COMMIT THIS FILE.**

    ```bash
    # backend/.env
    SECRET_KEY=your_new_production_secret_key
    DEBUG=False
    DJANGO_SETTINGS_MODULE=backend.settings.production
    DATABASE_URL=sqlite:////app/db.sqlite3 # Path inside the container
    ```

3.  **Place Docker Compose File:** Ensure the `docker-compose.yml` file is in the root of your project directory on the server.

4.  **Configure Nginx:** Create a new Nginx config file for your site.

    ```bash
    sudo nano /etc/nginx/sites-available/your_domain.com
    ```

    Paste the following configuration:

    ```nginx
    server {
        listen 80;
        server_name your_domain.com www.your_domain.com;

        location / {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_pass http://127.0.0.1:8000; # Forwards to the Docker container
        }
    }
    ```

    Then enable the site and restart Nginx:

    ```bash
    sudo ln -s /etc/nginx/sites-available/your_domain.com /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    ```

### Step 3: Configure and Deploy

1.  **Update CI/CD Workflow:** In `.github/workflows/deploy.yml`, update the Docker image name and the server path:

    ```yaml
    # ...
    tags: your_docker_username/your_app_name:latest
    # ...
    script: |
      cd /home/your_user/your_project_directory # <-- CHANGE THIS PATH

    # ...
    ```

2.  **Deploy:** Commit and push your changes to the `main` branch. GitHub Actions will automatically build your Docker image, push it to Docker Hub, and deploy it on your server.
    ```bash
    git add .
    git commit -m "Configure for production"
    git push origin main
    ```

Your application is now live!

## Available Scripts

- **`npm run dev`**: Starts the frontend development server.
- **`npm run build`**: Builds the frontend for production.
- **`npm run lint`**: Lints the frontend codebase for errors.
- **`npm run format`**: Formats the frontend codebase with Prettier.
