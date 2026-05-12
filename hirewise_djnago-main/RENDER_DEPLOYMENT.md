# Deployment Guide - Render

This guide explains how to deploy the Hirewise Django Job Portal to Render.

## Prerequisites

- GitHub account with this repository pushed
- Render account (https://render.com)

## Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Ready for deployment"
git remote add origin https://github.com/YOUR_USERNAME/hirewise-django.git
git push -u origin main
```

## Step 2: Create Render Account & Connect GitHub

1. Go to https://render.com and sign up
2. Connect your GitHub account
3. Grant access to your repositories

## Step 3: Deploy Using Blueprint (Recommended)

1. Go to **Dashboard** → **New +** → **Blueprint**
2. Select your GitHub repository
3. Render will detect `render.yaml` automatically
4. Review the configuration:
   - **Service**: Django web service
   - **Database**: PostgreSQL free tier
5. Click **Deploy**

**OR Step 3 Alternative: Manual Deployment**

1. **Create Web Service**:
   - Dashboard → **New +** → **Web Service**
   - Connect your GitHub repo
   - Configure:
     - **Name**: `hirewise-django`
     - **Runtime**: `Python`
     - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
     - **Start Command**: `gunicorn hirewise.wsgi:application`

2. **Create PostgreSQL Database**:
   - Dashboard → **New +** → **PostgreSQL**
   - Configure:
     - **Name**: `hirewise-db`
     - **Region**: Same as web service
     - **Plan**: Free

## Step 4: Configure Environment Variables

In Render Dashboard for your web service:

1. Go to **Environment**
2. Add these variables:
   ```
   DEBUG=False
   ALLOWED_HOSTS=your-app.onrender.com,www.your-app.onrender.com
   SECRET_KEY=<generate-random-string>
   DATABASE_URL=<automatically-filled-from-database>
   ```

3. Save environment variables

## Step 5: Deploy

1. Click **Deploy** to start the build
2. Wait for build to complete
3. Run migrations automatically or manually:
   ```bash
   render-cli run "python manage.py migrate"
   ```

## Step 6: Verify Deployment

1. Go to your service URL: `https://your-app-name.onrender.com`
2. Check logs if issues occur: **Logs** tab in Render Dashboard

## Troubleshooting

### Build Fails with Module Errors
- Check `requirements.txt` has all dependencies
- Verify `Procfile` and build commands are correct

### Database Connection Errors
- Verify `DATABASE_URL` is set in environment variables
- Check PostgreSQL instance is running in Render
- Run migrations: `python manage.py migrate`

### Static Files Not Loading
- Ensure `collectstatic` runs during build
- Check `STATIC_URL` and `STATIC_ROOT` in settings.py

### Application Errors
- Check logs: **Logs** tab in Render
- Ensure `SECRET_KEY` is set
- Verify `DEBUG=False` for production

## Development vs Production

**Development** (Local):
- Uses SQLite database
- `DEBUG=True`
- Static files served automatically

**Production** (Render):
- Uses PostgreSQL database
- `DEBUG=False`
- Static files served by WhiteNoise
- Uses Gunicorn WSGI server

## Important Security Notes

- Never commit `.env` file
- Change `SECRET_KEY` in production
- Use environment variables for sensitive data
- Keep `DEBUG=False` in production
- Use strong database password

## Useful Render Commands

```bash
# View logs
render-cli logs <service-id>

# Run migrations
render-cli run "python manage.py migrate"

# Create superuser
render-cli run "python manage.py createsuperuser"

# Collect static files
render-cli run "python manage.py collectstatic --noinput"
```

## Support

For more info:
- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/5.2/howto/deployment/
