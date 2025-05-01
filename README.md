# Leds for Rpi5

## Install deps

NVM - [Github repo](https://github.com/nvm-sh/nvm)
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

Install node
```bash
nvm install v22.15.0
```

Install pixi
```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

Install python requiments
```bash
pixi install
```

## Run

Run in dev mode - reloading when code changes
```bash
pixi run dev_mqtt
```

Run cli
```bash
pixi run cli
```

## Run as a service (systemd)

```
cp mqtt.service /etc/systemd/system/mqtt.service
sudo systemctl daemon-reload
sudo systemctl enable mqtt.service
sudo systemctl start mqtt.service
```