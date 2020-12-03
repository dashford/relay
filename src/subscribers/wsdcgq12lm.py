from blinker import signal
import json


class WSDCGQ12LM:
    def __init__(self, logger):
        self._logger = logger
        self._payload = None

    def _get_battery(self):
        if 'battery' in self._payload:
            return self._payload['battery']
        return 0

    def _get_humidity(self):
        if 'humidity' in self._payload:
            return self._payload['humidity']
        return 0

    def _get_link_quality(self):
        if 'linkquality' in self._payload:
            return self._payload['linkquality']
        return 0

    def _get_pressure(self):
        if 'pressure' in self._payload:
            return self._payload['pressure']
        return 0

    def _get_temperature(self):
        if 'temperature' in self._payload:
            return self._payload['temperature']
        return 0

    def _get_voltage(self):
        if 'voltage' in self._payload:
            return self._payload['voltage']
        return 0

    def callback(self, client, userdata, message):
        self._logger.debug('WSDCGQ12LM callback invoked for ' + message.topic + ' topic')
        self._payload = json.loads(message.payload)

        battery_signal = signal('battery')
        self._logger.debug('Broadcasting battery signal')
        battery_signal.send(self, battery=self._get_battery())
        self._logger.info('Broadcast battery value of {}'.format(self._get_battery()))

        humidity_signal = signal('humidity')
        self._logger.debug('Broadcasting humidity signal')
        humidity_signal.send(self, humidity=self._get_humidity())
        self._logger.info('Broadcast humidity value of {}'.format(self._get_humidity()))

        link_quality_signal = signal('link_quality')
        self._logger.debug('Broadcasting link_quality signal')
        link_quality_signal.send(self, link_quality=self._get_link_quality())
        self._logger.info('Broadcast link_quality value of {}'.format(self._get_link_quality()))

        pressure_signal = signal('pressure')
        self._logger.debug('Broadcasting pressure signal')
        pressure_signal.send(self, pressure=self._get_pressure())
        self._logger.info('Broadcast pressure value of {}'.format(self._get_pressure()))

        temperature_signal = signal('temperature')
        self._logger.debug('Broadcasting temperature signal')
        temperature_signal.send(self, temperature=self._get_temperature())
        self._logger.info('Broadcast temperature value of {}'.format(self._get_temperature()))

        voltage_signal = signal('voltage')
        self._logger.debug('Broadcasting voltage signal')
        voltage_signal.send(self, voltage=self._get_voltage())
        self._logger.info('Broadcast voltage value of {}'.format(self._get_voltage()))


# payload '{"battery":100,"humidity":70.92,"linkquality":5,"pressure":1019.3,"temperature":13.96,"voltage":3065}'
