#!/usr/bin/python
# coding:utf8
import requests
import random
import string


class theTaleApi:
	'''
	.. seealso:: http://the-tale.org/guide/api
	:param client_id: id of client app ("name-version")
	:type client_id: str
	'''
	def _check(self, r):
		if self.debug:
			print('Response text:' + r.text +
				'Request url' + r.request.url +
				'Request headers' + str(r.request.headers))
		result = r.json()
		if result['status'] != 'ok':
			raise Exception(
				{'Response text': r.text,
				'Request url': r.request.url,
				'Request headers': str(r.request.headers)})
		else:
			return result

	def __init__(self, client_id, debug=False):
		self.url = 'http://the-tale.org{path}'
		self.client_id = client_id
		self.debug = debug
		self.CSRFToken = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))

		self.session = requests.session()
		self.session.headers.update({'X-CSRFToken': self.CSRFToken})
		self.session.cookies['csrftoken'] = self.CSRFToken

	def base_info(self):
		'''
		.. function:: base_info()
		Получение базовой информации о текущих параметрах игры и некоторых других данных.

		:return: Ответ API
		:rtype: dict
		'''
		r = self.session.post(self.url.format(
			path='/api/info/'),
			params={'csrfmiddlewaretoken': self.CSRFToken,
				'api_client': self.client_id,
				'api_version': '1.0'})
		return self._check(r)

	def request_authorisation(self, appName, appInfo, appDesc):
		'''
		.. function:: request_authorisation(appName, appInfo, appDesc)
		Авторизация приложения для проведения операций от имени пользователя. \
Приложению не будут доступны «критические» операции и данные.

		:param appName: короткое название приложения (например, его название в google play)
		:type appName: str
		:param appInfo: краткое описание информации об устройстве пользователя.
		:type appInfo: str
		:param appDesc: описание приложения (без html разметки)
		:type addDesc: str
		:return: Ответ API
		:rtype: dict
		'''
		r = self.session.post(self.url.format(
			path='/accounts/third-party/tokens/api/request-authorisation'),
			params={'csrfmiddlewaretoken': self.CSRFToken,
				'api_client': self.client_id,
				'api_version': '1.0'},
			data={'application_name': appName,
				'application_info': appInfo,
				'application_description': appDesc})
		return self._check(r)

	def authorisation_state(self):
		'''
		.. function:: authorisation_state()
		Метод возвращает состояние авторизации для текущей сессии. \
Обычно вызывается после запроса авторизации.

		:return: Ответ API
		:rtype: dict
		'''
		r = self.session.get(self.url.format(
			path='/accounts/third-party/tokens/api/authorisation-state'),
			params={'csrfmiddlewaretoken': self.CSRFToken,
				'api_client': self.client_id,
				'api_version': '1.0'})
		return self._check(r)

	def login(self, email, password, next_url='/', remember=False):
		'''
		.. function:: login(email, password[, next_url='/', remember=False])
		Вход в игру. Используйте этот метод только если разрабатываете приложение для себя и друзей. \
В остальных случаях пользуйтесь «авторизацией в игре».

		:param email: email адрес пользователя
		:type email: str
		:param password: пароль пользователя
		:type password: str
		:param next_url: вернётся в ответе метода в случае успешного входа, по умолчанию равен "/"
		:type next_url: str
		:param remember: если флаг указан, сессия игрока будет сохранена на длительное время
		:return: Ответ API
		:rtype: dict
		'''
		data = {'email': email,
				'password': password}
		if remember:
			data['remember'] = True
		r = self.session.post(self.url.format(
			path='/accounts/auth/api/login'),
			params={'csrfmiddlewaretoken': self.CSRFToken,
				'api_client': self.client_id,
				'api_version': '1.0',
				'next_url': next_url},
			data=data)
		return self._check(r)

	def logout(self):
		'''
		.. function:: logout()
		Выйти из игры

		:return: Ответ API
		:rtype: dict
		'''
		r = self.session.post(self.url.format(
			path='/accounts/auth/api/logout'),
			params={'csrfmiddlewaretoken': self.CSRFToken,
				'api_client': self.client_id,
				'api_version': '1.0'})
		return self._check(r)

	def show(self, account):
		'''
		.. function:: show(account)
		Получить информацию об игроке

		:param account: идентификатор игрока
		:type account: str
		:return: Ответ API
		:rtype: dict
		'''
		r = self.session.get(self.url.format(
			path='/accounts/{acc}/api/show'.format(acc=account)),
			params={'csrfmiddlewaretoken': self.CSRFToken,
				'api_client': self.client_id,
				'api_version': '1.0'})
		return self._check(r)

	def info(self, account, client_turns):
		'''
		.. function:: info(account, client_turns)
		Информация о текущем ходе и герое

		:param account: идентификатор игрока
		:type account: str
		:param client_turns: номера ходов, по отношению к которым можно вернуть сокращённую информацию
		:type client_turns: list
		:return: Ответ API
		:rtype: dict
		'''
		client_turns = str(client_turns)
		r = self.session.post(self.url.format(
			path='/accounts/third-party/tokens/api/request-authorisation'),
			params={'csrfmiddlewaretoken': self.CSRFToken,
				'api_client': self.client_id,
				'api_version': '1.3'},
			data={'account': account,
				'aclient_turns': client_turns})
		return self._check(r)

	def use_ability(self, abilityId, building=None, battle=None):
		'''
		.. function:: use_ability(abilityId[, building=None, battle=None])
		Использование одной из способностей игрока (список способностей см. в разделе типов)

		:param abilityId: идентификатор способности
		:type abilityId: str
		:param building: идентификатор здания, если способность касается здания
		:type building: str
		:param battle: идентификатор pvp сражения, если способность касается операций с pvp сражением
		:type battle: str
		:return: Ответ API
		:rtype: dict
		'''
		data = {}
		if building is not None:
			data['building'] = building
		if battle is not None:
			data['battle'] = battle
		r = self.session.post(self.url.format(
			path='/game/abilities/{aId}/api/use'.format(aId=abilityId)),
			params={'csrfmiddlewaretoken': self.CSRFToken,
				'api_client': self.client_id,
				'api_version': '1.0'},
			data=data)
		return self._check(r)

	def select_in_quest(self, option_uid):
		'''
		.. function:: select_in_quest(option_uid)
		Изменение пути выполнения задания героем

		:param option_uid: уникальный идентификатор выбора в задании
		:type option_uid: str
		:return: Ответ API
		:rtype: dict
		.. note:: Метод является «неблокирующей операцией» (см. документацию), \
формат ответа соответствует ответу для всех «неблокирующих операций».
		'''
		r = self.session.post(self.url.format(
			path='/game/quests/api/choose/'),
			params={'csrfmiddlewaretoken': self.CSRFToken,
				'api_client': self.client_id,
				'api_version': '1.0',
				'option_uid': option_uid})
		return self._check(r)

	def cards_get(self):
		'''
		.. function:: cards_get()
		Взять новую карту в колоду игрока.

		:return: Ответ API
		:rtype: dict
		.. note:: Метод является «неблокирующей операцией» (см. документацию), \
формат ответа соответствует ответу для всех «неблокирующих операций».
		'''
		r = self.session.post(self.url.format(
			path='/game/cards/api/get'),
			params={'csrfmiddlewaretoken': self.CSRFToken,
				'api_client': self.client_id,
				'api_version': '1.0'})
		return self._check(r)

	def cards_merge(self, cards):
		'''
		.. function:: cards_merge(cards)
		Объединить карты из колоды игрока.

		:param cards: перечень уникальных идентификаторов карт в колоде игрока через запятую
		:type cards: str
		:return: Ответ API
		:rtype: dict
		.. note:: Метод является «неблокирующей операцией» (см. документацию), \
формат ответа соответствует ответу для всех «неблокирующих операций».
		'''
		r = self.session.post(self.url.format(
			path='/game/cards/api/combine'),
			params={'csrfmiddlewaretoken': self.CSRFToken,
				'api_client': self.client_id,
				'api_version': '1.0',
				'cards': cards})
		return self._check(r)

	def cards_use(self, card, person=None, place=None, building=None):
		'''
		.. function:: cards_use(card[, person, place, building])
		Использовать карту из колоды игрока

		:param card: уникальный идентификатор карты в колоде
		:type card: str
		:param person: идентификатор Мастера, если карта применяется к Мастеру
		:type person: str
		:param place: идентификатор города, если карта применяется к городу
		:type place: str
		:param building: идентификатор здания, если карта применяется к зданию
		:type building: str
		:return: Ответ API
		:rtype: dict
		.. note:: Метод является «неблокирующей операцией» (см. документацию), \
формат ответа соответствует ответу для всех «неблокирующих операций».
		'''
		data = {}
		if person is not None:
			data['person'] = person
		if place is not None:
			data['place'] = place
		if building is not None:
			data['building'] = building
		r = self.session.post(self.url.format(
			path='/game/cards/api/use'),
			params={'csrfmiddlewaretoken': self.CSRFToken,
				'api_client': self.client_id,
				'api_version': '1.0',
				'card': card},
			data=data)
		return self._check(r)

	def places_list(self):
		'''
		.. function:: places_use()
		Получить перечень всех городов с их основными параметрами

		:return: Ответ API
		:rtype: dict
		'''
		r = self.session.post(self.url.format(
			path='/game/places/api/list'),
			params={'csrfmiddlewaretoken': self.CSRFToken,
				'api_client': self.client_id,
				'api_version': '1.1'})
		return self._check(r)

	def places_show(self, place):
		'''
		.. function:: places_show(place)
		Подробная информация о конкретном городе

		:param place: идентификатор города
		:type place: str
		.. warning:: Это экспериментальный метод, \
при появлении новой версии не гарантируется работоспособность предыдущей!
		'''
		r = self.session.post(self.url.format(
			path='/game/places/{place}/api/show'.format(place=place)),
			params={'csrfmiddlewaretoken': self.CSRFToken,
				'api_client': self.client_id,
				'api_version': '2.0'})
		return self._check(r)

	def persons_show(self, person):
		'''
		.. function:: persons_show(person)
		Подробная информация о конкретном Мастере

		:param person: идентификатор Мастера
		:type person: str
		.. warning:: Это экспериментальный метод, \
при появлении новой версии не гарантируется работоспособность предыдущей!
		'''
		r = self.session.post(self.url.format(
			path='/game/places/{person}/api/show'.format(person=person)),
			params={'csrfmiddlewaretoken': self.CSRFToken,
				'api_client': self.client_id,
				'api_version': '1.0'})
		return self._check(r)
