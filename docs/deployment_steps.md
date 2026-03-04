# DigitalOcean Deployment Plan

This plan describes how to deploy the Rain Prediction application to a DigitalOcean Droplet.

## Prerequisites
- A DigitalOcean account.
- A Droplet created (recommended: Ubuntu 22.04 or 24.04 LTS).
- The public IPv4 address of the Droplet.

## Proposed Steps

### 1. Connect to the Droplet
Use SSH to connect to your Droplet:
```bash
ssh root@YOUR_DROPLET_IP
```

### 2. Install Docker (Rapid Setup)
On the Droplet terminal, run:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### 3. Run the Application
Pull and run the updated image from Docker Hub:
```bash
docker run -d -p 80:8501 --name rain-app --restart always jhondanielcalvache/prediccion-lluvia:latest
```
> [!NOTE]
> We map port `80` (HTTP standard) to the internal port `8501`. This allows your colleagues to access the app using just the IP address.

## Verification Plan

### Manual Verification
- Open a browser and navigate to `http://YOUR_DROPLET_IP`.
- Verify the application is fully functional.
