
.. function:: authorisation_state()

	Метод возвращает состояние авторизации для текущей сессии. Обычно вызывается после запроса авторизации.

	:return: Ответ API
	:rtype: dict
	
.. function:: base_info()

	Получение базовой информации о текущих параметрах игры и некоторых других данных.

	:return: Ответ API
	:rtype: dict
	
.. function:: cards_get()

	Взять новую карту в колоду игрока.

	:return: Ответ API
	:rtype: dict
	.. note:: Метод является «неблокирующей операцией» (см. документацию), формат ответа соответствует ответу для всех «неблокирующих операций».
	
.. function:: cards_merge(cards)

	Объединить карты из колоды игрока.

	:param cards: перечень уникальных идентификаторов карт в колоде игрока через запятую
	:type cards: str
	:return: Ответ API
	:rtype: dict
	.. note:: Метод является «неблокирующей операцией» (см. документацию), формат ответа соответствует ответу для всех «неблокирующих операций».
	
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
	.. note:: Метод является «неблокирующей операцией» (см. документацию), формат ответа соответствует ответу для всех «неблокирующих операций».
	
.. function:: info(account, client_turns)

	Информация о текущем ходе и герое

	:param account: идентификатор игрока
	:type account: str
	:param client_turns: номера ходов, по отношению к которым можно вернуть сокращённую информацию
	:type client_turns: list
	:return: Ответ API
	:rtype: dict
	
.. function:: login(email, password[, next_url='/', remember=False])

	Вход в игру. Используйте этот метод только если разрабатываете приложение для себя и друзей. В остальных случаях пользуйтесь «авторизацией в игре».

	:param email: email адрес пользователя
	:type email: str
	:param password: пароль пользователя
	:type password: str
	:param next_url: вернётся в ответе метода в случае успешного входа, по умолчанию равен "/"
	:type next_url: str
	:param remember: если флаг указан, сессия игрока будет сохранена на длительное время
	:return: Ответ API
	:rtype: dict
	
.. function:: logout()

	Выйти из игры

	:return: Ответ API
	:rtype: dict
	
.. function:: persons_show(person)

	Подробная информация о конкретном Мастере

	:param person: идентификатор Мастера
	:type person: str
	.. warning:: Это экспериментальный метод, при появлении новой версии не гарантируется работоспособность предыдущей!
	
.. function:: places_use()

	Получить перечень всех городов с их основными параметрами

	:return: Ответ API
	:rtype: dict
	
.. function:: places_show(place)

	Подробная информация о конкретном городе

	:param place: идентификатор города
	:type place: str
	.. warning:: Это экспериментальный метод, при появлении новой версии не гарантируется работоспособность предыдущей!
	
.. function:: request_authorisation(appName, appInfo, appDesc)

	Авторизация приложения для проведения операций от имени пользователя. Приложению не будут доступны «критические» операции и данные.

	:param appName: короткое название приложения (например, его название в google play)
	:type appName: str
	:param appInfo: краткое описание информации об устройстве пользователя.
	:type appInfo: str
	:param appDesc: описание приложения (без html разметки)
	:type addDesc: str
	:return: Ответ API
	:rtype: dict
	
.. function:: select_in_quest(option_uid)

	Изменение пути выполнения задания героем

	:param option_uid: уникальный идентификатор выбора в задании
	:type option_uid: str
	:return: Ответ API
	:rtype: dict
	.. note:: Метод является «неблокирующей операцией» (см. документацию), формат ответа соответствует ответу для всех «неблокирующих операций».
	
.. function:: show(account)

	Получить информацию об игроке

	:param account: идентификатор игрока
	:type account: str
	:return: Ответ API
	:rtype: dict
	
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
	
