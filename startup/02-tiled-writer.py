import numpy
import os

from bluesky_tiled_plugins import TiledWriter
from bluesky.callbacks.buffer import BufferingWrapper
from tiled.client import from_uri


# Mapping from spec to mimetype for use in TiledWriter
# TODO: Only keep the necessary specs here
MIMETYPE_LOOKUP = {
        "AD_TIFF": "multipart/related;type=image/tiff",
        "HDF5": "application/x-hdf5",

        # "A1_HDF5": "application/x-hdf5",  # esm_patches:A1SoftFileHandler(HDF5DatasetSliceHandler)
        # "AD_CBF": "multipart/related;type=image/tiff",
        # "AD_EIGER_MX": "application/x-hdf5",
        # "AD_EIGER2": "application/x-hdf5",
        # "AD_JPEG": "multipart/related;type=image/jpeg",
        # "AD_HDF5": "application/x-hdf5",
        # "AD_HDF5_GERM": "application/x-hdf5",
        # "AD_HDF5_SWMR_STREAM": "application/x-hdf5",
        # "AD_HDF5_SWMR_SLICE": "application/x-hdf5",
        # "AD_HDF5_SWMR": "application/x-hdf5",
        # "AD_HDF5_TS": "application/x-hdf5",    # area_detector_handlers.handlers:AreaDetectorHDF5TimestampHandler
        # "AD_HDF5_DET_TS": "application/x-hdf5",    # csx_transforms.AreaDetectorHDF5NDArrayTimeStampHandler
        # "APB": "application/x-pizzabox-binary",     # columns: timestamp, i0, it, ir, iff, aux1, aux2, aux3, aux4.   iss_patches:APBBinFileHandler
        # "APB_TRIGGER": "application/x-pizzabox-binary",  # columns: timestamp, transition,   iss_patches:APBTriggerFileHandler
        # "DEX_HDF5": "application/x-hdf5",
        # "EIGER2_STREAM": "application/x-hdf5",
        # "MERLIN_FLY_STREAM_V2": "application/x-hdf5",
        # "MERLIN_HDF5_BULK": "application/x-hdf5",
        # "PANDA": "application/x-hdf5",
        # "PIL100k_HDF5": "application/x-hdf5",      # iss_patches:ISSPilatusHDF5Handler
        # "PILATUS_HDF5": "application/x-hdf5",
        # "ROI_HDF5_FLY": "application/x-hdf5",
        # "ROI_HDF51_FLY": "application/x-hdf5",
        # "SIS_HDF51_FLY_STREAM_V1": "application/x-hdf5",
        # "TPX_HDF5": "application/x-hdf5",
        # "NPY_SEQ": "multipart/related;type=application/x-npy",
        # "SIS_HDF51": "application/x-hdf5",
        # "SPECS_HDF5_SINGLE_DATAFRAME": "application/x-hdf5",    # IOS
        # "XIA_XMAP_HDF5": "application/x-hdf5;type=xia-xmap",
        # "XSP3": "application/x-hdf5",        # iss_patches:ISSXspress3HDF5Handler, area_detector_handlers.handlers:Xspress3HDF5Handler
        # "XSP3_BULK": "application/x-hdf5",
        # "XSP3_FLY": "application/x-hdf5",
        # "XSP3_STEP": "application/x-hdf5",   # databroker.assets.handlers:Xspress3HDF5Handler, area_detector_handlers.handlers:Xspress3HDF5Handler
        # "XSP3X": "application/x-hdf5",
    }


# Define document-specific patches to be applied before sending them to TiledWriter
def patch_resource(doc):

    kwargs = doc.get("resource_kwargs", {})

    # Fix the resource path
    root = doc.get("root", "")
    if not doc["resource_path"].startswith(root):
        doc["resource_path"] = os.path.join(root, doc["resource_path"])
    doc["root"] = ""
    doc["resource_path"] = doc["resource_path"].replace("/nsls2/data3/cms", "/nsls2/data/cms")

    if doc.get("spec") in ["AD_TIFF"]:
        kwargs["template"] = "/" + kwargs["template"].lstrip("/")    # Ensure leading slash
        # kwargs["join_method"] = "stack"
        kwargs["join_method"] = "concat"

    return doc


def patch_descriptor(doc):
    for desc in doc['data_keys'].values():
        if len(desc["shape"]) < 3:
            desc["shape"] = [1]*(3-len(desc["shape"])) + desc["shape"]

    if 'pilatus800_image' in doc['data_keys']:
        desc = doc['data_keys']['pilatus800_image']
        desc.setdefault("dtype_str", "<i4")
        shape = desc['shape']
        if shape[-1] == 0:
            shape[-1] = 1
            desc['shape'] = shape[::-1]

    # Ensure dtype_str has the proper numpy format (to pass the EventModel validator)
    for key, val in doc["data_keys"].items():
        if "dtype_str" in val:
            val["dtype_str"] = numpy.dtype(val["dtype_str"]).str
        val["shape"] = tuple(map(lambda x: max(x, 0), val.get("shape", [])))

    return doc


# Initialize the Tiled client and the TiledWriter
api_key = os.environ.get("TILED_BLUESKY_WRITING_API_KEY_CMS")
tiled_writing_client_sql = from_uri("https://tiled.nsls2.bnl.gov", api_key=api_key)['cms/migration']
tw = TiledWriter(client = tiled_writing_client_sql,
                 backup_directory="/tmp/tiled_backup",   # NOTE: Pick a suitable backup directory
                 patches = {"descriptor": patch_descriptor,
                            "resource": patch_resource},
                 spec_to_mimetype = MIMETYPE_LOOKUP,
                 batch_size=10000   # NOTE: Set to 1 to disable batching
                 )

# Thread-safe wrapper for TiledWriter
tw = BufferingWrapper(tw)

# Subscribe the TiledWriter
RE.md["tiled_access_tags"] = (RE.md["data_session"],)
RE.subscribe(tw)
