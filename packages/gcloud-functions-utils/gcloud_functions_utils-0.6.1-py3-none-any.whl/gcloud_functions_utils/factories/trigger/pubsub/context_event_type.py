from enum import Enum


class ContextEventType(Enum):
    # PubSub topic event trigger
    PubSubTopicPublish = "google.pubsub.topic.publish"

    # Cloud storage event trigger
    StorageObjectFinalize = "google.storage.object.finalize"
    StorageObjectDelete = "google.storage.object.delete"
    StorageObjectArchive = "google.storage.object.archive"
    StorageObjectMetadataUpdate = "google.storage.object.metadataUpdate"
