from future.utils import python_2_unicode_compatible
from viber.api.messages.message import Message
from viber.api.messages.message_type import MessageType


class VideoMessage(Message):
	def __init__(self, tracking_data=None, keyboard=None, media=None, thumbnail=None, size=None, duration=None):
		super(VideoMessage, self).__init__(MessageType.VIDEO, tracking_data, keyboard)
		self._media = media
		self._thumbnail = thumbnail
		self._size = size
		self._duration = duration

	def to_dict(self):
		message_data = super(VideoMessage, self).to_dict()
		message_data['media'] = self._media
		message_data['thumbnail'] = self._thumbnail
		message_data['size'] = self._size
		message_data['duration'] = self._duration
		return message_data

	def from_dict(self, message_data):
		super(VideoMessage, self).from_dict(message_data)
		if 'media' in message_data:
			self._media = message_data['media']
		if 'thumbnail' in message_data:
			self._thumbnail = message_data['thumbnail']
		if 'size' in message_data:
			self._size = message_data['size']
		if 'duration' in message_data:
			self._duration = message_data['duration']
		return self

	def validate(self):
		return self._media is not None and self._size is not None

	def get_media(self):
		return self._media

	def get_thumbnail(self):
		return self._thumbnail

	def get_size(self):
		return self._size

	def get_duration(self):
		return self._duration

	@python_2_unicode_compatible
	def __str__(self):
		return u"VideoMessage [{0}, media={1}, thumbnail={2}, size={3}, duration={4}]".\
			format(super(VideoMessage, self).__str__(),
				   self._media,
				   self._thumbnail,
				   self._size,
				   self._duration)
