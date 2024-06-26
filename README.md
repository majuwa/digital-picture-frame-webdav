# Python Scripts to Use for a Digital Frame

This is a simple Python scripts which connects to a WebDAV folder and iteratively show the images within. It thereby prints the images directly to the screen buffer without requiring an installed desktop environment. My use case is to use it as a digital frame for showing my pictures stored in a Nextcloud folder. It runs on a Raspberry Pi Zero 2W.

**Attention:** The script is a bit rough and makes many assumptions. For my use case it works, but there is no guarantee. Use with caution. 

## Requirements
* *Pygame* - to display the images
* *webdavclient3* - to download the images from a WebDAV repository

The concrete packages and versions are listed in the `requirements.txt`.

## Installation

The installation consist of the following steps:

* Installation of the Python dependencies, e.g. by using the `requirements.txt` and pip
* Installation of the OS dependencies
    * Pygame uses SDL2 to write the images into the buffer
    * SDL2 needs to be installed, e.g. for Debian `sudo apt install libsdl2-2.0-0 libsdl2-ttf-2.0-0`

## Configuration

The webdav server connection is configured by configuration file. This uses the default syntax from the webdav3.client By default, it expects a `config.json` in the current working directory. The path can be adapted within the variable `config_file_path`. An example configuration looks like:

```json
{
    "webdav_hostname": "test-url/folder/diashow",
    "webdav_login":    "test-user",
    "webdav_password": "test-password",
    "webdav_timeout": 60,
    "online_check_address" : "http://test-url",
    "image_duration" : 30,
    "width" : 1024,
    "height" : 600
}
```

| **Field value** | **Description** |
|---------------|----------------|
| `webdav_hostname` | path to the `diashow`folder. A folder called `diashow` is expected |
| `webdav_login` | Webdav username |
| `webdav_password`| Password of the webdav user |
|`webdav_timeout` | Timeout for the webdav connection |
| `online_check_address` | Address which the scripts uses to check whether the network connection is up |
| `image_duration` | the time in seconds each image is shown |
| `width` | the screen width in pixels |
| `height` |the screen height in pixels |
