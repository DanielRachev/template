# --- Stage 1: Build the Frontend ---
FROM node:22.17.1-alpine AS frontend-builder

# Set the working directory for the frontend
WORKDIR /app/frontend

# Copy package.json and package-lock.json to leverage Docker cache
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm install

# Copy the rest of the frontend source code
COPY frontend/ ./

# Build the frontend application.
# The output will go to /app/backend/static/dist
RUN npm run build

# --- Stage 2: Build the Final Backend Image ---
FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install backend dependencies
# Copy requirements.txt first to leverage Docker cache
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory from your local machine to the container
COPY ./backend .

# Copy the BUILT frontend assets from the 'frontend-builder' stage
COPY --from=frontend-builder /app/backend/static/dist ./static/dist/

# Run collectstatic.
RUN python manage.py collectstatic --noinput

# Expose the port Gunicorn will run on
EXPOSE 8000

# Run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi"]