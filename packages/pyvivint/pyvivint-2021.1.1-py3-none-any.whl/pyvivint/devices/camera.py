"""Module that implements the Camera class."""
from datetime import datetime
from typing import Callable, List

from pyvivint.constants import CameraAttribute as Attributes
from pyvivint.devices import VivintDevice
from pyvivint.devices.alarm_panel import AlarmPanel

# Some Vivint supported cameras may be connected directly to your local network
# and the Vivint API reports these as having direct access availiable (cda).
# Ping cameras (alpha_cs6022_camera_device) can be setup to connect to your own
# Wi-Fi via a complicated process involving removing and resetting the camera,
# initiating WPS on your Wi-Fi and the Ping camera, and then adding a new camera
# from the panel within a limited timeframe. The Ping camera, however, seems to
# still have a VPN connection with the panel that prevents direct access except
# on very rare occasions. As such, we want to skip this model from direct access.
SKIP_DIRECT = ["alpha_cs6022_camera_device"]


class Camera(VivintDevice):
    """Represents a vivint camera device."""

    def __init__(self, data: dict, alarm_panel: AlarmPanel):
        super().__init__(data, alarm_panel)
        self.__thumbnail_ready_callbacks: List[Callable] = list()

    @property
    def manufacturer(self):
        """Return the camera manufacturer."""
        return self.data.get(Attributes.ACTUAL_TYPE).split("_")[0].title()

    @property
    def model(self):
        """Return the camera model."""
        return self.data.get(Attributes.ACTUAL_TYPE).split("_")[1].upper()

    @property
    def serial_number(self) -> str:
        """Return the camera's mac address as the serial number."""
        return self.mac_address

    @property
    def software_version(self) -> str:
        """Return the camera's software version."""
        return self.data.get(Attributes.SOFTWARE_VERSION)

    @property
    def capture_clip_on_motion(self) -> bool:
        "Return True if capture clip on motion is active."
        return self.data[Attributes.CAPTURE_CLIP_ON_MOTION]

    @property
    def ip_address(self) -> str:
        "Camera's IP address."
        return self.data[Attributes.CAMERA_IP_ADDRESS]

    @property
    def mac_address(self) -> str:
        """Camera's MAC Address"""
        return self.data[Attributes.CAMERA_MAC]

    @property
    def is_in_privacy_mode(self) -> bool:
        """Return True if privacy mode is active."""
        return self.data[Attributes.CAMERA_PRIVACY]

    @property
    def is_online(self) -> bool:
        """Return True if camera is online."""
        return self.data[Attributes.ONLINE]

    @property
    def wireless_signal_strength(self) -> int:
        """Camera's wireless signal strength."""
        return self.data[Attributes.WIRELESS_SIGNAL_STRENGTH]

    def add_thumbnail_ready_callback(self, callback: Callable) -> None:
        """Register a thumbnail_ready callback."""
        self.__thumbnail_ready_callbacks.append(callback)

    async def request_thumbnail(self) -> None:
        """Request a new thumbnail for the camera."""
        await self.vivintskyapi.request_camera_thumbnail(
            self.alarm_panel.id, self.alarm_panel.partition_id, self.id
        )

    async def get_thumbnail_url(self) -> str:
        """Returns the latest camera thumbnail URL."""
        camera_thumbnail_date = datetime.strptime(
            self.data[Attributes.CAMERA_THUMBNAIL_DATE], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        thumbnail_timestamp = int(camera_thumbnail_date.timestamp() * 1000)

        return await self.vivintskyapi.get_camera_thumbnail_url(
            self.alarm_panel.id,
            self.alarm_panel.partition_id,
            self.id,
            thumbnail_timestamp,
        )

    async def get_rtsp_url(self, internal: bool = False, hd: bool = False) -> str:
        """Returns the rtsp URL for the camera."""
        credentials = await self.alarm_panel.get_panel_credentials()
        url = self.data[f"c{'i' if internal else 'e'}u{'' if hd else 's'}"][0]
        return f"{url[:7]}{credentials[u'n']}:{credentials[u'pswd']}@{url[7:]}"

    async def get_direct_rtsp_url(self, hd: bool = False) -> str:
        """Returns the direct rtsp url for this camera, in HD if requested, if any."""
        return (
            f"rtsp://{self.data[u'un']}:{self.data[u'pswd']}@{self.ip_address}:{self.data[Attributes.CAMERA_IP_PORT]}/{self.data[u'cdp' if hd else u'cdps']}"
            if self.data["cda"] and self.data.get("act") not in SKIP_DIRECT
            else None
        )

    def handle_pubnub_message(self, message: dict) -> None:
        """Handles a pubnub message addressed to this camera."""
        super().handle_pubnub_message(message)

        if message.get(Attributes.CAMERA_THUMBNAIL_DATE):
            self._fire_callbacks(self.__thumbnail_ready_callbacks)
