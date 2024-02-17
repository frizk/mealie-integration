"""Platform for sensor integration."""
from __future__ import annotations
import aiohttp
import logging
import calendar
import json
import datetime

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import Entity
from . import MealieHub
from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    add_entities([])


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    mealie: MealieHub = hass.data[DOMAIN][config_entry.unique_id]
    entities = [MealieSensor(mealie.host, mealie.port, mealie._api_key)]
    for i in range (0, 7):
        entities.append(MealieSensor(mealie.host, mealie.port, mealie._api_key, i))
    async_add_entities(entities)


class MealieSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, host: str, port: str, api_key: str, day: int | None = None) -> None:
        self.host = host
        self.port = port
        self._api_key = api_key
        self._state = None
        self._attributes = {}
        self._day = day
        if day is None:
            self._unique_id = f"{host}_{port}_today_dinner"
            self._name = "Today Meal"
        else:
            dayname = calendar.day_name[day]
            self._unique_id = f"{host}_{port}_current_week_{dayname}_dinner"
            self._name = f"Current Week {dayname} Meal"

    @property
    def state(self):
        """Return the meal name."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        return self._attributes

    @property
    def name(self):
        """Return the name."""
        return self._name

    @property
    def unique_id(self):
        return self._unique_id

    async def async_update(self) -> None:
        """
        Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        headers = {"Authorization": f"Bearer {self._api_key}"}
        if self._day is None:
            url = f"http://{self.host}:{self.port}/api/groups/mealplans/today"
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as resp:
                    data = await resp.read()
                    if resp.ok:
                        data_entries = json.loads(data.decode("UTF-8"))
                        if len(data_entries) > 0:
                            today_recipe = data_entries[0]["recipe"]
                            self._map_recipe(today_recipe)
                    else:
                        _LOGGER.error("GET today meal returned: %s", resp)
        else:
            url = f"http://{self.host}:{self.port}/api/groups/mealplans"
            current_date = datetime.date.today()
            query_date = (current_date + datetime.timedelta(days=self._day) - datetime.timedelta(days=current_date.weekday())).isoformat()
            params = {
                "start_date": query_date,
                "end_date": query_date
            }
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url, params=params) as resp:
                    data = await resp.read()
                    if resp.ok:
                        data_entries = json.loads(data.decode("UTF-8"))
                        if "items" in data_entries and len(data_entries["items"]) > 0:
                            recipe = data_entries["items"][0]["recipe"]
                            self._map_recipe(recipe)
                    else:
                        _LOGGER.error("GET today meal returned: %s", resp)

    def _map_recipe(self, recipe: dict):
        self._state = recipe["name"]
        self._attributes['description'] = recipe.get("description")
        self._attributes['originalURL'] = recipe.get("orgURL")
        self._attributes['lastMade'] = recipe.get("lastMade")
        self._attributes['id'] = recipe.get("id")
        self._attributes['userId'] = recipe.get("userId")
        self._attributes['groupId'] = recipe.get("groupId")
        self._attributes['slug'] = recipe.get("slug")
        self._attributes['prepTime'] = recipe.get("prepTime")
        self._attributes['cookTime'] = recipe.get("cookTime")
        self._attributes['totalTime'] = recipe.get("totalTime")
        self._attributes['performTime'] = recipe.get("performTime")
        self._attributes['recipeCategory'] = recipe.get("recipeCategory")
        self._attributes['tags'] = recipe.get("tags")
        self._attributes['tools'] = recipe.get("tools")
        self._attributes['rating'] = recipe.get("rating")
        self._attributes['dateAdded'] = recipe.get("dateAdded")
        self._attributes['dateUpdated'] = recipe.get("dateUpdated")
        self._attributes['createdAt'] = recipe.get("createdAt")
        self._attributes['updateAt'] = recipe.get("updateAt")
        self._attributes['day'] = self._day

