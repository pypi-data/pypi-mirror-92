import asyncio as aio
import logging
import struct
import uuid
from dataclasses import dataclass

from ..utils import cr2032_voltage_to_percent
from .base import Device
from .xiaomi_base import XiaomiHumidityTemperature

logger = logging.getLogger(__name__)

LYWSD_DATA = uuid.UUID('EBE0CCC1-7A0A-4B0C-8A1A-6FF2997DA3A6')
LYWSD_BATTERY = uuid.UUID('EBE0CCC4-7A0A-4B0C-8A1A-6FF2997DA3A6')


@dataclass
class SensorState:
    battery: int
    temperature: float
    humidity: float

    @classmethod
    def from_data(cls, sensor_data, battery_data):
        t, h, voltage = struct.unpack('<hBH', sensor_data)
        return cls(
            temperature=round(t/100, 2),
            humidity=h,
            battery=int(cr2032_voltage_to_percent(voltage)),
        )


class XiaomiHumidityTemperatureLYWSD(XiaomiHumidityTemperature, Device):
    NAME = 'xiaomilywsd'
    DATA_CHAR = LYWSD_DATA
    BATTERY_CHAR = LYWSD_BATTERY
    SENSOR_CLASS = SensorState
    CONNECTION_FAILURES_LIMIT = 10

    async def read_and_send_data(self, publish_topic):
        logger.info(f'call {self}.read_and_send_data()')
        return await super().read_and_send_data(publish_topic)

    async def _notify_state(self, publish_topic):
        logger.info(f'call {self}._notify_state({self._state})')
        return await super()._notify_state(publish_topic)

    async def close(self):
        logger.info(f'Closing {self}...')
        return await super().close()

    async def handle(self, publish_topic, send_config, *args, **kwargs):
        sec_to_wait_connection = 0
        while True:
            logger.info(f'{self} Start handle...')
            if not self.client.is_connected:
                logger.info(f'{self} is not connected... sleep(1)')
                if sec_to_wait_connection >= 30:
                    raise TimeoutError(
                        f'{self} not connected for 30 sec in handle()',
                    )
                sec_to_wait_connection += 1
                await aio.sleep(1)
                continue
            try:
                await aio.wait_for(
                    self.read_and_send_data(publish_topic),
                    timeout=15,
                )
            except aio.CancelledError:
                raise
            except ValueError as e:
                logger.error(f'Cannot read values {str(e)}')
            except Exception:
                logger.exception(f'Exception in {self}')
                raise
            else:
                return

            await aio.sleep(1)
