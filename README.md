# relay

## notes

- configuration states the topics to subscribe to and the associated subscriber
- subscriber parses the message details and sends signals for associated values e.g.
    - message contains temp, humidity, and pressure
    - subscriber decodes the message and broadcasts signals for each value
    - any associated processor then does further things with the data e.g.
        - mqtt watcher - broadcast a new message
        - influxdb watcher - submit values into influxdb
        - grafana watcher - submit annotations