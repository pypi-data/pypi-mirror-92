import requests
from numpy import arange
import logging
from PIL import Image
import io
from .config import SlideCloudUrl
from .auth import get_access_token

logger = logging.getLogger(__name__)


class SlideCloudStorage:
    metadata_url = f"{SlideCloudUrl}/api/app/slideClientOnly/slideMetadata"
    tile_url = f"{SlideCloudUrl}/api/app/slideClientOnly/tileUrl"

    def get_metadata(self, slide_id):
        access_token = get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f'{self.metadata_url}/{slide_id}'
        metadata = requests.get(url, headers=headers).json()

        if 'error' in metadata:
            raise ValueError(metadata['error']['message'])

        result = Metadata(metadata)
        result.SlideId = slide_id
        return result

    def get_tile(self, slide_id, row, column, layer, lod):
        url = f'{self.tile_url}?id={slide_id}&Row={row}&Column={column}&Layer={layer}&LODLevel={lod}'
        access_token = get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        tile_url = requests.get(url, headers=headers).content
        response = requests.get(tile_url)

        if response.status_code >= 200 and response.status_code <= 299:
            return response.content
        return None


class Metadata(object):
    SlideId = ''
    Name = ''
    LayerCount = 0
    MinimumLODLevel = 0
    MaximumLODLevel = 0
    LODGaps = []
    QuickHash = ''
    Vendor = ''
    Version = None
    Comments = ''
    BackgroundColor = None
    HorizontalTileCount = 0
    VertialTileCount = 0
    LayerCount = 0
    TileSize = {}
    ContentRegion = {}
    HorizontalResolution = 0
    VeriticalResolution = 0
    AdditionalData = {}

    def __init__(self, metadata_dict):
        self.__dict__ = metadata_dict

    def get_default_layer(self):
        return 1 if self.LayerCount == 1 else 0

    def get_lod_to_world_scale(self, lod):
        if(lod < 0 or lod > self.MaximumLODLevel):
            raise ValueError(
                f'load {lod} out of range [0-{self.MaximumLODLevel}]')

        scale = 1.0

        if lod != 0:
            for gap in self.LODGaps:
                scale /= gap

        return scale


class Slide:
    def __init__(self, metadata, slide_storage):
        self._metadata = metadata
        self._slide_storage = slide_storage

    def read_region(self, x, y, width, height, layer, lod):
        final_layer = layer if layer else self._metadata.get_default_layer()
        final_lod = lod if lod else self._metadata.MinimumLODLevel
        tile_width = self._metadata.TileSize['Width']
        tile_height = self._metadata.TileSize['Height']
        tile_index_left = x / tile_width
        tile_index_top = y / tile_height
        tile_index_right = (x + width - 1) / tile_width
        tile_index_bottom = (y+height - 1)/tile_height

        new_image = Image.new('RGB', (width, height), (255, 255, 255))

        offset_y = y
        for row in arange(tile_index_top, tile_index_bottom, 1.0):
            row = int(row)
            tile_top = row * tile_height
            offset_x = x
            step_y = offset_y - tile_top
            for column in arange(tile_index_left, tile_index_right, 1.0):
                column = int(column)
                tile_left = column * tile_width
                step_x = offset_x - tile_left
                tile_data = self._slide_storage.get_tile(
                    self._metadata.SlideId, int(row), int(column), final_layer, final_lod)
                logger.info(
                    f'get tile {row}-{column}-{final_layer}-{final_lod} data')
                if tile_data:
                    image = Image.open(io.BytesIO(tile_data))
                    image_valid_area = (step_x,
                                        step_y,
                                        tile_width,
                                        tile_height)
                    cropped_image = image.crop(image_valid_area)
                    # cropped_image.save(f"{image_valid_area}.jpg")
                    new_image.paste(cropped_image, (offset_x - x, offset_y-y))
                offset_x += tile_width - step_x
            offset_y += tile_height - step_y
        return new_image


def open_slide(slide_id):
    slide_storage = SlideCloudStorage()
    metadata = slide_storage.get_metadata(slide_id)
    return Slide(metadata, slide_storage)


if __name__ == "__main__":
    slide = open_slide("4395d816-2832-e7b7-6472-39f9b9f93480")
    metadata = slide._metadata
