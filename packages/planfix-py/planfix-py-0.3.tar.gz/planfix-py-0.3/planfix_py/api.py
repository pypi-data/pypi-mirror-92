from requests import post
from requests.auth import HTTPBasicAuth

from jinja2 import Environment, PackageLoader

from .functions import Contact, Task


class PlanfixAPI(object):
	account = None
	token = None
	api_key = None 

	url = 'https://api.planfix.ru/xml'
	headers = {'Accept': 'application/xml', 'Content-Type': 'application/xml'}

	__templates_env = Environment(
			loader=PackageLoader('planfix_py', 'templates')
		)

	def __init__(self, account='', token='', api_key=''):
		self.account = account
		self.token = token
		self.api_key = api_key

		self.task = Task(self)
		self.contact = Contact(self)

	def _send_request(self, xml):
		response = post(
				self.url, 
				data=xml.encode('UTF-8'), 
				headers=self.headers, 
				auth=HTTPBasicAuth(
						self.api_key,
						self.token, 
					)
			)

		return response

	def _load_template(self, template_name, kwargs):
		template = self.__templates_env.get_template(template_name)

		kwargs['account'] = self.account
		request_message = template.render(**kwargs)

		return request_message

	def _get_response(self, template_name, kwargs):
		xml = self._load_template(template_name, kwargs)

		response = self._send_request(xml)
		return response.text
