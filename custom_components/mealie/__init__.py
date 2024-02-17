"""The Mealie Meal Planner integration."""
from __future__ import annotations
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from homeassistant.const import CONF_HOST, CONF_PORT, CONF_API_KEY
from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Mealie Meal Planner from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.unique_id] = MealieHub(entry.data.get(CONF_HOST), entry.data.get(CONF_PORT), entry.data.get(CONF_API_KEY))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class MealieHub:
    def __init__(self, host: str, port: str, api_key: str) -> None:
        self.host = host
        self.port = port
        self._api_key = api_key

    async def authenticate(self) -> bool:
        _LOGGER.info("Authenticating to %s with API key %s", self.host, self._api_key)
        return True