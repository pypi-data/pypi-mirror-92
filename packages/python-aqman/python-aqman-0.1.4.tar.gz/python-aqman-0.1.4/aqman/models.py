import attr
import datetime
from typing import List, Dict


@attr.s(auto_attribs=True, frozen=True)
class Device:
    """Object holding the Aqman101 device state."""

    serial_number: str
    dsm101_serial_number: str
    date_time: datetime.datetime
    device_type: int
    firmware_version: str
    upload_type: int
    smartplug_enable: int
    temperature: float
    humidity: int
    radon: int
    co2: int
    pm10: int
    pm2d5: int
    pm1: int
    tvoc: int

    @staticmethod
    def from_dict(data):
        return Device(
            serial_number=data["sn"],
            dsm101_serial_number=data["dsm101_sn"],
            date_time=data["dt"],
            device_type=0,
            firmware_version="V1.02A",
            upload_type=0,
            smartplug_enable=0,
            temperature=data["temp"],
            humidity=data["humi"],
            radon=data["radon"],
            co2=data["co2"],
            pm10=data["pm10"],
            pm2d5=data["pm2d5"],
            pm1=data["pm1"],
            tvoc=data["tvoc"]
        )


@attr.s(auto_attribs=True, frozen=True)
class UserInfo:
    """Object holding the user information of Aqman101 user"""

    devices: List[str]
    device_cnt: int

    @staticmethod
    def from_list(data: List[str]):
        device_list: List[str] = []

        for device in data:
            device_list.append(device)

        return UserInfo(device_list, len(device_list))
