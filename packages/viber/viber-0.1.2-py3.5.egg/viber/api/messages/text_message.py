from future.utils import python_2_unicode_compatible
from viber.api.messages.message import Message
from viber.api.messages.message_type import MessageType


class TextMessage(Message):
	def __init__(self, tracking_data=None, keyboard=None, text=None):
		super(TextMessage, self).__init__(MessageType.TEXT, tracking_data, keyboard)
		self._text = text

	def to_dict(self):
		message_data = super(TextMessage, self).to_dict()
		message_data['text'] = self._text
		return message_data

	def from_dict(self, message_data):
		super(TextMessage, self).from_dict(message_data)
		if 'text' in message_data:
			self._text = message_data['text']
		return self

	def validate(self):
		return self._text is not None

	@python_2_unicode_compatible
	def __str__(self):
		return u"TextMessage [{0}, text={1}]".format(super(TextMessage, self).__str__(), self._text)
