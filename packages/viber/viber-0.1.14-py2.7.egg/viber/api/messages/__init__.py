from .contact_message import ContactMessage
from .file_message import FileMessage
from .location_message import LocationMessage
from .picture_message import PictureMessage
from .sticker_message import StickerMessage
from .url_message import URLMessage
from .video_message import VideoMessage
from .message_type import MessageType
from .text_message import TextMessage
from .location_message import LocationMessage

MESSAGE_TYPE_TO_CLASS = {
	MessageType.URL: URLMessage,
	MessageType.LOCATION: LocationMessage,
	MessageType.PICTURE: PictureMessage,
	MessageType.CONTACT: ContactMessage,
	MessageType.FILE: FileMessage,
	MessageType.TEXT: TextMessage,
	MessageType.VIDEO: VideoMessage
}


def get_message(message_dict):
	if message_dict['type'] not in MESSAGE_TYPE_TO_CLASS:
		raise Exception("message type '{0}' is not supported".format(message_dict['type']))

	return MESSAGE_TYPE_TO_CLASS[message_dict['type']]().from_dict(message_dict)


