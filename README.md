# Mealie Meal Planner Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Home Assistant integration for selfhosted Mealie.

## Installation
Under HACS -> Integrations, add custom repository "https://github.com/frizk/mealie-integration/" with Category "Integration". 

Search for repository "Mealie Meal Planner" and download it. Restart Home Assistant.

Create an API key in your selfhosted mealie installation.

Go to Settings > Integrations and Add Integration "Mealie". Type in ip address, port, and paste in your api key.

Restart Home Assistant.

## Provided sensor values ##

* sensor.today_meal -> The first meal found planned for current date

* sensor.current_week_<day>_meal -> Meal for specific weekdays in the current week number. Resets after weekday 6.
