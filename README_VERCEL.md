# Vercel Deployment Guide

This Flask application is configured for deployment on Vercel.

## Prerequisites

1. A Vercel account (sign up at https://vercel.com)
2. Vercel CLI installed (optional, for local testing):
   ```bash
   npm i -g vercel
   ```

## Deployment Steps

### Option 1: Deploy via Vercel Dashboard

1. Push your code to GitHub
2. Go to https://vercel.com/new
3. Import your GitHub repository
4. Vercel will automatically detect the `vercel.json` configuration
5. Click "Deploy"

### Option 2: Deploy via Vercel CLI

1. Install Vercel CLI (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy:
   ```bash
   vercel
   ```

4. For production deployment:
   ```bash
   vercel --prod
   ```

## Project Structure

```
.
├── api/
│   └── index.py          # Vercel serverless function handler
├── app.py                # Main Flask application
├── models/               # ML model files (required)
├── static/               # Static files (CSS, etc.)
├── templates/            # HTML templates
├── requirements.txt      # Python dependencies
└── vercel.json          # Vercel configuration
```

## Important Notes

1. **Model Files**: Make sure all model files in the `models/` directory are committed to your repository, as they're needed for predictions.

2. **File Size Limits**: Vercel has limits on serverless function size. If your models are very large (>50MB), consider:
   - Using Vercel Pro plan (higher limits)
   - Storing models in external storage (S3, etc.) and loading them at runtime
   - Using model optimization techniques

3. **Cold Starts**: Serverless functions may experience cold starts. The first request after inactivity might be slower.

4. **Environment Variables**: If you need environment variables, add them in the Vercel dashboard under Project Settings > Environment Variables.

## Testing Locally

You can test the Vercel deployment locally:

```bash
vercel dev
```

This will start a local server that mimics Vercel's environment.

## Troubleshooting

### Static Files Not Loading
- Ensure `static/` folder is in the root directory
- Check that `vercel.json` has the static file route configured

### Model Files Not Found
- Verify all `.pkl` files are in the `models/` directory
- Check that files are committed to git (not in `.gitignore`)

### Import Errors
- Ensure `requirements.txt` includes all necessary packages
- Check that Python version is compatible (Vercel uses Python 3.9 by default)

## Support

For Vercel-specific issues, check:
- [Vercel Python Documentation](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python)
- [Vercel Community](https://github.com/vercel/vercel/discussions)

