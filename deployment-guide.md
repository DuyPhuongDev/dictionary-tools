# Deployment Guide for Render

## Deploy to Render

### Option 1: Automatic Deployment (Recommended)

1. **Push to GitHub**: Push your code to a GitHub repository

2. **Connect to Render**:
   - Go to [Render Dashboard](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure Service**:
   - **Name**: `vocabulary-app`
   - **Environment**: `Docker`
   - **Region**: Choose your preferred region
   - **Branch**: `main`
   - **Dockerfile Path**: `./Dockerfile`

4. **Environment Variables**:
   ```
   PORT=10000
   DEBUG=false
   APP_HOST=0.0.0.0
   MAX_FILE_SIZE=10MB
   ALLOWED_FILE_TYPES=txt
   REQUESTS_PER_MINUTE=30
   ```

5. **Deploy**: Click "Create Web Service"

### Option 2: Using render.yaml

1. **Add render.yaml**: The `render.yaml` file is already included in the project

2. **Deploy**: 
   - Push to GitHub
   - In Render Dashboard, click "New +" → "Blueprint"
   - Connect your repository
   - Render will automatically read the `render.yaml` configuration

## Local Docker Testing

### Build and Run with Docker Compose

```bash
# Build and start the application
docker-compose up --build

# Access the application
open http://localhost:8000

# Stop the application
docker-compose down
```

### Build and Run with Docker only

```bash
# Build the image
docker build -t vocabulary-app .

# Run the container
docker run -p 8000:8000 \
  -e PORT=8000 \
  -e DEBUG=true \
  vocabulary-app

# Access the application
open http://localhost:8000
```

## Production Setup with Nginx

For high-traffic production environments:

```bash
# Start with nginx proxy
docker-compose --profile production up --build

# This will start:
# - vocabulary-app on port 8000
# - nginx proxy on port 80
```

## Health Checks

The application includes health checks:
- **Docker Health Check**: `/api` endpoint
- **Render Health Check**: `/api` endpoint

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8000` | Port for the application |
| `DEBUG` | `True` | Enable debug mode |
| `APP_HOST` | `0.0.0.0` | Host binding |
| `MAX_FILE_SIZE` | `10MB` | Maximum upload file size |
| `ALLOWED_FILE_TYPES` | `txt` | Allowed file types |
| `REQUESTS_PER_MINUTE` | `30` | Rate limiting |

## Troubleshooting

### Common Issues

1. **Build Fails**:
   - Check Docker logs: `docker-compose logs vocab-app`
   - Verify all dependencies are in `requirements.txt`

2. **App Crashes**:
   - Check application logs in Render dashboard
   - Verify environment variables are set correctly

3. **Slow Performance**:
   - Consider upgrading Render plan
   - Enable nginx caching in production

### Monitoring

- **Render Dashboard**: View logs, metrics, and deployments
- **Health Endpoint**: `https://your-app.onrender.com/api`
- **Application**: `https://your-app.onrender.com/`

## Security Notes

- The application runs as a non-root user in Docker
- nginx includes security headers
- Rate limiting is configured for API endpoints
- File uploads are restricted to `.txt` files only

## Scaling

For high-traffic scenarios:
1. Upgrade to Render paid plans for better performance
2. Enable horizontal scaling in Render
3. Consider using a CDN for static files
4. Implement caching strategies for API responses 