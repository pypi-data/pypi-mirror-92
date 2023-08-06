from future.utils import python_2_unicode_compatible
from viberbot.api.event_type import EventType
from viberbot.api.viber_requests.viber_request import ViberRequest


class ViberDeliveredRequest(ViberRequest):
	def __init__(self):
		super(ViberDeliveredRequest, self).__init__(EventType.DELIVERED)
		self._message_token = None
		self._user_id = None

	def from_dict(self, request_dict):
		super(ViberDeliveredRequest, self).from_dict(request_dict)
		self._message_token = request_dict['message_token']
		self._user_id = request_dict['user_id']
		return self

	def get_meesage_token(self):
		return self._message_token

	def get_user_id(self):
		return self._user_id

	@python_2_unicode_compatible
	def __str__(self):
		return u"ViberDeliveredRequest [{0}, message_token={1}, user_id={2}]" \
			.format(super(ViberDeliveredRequest, self).__str__(),
					self._message_token,
					self._user_id)

