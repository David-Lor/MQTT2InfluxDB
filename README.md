# MQTT2InfluxDB

Python Service that subscribes to one or multiple MQTT topics and insert the received messages on InfluxDB,
using a Redis DB as a queue to bulk insert messages on Influx, and keep them during Influx server downtime.

- [Requirements](#requirements)
- [Changelog](#changelog)
- [TODO](#todo)
- [FAQ](#faq)
- [Settings](#settings)
- [Data structure](#data-structure)
- [Installing & running](#installing--running)

## Requirements

- Python >= 3.6
- Requirements listed on [requirements.txt](requirements.txt)
- A MQTT broker
- An InfluxDB server
- A Redis server

## Changelog

- 0.0.2 - Add support for authentication & SSL to MQTT
- 0.0.1 - Initial version (functional code)

## TODO

- Fix insertion of JSON with booleans (crashes data writing into Influx)
- Handle errors on all connectors (MQTT, Redis, Influx)
- Add locks to Redis while reading/writing to the queue
- Only insert string payloads and not arbitrary binary data
- Support MQTT authentication & SSL
- Shorter payload debug logging records?
- Set Redis optional (Redis connector being a mocked class with a Python list to store messages)
- Support Redis authentication
- Support InfluxDB authentication
- Unit & integration tests

## FAQ

- **Why is this even a thing?**

  When using MQTT for IoT communication, I found useful to have all the messages registered on some persistent storage.
  This allows me to search through topics and see their context. And most important, can create statistics for
  monitorized data, and even analytics and graphs, using InfluxDB + Chronograf, Grafana or other similar tools.

- **Why is Redis required?**

  On my particular setup scenario, the server that will hold the data will not be always available, while MQTT messages
  get sent 24/7, and this service is running on a 24/7 device. A simpler solution, as a Python list, could be used,
  but preferred to externalize it on a Redis queue.
  
  This can be useful if this service is down, restarts or even if the device running it restarts,
  since Redis can persist the data on disk (must be configured on Redis).
  
  Other advantage is to do bulk insertions on InfluxDB, instead of performing a request by each single message received
  on MQTT.

- **Why not using Telegraf?**

  Telegraf is part of the Influx stack, as a counterpart of Logstash on the Elastic stack.
  It [can subscribe to MQTT](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/mqtt_consumer) and insert the received messages on Influx, but is not very flexible when dealing with different types of variables.

- **Why parsing & storing the payload?**

  By default, payloads are read as strings, but they get converted to numbers, booleans or JSON if possible.
  InfluxDB is not very friendly with string to number parsing during queries to create, for example, graphs in Chronograf.
  That's why all the messages get their payload parsed to the closest type and stored on a different field.

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

## Data structure

```json
{
    "measurement": "mqtt",
    "tags": {
        "topic": "{topic}",
        "qos": {qos}
    },
    "time": "2020-01-02T16:20:00Z",
    "fields": {
        "payload": "1.2345",
        "payload_number": 1.2345
    }
}
```

- `measurement` is the same for all MQTT messages (`mqtt` by default)
- `fields.payload` stores the payload as string
- the payload tries to be converted to:
    - number -> `fields.payload_number`
    - json -> `fields.payload_json`
    - boolean -> `fields.payload_bool`

## Installing & Running

The recommended method to install is using the [Python-Autoclonable-App](https://hub.docker.com/r/davidlor/python-autoclonable-app/) image.

### Run through Docker with Python-Autoclonable-App image

```bash
# TODO
```

### Run through Docker-Compose

```bash
git clone https://github.com/David-Lor/MQTT2InfluxDB.git
cd MQTT2InfluxDB/tools/deployment/mqtt2influxdb
docker-compose up -d
```

### Run locally

```bash
git clone https://github.com/David-Lor/MQTT2InfluxDB.git
cd MQTT2InfluxDB

# Set your environment variables
cp sample.env .env
nano .env

# Run
python3 .
```

