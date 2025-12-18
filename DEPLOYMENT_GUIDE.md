# Deployment Guide to EC2 (Side-by-Side)

Since you already have a service running on your EC2 instance, we will deploy "Soko Hub" using **Docker** on a **specific port (8001)** to avoid conflicts.

## Prerequisites on VPS
Ensure Docker and Docker Compose are installed on your EC2 instance:
```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker $USER
```
*(You may need to logout and login again after the usermod command)*

## Step 1: Transfer Files
Push your code to GitHub and pull it on the server, OR copy the files directly using `scp`.

**Important Files to have on server:**
- `Dockerfile`
- `docker-compose.yml`
- `entrypoint.sh`
- `requirements.txt`
- `.env` (Create this manually on the server with your secrets)

## Step 2: Configure Environment (.env)
Create a `.env` file in the project directory on your server:
```ini
DEBUG=0
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,localhost,127.0.0.1
GEMINI_API_KEY=your-gemini-key
# ... other keys ...
```

## Step 3: Run the Application
Run the following command to build and start the containers. This will bind the app to port **8001** (as defined in `docker-compose.yml`).
```bash
docker-compose up -d --build
```
Check if it's running:
```bash
docker-compose ps
# curl http://localhost:8001
```

## Step 4: Configure Nginx Reverse Proxy
You likely already have Nginx running for your other service. You just need to add a new server block.

1. Create a new config file:
   ```bash
   sudo nano /etc/nginx/sites-available/sokohub
   ```
2. Paste the content from `nginx.conf.example` (included in your repo), updating the `server_name` to your domain.
   ```nginx
   server {
       listen 80;
       server_name new-app.yourdomain.com; # Your new domain

       location / {
           proxy_pass http://127.0.0.1:8001;
           proxy_set_header Host $host;
           # ...
       }
   }
   ```
3. Enable the site and test:
   ```bash
   sudo ln -s /etc/nginx/sites-available/sokohub /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

Now your existing service continues running on its port, and Soko Hub runs on port 8001, accessible via your specific domain name!
