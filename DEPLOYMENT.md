# Deployment Guide

This guide explains how to deploy the Skin Disease Classifier application to production.

## Deployment Options

### Option 1: Separate Hosting (Recommended)

Deploy frontend and backend to separate services:

#### Frontend Deployment (Vercel/Netlify)

1. **Build the frontend:**
```bash
cd frontend
npm run build
```

2. **Deploy to Vercel:**
```bash
npm install -g vercel
vercel
```

Or deploy to Netlify:
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

3. **Environment Variables:**
Set these in your hosting platform:
- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`

4. **Update API URL:**
Change the proxy configuration in `vite.config.js` or update `API_URL` in components to point to your production backend URL.

#### Backend Deployment (Railway/Render/Heroku)

1. **Prepare for deployment:**
Create a `Procfile` in the backend directory:
```
web: python app.py
```

2. **Update Flask to use production settings:**
In `backend/app.py`, change:
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

3. **Deploy to Railway:**
```bash
cd backend
railway init
railway up
```

Or deploy to Render:
- Connect your GitHub repository
- Set build command: `pip install -r requirements.txt`
- Set start command: `python app.py`

4. **Upload Model File:**
Make sure `DermNet_Samples.keras` and `dermnet_disease.json` are included in your deployment.

### Option 2: Docker Deployment

#### Create Dockerfile for Backend

`backend/Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY ../DermNet_Samples.keras /app/
COPY ../dermnet_disease.json /app/

EXPOSE 5000

CMD ["python", "app.py"]
```

#### Create Dockerfile for Frontend

`frontend/Dockerfile`:
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose

`docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./DermNet_Samples.keras:/app/DermNet_Samples.keras
      - ./dermnet_disease.json:/app/dermnet_disease.json

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - VITE_SUPABASE_URL=${VITE_SUPABASE_URL}
      - VITE_SUPABASE_ANON_KEY=${VITE_SUPABASE_ANON_KEY}
    depends_on:
      - backend
```

Run with:
```bash
docker-compose up -d
```

### Option 3: Single Server Deployment

Deploy both frontend and backend on the same server (e.g., DigitalOcean, AWS EC2).

1. **Install dependencies:**
```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Python
sudo apt-get install python3 python3-pip
```

2. **Clone and setup:**
```bash
git clone <your-repo>
cd project

# Setup backend
cd backend
pip3 install -r requirements.txt

# Setup frontend
cd ../frontend
npm install
npm run build
```

3. **Use PM2 to run backend:**
```bash
sudo npm install -g pm2
cd backend
pm2 start app.py --interpreter python3 --name skin-classifier-api
```

4. **Serve frontend with Nginx:**
```bash
sudo apt-get install nginx
sudo nano /etc/nginx/sites-available/default
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /path/to/project/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Restart Nginx:
```bash
sudo systemctl restart nginx
```

## Environment Configuration

### Production Environment Variables

Create a `.env.production` file:

```env
# Supabase
VITE_SUPABASE_URL=your_production_supabase_url
VITE_SUPABASE_ANON_KEY=your_production_anon_key

# Backend (if needed)
FLASK_ENV=production
```

## Security Checklist

- [ ] Remove debug mode in Flask (`debug=False`)
- [ ] Use HTTPS in production
- [ ] Set proper CORS origins (not `*`)
- [ ] Secure Supabase RLS policies
- [ ] Add rate limiting to API endpoints
- [ ] Implement proper error handling
- [ ] Set up monitoring and logging
- [ ] Add authentication for sensitive operations

## Performance Optimization

1. **Frontend:**
   - Enable gzip compression
   - Use CDN for static assets
   - Implement lazy loading for images
   - Add service worker for offline support

2. **Backend:**
   - Use gunicorn instead of Flask dev server
   - Implement caching for predictions
   - Add request rate limiting
   - Optimize model loading

Example gunicorn command:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Monitoring

Recommended monitoring tools:
- **Uptime monitoring:** UptimeRobot, Pingdom
- **Error tracking:** Sentry
- **Analytics:** Google Analytics, Plausible
- **Logs:** Papertrail, Loggly

## Backup

Regular backups for:
- Supabase database (automatic with Supabase)
- Model files
- Application code (Git)

## Cost Estimation

### Free Tier Options:
- **Frontend:** Vercel/Netlify (Free)
- **Backend:** Railway (Free tier), Render (Free tier)
- **Database:** Supabase (Free tier: 500MB, 2GB transfer)

### Paid Options (Monthly):
- **Frontend:** Vercel Pro ($20)
- **Backend:** Railway ($5-20), Render ($7+)
- **Database:** Supabase Pro ($25)

## Support

For deployment issues:
1. Check application logs
2. Verify environment variables
3. Test API endpoints separately
4. Check CORS configuration
5. Verify model file paths

## Rollback Plan

Keep previous versions:
```bash
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0
```

To rollback:
```bash
git checkout v1.0.0
# Redeploy
```
