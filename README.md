# Python Script for a Digital Frame

A Python script that displays images on a screen in a continuous slideshow. It supports multiple image sources: a WebDAV server (e.g. Nextcloud), a local folder, or a USB stick. Images are automatically rotated based on their EXIF orientation. It runs on a Raspberry Pi Zero 2W using Pygame to write directly to the screen buffer without requiring a desktop environment.

**Attention:** The script is a bit rough and makes many assumptions. For my use case it works, but there is no guarantee. Use with caution.

## Requirements
* *Pygame* - to display the images
* *Pillow* - for EXIF-based image rotation
* *webdavclient3* - to download images from a WebDAV server (only needed for the `webdav` source)

The concrete packages and versions are listed in the `requirements.txt`.

## Installation

* Install the Python dependencies, e.g. using `requirements.txt` and pip
* Install the OS dependencies:
    * Pygame uses SDL2 to write images into the buffer
    * SDL2 needs to be installed, e.g. for Debian: `sudo apt install libsdl2-2.0-0 libsdl2-ttf-2.0-0`

## Usage

```bash
python digital_frame.py [path/to/config.json]
```

The config path defaults to `config.json` in the current working directory if not provided.

## Configuration

The image source and display settings are configured via a JSON file. The `source` field selects which image source to use.

### WebDAV (e.g. Nextcloud)

```json
{
    "source": "webdav",
    "webdav_hostname": "https://your-nextcloud/remote.php/dav/files/user/diashow",
    "webdav_login":    "user",
    "webdav_password": "password",
    "webdav_timeout":  60,
    "online_check_address": "live-address-to-check",
    "image_duration": 30,
    "width": 1024,
    "height": 600
}
```

### Local Folder

```json
{
    "source": "local_folder",
    "image_folder": "/path/to/images",
    "image_duration": 30,
    "width": 1024,
    "height": 600
}
```

### USB Stick

```json
{
    "source": "usb_mount",
    "usb_device": "/dev/sda1",
    "usb_mount_point": "/mnt/stick",
    "image_duration": 30,
    "width": 1024,
    "height": 600
}
```

### Configuration Fields

| **Field** | **Description** |
|---|---|
| `source` | Image source: `webdav`, `local_folder`, or `usb_mount` |
| `webdav_hostname` | Full URL to the WebDAV folder |
| `webdav_login` | WebDAV username |
| `webdav_password` | WebDAV password |
| `webdav_timeout` | Timeout in seconds for the WebDAV connection |
| `online_check_address` | URL polled until reachable before starting (optional) |
| `image_folder` | Path to the local image folder (`local_folder` source) |
| `usb_device` | Device path of the USB stick, e.g. `/dev/sda1` (`usb_mount` source) |
| `usb_mount_point` | Mount point for the USB stick (`usb_mount` source) |
| `image_duration` | Time in seconds each image is shown |
| `width` | Screen width in pixels |
| `height` | Screen height in pixels |
