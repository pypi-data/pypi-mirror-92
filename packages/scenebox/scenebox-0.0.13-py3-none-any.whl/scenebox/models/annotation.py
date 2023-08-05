#  Copyright (c) 2020 Caliber Data Labs.
#  All rights reserved.
#
import logging

from ..clients.asset_manager_client import AssetManagerClient
from ..constants import (AnnotationMediaTypes, AnnotationProviders,
                         AnnotationTypes)
from ..custom_exceptions import InvalidAnnotationError
from ..tools import misc, time_utils


class Annotation(object):
    def __init__(
            self,
            asset_manager_client=None,
            annotation_meta=None):
        self.id = None
        self.timestamp = None
        self.asset_id = None
        self.media_type = None
        self.provider = None
        self.annotation_type = None
        self.annotation_entities = []
        self.annotation_meta = annotation_meta or {}
        self.sets = []
        self.session_uid = None
        self.sensor = None

        try:
            self.set_id()
            self.set_timestamp()
            self.set_asset_id()
            self.set_media_type()
            self.set_provider()
            self.set_annotation_type()
            self.set_annotation_entities()
            self.set_set_membership()
            if asset_manager_client is not None:
                self.set_session_uid(
                    asset_manager_client=asset_manager_client)
                self.set_sensor(
                    asset_manager_client=asset_manager_client
                )
        except KeyError as e:
            logging.error("Failed to create the annotation::: {}".format(e))
            # raise InvalidAnnotationError(str(e))

        self.__sanity_check()

    def set_id(self):
        self.id = None

    def set_session_uid(self, asset_manager_client: AssetManagerClient):
        self.set_asset_id()
        self.set_media_type()

        session_uid = asset_manager_client.with_asset_state(
            self.media_type,
            True).get_metadata(
            self.asset_id).get('session_uid')

        self.session_uid = session_uid

    def set_sensor(self, asset_manager_client: AssetManagerClient):
        self.set_asset_id()
        self.set_media_type()

        sensor = asset_manager_client.with_asset_state(
            self.media_type,
            True).get_metadata(
            self.asset_id).get('sensor')

        self.sensor = sensor

    def set_timestamp(self):
        self.timestamp = None

    def set_asset_id(self):
        self.asset_id = None

    def set_media_type(self):
        self.media_type = None

    def set_provider(self):
        self.provider = None

    def set_annotation_type(self):
        self.annotation_type = None

    def set_annotation_entities(self):
        self.annotation_entities = []

    def set_set_membership(self):
        self.sets = []

    def __sanity_check(self):
        if self.annotation_type not in AnnotationTypes.VALID_TYPES:
            raise InvalidAnnotationError(
                "invalid annotation type {}".format(self.annotation_type)
            )

        if self.provider not in AnnotationProviders.VALID_PROVIDERS:
            raise InvalidAnnotationError(
                "invalid annotation provider {}".format(self.provider)
            )

        if self.media_type not in AnnotationMediaTypes.VALID_TYPES:
            raise InvalidAnnotationError(
                "invalid annotation type {}".format(self.media_type)
            )

    def to_dic(self):
        """
        return a dictionary object representative of Annotation
        :return: dictionary object
        """
        annotation_entities_ = []
        labels = set()
        for annotation_entity in self.annotation_entities:
            annotation_entities_.append(annotation_entity.to_dic())
            labels.add(annotation_entity.label)
        return {
            "id": self.id,
            "session_uid": self.session_uid,
            "timestamp": time_utils.datetime_to_iso_utc(self.timestamp),
            "asset_id": self.asset_id,
            "media_type": self.media_type,
            "provider": self.provider,
            "annotation_type": self.annotation_type,
            "annotation_entities": annotation_entities_,
            "sets": self.sets,
            "binary_id": self.annotation_meta.get("binary_id"),
            "labels": list(labels),
        }


class RelatedAnnotation(object):
    # initialize a related annotation object(
    def __init__(self, related_annotation_dic):
        try:
            # annotation label
            self.uid = related_annotation_dic["uid"]

            # the unique (worldwide) id of the entity
            self.relationship = related_annotation_dic["relationship"]
            if self.relationship not in {"parent", "child", "sibling"}:
                raise InvalidAnnotationError(
                    "unrecognized relation {}".format(self.relationship)
                )

        except KeyError as e:
            raise InvalidAnnotationError(str(e))

    def to_dic(self):
        """
        return a dictionary object representative of Annotation entity
        :return: dictionary object
        """
        return {"uid": self.uid, "relationship": self.relationship}


class AnnotationEntity(object):
    # initialize an annotation object (a single annotation such as tire,
    # pedestrian, etc)
    def __init__(self, annotation_entity_dic: dict,
                 annotation_uid=None):
        try:
            # annotation label
            self.label = annotation_entity_dic["label"]
            self.category_id = annotation_entity_dic.get(
                "category_id")

            # the unique (worldwide) id of the entity
            if "uid" in annotation_entity_dic:
                self.uid = annotation_entity_dic["uid"]
            elif annotation_uid:
                self.uid = misc.get_md5_from_json_object(
                    {"annotation_uid": annotation_uid,
                        "dic": annotation_entity_dic}
                )
            else:
                self.uid = misc.get_guid()

            # annotation_type polygon, free_space, line, point, mixed (some
            # datatang annotations)
            self.annotation_type = annotation_entity_dic["annotation_type"]
            self.binary_id = annotation_entity_dic.get("binary_id")
            if self.annotation_type not in AnnotationTypes.VALID_TYPES:
                raise InvalidAnnotationError(
                    "invalid annotation type {}".format(self.annotation_type)
                )

        except KeyError as e:
            raise InvalidAnnotationError(str(e))

        # x, y coordinates
        self.coordinates = []

        try:
            for point in annotation_entity_dic.get("coordinates", []):
                self.coordinates.append({"x": point["x"], "y": point["y"]})

        except KeyError:
            raise InvalidAnnotationError(str(KeyError))

        # coordinate checks for various geometry types:
        if self.annotation_type == AnnotationTypes.POINT and len(
                self.coordinates) != 1:
            raise InvalidAnnotationError(
                "point annotations should exactly have 1 point"
            )

        if self.annotation_type == AnnotationTypes.TWO_D_BOUNDING_BOX and len(
                self.coordinates) != 4:
            raise InvalidAnnotationError(
                "bounding_box annotations should exactly have 4 points"
            )

        if self.annotation_type in {
                AnnotationTypes.POLYGON,
                AnnotationTypes.LINE} and not self.coordinates:
            raise InvalidAnnotationError(
                "empty coordinates for annotation_type = {}".format(
                    self.annotation_type
                )
            )

        # get all related_annotations
        self.related_annotations = []

        for related_annotation in annotation_entity_dic.get(
                "related_annotations", []):
            self.related_annotations.append(
                RelatedAnnotation(related_annotation))

        # optional attributes of an entity
        self.attributes = annotation_entity_dic.get("attributes")

        # optional url of an entity
        self.url = annotation_entity_dic.get("url")

        # optional annotation resource (for example the png mask for semantic
        # segmentation)
        self.resource = annotation_entity_dic.get("resource")

    def to_dic(self):
        """
        return a dictionary object representative of Annotation entity
        :return: dictionary object
        """
        related_annotations_ = []
        for related_annotation in self.related_annotations:
            related_annotations_.append(related_annotation.to_dic())
        return {
            "uid": self.uid,
            "label": self.label,
            "annotation_type": self.annotation_type,
            "attributes": self.attributes,
            "url": self.url,
            "resource": self.resource,
            "coordinates": self.coordinates,
            "related_annotations": related_annotations_,
            "binary_id": self.binary_id,
            "category_id": self.category_id
        }
