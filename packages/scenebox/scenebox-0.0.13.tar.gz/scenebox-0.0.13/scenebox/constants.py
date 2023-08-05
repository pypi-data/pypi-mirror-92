#  Copyright (c) 2020 Caliber Data Labs.
#  All rights reserved.
#

from datetime import datetime

import pytz


class JobConstants:
    STATUS_QUEUED = "queued"
    STATUS_RUNNING = "running"
    STATUS_FINISHED = "finished"
    STATUS_INITIALIZED = "initialized"
    STATUS_ABORTED = "aborted"
    STATUS_CANCELLED = "cancelled"


class OperationTypes:
    ANNOTATION = "annotation"
    SMOOTHING_TIME_SERIES = "smoothing_time_series"
    GROWTH_STAGES_EXTRACTION = "growth_stages_extraction"
    CDL_MASK_CREATION = "cdl_mask_creation"
    MULTISPECTRAL_TIME_SERIES_BUILDING = "multispectral_time_series_building"
    ROSBAGS_TO_XVIZ = "rosbags_to_xviz"

    VALID_TYPES = {
        ANNOTATION,
        SMOOTHING_TIME_SERIES,
        GROWTH_STAGES_EXTRACTION,
        CDL_MASK_CREATION,
        MULTISPECTRAL_TIME_SERIES_BUILDING,
        ROSBAGS_TO_XVIZ,
    }


class JobTypes:
    EXTRACTION = "media_extraction"
    SET_ADDITION = "set_addition"
    SET_REMOVAL = "set_removal"
    ZIPPING = "zipping"
    SESSION_RESOLUTION = "session_resolution"
    SESSION_DELETION = "session_deletion"
    ASSETS_REMOVAL = "media_removal"
    SESSION_ENRICHMENT = "session_enrichment"
    IMAGE_COMPRESSION = 'image_compression'
    VIDEO_COMPRESSION = 'video_compression'
    VIDEO_CONCATENATION = 'video_concatenation'
    SYNTHETIC_INDEXING = 'synthetic_indexing'
    COCO_FORMATTING = 'coco_formatting'
    VIDEO_EXTRACTION = 'video_extraction'
    SESSION_REGISTRATION = 'session_registration'

    VALID_TYPES = {
        None,
        EXTRACTION,
        SET_ADDITION,
        SET_REMOVAL,
        ZIPPING,
        SESSION_RESOLUTION,
        ASSETS_REMOVAL,
        SESSION_ENRICHMENT,
        IMAGE_COMPRESSION,
        VIDEO_COMPRESSION,
        VIDEO_CONCATENATION,
        SYNTHETIC_INDEXING,
        COCO_FORMATTING,
        VIDEO_EXTRACTION,
        SESSION_REGISTRATION,
        SESSION_DELETION
    } | OperationTypes.VALID_TYPES


class SessionTypes:
    ROSBAGS_SESSION_ID = "rosbags"
    VIDEOS_SESSION_ID = "videos"
    HLS_SESSION_ID = "hls"
    GENERIC_SESSION_ID = "generic"
    VALID_TYPES = {
        ROSBAGS_SESSION_ID,
        VIDEOS_SESSION_ID,
        HLS_SESSION_ID,
        GENERIC_SESSION_ID
    }


class AssetsConstants:
    MODELS_ASSET_ID = "models"
    SESSIONS_ASSET_ID = "sessions"
    ANNOTATION_PROJECTS_ASSET_ID = "annotation_projects"
    ANNOTATIONS_ASSET_ID = "annotations"
    CONFIGS_ASSET_ID = "configs"
    IMAGES_ASSET_ID = "images"
    LIDARS_ASSET_ID = "lidars"
    IMAGE_SEQUENCES_ASSET_ID = "image_sequences"
    VIDEOS_ASSET_ID = "videos"
    ROSBAGS_ASSET_ID = "rosbags"
    HLS_ASSET_ID = "geotifs"
    SETS_ASSET_ID = "sets"
    PROJECTS_ASSET_ID = "projects"
    OPERATIONS_ASSET_ID = "operations"
    JOBS_ASSET_ID = "jobs"
    ZIPFILES_ASSET_ID = "zipfiles"
    ZIPARRAYS_ASSET_ID = "ziparrays"
    SESSION_CONFIGURATIONS_ASSET_ID = "session_configurations"
    XVIZ_ASSET_ID = "xviz"
    LIDAR_SEQUENCES_ASSET_ID = "lidar_sequences"

    UNDEFINED_ASSET_TYPE = (
        None  # The asset manager can dynamically update its asset type
    )
    SESSIONS_MANAGER_ASSET_ID = "session_manager"  # TODO: This isn't really an asset
    TENSORS_ASSET_ID = "tensors"  # TODO: Tensors aren't used

    VALID_ASSETS = {
        MODELS_ASSET_ID,
        SESSIONS_ASSET_ID,
        ANNOTATION_PROJECTS_ASSET_ID,
        ANNOTATIONS_ASSET_ID,
        CONFIGS_ASSET_ID,
        IMAGES_ASSET_ID,
        LIDARS_ASSET_ID,
        VIDEOS_ASSET_ID,
        ROSBAGS_ASSET_ID,
        HLS_ASSET_ID,
        SETS_ASSET_ID,
        PROJECTS_ASSET_ID,
        OPERATIONS_ASSET_ID,
        JOBS_ASSET_ID,
        ZIPFILES_ASSET_ID,
        ZIPARRAYS_ASSET_ID,
        SESSION_CONFIGURATIONS_ASSET_ID,
        XVIZ_ASSET_ID,
        SESSIONS_MANAGER_ASSET_ID,
        TENSORS_ASSET_ID,
        IMAGE_SEQUENCES_ASSET_ID,
        LIDAR_SEQUENCES_ASSET_ID,
        UNDEFINED_ASSET_TYPE,
    }

    METADATA_ONLY_ASSETS = {
        SESSIONS_ASSET_ID,
        ANNOTATION_PROJECTS_ASSET_ID,
        ANNOTATIONS_ASSET_ID,
        CONFIGS_ASSET_ID,
        SETS_ASSET_ID,
        PROJECTS_ASSET_ID,
        OPERATIONS_ASSET_ID,
        JOBS_ASSET_ID,
        SESSION_CONFIGURATIONS_ASSET_ID,
        XVIZ_ASSET_ID,
        SESSIONS_MANAGER_ASSET_ID,
        TENSORS_ASSET_ID,
        UNDEFINED_ASSET_TYPE,
    }


class SetsAssets:
    VALID_ASSET_TYPES = {
        AssetsConstants.IMAGES_ASSET_ID,
        AssetsConstants.VIDEOS_ASSET_ID,
        AssetsConstants.ROSBAGS_ASSET_ID,
        AssetsConstants.SESSIONS_ASSET_ID,
        AssetsConstants.LIDARS_ASSET_ID,
        AssetsConstants.ANNOTATIONS_ASSET_ID,
        AssetsConstants.ZIPARRAYS_ASSET_ID,
        AssetsConstants.XVIZ_ASSET_ID,
    }


class SetsStates:
    READY = "ready"
    DELETE = "being deleted"
    MOVE = "moving assets"
    ZIP = "being zipped"
    POPULATING = "being populated"
    VALID_STATES = {
        READY,
        DELETE,
        MOVE,
        ZIP,
        POPULATING,
    }


class ConfigTypes:
    SEARCH = 'search'
    ANNOTATION_INSTRUCTION = 'annotation_instruction'
    ADMIN_PANEL = 'admin_panel'
    SESSION_VIEW = "session_view"
    SUMMARY_VIEW = "summary_view"
    HEADER_FILTER_GROUP = "header_filter_group"

    VALID_TYPES = {
        SEARCH,
        ANNOTATION_INSTRUCTION,
        ADMIN_PANEL,
        SESSION_VIEW,
        SUMMARY_VIEW,
        HEADER_FILTER_GROUP
    }


class EntityTypes:
    GEO_ENTITY_TYPE = 'geo'
    SCALAR_ENTITY_TYPE = 'scalar'
    VECTOR_ENTITY_TYPE = 'vector'
    STATE_ENTITY_TYPE = 'state'
    STATE_SET_ENTITY_TYPE = 'state_set'
    STATE_VECTOR_ENTITY_TYPE = 'state_vector'
    MEDIA = 'media'

    VALID_TYPES = {
        GEO_ENTITY_TYPE,
        SCALAR_ENTITY_TYPE,
        VECTOR_ENTITY_TYPE,
        STATE_VECTOR_ENTITY_TYPE,
        STATE_SET_ENTITY_TYPE,
        STATE_ENTITY_TYPE,
        STATE_VECTOR_ENTITY_TYPE
    }


class EntityNames:
    """This is the name as it appears when searching."""
    WEATHER_CONDITIONS = "weather_conditions"
    TRAFFIC_OBJECTS = 'traffic_objects'
    IMAGE = 'image'
    VIDEO = 'video'
    LIDAR = 'lidar'
    ZIPARRAY = 'ziparray'
    GEOLOCATION = 'geolocation'
    COMMENT = 'comment'
    COMMENTATOR = 'commentator'


class SummaryEntities:
    DEFAULT_ENTITIES_TO_SUMMARIZE = [
        "traffic_objects",
        "weather_descriptions",
        "country",
        "city",
        "comment",
        "commentator"]
    DEFAULT_ENTITY_SUMMARY_TYPES = [
        EntityTypes.STATE_SET_ENTITY_TYPE,
        EntityTypes.STATE_ENTITY_TYPE,
        EntityTypes.STATE_VECTOR_ENTITY_TYPE]


class AssetEntities:
    """This is used as a blacklist in searchable fields."""
    IMAGE = 'image'
    VIDEO = 'video'
    LIDAR = 'lidar'
    ZIPARRAY = 'ziparray'
    GEOLOCATION_LAT = 'geolocation.lat'
    GEOLOCATION_LON = 'geolocation.lon'


class EntityInfluenceTypes:
    POINT = 'point'
    LINEAR_INTERPOLATION = 'linear_interpolation'
    GEO_INTERPOLATION = 'geo_interpolation'
    INTERVAL = 'interval'
    START_STOP = 'start_stop'
    AFFECT_FORWARD = 'affect_forward'
    AFFECT_BACKWARD = 'affect_backward'

    VALID_TYPES = {
        POINT,
        LINEAR_INTERPOLATION,
        GEO_INTERPOLATION,
        INTERVAL,
        START_STOP,
        AFFECT_FORWARD,
        AFFECT_BACKWARD
    }


class AnnotationTypes:
    SEMANTIC_SEGMENTATION = "semantic_segmentation"
    TWO_D_BOUNDING_BOX = "two_d_bounding_box"
    CUBOID = "cuboid"
    POINT = "point"
    POLYGON = "polygon"
    LINE = "line"
    CLASSIFICATION = "classification"
    MIXED = "mixed"
    CUSTOM = "custom"

    VALID_TYPES = {
        SEMANTIC_SEGMENTATION,
        TWO_D_BOUNDING_BOX,
        CUBOID,
        POINT,
        POLYGON,
        LINE,
        CLASSIFICATION,
        CUSTOM,
        MIXED,
    }


class AnnotationMediaTypes:
    IMAGE = AssetsConstants.IMAGES_ASSET_ID
    VIDEO = AssetsConstants.VIDEOS_ASSET_ID
    LIDAR = AssetsConstants.LIDARS_ASSET_ID
    IMAGE_SEQUENCE = AssetsConstants.IMAGE_SEQUENCES_ASSET_ID
    LIDAR_SEQUENCE = AssetsConstants.LIDAR_SEQUENCES_ASSET_ID

    VALID_TYPES = {
        IMAGE,
        VIDEO,
        LIDAR,
        IMAGE_SEQUENCE,
        LIDAR_SEQUENCE,
    }


class AnnotationProviders:
    SCALE = "scale"
    SCALE_MOCKED = "scale_mocked"
    DEEPEN = "deepen"
    LABELBOX = "labelbox"
    MRCNN_INFERENCE = "mrcnn_inference_labelling"
    RENDERED = "rendered"
    MOTIONAL = "motional"

    VALID_PROVIDERS = {
        SCALE,
        SCALE_MOCKED,
        DEEPEN,
        LABELBOX,
        MRCNN_INFERENCE,
        RENDERED,
        MOTIONAL
    }


class SmoothingMediaTypes:
    ZIPARRAY = AssetsConstants.ZIPARRAYS_ASSET_ID
    SESSION = AssetsConstants.SESSIONS_ASSET_ID

    VALID_TYPES = {
        ZIPARRAY,
        SESSION,
    }


class SmoothingBands:
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'
    NIR_NARROW = 'nir_narrow'
    SWIR1 = 'swir1'
    SWIR2 = 'swir2'
    NDVI = 'ndvi'

    VALID_BANDS = {
        RED,
        BLUE,
        GREEN,
        NIR_NARROW,
        SWIR1,
        SWIR2,
        NDVI,
    }


class SearchableFieldTypes:
    TIME = "time"
    TAG = "tag"
    TEXT = "text"
    NUMBER = "number"
    GEO = "geo"
    BOOLEAN = "boolean"


class Tagging:
    TIME = "time"
    TAG = "tag"
    TEXT = "text"
    NUMBER = "number"
    GEO = "geo"
    BOOLEAN = "boolean"


class TrafficObjectTagging:
    GOOGLE_VISION = 'google-vision'
    MRCNN = 'mrcnn'


class SetTags:
    AUTOMATED_SET_CREATION_TAG = 'automatically-generated'
    EXTRACTION_SET_TAG = 'extraction'
    ANNOTATION_SET_TAG = 'annotation'


class WeatherStackAttributes:
    VISIBILITY = 'visibility'
    WEATHER_DESCRIPTION = 'weather_descriptions'


class AIRFLOW_DAG_IDS:
    VIDEO_INDEXING_DAG_ID = 'video-indexing-task'
    ROSBAG_INDEXING_DAG_ID = 'rosbag-indexing-task'
    SESSION_RESOLVING_DAG_ID = 'session-resolving-task'
    SESSION_DELETING_DAG_ID = 'session-deleting-task'


class RosbagsMessageTypes:
    IMAGE_MESSAGE_TYPE = "sensor_msgs/Image"
    FIX_MESSAGE_TYPE = "sensor_msgs/NavSatFix"
    IMU_MESSAGE_TYPE = "sensor_msgs/Imu"
    LIDAR_MESSAGE_TYPE = "sensor_msgs/PointCloud2"
    TF_MESSAGE_TYPE = "tf2_msgs/TFMessage"

    VALID_TYPES = {
        IMAGE_MESSAGE_TYPE,
        FIX_MESSAGE_TYPE,
        IMU_MESSAGE_TYPE,
        LIDAR_MESSAGE_TYPE,
        TF_MESSAGE_TYPE
    }


class Sensors:
    CAMERA = "CAM"
    LIDAR = "LIDAR"
    RADAR = "RADAR"

    VALID_SENSORS = {
        CAMERA,
        LIDAR,
        RADAR
    }


class UsageOperationTypes:
    CREATE_VIDEO_SESSION = "create_video_session"
    CREATE_SET = "create_set"
    CREATE_PROJECT = "create_project"
    CREATE_ANNOTATION = "create_annotation"
    CREATE_ZIPFILE = "create_zipfile"
    CREATE_CONFIG = "create_config"
    DO_VIDEO_EXTRACTION = "do_video_exaction"
    DO_IMAGE_EXTRACTION = "do_image_exaction"
    DO_LIDAR_EXTRACTION = "do_lidar_exaction"


class Time:
    START_OF_TIME_STRING = "1970-01-01T00:00:00Z"
    START_OF_TIME_DATETIME = datetime(1970, 1, 1, tzinfo=pytz.utc)
    END_OF_TIME_STRING = "2070-01-01T00:00:00Z"
    END_OF_TIME_DATETIME = datetime(2070, 1, 1, tzinfo=pytz.utc)


ACK_OK_RESPONSE = {"acknowledged": True}


class VideoTags:
    CONCATENATED = "concatenated"
    EXTRACTED = "extracted"
    RAW = "raw"


class AnnotationTags:
    EMPTY = "empty"
