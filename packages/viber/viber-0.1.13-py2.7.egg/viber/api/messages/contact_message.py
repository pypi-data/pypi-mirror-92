from future.utils import python_2_unicode_compatible
from .data_types.contact import Contact
from .message import Message
from .message_type import MessageType


class ContactMessage(Message):
	def __init__(self, tracking_data=None, keyboard=None, contact=None):
		super(ContactMessage, self).__init__(MessageType.CONTACT, tracking_data, keyboard)
		self._contact = contact

	def to_dict(self):
		message_data = super(ContactMessage, self).to_dict()
		if self._contact is not None:
			message_data['contact'] = self._contact.to_dict()
		return message_data

	def from_dict(self, message_data):
		super(ContactMessage, self).from_dict(message_data)
		if 'contact' in message_data:
			self._contact = Contact().from_dict(message_data['contact'])
		return self

	def validate(self):
		return self._contact is not None \
			   and self._contact.get_name() is not None \
			   and self._contact.get_phone_number() is not None

	@python_2_unicode_compatible
	def __str__(self):
		return u"ContactMessage [{0}, contact={1}]". \
			format(super(ContactMessage, self).__str__(),
				   self._contact)
