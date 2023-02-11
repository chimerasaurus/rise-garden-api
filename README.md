# rise-garden-api
Python client for the [Rise Garden](https://www.risegardens.com) API.

*This is a (messy) work in progress.*

## Description
The Rise Garden is an indoor hydroponic garden. This Python module works with the Rise Garden API. This API provides information about your garden(s) and allows you to change the state of the garden (_eg:_ Turn lights on and off.) 

### Functionality
Specifically, this Python module has the folling functionality when working with the Rise API:

* Get Rise Gardens
* Get information for each garden
  * ID
  * Name
  * Last reading datestamp
  * Type
  * Mainboard and software information
  * Network / wifi details
  * Tank status
    * Water level
    * Water LED status
  * Ambient temperature
* Adjust lights
  * Toggle on and off
  * Set light level

## Notes
*This is an unofficial project and not associated with Rise Gardens*. This project is also inspired by and based on [homebridge-rise-garden](https://github.com/viamin/homebridge-rise-garden) by Bart Agapinan. I wanted a Python module so I could build a Home Assistant integration. 
