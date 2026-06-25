"""Centralized detector tiling configuration for stitched acquisitions.

This module is intentionally data-focused so tiling definitions are easy to
review and update without editing measurement logic.
"""


TILING_CONFIG = {
    "ygaps": {
        "tile_count": 2,
        "positions": {
            "pos1": {
                "label": "pos1",
                "index": 1,
                "detector_position": "lower",
                "detector_offsets": {
                    "pilatus2M": {"SAXSy": 0},
                    "pilatus800": {"WAXSy": 0},
                },
            },
            "pos2": {
                "label": "pos2",
                "index": 2,
                "detector_position": "upper",
                "detector_offsets": {
                    "pilatus2M": {"SAXSy": 5.16},
                    "pilatus800": {"WAXSy": 5.16},
                },
            },
        },
        "measurement_order": ["pos1", "pos2"],
    },
    "xygaps": {
        "tile_count": 4,
        "positions": {
            "pos1": {
                "label": "pos1",
                "index": 1,
                "detector_position": "lower_left",
                "detector_offsets": {
                    "pilatus2M": {"SAXSx": 0, "SAXSy": 0},
                    "pilatus800": {"WAXSx": 0, "WAXSy": 0},
                },
            },
            "pos2": {
                "label": "pos2",
                "index": 2,
                "detector_position": "upper_left",
                "detector_offsets": {
                    "pilatus2M": {"SAXSx": 0, "SAXSy": 5.16},
                    "pilatus800": {"WAXSx": 0, "WAXSy": 5.16},
                },
            },
            "pos3": {
                "label": "pos3",
                "index": 3,
                "detector_position": "lower_right",
                "detector_offsets": {
                    "pilatus2M": {"SAXSx": 5.16, "SAXSy": 0},
                    "pilatus800": {"WAXSx": -5.16, "WAXSy": 0},
                },
            },
            "pos4": {
                "label": "pos4",
                "index": 4,
                "detector_position": "upper_right",
                "detector_offsets": {
                    "pilatus2M": {"SAXSx": 5.16, "SAXSy": 5.16},
                    "pilatus800": {"WAXSx": -5.16, "WAXSy": 5.16},
                },
            },
        },
        "measurement_order": ["pos1", "pos2", "pos4", "pos3"],
    },
}


def get_tiling_config(tiling_mode):
    if tiling_mode not in TILING_CONFIG:
        raise ValueError("Unknown tiling mode: {}".format(tiling_mode))
    return TILING_CONFIG[tiling_mode]
