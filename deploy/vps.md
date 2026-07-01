# 🖥️ Deploy on VPS (Ubuntu/Debian)

## Quick Setup

### 1. Update system & install Python
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git -y
```

### 2. Clone the repo
```bash
git clone https://github.com/ragini19854-prog/aura_x_holder
cd aura_x_holder
```

### 3. Install dependencies
```bash
pip3 install -r requirements.txt
```

### 4. Set environment variables
```bash
cp .env.example .env
nano .env   # fill in API_ID, API_HASH, BOT_TOKEN
```

### 5. Test run
```bash
python3 main.py
```

### 6. Run as a background service (systemd)
```bash
sudo cp deploy/madara-bot.service /etc/systemd/system/
# Edit the WorkingDirectory and User in the service file:
sudo nano /etc/systemd/system/madara-bot.service

sudo systemctl daemon-reload
sudo systemctl enable madara-bot
sudo systemctl start madara-bot
```

### 7. Check status & logs
```bash
sudo systemctl status madara-bot
sudo journalctl -u madara-bot -f
```

## Using Docker (any VPS)

```bash
# Build
docker build -t madara-bot .

# Run with env file
docker run -d \
  --name madara-bot \
  --env-file .env \
  --restart unless-stopped \
  -v $(pwd)/sessions:/app/sessions \
  -v $(pwd)/madara.db:/app/madara.db \
  madara-bot

# Logs
docker logs -f madara-bot
```

## Using Screen (simple)
```bash
screen -S madara-bot
python3 main.py
# Detach: Ctrl+A then D
# Reattach: screen -r madara-bot
```
