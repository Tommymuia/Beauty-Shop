# Vercel Deployment Configuration

## Backend URL
Your backend is deployed at: `https://beauty-shop-s0xb.onrender.com`

## Required Environment Variable in Vercel

You need to add this environment variable in your Vercel project:

**Variable Name:** `VITE_API_BASE_URL`  
**Variable Value:** `https://beauty-shop-s0xb.onrender.com/api`

## Step-by-Step Instructions

### 1. Add Environment Variable
1. Go to https://vercel.com/dashboard
2. Select your Beauty Shop project
3. Click on "Settings" tab
4. Click on "Environment Variables" in the left sidebar
5. Click "Add New" button
6. Enter:
   - **Key**: `VITE_API_BASE_URL`
   - **Value**: `https://beauty-shop-s0xb.onrender.com/api`
   - **Environment**: Check all three boxes (Production, Preview, Development)
7. Click "Save"

### 2. Redeploy Your Application
1. Go to the "Deployments" tab
2. Find your latest deployment
3. Click the three dots menu (•••) next to it
4. Select "Redeploy"
5. **Uncheck** "Use existing Build Cache" (important!)
6. Click "Redeploy" button

### 3. Wait for Deployment
- Vercel will rebuild your app with the new environment variable
- Wait 2-3 minutes for the deployment to complete
- You'll see a "Ready" status when done

### 4. Test Your Site
Visit your Vercel URL and test:
- Login should work
- Products should display
- M-Pesa checkout should trigger the payment prompt

## Notes
- Render free tier has cold starts (backend sleeps after 15min of inactivity)
- First API call may take 30-60 seconds if backend is asleep
- Subsequent calls will be fast

## Verify Backend is Active
Before testing, visit: https://beauty-shop-s0xb.onrender.com/
- You should see: `{"message":"Beauty Shop Backend is Active"}`
- If it takes 30+ seconds to load, the backend was sleeping and is now waking up
