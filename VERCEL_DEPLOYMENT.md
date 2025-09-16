# Vercel Deployment Guide for FastAPI

## Prerequisites
- Vercel account (https://vercel.com/signup)
- Vercel CLI installed (optional): `npm i -g vercel`
- GitHub repository for the project

## Files Created
- `vercel.json` - Vercel configuration
- `requirements.txt` - Python dependencies

## Deployment Steps

### Option 1: Deploy via GitHub (Recommended)

1. **Push to GitHub**
   ```bash
   git add vercel.json requirements.txt
   git commit -m "Add Vercel deployment configuration"
   git push origin main
   ```

2. **Connect to Vercel**
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - Select the repository

3. **Configure Environment Variables**
   Add these in Vercel dashboard under Settings > Environment Variables:
   ```
   DATABASE_URL=postgresql+asyncpg://[your-neon-connection-string]
   DATABASE_URL_SYNC=postgresql://[your-neon-connection-string]
   AZURE_VISION_KEY=[your-azure-key]
   AZURE_VISION_ENDPOINT=[your-azure-endpoint]
   ```

4. **Deploy**
   - Click "Deploy"
   - Wait for build completion

### Option 2: Deploy via CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   vercel
   ```
   Follow the prompts to:
   - Link to existing project or create new
   - Set environment variables
   - Deploy

## Important Limitations on Vercel

### ⚠️ Database Connections
- Each request creates new connection (no persistent pooling)
- Consider using Neon's serverless driver for better performance
- May need to modify `app/core/database.py` for serverless environment

### ⚠️ File Storage
- Uploaded files are NOT persistent
- Only `/tmp` directory is writable
- Consider using external storage (S3, Azure Blob) for file uploads

### ⚠️ Function Limits (Free Plan)
- Max execution time: 10 seconds
- Max deployment size: 250MB
- Memory: 512MB

### ⚠️ Features That Won't Work
- WebSockets
- Background tasks (use external queue service)
- File uploads (need external storage)
- Long-running operations

## Potential Issues & Solutions

### Issue 1: Deployment Size Too Large
**Solution**: Create `.vercelignore` file:
```
.venv/
__pycache__/
*.pyc
.git/
.github/
tests/
docs/
*.md
!VERCEL_DEPLOYMENT.md
.env
```

### Issue 2: Database Connection Errors
**Solution**: Modify database connection for serverless:
- Use connection string with `?sslmode=require`
- Implement connection retry logic
- Consider using Neon's serverless driver

### Issue 3: Import Errors
**Solution**: Ensure all imports use absolute paths:
- Change relative imports to absolute
- Update `main.py` if needed

## Testing Deployment

After deployment:
1. Visit: `https://[your-project].vercel.app`
2. Test API docs: `https://[your-project].vercel.app/docs`
3. Check function logs in Vercel dashboard

## Alternative Platforms (Better for This Project)

Given your project's requirements (database, file uploads, Azure integration), consider:

1. **Railway** (https://railway.app)
   - Better database support
   - Persistent file system
   - Easy PostgreSQL integration

2. **Render** (https://render.com)
   - Built-in PostgreSQL
   - Persistent disk storage
   - Better for full applications

3. **Fly.io** (https://fly.io)
   - Global deployment
   - Persistent volumes
   - Better for stateful applications

## Rollback if Needed

If deployment fails or has issues:
```bash
# Remove Vercel files
rm vercel.json
rm requirements.txt
rm VERCEL_DEPLOYMENT.md

# Use original development setup
uv run uvicorn main:app --reload
```