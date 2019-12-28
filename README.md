# MQTT2InfluxDB

Service that subscribes to one or multiple MQTT topics and insert the received messages on InfluxDB,
using a Redis DB as a queue to bulk insert messages on Influx, and keep them during Influx server downtime.

## Requirements

- Python >= 3.6
- Requirements listed on [requirements.txt](requirements.txt)
- A MQTT broker
- An InfluxDB server
- A Redis server

## Changelog

- 0.0.1 - Initial version (base functional code, ...)

## Settings

Settings can be defined through environment variables or using a `.env` file (located within the `__main__.py` file).

### MQTT Settings

- `MQTT_BROKER`: MQTT broker host (default: `localhost`)
- `MQTT_PORT`: MQTT broker port (default: `1883`)
- `MQTT_SUBSCRIBE`: MQTT topic/s to subscribe to (default: `#`); split multiple topics by the `MQTT_SUBSCRIBE_SEPARATOR` (default: `,`)
- `MQTT_SUBSCRIBE_SEPARATOR`: character/sequence used to split multiple topics on the `MQTT_SUBSCRIBE` env var (default: `,`)
- `MQTT_CLIENT_ID`: MQTT client ID (default: `MQTT2InfluxDB_{uuid1(node)}`)
- `MQTT_KEEPALIVE`: keepalive time in seconds (default: `60`)
- `MQTT_QOS`: MQTT QoS used when subscribing to topic/s (default: `0`)

### InfluxDB Settings

- `INFLUX_HOST`: InfluxDB server host (default: `localhost`)
- `INFLUX_PORT`: InfluxDB server port (default: `8086`)

### Redis Settings

- `REDIS_HOST`: Redis server host (default: `localhost`)
- `REDIS_PORT`: Redis server port (default: `6379`)
- `REDIS_DB`: Redis database index (default: `0`)
- `REDIS_QUEUE_NAME`: Name of the key used to store messages in queue (default: `mqtt2influxdb_{uuid1(node)}`)

### General (system) Settings

- `LOG_LEVEL`: level of the internal logger (default: `INFO`)

## Installing

The recommended method to install is using the [Python-Autoclonable-App](https://hub.docker.com/r/davidlor/python-autoclonable-app/) image.

### Running tests

Tests are integration tests, requiring MQTT, Redis & Influx servers deployed.

```bash
# After cloning...
cd MQTT2InfluxDB
pip install -r tests/requirements.txt
pytest
```

