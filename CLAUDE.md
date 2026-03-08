# Claude Code Instructions

## Project
Digital picture frame — displays images in a slideshow via Pygame. Runs on a Raspberry Pi Zero 2W. Single entry point: `digital_frame.py`.

## Running
Always use the project virtual environment:
```bash
.venv/bin/python digital_frame.py [config.json]
```

## Image Sources
Configured via the `"source"` field in `config.json`:
- `"webdav"` — streams from a WebDAV server (e.g. Nextcloud) using in-memory BytesIO buffers
- `"local_folder"` — reads from a local directory
- `"usb_mount"` — mounts a USB device (Linux only, uses `/proc/mounts`) then reads from it

## Key Conventions
- All sources implement `iter_images()` yielding `(source, label)` tuples
- `source` is a file path (local/USB) or `BytesIO` buffer (WebDAV)
- `load_image_with_orientation()` accepts both — PIL's `Image.open()` handles either
- EXIF auto-rotation is applied via `ImageOps.exif_transpose()` for all sources
- `online_check_address` in config is optional — if present, the script waits for it to be reachable before starting
