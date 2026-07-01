# 🚀 Deploy to Heroku

## One-click Deploy

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Manual Steps

### 1. Install Heroku CLI
```bash
curl https://cli-assets.heroku.com/install.sh | sh
heroku login
```

### 2. Create the app
```bash
heroku create your-bot-name
```

### 3. Set environment variables
```bash
heroku config:set API_ID=your_api_id
heroku config:set API_HASH=your_api_hash
heroku config:set BOT_TOKEN=your_bot_token
```

### 4. Deploy
```bash
git push heroku main
```

### 5. Start the worker dyno
```bash
heroku ps:scale worker=1
```

### 6. Check logs
```bash
heroku logs --tail
```

> **Note:** Use a free Heroku account with the `Eco Dynos` plan ($5/month).  
> The bot runs as a **worker** dyno (not web), so no port binding is needed.
