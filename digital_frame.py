import pygame
import io
import time
import json
import os
import sys
from urllib import request
from PIL import Image, ImageOps


IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png")


# --- Config ---

def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {file_path}: {e}")
        return None


# --- Image utilities ---

def load_image_with_orientation(source):
    """Loads an image (from a file path or file-like object), corrects EXIF orientation."""
    with Image.open(source) as img:
        img = ImageOps.exif_transpose(img)
        img = img.convert("RGB")
        mode = img.mode
        size = img.size
        data = img.tobytes()
        return pygame.image.fromstring(data, size, mode)


def aspect_scale(img, bx, by):
    ix, iy = img.get_size()
    if ix > iy:
        scale_factor = bx / float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by / float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        scale_factor = by / float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx / float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by
    return pygame.transform.scale(img, (int(sx), int(sy)))


def is_image_file(filename):
    return (
        not filename.startswith(".")
        and "." in filename
        and filename.lower().endswith(IMAGE_EXTENSIONS)
    )


# --- Image sources ---

class LocalFolderSource:
    """Yields images from a local directory."""

    def __init__(self, folder_path):
        self.folder_path = folder_path

    def iter_images(self):
        files = sorted(f for f in os.listdir(self.folder_path) if is_image_file(f))
        for filename in files:
            yield os.path.join(self.folder_path, filename), filename


class UsbMountSource:
    """Mounts a USB device if needed, then yields images from it."""

    def __init__(self, device_path, mount_point):
        self.device_path = device_path
        self.mount_point = mount_point

    def _is_mounted(self):
        try:
            with open("/proc/mounts", "r") as f:
                for line in f:
                    parts = line.split()
                    if len(parts) >= 2 and parts[0] == self.device_path:
                        if parts[1] == self.mount_point:
                            return True
            return False
        except FileNotFoundError:
            print("Error: /proc/mounts not found. USB mount check requires Linux.")
            return False

    def _ensure_mounted(self):
        if self._is_mounted():
            print("Device already mounted, skipping")
            return
        import subprocess
        print(f"Mounting {self.device_path} to {self.mount_point}")
        subprocess.run(["mount", self.device_path, self.mount_point], check=True)

    def iter_images(self):
        self._ensure_mounted()
        files = sorted(f for f in os.listdir(self.mount_point) if is_image_file(f))
        for filename in files:
            yield os.path.join(self.mount_point, filename), filename


class WebDavSource:
    """Streams images from a WebDAV server (e.g. Nextcloud) into memory."""

    def __init__(self, options):
        self.options = options

    def iter_images(self):
        from webdav3.client import Client
        client = Client(self.options)
        for filename in client.list():
            if filename.endswith("/"):
                continue
            res = client.resource(filename)
            buffer = io.BytesIO()
            res.write_to(buffer)
            buffer.seek(0)
            yield buffer, filename


def create_source(options):
    source_type = options.get("source", "local_folder")
    if source_type == "usb_mount":
        return UsbMountSource(
            device_path=options["usb_device"],
            mount_point=options["usb_mount_point"],
        )
    if source_type == "webdav":
        return WebDavSource(options)
    return LocalFolderSource(folder_path=options["image_folder"])


# --- Display ---

def internet_on(domain):
    try:
        request.urlopen(domain, timeout=1)
        return True
    except request.URLError as err:
        print(err)
        return False


def handle_error(screen, font, options, e):
    print(e)
    pygame.event.get()
    screen.fill("black")
    message = "Error: " + repr(e)
    text_color = (255, 255, 255)
    text_surface = font.render(message, True, text_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (options["width"] / 2, options["height"] / 2)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()


def display_image(screen, options, image_source, label):
    pygame.event.get()
    screen.fill("black")
    img = load_image_with_orientation(image_source)
    img = aspect_scale(img, options["width"], options["height"])
    imgrect = img.get_rect()
    imgrect.center = (options["width"] / 2, options["height"] / 2)
    screen.blit(img, imgrect)
    pygame.display.flip()
    print(f"Showing: {label}")
    time.sleep(options["image_duration"])


# --- Main ---

def main():
    config_file_path = sys.argv[1] if len(sys.argv) > 1 else "config.json"
    options = load_config(config_file_path)
    if options is None:
        sys.exit(1)

    if "online_check_address" in options:
        while not internet_on(options["online_check_address"]):
            time.sleep(2)

    pygame.init()
    screen = pygame.display.set_mode((options["width"], options["height"]))
    pygame.mouse.set_visible(False)
    font = pygame.font.Font(None, 36)

    source = create_source(options)

    while True:
        try:
            for image_source, label in source.iter_images():
                try:
                    display_image(screen, options, image_source, label)
                except (Exception, OSError) as e:
                    handle_error(screen, font, options, e)
                    time.sleep(5)
        except (Exception, OSError) as e:
            handle_error(screen, font, options, e)
            time.sleep(5)


if __name__ == "__main__":
    main()
    pygame.quit()
