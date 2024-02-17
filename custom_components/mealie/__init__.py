"""The Mealie Meal Planner integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from homeassistant.const import CONF_HOST, CONF_PORT, CONF_API_KEY
from .const import DOMAIN

# TODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Mealie Meal Planner from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    # TODO 1. Create API instance
    # TODO 2. Validate the API connection (and authentication)
    # TODO 3. Store an API object for your platforms to access
    hass.data[DOMAIN][entry.unique_id] = MealieHub(entry.data.get(CONF_HOST), entry.data.get(CONF_PORT), entry.data.get(CONF_API_KEY))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    hass.states.async_set("mealie.host", entry.data.get(CONF_HOST))
    hass.states.async_set("mealie.port", entry.data.get(CONF_PORT))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class MealieHub:
    def __init__(self, host: str, port: str, api_key: str):
        self.host = host
        self.port = port
        self._api_key = api_key