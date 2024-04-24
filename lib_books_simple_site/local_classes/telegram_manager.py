
from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputPeerEmpty, MessageMediaPhoto, MessageMediaDocument
from tqdm import tqdm
import asyncio
from noocube.switch import Switch
import noocube.funcs_general as FG

from noocube.funcs_general_class import FunctionsGeneralClass

from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup
from noocube.sqlite_pandas_processor_speedup import SqlitePandasProcessorSpeedup

# import telebot
from telebot import types

# from telegram_monitor.local_classes.tg_pyrogram_manager import TgPyrogramManager

from noocube.funcs_general_class import FunctionsGeneralClass

from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup 

from noocube.re_manager import ReManager
from noocube.re_constants import *
import re


import sys
sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')
import settings_bdp_main as ms # общие установки для всех модулей

from noocube.files_manager import FilesManager


from telegram_monitor.local_classes.book_library_funcs import BookLibraryFuncs

from telegram_monitor.local_classes.tg_local_funcs import TgLocalFuncs

from beeprint import pp


from telegram_monitor.local_classes.book_library_manager import BookLibraryManager


from telegram_monitor.local_classes.audiobooks_channel_telegram_manager import AudiobooksChannelTelegramManager


class TelegramManager ():
    """ w
    Класс для  общей работы с Телеграм общий.
    TODO: Перенести в пакет NOOCUBE !
    """
    
    
    blf = BookLibraryFuncs()
    tlf = TgLocalFuncs()

    def __init__(self, auth = {}, dicThrough={}):
        """
        dicThrough - Сквозной глобальный словарь для передачи разнообразных параметров
        auth - Словарь с авторизационными и настроечными данными. Полный формат данных паторизации и настроек ниже:
        auth = {
            'api_id' : 20460272,
            'api_hash' : '9e6f44844a41f717e5c035cb0add2984',
            'session_name' : 'anon', # Название файла с сессией (БД sqlite, если нет прочих настроек по формату сесссии. Хранится в рабочей директории, где manage.py)
            'bot_token' : '6982698935:AAFQQdz8uApzejMak2ily8azWVKytfIeuNQ', # тоукен своего бота
            'own_bot_chat_id' : -4104980551, # id своего ТГ чата-бота
            # 'curr_own_chat_id' : -1001811098741, # ID чата своего текущего чата-канала в ТГ (но может задаваться и динамически в коде, так как собственных чатов может быть несколько)
        }
        """
        
        # Сквозной глобальный словарь
        self.dicThrough = dicThrough 
        
        # Словарь с авторизационными и настроечными данными
        self.auth = auth
        
        # Инициализация id своего ТГ приложения (базовые ТГ данные)
        if 'api_id' in self.auth: 
            self.apiId = self.auth['api_id']
            
        # Инициализация хэша своего ТГ приложения (базовые ТГ данные)
        if 'api_hash' in self.auth: 
            self.apiHash = self.auth['api_hash']
            
        # Инициализация сессии для ТГ оперций (базовые ТГ данные)
        if 'session_name' in self.auth: 
            self.sessionName = self.auth['session_name']
        
        # # Инициализация собственного бота (bot = telebot.TeleBot(token='6982698935:AAFQQdz8uApzejMak2ily8azWVKytfIeuNQ'))
        # if 'bot_token' in self.auth: 
        #     self.bot = telebot.TeleBot(token = self.auth['bot_token']) 
            
        # Инициализация id чата собственного бота
        if 'own_bot_chat_id' in self.auth:
            self.botChatId = self.auth['own_bot_chat_id'] # # id своего ТГ чата-бота
            
        
        self.sps = SqliteProcessorSpeedup(ms.DB_CONNECTION)
        self.blf = BookLibraryFuncs()
        self.blm = BookLibraryManager()
        
            
        # # Инициализация  id текущего своего чата (но может задаваться и динамически в коде, так как собственных чатов может быть несколько)
        # if 'curr_own_chat_id' in self.auth:
        #     self.ownCurrChattId = self.auth['curr_own_chat_id']  # D чата своего чата-канадла в ТГ 
        
        

    # DO NOT DELETE YET !!!! Современное подключение к телеграм-каналу !
    @staticmethod
    def auth_for_session(session_name = 'anon', api_id = 20460272, api_hash = '9e6f44844a41f717e5c035cb0add2984'):
        """
        Современное подключение к телеграм-каналу !
        TODO: Перевести client_dynamic_method_execute_telegram_self() на этот более современный подход без  loop !!! 
        
        Авторизация для создания сессии
        session_name - первый домен в имени файла-сессии, который появляется в рабочем катологе проекта
        api_id - api id аккаунта
        api_hash - аккаунт хэш 
        ПРИМ: Либо этот код может быть вставлен в код и в терминале сайта можно будет пройти авторизацию
        ПРИМ: Если сессии не было, то в терминале будет необходимо интереактивно пройти авторизацию со своим аккаунтом-каналом 
        Телеграм при первом выполнении этого метода
        """

        # 'anon' - название файла сессии, который появляется в рабочем катологе проекта
        client = TelegramClient(session_name, api_id, api_hash)
        
        async def auth_empty():
            """ 
            Пустой вспомогательный метод для вставки
            """
            async for message in client.iter_messages('me'):
                pass

        with client:
            client.loop.run_until_complete(auth_empty())


        
        
        
        
    async def download_media_telegram_self (self, client, **tgwargs):
        """ 
        TelegramManager
        Скачать картинки из канала с ограничением по кол-ву , а так же с возможностью задания интервала channel_messages_id (минимальная и максимальная ограничение по id),
        с порядком: от последних к первым
        
        TODO: Изменить название метода на примерно : analyse_channel_messages_download_and_manage_results_with_dynamic_func ()
        Обработка результата может зависеть от специфики задач програмного блока. Поэтому этот метод обработки должен подгружаться динамически, 
        независимо от данного метода и его местонахождения (которые ориентировочно будет в пакете NOOCUBE).
        
        Этот метод анализирует сообщения и скачивает необходимые документы и картинки в задаваемый каталог по альтернативных настройках параметров метода
        ~ https://docs.telethon.dev/en/stable/modules/client.html#telethon.client.messages.MessageMethods.iter_messages
        """
        
        print(f"PR_A207 --> START: download_media_telegram_self()")
        
        
        print(f"PR_B096 --> tgwargs['loadDoc'] = {tgwargs['loadDoc']}")
        
        
        # sps = SqliteProcessorSpeedup(ms.DB_CONNECTION)
        # Смысловая инициализация
        channeChatName = self.dicThrough['dfunc_params_telegram']['channel_name']
        # табличное id источника (ТГ-канала) в  табл 'lib_orig_sources' ( должен быть динамическим)
        
        
        
        origSourceId = tgwargs['origSourceId']
        
        # Тип сохранения данных о загруженном сообщении в таблицах 'tg_messages_proceeded'  и 'tg_message_proceeded_ext'
        # ПРИМ:  другие tg_procceeded... таблицы в случаях UPDATE нас не интересуют, поэтому только две вышеуказанные таблицы участвуют в процессе UPDATE
        saveDataExecuteType = tgwargs['saveDataExecuteType']
        print(f"PR_B073 --> point A")
        
        # параметр настройки типа sql-операции для сохраенния данных в БД
        saveDataExecuteType =  tgwargs['saveDataExecuteType']
        
        print(f"PR_B073 --> saveDataExecuteType = {saveDataExecuteType}")
        
        # Ограничение по кол-ву скачиваемых сообщений , отсчет с конца чата вверх
        # ПРИМ: !!! Расположение if блоков в двнном случае выполняет еще роль иерархии. так как в каждой из этих if-блоков переписываются именные парамтеры msgKwargs -
        if 'dfunc_params_telegram' in self.dicThrough and 'limit' in self.dicThrough['dfunc_params_telegram'] and self.dicThrough['dfunc_params_telegram']['limit'] != -1:
            limit = self.dicThrough['dfunc_params_telegram']['limit']
            print(f"PR_A194 --> SYS LOG: Ограничение по кол-ву скачиваемых сообщений = {limit}")
            msgKwargs = {'limit' : limit} # Именные параметры для цикла итерации по ТГ сообщениям
        else:
            limit = None
            print(f"PR_A210 --> DEBUG LOG: limit  не задан")
            
            
            
        # Верхняя и нижняя границы интервала ID скачиваемых сообщений. Или конкретное ID . Сообщений с этим ID будут скачены, другие - нет
        # Этот интервал отменяет ограничение по кол-ву скачиваемых сообщений:
        
        # Минимальное ограничение по интервалу скачиваемых ID сообщений (невключителльно)
        if ('dfunc_params_telegram' in self.dicThrough and 'min_message_id_for_load_lim' in self.dicThrough['dfunc_params_telegram'] 
            and self.dicThrough['dfunc_params_telegram']['min_message_id_for_load_lim'] != -1):
            
            min_message_id_for_load_lim = self.dicThrough['dfunc_params_telegram']['min_message_id_for_load_lim']
            print(f"PR_A193 --> SYS LOG: Минимальный ID для интервала скачиваемых сообщений = {min_message_id_for_load_lim}")
        else:
            min_message_id_for_load_lim = None
            print(f"PR_A209 --> DEBUG LOG: min_message_id_for_load_lim для поиска интервалов сообщений не задан")
            
            
        # Максимальное ограничение по интервалу скачиваемых ID сообщений (невключителльно)
        if ('dfunc_params_telegram' in self.dicThrough and 'max_message_id_for_load_lim' in self.dicThrough['dfunc_params_telegram'] 
            and self.dicThrough['dfunc_params_telegram']['max_message_id_for_load_lim'] != -1):
            
            max_message_id_for_load_lim = self.dicThrough['dfunc_params_telegram']['max_message_id_for_load_lim']
            print(f"PR_A195 --> SYS LOG: Максимальный ID для интервала скачиваемых сообщений = {max_message_id_for_load_lim}")
        else:
            max_message_id_for_load_lim = None      
            print(f"PR_A208 --> DEBUG LOG: max_message_id_for_load_lim для поиска интервалов сообщений  не задан")
            
        # Именные параметры для цикла итерации по ТГ сообщениям в случае интервала по IDs (то есть поиск сообщений , входящих в задаваемый интервал IDs)
        # ПРИМ: !!! Расположение if блоков в двнном случае выполняет еще роль иерархии. так как в каждой из этих if-блоков переписываются именные парамтеры msgKwargs -
        if min_message_id_for_load_lim and max_message_id_for_load_lim:
            msgKwargs = {'min_id' : min_message_id_for_load_lim, 'max_id' : max_message_id_for_load_lim,} # Именные параметры для цикла итерации по ТГ сообщениям
        
        
            
            
        # ПРИМ: !!! Расположение if блоков в двнном случае выполняет еще роль иерархии. так как в каждой из этих if-блоков переписываются именные парамтеры msgKwargs -
        # настрйоки для метода итерации цикла iter_messages(...). то есть тот бдлк , который ниже всех имеет приоритет перед верхними
        # ID поиска для скачиваемого сообщения
        if (
            'dfunc_params_telegram' in self.dicThrough 
            and 'message_id_for_load' in self.dicThrough['dfunc_params_telegram'] 
            and self.dicThrough['dfunc_params_telegram']['message_id_for_load'] != -1
            ):
            
            message_id_for_load = self.dicThrough['dfunc_params_telegram']['message_id_for_load']
            print(f"PR_A196 --> SYS LOG: ID для поиска сообщения = {message_id_for_load}")
            
            msgKwargs = {'ids' : message_id_for_load} # Именные параметры для цикла итерации по ТГ сообщениям
        else:
            print(f"PR_A198 --> DEBUG LOG: ID для поиска сообщения не задан")

            message_id_for_load = None   
            
            
        # INI
        # Смысловая инициализация для динамического метода обработки сообщений 
        # Обработка может быть специфической в каждом случае, поэтому и подключается динамически
        file_path = tgwargs['dynamicFuncAddress']['file_path']
        class_name = tgwargs['dynamicFuncAddress']['class_name']
        func_name = tgwargs['dynamicFuncAddress']['func_name'] # analyze_parse_and_save_data_in_messages_of_channel_with_ID_01_tg()
        # func_name_for_ids_massages_lists = tgwargs['dynamicFuncAddress']['func_name_for_ids_massages_lists']
        loadImgAnyway = tgwargs['loadImgAnyway'] # Флаг скачивания картинок, несмотря на то, что система обнаруживает, что сообщение с картинкой и описанием уже было обработано
        # loadDocsAnyway = tgwargs['loadDocsAnyway'] # Флаг скачивания документов, несмотря на то, что система обнаруживает, что сообщение с картинкой и описанием, к которым относится этот документ, уже было обработано



        objCls = FunctionsGeneralClass.load_class_obj_from_file(file_path, class_name) # Обьект динамически подключаемого класса
        
        # Динамичный метод обработки сообщения после его скачивания 
        # это именно тот метод, который в каждом случае можно заменять динамично !!!!
        oFunc = getattr(objCls, func_name) 
        print(f"PR_A210 --> SYS LOG: Динамичный метод обработки сообщения в цикле : \n{oFunc}")
        
        
        
        
        # F. СОЗДАНИЕ СПИСКОВ полностью сгруженных и обработанных сообщений канала из таблиц 'tg_messages_proceeded' и 'tg_auxilary_messages_proceeded'
        # Для дальнейшей проверки в цикле - нужна ли обработка данного текущего сообщения, или его обработка и сгрузка файлов уже полностью исполнена ранее
        # Создать два списка id сообщений из табл 'tg_messages_proceeded', где присуттсвуют id сообщений со статусами : 

        # # Динамический метод считывания данных из БД по уже внесенным ранее обработанным сообщениям для исключения повторения по уже законченным обработанным сообщениям
        # oFunc2 = getattr(objCls, func_name_for_ids_massages_lists) # Обьект динамически подключаемого метода
        # print(f"PR_A211 --> SYS LOG: Динамичный метод считывания данных из БД по уже внесенным ранее обработанным сообщениям для исключения повторения : \n{oFunc2}")


        # # Ids зарегестрированных обработанных сообщений для ОТСЕЧЕНИЯ сообщений при первичной загрузке с заданного ТГ-канала
        # listsMessagesIds = oFunc2(**tgwargs) 
        
        # # общий список ids сообщений, обоих типов Photo и Audio, которые уже выполнили свою роль и на базе их были образованы и зарегестрированы
        # # книги и их томы в библиотеке LABBA или Lib
        # listLibMessagesIdsDone = self.blf.obtain_lib_books_and_volumes_given_source_messages_ids_done_blf (origSourceId)
        
        # # print(f"PR_A134 --> listsMessagesIds = {listsMessagesIds}")

        print(f"PR_A336 --> SYS LOG: Настройки iter_messages msgKwargs = {msgKwargs}")
        
        # ЦИКЛ ПО ИТТЕРИРОВАННЫМ СООБЩЕНИЯМ. ** msgKwargs - именные параметры - настройки для метода iter_messages(...)
        fInx = 0
        
        
        
        # Если тип сохранения sql _INSERT_ , то тогда создаем маркер сэмпла и маркируем вытяжку сообщений этим маркером
        if '_INSERT_' in saveDataExecuteType:
        
            # Маркер данного сэмпла вытяжки сообщений из ТГ-канала
            # ch<sysChannelId>_cond<Условия по **msgKwargs, сформировать в строку>_<дата старта, Y_M_D_H_M включая часы и минуты >
            # Присвоить этот маркер всем связанным с этой загрузкой книгам и томам. Для этого завести таблицу сэмплов и реферальные связи, вплоть до конечных сущностей
            # в библиотеке. Если книга заводится вручную, то маркер сэмплов будет пустым? (Либо ввести таблицу типа ввода книги: Ручной, Автоматический)
            
            # print(f"PR_A757 --> msgKwargs = {msgKwargs}")
            # Сформировать название сэмпла вытяжки из ТГ
            # INI PARS
            startTime = FG.get_current_time_format4_2()
            
            # ID канала в системе LIBCUBE (в таблице 'tg_channels')
            channelSysId = tgwargs['channelId']
            
            # Условия по **msgKwargs . Для маркера сэмпла 
            sampleConds = ''
            for key, val in msgKwargs.items():
                sampleConds += f"{key}: {val},"
                
            sampleConds = sampleConds.rstrip(',')
            
            # Маркер сэмпла вытяжки из ТГ
            currSampleMarker = f"chsys:{channelSysId} cnds[{sampleConds}] stime: {startTime}"
            
            
            # L. Создать новую запись с маркером по сэмплу-вытяжке из ТГ канала , соотвтетсвующей текущей вытяжки сообщений из ТГ канала в таблице 'tg_samples_markers'
            
            sql = f"INSERT INTO {ms.TB_TG_SAMPLES_MARKERS} (status_marker) VALUES ('{currSampleMarker}')"
            
            print(f"PR_A763 --> sql = {sql}")
            
            # EXECUTE INSERT SQL
            try: 
                # Последний инкрементный id в БД после вставки . Он же - id маркера текущей вытяжки
                currSampleId = self.sps.execute_sql_SPS(sql)
                print(f"PR_A759 --> SYS LOG: В таблицу 'tg_samples_markers' создан маркер текущей вытяжки {currSampleMarker} с id = {currSampleId}")
                
            except Exception as err:
                
                print(f"PR_A761 --> SYS LOG: ERRORR !!! {err}")
                raise Exception(f"PR_A760 --> SYS LOG: При выполнении запроса произошла ОШИБКА !!!: \n{sql}") 


            # Добавить параметр с id маркера сэмпла текущей вытяжки в сквозные параметры **tgwargs, которые попадут в функцию обработки данных после скачивания и считывания 
            # сообщений по циклу ниже. А именно в функцию analyze_parse_and_save_data_in_messages_of_channel_with_ID_01_tg() [модуля audiobooks_channel_telegram_manager.py]
            # Для присвоения этого атрибута всем сообщениям текущей обрабатываемой вытяжки в таблицах 'tg_messages_proceeded' и 'tg_auxilary_messages_proceeded'
            tgwargs['currSampleId'] = currSampleId
            
            
            print(f"PR_A758 --> currSampleMarker = {currSampleMarker}")
            

        # # Если тип сохранения sql _UPDATE_ или не задан , то тогда маркер сэмпла НЕ создается
        else:
            tgwargs['currSampleId'] = -1
            
            
            
        # # L. OBSOLETED: Удалять неправильные статусы нельзя. так как теперь по алгоритмам. если сообщение загрузилось в систему. она не может быть удалено
        # # из нее насилльственным путем. эти сообщение должны быть перезагружены с исправвлением статусов. 
        # # ПРЕДВАРИТЕЛЬНАЯ ОЧИСТКА таблиц tg_messages_proceeded и tg_auxilary_messages_proceeded от  сообщений с ошибками в статусе
        # # Оставляем только сообщения с правильными статусами и удаляем с неправильными: 2, 3, 5, 6, 8
        # # !!! Очистка старых записей только по неправильному типу сообщений
        
        # wrongStatuses = [2, 3, 5, 6, 8]
        # self.blm.clear_tg_proceeded_tables_from_messages_with_given_statuses_blm (wrongStatuses)
        
        
        # M. ОЧИСТКА I уровень
        # таблицы  tg_messages_proceeded от сообщений уже реализованных в комплектах книг или в регистрации в библиотеке
        # Очистка по уже реализовавших свою миссию сообщений
        # Очистка таблицы tg_messages_proceeded от уже оприходованных сообщений-книг и томов ПОСЛЕ ЗАГРУЗКИ СООБЩЕНИЙ ИЗ ТГ-КАНАЛА
        
        # НАстройка : Флаг Очищать ненужный использованный материал после регистрации книги
        if tgwargs['clearUsedOutDataAfterRegistration']:
        
            print(f"PR_A991 --> SYS LOG: Очистка таблицы tg_messages_proceeded от сообщений уже реализованных в комплектах книг или в регистрации в библиотеке")
            
            # УДАЛИТЬ ЗАПИСИ в таблице tg_messages_proceeded по текущему источнику и по id ТГ-соощения, который принадлежит totalRejectMessagesIdsOfFirstLevel
            self.blf.remove_all_registered_messages_from_tg_procceeded_blf()
            
            print(f"PR_A996 --> POINT D")
            
        
        # END M. Очистка таблицы
        
            
            
        # !!!!!!! TG MESSAGES ITER CYCLE !!!!!!!!!!!!!!!!!!!!
        
        async for message in client.iter_messages(channeChatName, **msgKwargs): 
            
        # async for message in client.iter_messages(channeChatName, ids = [4430, 4429, 4425, 4433, 4428]): 
        
            print(f"PR_B030 --> type(message.media) = {type(message.media)}")
            
            print(f"PR_A348 --> Цикл по сообщениям: {fInx}")
        
        
            # Z. Отработка типов сообщений в telethon
            
            self.get_message_type_in_project_space(message)
        
        

            
            # C. Сделать принудительный цикл скачивания и фиксации данных по скаченным обьектам. В случае возникновения каких-либо ошибок, выбивающих
            # цикл, необходимо вносить в БД последнюю точку, в которой произошла обшибка. Что бы при новом запуске цикл не повторял загрузки
            # уже загруженных и проанализированных сообщений !!!
            messageId = message.id # ID сообщения в канале
            print(f"\n PR_B076 --> В цикле производится обработка сообщение с ID = {messageId}")
            
            print(f" PR_B077 --> В цикле производится обработка сообщение с текстом = {message.text}\n")

            
            # F. Отсечение по типу: Отсекаем сообщения типа 'TEXT_SIMPLE_MSSG_' - 4,  что бы не засорять БД

            # D. ОТСЕЧЕНИЕ I УРОВНЬ:
            # 
            # (загрузка сообщений с ТГ-канала)
            
            # TODO: Сделать отсечение для tg_auxilary_messages_proceeded и урны !!!

            # Получить общий список messagesIds всех типов, которые уже находятся в сформированных книжных комплектах  + зарегестрированных в библиотеке
            # Reject-список для первого уровня, скачивание сообщений с ТГ-канала
            totalRejectMessagesIdsOfFirstLevel = self.blf.get_reject_messages_ids_list_for_first_level_blf(origSourceId)
                
            print(f"PR_A975 --> SYS LOG: Reject-список -->> {totalRejectMessagesIdsOfFirstLevel}")
            
            # !!!! ОТСЕЧЕНИЕ REJECTOR!!!!    
            # Остечение сообщение от дальнейшей обработки с анализом по сообщениям только от того источника, к каоторому принадлежит текущее сообщение
            ifReject = self.blf.reject_proccessing_if_in_reject_messages_ids_list_blf(messageId, totalRejectMessagesIdsOfFirstLevel)    
            
            print(f"PR_A958 --> POINT A")

            # Пропускаем цикл, если messageId входит в подмножество уже реализованных сообщений (или с неправилльным статусом) и !!! 
            # Если речь НЕ идет о перезагрузке неправильных сообщений, которые нужно апдейтить, а не вставлять
            if ifReject and saveDataExecuteType != '_UPDATE_':
                
                print(f"PR_A954 --> SYS LOG: Сообщение с ID = {messageId} уже обработано системой, файлы сгружены и данные занесены в БД ранее. Пропускаем цикл")

                continue
        
        
            # END ОТСЕЧЕНИЕ I УРОВНЬ:
        
        
            print(f"PR_B096 --> tgwargs['loadDoc'] = {tgwargs['loadDoc']}")
        
            # A. ИСПОЛНЕНИЕ: Возможная загрузка картинок и документов, и считывание всех необходимых данных по обрабатываемым сообщениям из канала в currDicMessageData
            # Словарь со всеми необходимыми данными по запрошенным сообщениям из канала и их адресов файлов-документов при возможнос скачивании в локальную проектную файловую систему
            currDicMessageData = await TelegramManager.get_channel_message_data_alter_download_docs_with_img_name_fixed_as_dic_tm_stat (message, **tgwargs)
            
            # Присвоить данные в сквозной словарь
            self.dicThrough['currDicMessageData'] = currDicMessageData
            
            
            # K.Задать алгоритм обработки проанализированных сообщений в зависимости от формата канала и целей. В каждом канале могут быть разные форматы представления библиотеки ацдио-книг. В данном случае пока 
            # анализируется канадл с названием 'Аудиокниги фантастика'. Но в других каналах может быть иной формат и инной парсинг и анализ сообщений

            # ======== ОБРАБОТКА РЕЗУЛЬТАТА ОБРАБОТКИ СООБЩЕНИЯ: ПАРСИНГ телеграм -канала с названием "Аудиокниги фантастика ~ https://t.me/akniga" 
            # Обработка результата может зависеть от специфики задач програмного блока. Поэтому этот метод обработки должен подгружаться динамически, 
            # независимо от данного метода и его местонахождения (которые ориентировочно будет в пакете NOOCUBE)

            
            # Функция обработки словаря проанализированного сообщения канала  !!!!!!!!
            # Динамическая функция обработки данных после загрузки сообщения. Информация о загруженном сообщении хранится в dicMessageData
            # Во View: analyze_and_download_messages_from_ch_id_01 () - массовая автоматическая загрузка сообщений эта фурнкция обработки ->>>
            # ->>> analyze_parse_and_save_data_in_messages_of_channel_with_ID_01_tg() [модуля audiobooks_channel_telegram_manager.py]
            # Для других задач(например одиночного скачивания сообщения) - эта функция создается и выполняет поставленные задачи
            await oFunc(currDicMessageData, **tgwargs) 
            
            # ======== END ОБРАБОТКА РЕЗУЛЬТАТА ОБРАБОТКИ СООБЩЕНИЯ:  
            
            fInx += 1
            
            
        # АНАЛИЗ ОШИБОК В ЗАГРУЖЕННЫХ СООБЩЕНИЯХ
        actm = AudiobooksChannelTelegramManager()
        
        exeAnalisysList = [1,2,3]
        
        analisysResultsList = actm.analyzers_I_II_III_logic_wrong_messages_first_lv_actm(exeAnalisysList)
        
        # END АНАЛИЗ ОШИБОК В ЗАГРУЖЕННЫХ СООБЩЕНИЯХ
            

        # ОЧИЩЕНИЕ LV1: I, III после завершения всех загрузок: 1 уровень
        # Анализ и удаление обьектов, которые либо бракованы либо аудио-тома без описания. Удаление по спискам analisysList1 и analisysList2

        
        totalMessageErrlist = analisysResultsList[1] + analisysResultsList[3]
        
        print(f"PR_B314 --> totalMessageErrlist = {totalMessageErrlist}")

        self.tlf.delete_messages_from_tbs_procceeded_based_on_tbids_list_tlf(totalMessageErrlist)
        
        # END ОЧИЩЕНИЕ LV1: I, III 
        
        
        # ОЧИЩЕНИЕ-ПЕРЕНОС LV1: II 
        # анализ и перенос из таблиц tg_procceeded.. в таблицы tg_procceeded_err на базе списка-анализа II (псевдо-книги), куда сгружаются все сообщения, 
        # распознанные системой как ошибочные, но которые система не может сама удалить , так как на 100% не уверена в том. что сообщения подлежат удалению
        
        analisysList2 = analisysResultsList[2]
        
        print(f"PR_B334 --> Список скачанных ошибочных сообщений. Вид 2 = {analisysList2}")
        
        self.tlf.transfer_logic_error_messages_to_errors_tables_by_tbids_tlf(analisysList2)
        
        
        # END ОЧИЩЕНИЕ-ПЕРЕНОС LV1: II 
        
        
        
        # Перенос загруженных картинок из первичного Хранилища в проектный директорий
        self.tlf.transfer_downloaded_images_from_prime_storage_to_project_dir_tlf()
        





        # RET: Возврат - сохранение результатов в глобальный сквозной словарь. ПОКА НЕ УДАЛЯТЬ !!!s
        # self.dicThrough['res_telegram'] = dicMessageData   
        
        print(f"PR_A084 --> END: download_media_telegram_self()")
        
        
        
        
        
        
        
        
        
        
        
        
        
        



    
    def read_own_channel_saved_messages_telegram_self(self, client):
        """ 
        Считать сообщения из категории  "Сохраненное" собственного канала
        """
        
        print(f"PR_A051 --> START: read_own_channel_saved_messages_telegram_self()")
        
        mssgs = {}
        
        if 'dfunc_params_telegram' in self.dicThrough and 'limit' in self.dicThrough['dfunc_params_telegram']:
            limit = self.dicThrough['dfunc_params_telegram']['limit']
        else:
            limit = None
            
        for message in client.iter_messages('me', limit = limit):
            # print(message.id, message.text)
            mssgs[message.id] = message.text
            
            # if message.photo:
            #     print('File Name :' + str(message.file.name))
            #     path = await client.download_media(message.media, "youranypathhere")
            #     print('File saved to', path)  # printed after download is done

        # Возврат - сохранение результатов в глобальный сквозной словарь
        self.dicThrough['res_telegram'] = mssgs

        print(f"PR_A052 --> END: read_own_channel_saved_messages_telegram_self()")
    
    
    
    
    
    
    def client_dynamic_method_execute_telegram_self_PREV(self, dFunc, **tgwargs):
        """ 
        Запустить в корутине цикл выполнения динамически задаваемого прикладного метода телеграма
        TODO: Применить в этом методе более современный подход из метода auth_for_session() !!! без loop
        """

        api_id = self.auth['api_id']
        api_hash = self.auth['api_hash']
        session_name = self.auth['session_name']

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            client = TelegramClient(session_name, api_id, api_hash, loop=loop)
            client.connect()
            
            # ВЫПОЛНЕНИЕ ДИНАМИЧЕСКИХ МЕТОДОВ
            
            for case in Switch(dFunc):
                
                # Загрузка сообщений и картинок с задаваемого канала
                if case('download_media_telegram_self'): 
                    print(f"PR_A886 -->  execute telegram func: download_media_telegram_self()")
                    
                    client.loop.run_until_complete(self.download_media_telegram_self(client, **tgwargs))
                    break
                
                # Загрузка сообщений (в частности текстовых) с собственного канала из раздела сохраненное
                if case('read_own_channel_saved_messages_telegram_self'): 
                    print(f"PR_A054 --> execute telegram func: read_self_channel_favorites_messages()")
                    client.loop.run_until_complete(self.read_own_channel_saved_messages_telegram_self(client))
                    break
                
                if case(): # default
                    print('Другое число')
                    break
            
        except:
            pass
        
        finally:
            client.disconnect() # Правильно закрыть клиента ~ https://docs.telethon.dev/en/stable/quick-references/faq.html#what-does-task-was-destroyed-but-it-is-pending-mean
    
    
    
    
    
    def client_dynamic_method_execute_telegram_self (self, dFunc, **tgwargs):
        """ 
        Запустить в корутине цикл выполнения динамически задаваемого прикладного метода телеграма
        NEW: [02-02-2024 07-57]
        """

        api_id = self.auth['api_id']
        api_hash = self.auth['api_hash']
        session_name = self.auth['session_name']

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            client = TelegramClient(session_name, api_id, api_hash, loop=loop)
            client.connect()
            
            # ВЫПОЛНЕНИЕ ДИНАМИЧЕСКИХ МЕТОДОВ
            
            

            for case in Switch(dFunc):
                
                # Загрузка сообщений и картинок с задаваемого канала
                if case('download_media_telegram_self'): 
                    
                    print(f"PR_A887 -->  execute telegram func: download_media_telegram_self()")
                    
                    # client.loop.run_until_complete(self.download_media_telegram_self(client, **tgwargs))
                    
                    print(f"PR_B098 --> tgwargs['loadDoc'] = {tgwargs['loadDoc']}")
                    
                    with client:
                        client.loop.run_until_complete(self.download_media_telegram_self(client, **tgwargs))
                    
                    break
                
                # Загрузка сообщений (в частности текстовых) с собственного канала из раздела сохраненное
                if case('read_own_channel_saved_messages_telegram_self'): 
                    print(f"PR_A054 --> execute telegram func: read_self_channel_favorites_messages()")
                    
                    # client.loop.run_until_complete(self.read_own_channel_saved_messages_telegram_self(client))
                    
                    with client:
                        client.loop.run_until_complete(TelegramManager.test(client))
                    
                    break
                
                
                if case('send_message_to_own_channel_through_own_bot_tm_self'): 
                    
                    print(f"PR_A596 -->  execute telegram func: send_message_to_own_channel_through_own_bot_tm_self()")
                    
                    # client.loop.run_until_complete(self.download_media_telegram_self(client, **tgwargs))
                    
                    
                    with client:
                        client.loop.run_until_complete(self.send_message_to_own_channel_through_own_bot_tm_self(**tgwargs))


                    break
                
                
                
                if case(): # default
                    print('Другое число')
                    break
            
        except:
            pass
        
        # finally:
        #     client.disconnect() # Правильно закрыть клиента ~ https://docs.telethon.dev/en/stable/quick-references/faq.html#what-does-task-was-destroyed-but-it-is-pending-mean
    
    
    

    
    
    
    
    
    
    
    
    @staticmethod
    def client_dynamic_method_execute_telegram_stat (auth, dfunc, **twargs):
        """ 
        Запустить в корутине цикл выполнения динамически задаваемого прикладного метода телеграма. 
        """

        api_id = auth['api_id']
        api_hash = auth['api_hash']
        session_name = auth['session_name']

        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            client = TelegramClient(session_name, api_id, api_hash, loop=loop)
            client.connect()
            
            # ВЫПОЛНЕНИЕ ДИНАМИЧЕСКИХ МЕТОДОВ
            
            for case in Switch(dfunc):
                
                # Загрузка сообщений и картинок с задаваемого канала
                if case('download_media'): 
                    print(f"PR_A888 -->  telegram func: download_media()")
                    client.loop.run_until_complete(TelegramManager.download_media_telegram(client, twargs['channel_name']))
                    break
                # Загрузка сообщений (в частности текстовых) с собственного канала из раздела Избранное
                if case('read_self_channel_favorites_messages'): 
                    print(f"PR_A046 -->  telegram func: read_self_channel_favorites_messages()")
                    client.loop.run_until_complete(TelegramManager.read_self_channel_favorites_messages_telegram(client))
                    break
                
                if case(): # default
                    print('Другое число')
                    break
            
        except:
            pass
        
        finally:
            client.disconnect() # Правильно закрыть клиента ~ https://docs.telethon.dev/en/stable/quick-references/faq.html#what-does-task-was-destroyed-but-it-is-pending-mean
    
    
    
    
    
    



    @staticmethod
    def test_download():
        """ 
        
        """
            
        from telethon import TelegramClient

        api_id = 20460272
        api_hash = '9e6f44844a41f717e5c035cb0add2984'
        
        client = TelegramClient('anon', api_id, api_hash)

        async def main():
            async for message in client.iter_messages('me'):
                print(message.id, message.text)
                if message.photo:
                    print('File Name :' + str(message.file.name))
                    path = await client.download_media(message.media, "youranypathhere")
                    print('File saved to', path)  # printed after download is done

        with client:
            client.loop.run_until_complete(main())
            
            
            
            
            
    # II. Методы анализа и дальнейшей обработки в интеграции с БД сообщений в канале ************************************************************
    
    @staticmethod
    async def  get_channel_message_data_alter_download_docs_with_img_name_fixed_as_dic_tm_stat (message, **tgwargs):
        """ 
        TelegramManager
        Получить данные сообщения канала в виде словаря с альтернативной возможность скачивания документов и картинок с фиксированным названием картинок
        message - сообщение в формате пакета telethon
        loadDoc - флаг загрузки файлов документа (не картинки и не текст сообщения). Если True, то документ загружается в задаваемый директорий loadPath
        loadImg - флаг загрузки картинки сообщения (не документа типа аудио-записи, видео и пр, и не текст сообщения). Если True, то картинка загружается в задаваемый директорий loadPath
        loadPath - директорий, в который загружаются документы и картинки, если флаг loadDocs = True
        ПРИМ: При загрузке картинок к ним по умолчанию прибавляется маркер текущей календарной даты в формате D_M_Y_H_M_S после добавочного суффикса '_msg_photo_'
            Первый фрагмент названия сохраняемой картинки - ID сообщения
        RET: Словарь dicMessageData с данными по сообщению из канала
        
        ПРИМ: ЗОНА, в которой в run-time в консоль не выводятся ошибки !!!! Поэтому внисательно все проверять ОШИБКИ НЕ ВЫВОДЯТСЯ!!! Скорее всего, потому что динамически подгружаемый метод
        И, если происходит ошибка, то программ не выбивается ошибкой, а просто типа все прошло нормально, вот только на самом деле программа перестает работу в этой точке, создавая видимость, 
        что все закончилось нормалльно !!!
        
        """
        

        # loadDoc = False, loadImg = False, loadPath = ''
        # INI
        
        blf = BookLibraryFuncs()
        
        flagLoadDoc = tgwargs['loadDoc'] # флаг загрузки файлов документа
        
        print(f"PR_B095 --> flagLoadDoc = {flagLoadDoc}")
        
        
        flagLoadImg = tgwargs['loadImg'] # флаг загрузки картинки сообщения
        loadPathDir = tgwargs['loadPathDir'] # 
        trashPathDir = tgwargs['trashPathDir']
        
        if 'pseudoLoadingDoc' in tgwargs: # флаг ложной загрузки (когда отключается только лишь функция скачивания документа)
            flagPseudoLoadingDoc =  tgwargs['pseudoLoadingDoc']
        
        flagLoadImgAnyway = tgwargs['loadImgAnyway'] # Флаг скачивания картинок, несмотря на то, что система обнаруживает, что сообщение с картинкой и описанием уже было обработано
        flagLoadDocsAnyway = tgwargs['loadDocsAnyway'] # Флаг скачивания документов, несмотря на то, что система обнаруживает, что сообщение с картинкой и описанием, к которым относится этот документ, уже было обработано

        channelSysId = tgwargs['channelId'] # ID канала из табл 'tg_channels'
        

        print(f"PR_A085 -->  START:  get_channel_message_data_alter_download_docs_with_img_name_fixed_as_dic_tm_stat()") # Маркер старта метода для лога в консоли
        
        
        # print(f"PR_A087 --> Флаг loadImg = {loadImg}")
        
        messageId = message.id # ID сообщения в канале
        
        
        dicMessageData = {
            'message_id' : messageId,
            'proj_path': None,
            'download_path' : None,
            'document_file_name' : None,
            'document_file_size' : None,
            'image_file_name' : None,
            'message_text' : None,
            'curr_calend_date' : None,
            'current_unix_date' : None,
            'status' : None,
        }
        
        
        # Получение текущего времени в формате 1: %d_%m_%Y_%H_%M_%S , в формате 2: %d-%m-%Y %H:%M:%S и в формате unix без округления
        currCalendDateFormat1, currCalendDateFormat2, currCalendDateUnix = FG.get_current_time_format_1_and_2_and_universal_unix() 
        
        dicMessageData['curr_calend_date'] = currCalendDateFormat2
        dicMessageData['current_unix_date'] = currCalendDateUnix
        
        print(f"PR_A153 --> currCalendDateUnix = {currCalendDateUnix}")
        

        
        # !!!! СКАЧИВАНИЕ ДОКУМЕНТА !!!!
        # Если сообщения является документом (аудио-файл, ... не картинка)
        if type(message.media) == MessageMediaDocument: # документы кроме картинок
            
            print(f"PR_A146 --> IF BRENCH: если сообщение является документом ... ")
            print(f"PR_A338 -->  ID сообщения-документа = {messageId}. ")
            
            dicMessageData['messages_type'] = 'DOCUMENT_FILE_MSSG_'
            
            # id типа
            dicMessageData['mssg_type_id'] = 2
                
            # Групповой id сообщения (либо None,  либо цифра типа message.grouped_id: 13690994442196138)
            # Дифференциация альбомных, группвых фото от сообщения с одной фото
            if message.grouped_id is not None:
                
                print(f"PR_B111 --> message.grouped_id: {message.grouped_id}")

                messageGroupedId = message.grouped_id

            else: 
                
                print(f"PR_B112 --> Message Type: DOCUMENT_FILE_MSSG_")
                
                messageGroupedId = -1
                
            dicMessageData['messages_grouped_id'] = messageGroupedId
            

            
            # INI
            docType = 'audio_volume'
            gr = 1
            

            # Считываем название документа-файла
            
            # Название скачиваемого файла в нужном формате. отображающем ID канала и id сообщения в нем, соотвтетсвующего этому документу
            
            
            # Парсинг названия файла с расширением. чтобы добавить в название нужные маркеры и закончить его правильным расширением (типа .mp3)
            
            parts = message.file.name.split('.')
            

            
            
            
            fileExt = parts[-1] # расширение файла
            
            print(f"PR_A337 --> fileExt = {fileExt}")
            
            fileName =  message.file.name.replace(fileExt, '').rstrip('.') # Название файла 1. ОКЗ. Горелый магистр._message_document__ch_1_4260.mp3
            
            # Кодирование id сообщения источника (пеервод в буквенное обозначение цифр. А , если понадобится получить цифровой id сообщения источника из,
            # допустим, названия какого-то тома, то легко транспонировать из буквенного обраьно в цифровое представление id сообщения)
            
            
            print(f"PR_A854 --> P1: fileName = {fileName}")
            

            
            alphabetMessageId = FunctionsGeneralClass.code_digits_sequence_to_alphabet_one_coder_01_blf(messageId)
            
            
            
            # !!! ФОРМИРОВАНИЕ НАЗВАНИЯ ФАЙЛА
            messageFileName = f"{fileName}_ch{channelSysId}_gsm{alphabetMessageId}_gr{gr}_{docType}.{fileExt}"    
            
            print(f"PR_A147 --> Название файла сообщения-документа = {messageFileName}")
            
            
            print(f"PR_A855 --> P2: messageFileName = {messageFileName}")
            
            # записать названия документа в словарь данных по сообщению-документу
            dicMessageData['document_file_name'] = messageFileName 
            
            # Размер скачиваемого фала
            messageFileSize = message.file.size # Размер файла в байтах
            dicMessageData['document_file_size'] = messageFileSize
            
            print(f"PR_A152 --> Размер файла сообщения-документа = {messageFileSize}")
            
            
            # Если флаг loadDoc разрешает загрузку документа
            if flagLoadDoc or flagLoadDocsAnyway:
                
                print(f"PR_A148 --> IF BRENCH: если флаг загрузки файла сообщения-документа loadDoc = {flagLoadDoc} , то пытаемся (try) загрузить документ")
                
                # L. Проверить в директории наличие картинки с именем файла, которое сейчас будет сгружено. И , если такое есть, то либо удалить ее предварительно, либо перенести в другую 
                # вспомогательную для этого директорию
                
                # # Проверка наличия файла или обломков файла (прерванная неправильно загрузка. но осколок файла остается). Если такой обломок есть, то переносим
                # # его  в другой директорий - что бы уменьшить ущерб от возможной ошибки удалить нормальный фалй по каким-то причинам
                
                # print(f"PR_A149 --> loadPath = {loadPath}")
                
                # N. присвоить названию файла индивидуальный номер тома, образованный из сирийного номера книги и группы, отвечающей за тома аудио-книги
                
                # полный путь скачиваемого файла, то есть адрес, куда и под каким именем скачать документ из ТГ-канала
                fullFilePath = loadPathDir + '/' + messageFileName # Полный адрес скачиваемого файла
                
                print(f"PR_A856 --> P3: fullFilePath = {fullFilePath}")
                
                currCalendDate = currCalendDateFormat1 # Текущая календарная дата в формате D_M_Y_H_M_S
                # Название файла дополняется маркером текущейго момента для уникальности (что бы никогда не совпали названия переносимых файлов в урну)
                trashFullFilePath = f'{trashPathDir}/{messageFileName}_{currCalendDate}' # Путь к урне репозитория

                # Проверяем наличие файла, если система дала добро на загрузку документа, а в репозитории есть файл с таким названием, например, осколок
                if FilesManager.if_file_exist (fullFilePath) : 

                    # переносим файл в вспомогательный лиректорий. 
                    FilesManager.move_file_to_another_dir_if_exists_in_this_dir(fullFilePath, trashFullFilePath)
                    
                    print(f"PR_A151 --> SYS LOG: В директории для скачивания файлов был найден осколок файла с текущим названием {messageFileName}. Он был перенесен и переименован в урну по адресу: \n --> {trashFullFilePath}")
                    
                
                # АНАЛИЗ НАЗВАНИЯ И ЗАГРУЗКА ДОКУМЕНТА
                try: 
                    
                    print(f"PR_A316 --> SYS LOG: Система приступила к скачиванию из ТГ канала документа с названием {messageFileName} из сообщения message_id = {message.id}")
                    # Загрузить документ (но не картинку), отфильтрованную от картинки и текста оператором if 
                    # downloadPath = await message.download_media(loadPathDir + f'/{messageFileName}') # PREV
                    
                    # АНАЛИЗ ПОДЛЕЖАЩЕГО К СКАЧИВАНИЮ ФАЙЛА. Анализ по названию. в разных каналах могут быть разные названия для ОЖДАЮЩИХ файлов mp3. 
                    # Сверка происходит по словарю для замещения ожидающих файлов , прописываемому в settings.py в VOCABULARY_AWAIT_VOLUME_REPLACE
                    
                    # СКАЧИВАНИЕ !!! документа сообщения в файл, определяемый полным путем fullFilePath
                    
                    listDicKeys = list(ms.VOCABULARY_LIST_AWAIT_VOLUME_REPLACE)
                    
                    print(f"PR_A857 --> P4: listDicKeys = {listDicKeys}")
                    
                    # ПОДСТАВКА ПУСТЫШКИ, если есть искомый маркер в названи (ПРИМ: это отсносится только к парсингу названий по источнику-каналу с id = 1)
                    # Проверить, есть ли в названии документа, который сейчас будет скачен с сообщения из ТГ-канала, фрагмент, определяемый в ключах словаря замещений
                    # Если фрагмент найден, то документ не загружаем, а вместо него копируем свою пустышку и даем ему название с замещением фрагмента переводом из словаря
                    foundKey = BookLibraryFuncs.check_if_vocabulary_volume_replace_keys_exists_in_to_load_document_full_path_blf (fullFilePath, ms.VOCABULARY_LIST_AWAIT_VOLUME_REPLACE)
                        
                    if foundKey:
                        
                        print(f"PR_A863 --> SYS LOG: В названии файла, который должен быть скачен, найден фрагмент пустого файла-заставки {foundKey}. Файл не скачиваем, а копируем заглушку от нашей системы и формируем название для нее")
                        
                        # Заготовка mp3 пустышки
                        src = ms.EMPTY_MP3_SAMPLE
                    
                    
                        
                    
                        dst = fullFilePath.replace(foundKey, ms.VOCABULARY_LIST_AWAIT_VOLUME_REPLACE[foundKey])
                        
                        # print(f"PR_A864 -->  dst = {dst}")
                    
                        FilesManager.copy_file_shutil(src, dst)
                        
                        print(f"PR_A961 --> SYS LOG: Создан файл-заставка с названием -> {dst}  ")
                        
                        # СОЗДАНИЕ документа-пустышки
                        newDocumentFileName = FilesManager.get_file_name_from_path (dst)
                        
                        # записать названия документа в словарь данных по сообщению-документу
                        dicMessageData['document_file_name'] = newDocumentFileName 
                        
                        downloadPath = dst
                        
                        # Присваивание статуса 
                        dicMessageData['status'] = 'DOCUMENT_CREATED_INSTEAD_DOWNLOADING_' 
                    
                    
                    
                    else:
                        if not flagPseudoLoadingDoc:
                            
                            # ЗАГРУЖАЕМ ДОКУМЕНТ !!!
                            downloadPath = await message.download_media(fullFilePath)
                            
                            # docFileName = FilesManager.get_file_name_from_path (downloadPath)
                            
                            # # записать названия документа в словарь данных по сообщению-документу
                            # dicMessageData['document_file_name'] = docFileName 
                            
                            # Присваивание статуса 
                            dicMessageData['status'] = 'DOCUMENT_DOWNLOADED_' 
                            
                        else: 
                                
                            # Присваивание статуса 
                            dicMessageData['status'] = 'DOCUMENT_PSEUDO_DOWNLOADED_' 
                            
                            # Создать пустышку   mp3 с названием и адресом fullFilePath. Этот файл по размеру малый, но по названию соотвтетсвует какбуд-то бы 
                            # скачаннмоу файлу аудио-тома книги. Поэтому с этим физическим книжным комплектом можно эксперементировать для выгрузки на наш канал
                            FilesManager.copy_file_shutil(ms.EMPTY_MP3_SAMPLE, fullFilePath) 
                            # искучтвенно подставляем возвратный путь скачанного файла
                            downloadPath = fullFilePath
                            
                            print(f"PR_B213 --> SYS LOG: Файл-пустышка mp3 создан вместо mp3 аудил-тома, который должен был бы быть скачен, если бы не стоял флаг pseudoLoading")
                            print(f"PR_B214 --> Полный путь нового аудио-тома пустышки: {fullFilePath}")


                                
                    
                    print (f"PR_A089 --> SYS LOG: Документ {messageFileName} загружен в каталог: {downloadPath}")
                    # print(f"PR_A059 --> mssfFilePath = {mssfFilePath}")
                    
                    # Присваиваем путь загруженного файла
                    dicMessageData['download_path'] = downloadPath
                    

                # Обработка ошибки при загрузки документа (или каких-то ошибок кроме загрузки внутри try)        
                except Exception as err:
                    # TODO: Прмиенить анализ ошибок и созданию своих классов ошибок и их обработки !!!
                    print(f"PR_A090 --> SYS LOG: ОШИБКА !!! при загрузке документа : {err}")
                    dicMessageData['status'] = 'DOCUMENT_DOWNLOADING_ERROR_'
                    
            else: # Иначе, если флаг не разрешает   загрузку документа
                # Присваивание статуса : 'AUDIO_DOWNLOADED_' 
                dicMessageData['status'] = 'DOCUMENT_DOWNLOADING_PROHIBITED_BY_FLAG_' 
            


                
        # Если флаг загрузки картинки loadImg = True и сообщение является картинкой с возможным текстом, то загржаем картинку в директорий loadPath 
        # с заданным форматом названия, основанном на дате-вреени загрузки процесса
        # if loadImg and type(message.media) == MessageMediaPhoto: # фильтруем только картинки
        
        # !!!! СКАЧИВАНИЕ КАРТИНКИ !!!!
        # фильтруем только картинки
        if type(message.media) == MessageMediaPhoto:
            
            print(f"PR_A312 --> IF BRENCH: если сообщение является картинкой с описанием ... ")

            dicMessageData['messages_type'] = 'TEXT_WITH_IMAGE_MSSG_'
            # id типа
            dicMessageData['mssg_type_id'] = 1
            
            # Создание уникального имени скачиваемого файла (если скачивание картинки разрешена будет. )
            # ПРИМ: Но имя все равно остается уникальное с этого момента
            # currCalendDate = currCalendDateFormat1 # Текущая календарная дата в формате D_M_Y_H_M_S
            
            # Групповой id сообщения (либо None,  либо цифра типа message.grouped_id: 13690994442196138)
            # Дифференциация альбомных, группвых фото от сообщения с одной фото
            if message.grouped_id is not None:
                print(f"PR_B108 --> message.grouped_id: {message.grouped_id}")
                messageGroupedId = message.grouped_id
                dicMessageData['messages_grouped_id'] = messageGroupedId
            else: 
                messageGroupedId = -1
                
            dicMessageData['messages_grouped_id'] = messageGroupedId
                
            
            origSourceMarker = f'ch{channelSysId}' # id канала (Напромер. 1 - это 'Аудиокниги фантастика')
            imgType = 'bdescr_photo' # Тип скачиваемой картинки
            
            grpOrderMarker = 'gr1' # Иаркер главной картинки в группе (если будет группа)
            
            # Кодируем цифры id сообщения в буквы
            alphabetMessageId = FunctionsGeneralClass.code_digits_sequence_to_alphabet_one_coder_01_blf(message.id)
            # Название файла картинки, которое присваивается к скачиваемой картинке сообщения с картинкой и описанием
            # !!! ФОРМИРОВАНИЕ НАЗАНИЯ ФАЙЛА
            imgName = f'{origSourceMarker}_gsm{alphabetMessageId}_{grpOrderMarker}_{imgType}.jpg'
            
            print(f"PR_A756 --> imgName = {imgName}")
            
            # Сохраняем созданное имя картинки
            dicMessageData['image_file_name'] = imgName
            
            
            
            
            
        
            # Если загрузка картинки разрешена, сгружаем картинку из сообщения
            if flagLoadImg or flagLoadImgAnyway: 
                
                print(f"PR_A315 --> SYS LOG: Флаг разрешения скаивания картинки установлен на loadImg = {flagLoadImg}. Значит пытаемся (try) скачать картинку ")
                
                
                # E. Проверяем, если такой файл уже есть в репозитории скачиваемых картинок, то прееносим его в урну 
                fullFilePath = loadPathDir + '/' + imgName
                
                print(f"PR_A327 --> DEBUG LOG: Проверить наличие файла {fullFilePath} по заданному в нем адресу")
                
                currCalendDate = currCalendDateFormat1 # Текущая календарная дата в формате D_M_Y_H_M_S
                

                # print(f"PR_A333 --> trashPath = {trashPath}")
                # print(f"PR_A331 --> messageFileName = {imgName}")
                # print(f"PR_A332 --> currCalendDate = {currCalendDate}")

                
                # Название файла дополняется маркером текущейго момента для уникальности (что бы никогда не совпали названия переносимых файлов в урну)
                trashFullFilePath = f'{trashPathDir}/{imgName}_{currCalendDate}' # Путь к урне репозитория
                
                print(f"PR_A329 --> trashFullFilePath = {trashFullFilePath}")

                if FilesManager.if_file_exist (fullFilePath) : # Проверяем наличие файла, если система дала добро на загрузку документа, а в репозитории есть файл с таким названием, например, осколок

                    print(f"PR_A326 --> SYS LOG: В директории для скачивания файлов {loadPathDir} был найден осколок или файл с текущим адресом {fullFilePath}")


                    # переносим файл в вспомогательный лиректорий. 
                    FilesManager.move_file_to_another_dir_if_exists_in_this_dir(fullFilePath, trashFullFilePath)
                    
                    
                    print(f"PR_A399 --> SYS LOG: Файл с  названием {imgName} был перенесен в урону по адресу {trashFullFilePath}")

                    
                    
                # END E. Проверяем, если такой файл уже есть в репозитории скачиваемых картинок, то прееносим его в урну 

                try: 
                    
                    print(f"PR_A317 --> SYS LOG: Система приступила к скачиванию из ТГ канала картинки с названием {imgName} из сообщения message_id = {message.id}")
                    downlodingFullPath = loadPathDir + f'/{imgName}'
                    print(f"PR_A318 --> SYS LOG: Конечный файл после скачивания должен находится по адресу {downlodingFullPath}")
                    
                    
                    
                    
                    
                    
                    # Загрузить картинку, отфильтрованную от других медиа оператором if type(message.media) == MessageMediaPhoto
                    downloadPath = await message.download_media(
                        loadPathDir + f'/{imgName}',
                        # file_path=downloadPath,
                    )
                    
                    print (f"PR_A314 --> SYS LOG: картинка {imgName} загружен в каталог: {downloadPath}")

                    # Присваиваем путь загруженного файла
                    dicMessageData['download_path'] = downloadPath
                    
                    
                    # Присваивание статуса: 'IMAGE_DOWNLOADED_' 
                    dicMessageData['status'] = 'IMAGE_DOWNLOADED_' 
                    
                except:
                    print(f"PR_A088 --> ОШИБКА !!! при загрузке картинки")
                    dicMessageData['image_file_name'] = 'PR_A092 --> ОШИБКА ПРИ ЗАГРУЗКЕ КАРТИНКИ'
                    dicMessageData['status'] = 'IMAGE_DOWNLOADING_ERROR_' # Присваивание статуса
                    
                    
            else: # Иначе, если флаг не разрешает
                # Присваивание статуса : 'AUDIO_DOWNLOADED_' 
                dicMessageData['status'] = 'IMAGE_DOWNLOADING_PROHIBITED_BY_FLAG_' 
            
            
            
        # все остальные - текстовые (но не факт. Так как могут быть еще альбомы)
        # Считывание текстового сообщения, если есть в текущем сообщении канала (без всяких условий if, считая, что у каждого сообщения может быть текст . Но может и отсутствовать)
        dicMessageData['message_text'] = message.text
        
        
        print(f"PR_A589 --> dicMessageData = {dicMessageData}")
        
        
        
        print(f"PR_A086 -->  END:  get_channel_message_data_alter_download_docs_with_img_name_fixed_as_dic_tm_stat()") # Маркер старта метода для лога в консоли

        
        return dicMessageData





# END II. Методы анализа сообщений в канале *****
    



# #######################  III. РАБОТА С БОТАМИ И КАНАЛАМИ НЕПОСРЕДСТВЕННО ДЛЯ УПРАВЛЕНИЯ ИМИ. ОТПРАВКА СООБЩЕНИЙ НА ТГ ЧАТ  ===============================





    async def send_message_to_own_channel_through_own_bot_tm_self (self, client, **dicThrow):
        """ 
        Отправить сообщения в свой канал с помощью своего бота
        
        Типы сообщений:
        
        1	TEXT_WITH_IMAGE_MSSG_
        2	DOCUMENT_FILE_MSSG_
        3	TEXT_WITH_LINK_MSSG_
        4	TEXT_SIMPLE_MSSG_
        
        Статусы сообщений: 
        1	IMAGE_DOWNLOADED_
        2	IMAGE_DOWNLOADING_ERROR_
        3	IMAGE_DOWNLOADING_PROHIBITED_BY_FLAG_
        4	DOCUMENT_DOWNLOADED_
        5	DOCUMENT_DOWNLOADING_ERROR_
        6	DOCUMENT_DOWNLOADING_PROHIBITED_BY_FLAG_
        
        
        PARS Пример:
        
            auth = {
                'api_id' : 20460272,
                'api_hash' : '9e6f44844a41f717e5c035cb0add2984',
                'session_name' : 'anon', # Название файла с сессией (БД sqlite, если нет прочих настроек по формату сесссии. Хранится в рабочей директории, где manage.py)
                'bot_token' : '6982698935:AAFQQdz8uApzejMak2ily8azWVKytfIeuNQ', # тоукен своего бота
                'own_bot_chat_id' : -4104980551, # id своего ТГ чата-бота
            }
            
            # id своего чата, куда мы хотим отправить сообщение messageDic
            ownChatId = -1001811098741
            
            tm = TelegramManager(auth)
            
            # Текст
            text = 'Картинка с <b>мишкой!</b>'
            
            # Картинка
            img = '/home/ak/Yandex.Disk/Мишки.jpg' 
            
            
            # Словарь сообщения
            messageDic = {
                
                'message_type' : 'TEXT_WITH_IMAGE_MSSG_', # Тип сообщения
                'text' : text,
                'image' : img
                
            }
                
        """
        
        print(f"PR_A597 --> START: send_message_to_own_channel_through_own_bot_tm_self()")
        
        # INI: Смысловые: сообщения
        
        messageDic = dicThrow['messageDic']
        
        ownChatId = dicThrow['ownChatId']
        
        messageType = messageDic['message_type'] # Тип сообщения, заданный в словаре сообщения


        for case in Switch(messageType):
            """ ПРИМ: тутпока реализована отправка через бота. а не через клиента юзера """
            if case('TEXT_WITH_IMAGE_MSSG_'): 
                
                img = messageDic['image'] # Картинка
                text = messageDic['text'] # Сообщение
                                
                markup = types.InlineKeyboardMarkup(row_width=2)
                # Отправить сообщение
                self.bot.send_photo(ownChatId, photo = open(img, 'rb'), caption=text, reply_markup = markup, parse_mode='html')
                break
            
            if case('DOCUMENT_FILE_MSSG_'): 
                """ ПРИМ:  через клиента юзера (а не через бота) """
                
                # Printing upload progress
                def callback(current, total):
                    print('Uploaded', current, 'out of', total,
                        'bytes: {:.2%}'.format(current / total))
                                
                
                print(f"PR_A599 --> SYS LOG:Идентифиуирован тип сообщения ->>  DOCUMENT_FILE_MSSG_ (документ или файл)")
                pass
                mp3File = messageDic['file']
                        
                # self.bot.send_message(message.chat.id, "Files incoming")
                # mp3File = open(fl, 'rb') 
                
                chatName = 'Аудиокниги фантастика'
                
                await client.send_file(chatName, mp3File, voice_note=True, progress_callback=callback)
                
                
                # f = open('file_path', 'rb')
                # bot.send_audio(chat_id, f)
                            
                    
            
                break
            
            if case('TEXT_WITH_LINK_MSSG_'): 
                print('Число от 1 до 3')
                break
            
            if case('TEXT_SIMPLE_MSSG_'): 
                print('Число 4')
                break
            
            if case(): # default
                print('Задан тип, которого нет в переключателе')
                break
            
            
        print(f"PR_A598 --> START: send_message_to_own_channel_through_own_bot_tm_self()")






    def send_message_to_own_bot_chat_through_own_bot_tm (self, messageDic, **dicThrow):
        """ 
        Отправить сообщения в свой чат бота с помощью своего бота
        
        Прим въодного параметра:
        Словарь сообщения:
        messageDic = {
            'message' : 'Привет! Это сообщение от бота прямо сейчас!' # Тип сообщения
        }
        """

        self.bot.send_message(self.botChatId, messageDic['message'])








    @staticmethod
    async def print_all_messages(client): 
        
        
        async for message in client.iter_messages('Аудиокниги фантастика'):
            print(message.id, message.text)
        
        
        








# #######################  END III. РАБОТА С БОТАМИ И КАНАЛАМИ НЕПОСРЕДСТВЕННО ДЛЯ УПРАВЛЕНИЯ ИМИ. ОТПРАВКА СООБЩЕНИЙ НА ТГ ЧАТ  ===============================




# #######################   IV. ПРОЕКТНЫЕ АЛГОРИТМЫ  ===============================


    # НЕ УДАЛЯТЬ
    # @staticmethod
    # def get_volums_of_book_by_next_book_id (listAllBooks, listAllVolumes):
    #     """ 
    # OBSOLETED: Этот алгоритм устарел. тепреь используется assemble_book_complects_from_messages_types_sequence()
    #     Найти тома книги, используя ее id и id сообщения книги следующей за ней. 
    #     Или найти ids-сообщений, находящихся в интервале между ними, не включая их самих
        
    #     """
    #     listBookComplects =  [] # Список для сохранения формируемых словарей с книжным комплектом
    #     dicTgBookComplectData = {} # Словарь для книжного комплекта (описание книги и ее тома, все в виде их messages_id в ТГ канале)
        
    #     for i, bookId in enumerate(listAllBooks): 
            
    #         # print(f"\nPR_A265 --> START: cycle ->>  {i} | bookId = {bookId}\n")
            
    #         # для первой книги с конца канала, у которой нет нижнего ограничения в виде описания новой книги
    #         if i == 0:
    #             listBookVolumes = [x for x in listAllVolumes if x > listAllBooks[i]] 
                
    #             listQn = len(listBookVolumes)
                
    #             # Формируем пронумерованный словарь аудио-томов книги
    #             dicBookVolumes = {listQn - i:listBookVolumes[i] for i in range(listQn)}
                
    #             # print(f"PR_A263 --> i = {i} | listBookVolumes 0 = {listBookVolumes}")
                
    #         # Для остальных книг, нижней границей для которых является предыдущая с конца описание книги в канале ТГ    
    #         else:
    #             listBookVolumes = [x for x in listAllVolumes if x > listAllBooks[i] and x < listAllBooks[i-1]]
                
    #             listQn = len(listBookVolumes)
                
    #             dicBookVolumes = {listQn - i:listBookVolumes[i] for i in range(listQn)}
                
    #             # print(f"PR_A264 --> i = {i} | listBookVolumes = {listBookVolumes}")
            
            
    #         dicTgBookComplectData['book'] = bookId
    #         dicTgBookComplectData['volumes'] = dicBookVolumes
            
    #         listBookComplects.append(dicTgBookComplectData.copy())
            
    #         # print(f"\nPR_A262 --> listBookComplects = {listBookComplects}")
            
    #     return listBookComplects







    @staticmethod
    def assemble_book_complects_from_messages_types_sequence (messagesTypesSequence, correspondingMessagesTbIds):
        """ 
        Сформировать книжные комплекты из последовательности типов сообщений
        Последовательность переключается 22212212222..., где 1 - это описание книги, 2 - тома книги
        В начале всегда идут тома, которые завершаются описанием книги для этих томов. Соотвтетсвенно, любое переключение последовательности типа
        2221 .. на какой либо другой тип сообщает о том, что книжный комплект завершен и он описывается этой последовательностью 2221
        
        То есть метод ищет переключения с 1 на любой другой и формирует книжный комплект
        ПРИМ: Этот метод должен быть более точным. чем метод формирования книжных комплектов get_volums_of_book_by_next_book_id(), так как он не отсекает комплект
        при отсутствии нового описания книги, а вычленяет комлект по переключению типа сообщения
        
        ~ https://pynative.com/python-regex-capturing-groups/ [работа с группами и спанами RE]
        
        """
        
        print(f"PR_A825 --> START: assemble_book_complects_from_messages_types_sequence()")
        
        # создать строку с типами
        typesString = "".join(map(str,messagesTypesSequence))

        print(f"PR_A820 -->  typesString = {typesString}")
        
        print(f"PR_B239 --> correspondingMessagesTbIds = {correspondingMessagesTbIds}")
        
        # Поиск последовательностей начинающихся с 2 (соержащие хоть сколько их внутри) и оканчивающиеся 1 
        # 1 - это описание книги, 2 - это аудио-том книги. а такая последовательность отражает книжный комплект
        rExpr = r"(2+1)"
        
        
        #   Список КК-цепочек, разбитых по формуле rExpr из исходной typesString
        # ФОРМАТ: bComplects = ['221', '221', '21', '21', '2222222222221', '222221', '2221', '221', '22222222222221', '222221', '21', '21', '21', '21']
        bComplects = re.findall(rExpr,typesString)
        
        # Список для сохранения формируемых словарей с книжным комплектом
        listBookComplects =  [] 
    
        # Если найдены последовательности, отражающие суть книжного комплекта, то формируем из них словарь книжного комплекта
        if bComplects:
            
            print(f"PR_A820 -->  mo = {bComplects}")

            # Словарь для описания книги
            dicTgBookComplectData = {}


            # ЦИКЛ ПО ПЕРВИЧНЫМ КНИЖНЫМ КОМПЛЕКТАМ
            # Найденные группы соотвтетсвуют образу книжного комплекта, где 1 - это описание книги, а двойки - это аудио-тома книги
            # организовать цикл по образам книжных комплектов по найденным группам в анализируемой строке
            for inx, complect in enumerate(re.finditer(rExpr, typesString)):
                
                print(f"PR_B247 --> Текущий индекс КК в цикле: {inx}")
                
                # Словарь для аудио-томов книги
                dicBookVolumes = {}
                    
                
                # print(f'PR_A821 --> rExpr: {rExpr} found', complect.start(), complect.end())  
                
                # A. Найти id сообщений в списке correspondingMessagesIds, соотвтетсвующих типам из найденной группы, 
                # используя стартовый и конечный ндекс в анализируемой строке typesString, которые соотвтетсвуют индексам в списке  correspondingMessagesIds
                
                # INI
                # табличный id из correspondingMessagesIds в соотвтетсвии по индексу позиции 1, определяемой текущей найденной группой
                # возможное описание в последовательности (если это не группа. в этом случае есть вероятность, что другая картинка - описание)
                
                # ОПИСАНИЕ КНИГИ ( tbid сообщения с описанием книги , если бы описание было не групповым. Далее еще предстоит анализ в группе)
                bookTbId = correspondingMessagesTbIds[complect.end()-1] 
                
                print(f"PR_B253 --> Текущее картинка - описание tbid = {bookTbId} ")
                
                
                
                # print(f"PR_B240 --> POINT X: messageGroupId = ")
                
                # Цикл по образам аудио-томов книги 

                
                print(f"PR_B254 --> ФОРМИРОВАНИЕ СЛОВАРЯ С АУДИО-ТОМАМИ к КК с текущем индексом в цикле: {inx}")
                
                # ФОРМИРОВАНИЕ СЛОВАРЯ С АУДИО-ТОМАМИ К ОПИСАНИЮ КНИГИ
                for i, volumeInx in enumerate(range(complect.end()-2, complect.start()-1, -1)):
                    
                    
                    
                
                    # АНАЛИЗ всех томов книги в текущей цепочке КК, на предмет наличия затесавшихся осколков, не принадлежащих КК
                    # Анализ самого первого тома, состыкующегося с описанием книги в КК-цепочке
                    if i==0:
                    
                        # tbid тома в табл 'tg_messages_proceeded'
                        firstBookVolumeTbid = correspondingMessagesTbIds[volumeInx]
                        print(f"PR_B250 --> firstBookVolumeTbid = {firstBookVolumeTbid}")
                        
                        # Узнать идентификатор группы первого аудио-тома книги, если он есть. Если его нет, то идентификатор будет = -1
                        firstVolumeGroupId = TelegramManager.tlf.get_grpoup_id_by_message_tbid_tlf (firstBookVolumeTbid)
                        print(f"PR_B248 -->  Идентификатор группы первого тома книги = {firstVolumeGroupId}")
                        
                        #  Занести tbid тома в словарь аудио-томов книги
                        dicBookVolumes[i+1] = firstBookVolumeTbid
                                

                        continue
                        
                    # ОТСЕЧЕНИЕ, если первый том ениги не имеет группы. (немного защищает от вероятных присоединений осколков, так как только один том у книги)           
                    # Если messageGroupId у аудио-тома = -1, то значит этот том по умолчанию один в КК и все прочие - ршибочные осколки, 
                    # которые надо удалить из текущей КК-цепочки
                    if firstVolumeGroupId < 0: 
                        
                        print(f"PR_B249 --> Насильно прекращаем цикл с индексом : {inx}")
                        
                        # Отсекаем все прочие тома, которые могли прилипнуть к КК-цепочке в виде осколков от предыдущих загрузок
                        # прерываем цикл for
                        break  
                    
                    
                    currVolumeTbId = correspondingMessagesTbIds[volumeInx]
                    
                    print(f"PR_B251 --> currVolumeTbId = {currVolumeTbId}")
                    
                    dicBookVolumes[i+1] = currVolumeTbId
                    
                    
                    # # НЕ УДАЛЯТЬ!!!
                    # # АНАЛИЗ ТОМОВ НА ПРИЧАСТНОСТЬ К ОДНОЙ ГРУППЕ. Прим: Проблема в том, что группы аудио-томов могут быть более 10. 
                    # # И тогда возникает отсечение остальных томов,  > 10. Поэтому пока отключаем . Но не удалять из кода пока
                    # # Если груповой идентификатор существует, значт книга имеет болььше одного тома. Анализируем каждый следующий том
                    # # на соотвтетсвие его группового идентификатора - самому первому тому. Если он не соотвтетсвует, то отсекаем том от 
                    # # словаря томов книги
                    # else:

                    #     currVolumeTbId = correspondingMessagesTbIds[volumeInx]
                        
                    #     print(f"PR_B251 --> currVolumeTbId = {currVolumeTbId}")
                        
                    #     # Идентификатор группы текущего аудио-тома книги
                    #     currVolumeGroupId = TelegramManager.tlf.get_grpoup_id_by_message_tbid_tlf (currVolumeTbId)
                        
                    #     print(f"PR_B252 -->  Идентификатор группы  текущего тома книги = {currVolumeGroupId}")
                        
                    #     # Если идентификатор группы текущего по циклу тома равен идентификатору группы самого первого тома, то это
                    #     # значит, что том принадлежит книжному комплекту. Добавляем кго в словарь аудио-томов КК. Иначе - пропускаем
                    #     if currVolumeGroupId == firstVolumeGroupId:
                            
                    #         print(f"PR_B255 --> Идентификатор группы  текущего тома: {currVolumeTbId} равен ИГ первого тома КК. Регестрируем его в словаре аудио-томов КК")
                    
                    #         dicBookVolumes[i+1] = currVolumeTbId
                            
                    #     else:
                            
                    #         print(f"PR_B256 --> Идентификатор группы  текущего тома: {currVolumeTbId} НЕ равен ИГ первого тома КК. НЕ регестрируем его в словаре аудио-томов КК")
                        
                    # # END АНАЛИЗ ТОМОВ НА ПРИЧАСТНОСТЬ К ОДНОЙ ГРУППЕ.
                    
                    
                    
                    
                print(f"PR_A824 --> dicBookVolumes = {dicBookVolumes}")
                    
                    
                    
                    
                # B. Анализ не является ли найденное первое сообщение типа Photo на стыке дальнейших аудио-томов [rExpr = r"(2+1)"], которое 
                # в простейшем случае и является описанием книги, не является ли это сообщение одним из группы сообщений-photo из группы
                # Если это найденное сообщение прнадлежит группе, то оно не явялется описанием книги, а лишь последним по порядку в альбоме 
                # картинкой. Поэтому, если это группа, то надо найти первое сообщение в группе уартинок. Именно оно в этом случае будет являтся
                # описанием книги. Индикатором того, Что картинка (или документ) принадлежит группе является не NULL целое число в 
                # поле 'messages_grouped_id' в таблице 'tg_message_proceeded_ext'
                if TelegramManager.blf.if_tg_message_belongs_to_message_group_objects_blf(bookTbId):
                    
                    # C. Найти групповой идентификатор текущего сообщения-картинки 
                    
                    messageGroupedId = TelegramManager.blf.get_tg_message_grouped_id_if_any_by_mssg_tbid_blf (bookTbId)
                    print(f"PR_B241 --> messageGroupedId = {messageGroupedId}")
                    
                    # Если в сообщении естьгруппа, то провдим анализ
                    if messageGroupedId > 0:

                        # D. Найти все сообщения-картинки группы 
                        messagesTbIdsOfGivenGroup = TelegramManager.tlf.obtain_all_messages_ids_with_given_grouped_id_tlf(messageGroupedId)
                        
                        print(f"PR_B114 --> messagesTbIdsOfGivenGroup = {messagesTbIdsOfGivenGroup}")
                        
                        # E. Найти сообщение самое первое в группе (то есть с минимальным messageId или ьаксимальной)
                        
                        # OBSOLETED: caption может быть присвоен любой картинке, а не только первой. Поэтому методика определения главной картинки 
                        # с надписью меняется
                        # bookTbId =  max(messagesTbIdsOfGivenGroup)
                        
                        # E'. Найти какое из сообщений имеет в поле message_text табл tg_message_proceeded_ext описание. Взять минимум текста какой-то. 
                        # Допустим 30 знаков 
                        
                        # Основная картинка с описанием книги 
                        bookMainMessageId = TelegramManager.tlf.find_grouped_photo_message_book_description_tlf(messageGroupedId)
                        
                        print(f"PR_B242 --> bookMainMessageId = {bookMainMessageId}")
                        
                        # Если не найдено описание, то значит ? (ничего не значит, потомы что были книги, которые не имели описания. Все было еа фото)
                        # Поэтому критерий завершения тома нужно искать в анализе рядов 
                        # если не найдено, То bookMainMessageId = -1
                        if bookMainMessageId < 0: 
                            bookTbId =  max(messagesTbIdsOfGivenGroup)
                            print(f"PR_B240 --> POINT Z: bookTbId = {bookTbId}")
                        elif bookMainMessageId > 0:
                            
                            bookTbId = bookMainMessageId
                            print(f"PR_B240 --> POINT W: bookTbId = {bookTbId}")
                            
                            
                        print(f"PR_B240 --> POINT Y: bookTbId = {bookTbId}")
                            
                    # Если в сообщении НЕТ ГРУППЫ !!! , то главная  само текущее сообщение -описание и 
                    # есть главное сообщение-картинка (в которой находится и описание). тогда присваиваем текущее значение id в  bookMainMessageId     
                    else:
                        pass
                            
                            
                        
                    bookMainMessageId = bookTbId
                        
                        

                    
                    # F. Присвоить это сообщение в качестве описания книги
                    
                    # G. Сохранить группу или список всех других кроме описания картинок в dicTgBookComplectData['group_photo_mssgs']
                
                # Если нет альбомного описания книги (нет группы картинок, есть только одна)
                else:
                    messagesTbIdsOfGivenGroup = -1
                    messageGroupedId = -1
                    bookMainMessageId = -1
                    
                
                
                # ФОРМИРОВАНИЕ КНИЖНОГО КОМПЛЕКТА @@@ Прим: все идентификаторы сообщений в книжном комплекте выражены в табличных id из 
                # табл 'tg_messages_proceeded'
                #
                # # Если сообщение -каринка или документ не групповой, то получаес книжный комплект как обычно ранее было
                # id сообщения с описанием книги
                dicTgBookComplectData['book'] = bookTbId
                # словарь с перечнем томов. индексированным по ключу
                dicTgBookComplectData['volumes'] = dicBookVolumes.copy()
                
                # Группа картинок , если описание книги - альбомное
                if messageGroupedId > 0: # Если есть группа картинок
                    # Вся найденная группа сообщений - картинок с одним и тем же идентификатором группы messageGroupedId
                    dicTgBookComplectData['groupedImgMessages'] = messagesTbIdsOfGivenGroup 
                    # идентификационны id группы
                    dicTgBookComplectData['groupedId'] = messageGroupedId 
                    # Основная картинка с описанием книги
                    dicTgBookComplectData['bookMainMessageId'] = bookMainMessageId 
                

                # КОНЕЧНЫЙ СПИСОК, содержащий сформированные книжные комплекты в виде словаря dicTgBookComplectData с двумя 
                # элементами: 'book' книги и словарь томов    
                listBookComplects.append(dicTgBookComplectData.copy())
                
                
                
                
                
            # АНАЛИЗ конца цепочки, если присутствует групповые картинки с описании книги. Если нет группы, то не надо анализировать конец цепочки
            # Правильность загрузки комплекта в последнем случае однозначно определяется анализом переключения (2-->1) регулярным выражением
            # H. !!! Анализ верхнего конца цепочки ряда книжного комплекта (который обладает меньшим messageId). С этимокончанием могут быть проблемы,
            # а именно - неправильно проанализированное завершение книжнрого комплекта. Поэтому надо более тонко проанализировать это окончание 
            # книжного тома по следующим критериям: 
            #       1. Признаком правильного завершения верхнего по ТГ книжного комплекта может являтся , что следующий за ним сообщение 
            #           не входит в группу картинок описаний книги. Значит все групповые картинки загруэенны и значит загружен и весь КК 
            #           ПРИМ: это в случае, когда описание книги - это групповой набор картинок с одной основной в них. Но все они находятся под
            #           под одним и тем же groupedId. А так же в случае, если следующее за оконцовкой сообщение является каким-то псевдо книгой без томов
            #       2. Если следующий за концом сообщение является аудио-томом, то это тоже служит признаком правильного завершения книжного комплекта
            #       
            #   РЕЗЮМЕ: На данный момент эти два признака определяют завершение книжного комплекта. Если один из них проявляется, то КК считаем правильно  
            #       завершенным. В иных случаях (на данный момент) считаем КК не завершенным и он не должен иметь представление в 
            #       табл 'tg_book_complects_ch_01' и 'tg_book_complect_volumes_ch_01' . То есть такой КК незавершенный удаляется 
            #        из    listBookComplects , подающийся на выход !!!
            #
            #
            #   ПРИМ: !!! Первая часть выше описывает лишь случай, когда скачаны тома и по тем или иным причинам не докачались картинки для группы описания 
            #   книги. Но этот алгоритм не описывает случай, когда недозакачены аудио-тома. Например стоит limit на скачивание и он как раз заканчивается
            #   посередине группы аудио-томов. Тогад система видит это как завершенный комплект. Хотя на самом деле аудио-тома с ТГ канала закачены 
            #   не все. Хотя - НЕЕЕЕТ!!!! Тогда эта последовательность не подпадет под поиск последовательностей по REGEXP. ТАк как не будет правильного
            #   переключения с 2 на 1 по типам. А тома всегда идут сначала и заканчиваютсанием, если идти снизу вверх по уменьшению messageId !!!
            #
            #
            
            # K. Найти книжный комплект с самым бОльшим tbid у главного сообщения описания книги  dicTgBookComplectData['book']. 
            # ПРИМ: Самый бОльший tbid соотвтетсвует самому меньшему tgMessageId. То есть это крайний книжный комплект сверху в ленте ТГ канала (внизу 
            # КК с болшими значениями tgMessageId и с ними все работает однозначно. Проверить нужно только верхний конец последовательности)
            
            if messageGroupedId > 0:
            
            
                maxDic = max(listBookComplects, key=lambda x: x['book'])
                
                # maxDicMainMssgTbid = maxDic['bookMainMessageId']
                
                print(f"PR_B159 --> maxDic = {maxDic}")
                
                
                # L. В группе картинок найти, если ли еще большее значния tbid, Так как главное сообщение-картинка с описанием сожет быть любая из 
                # групповых картинок альбома, а нам надо найти самую крайнюю сверху, конец цепочки сверху ТГ-канала, лпределяющей книжный комплект
                # И по анализу которого нам нужно определить признаки праовильного завершения крайнего сверху книжного комплекта
                
                
                # Найти максимальный элемент в списке грцпповых картинок-сообщений этого книжного комплекта с макисмальным x['book'] (tbid главного 
                # сообщения - описания с картинкой). Этот максимальный  tbid сообщения в группе картинок и есть верхний конец цепочки, который 
                # надо исследовать на признаки правильного завершения КК
                
                groupedImgMessages = dicTgBookComplectData['groupedImgMessages']
                
                
                # ВЕРХНИЙ КОНЕЦ ЦЕПОЧКИ САМОГО КРАЙНЕГО СВЕРХУ КК (это тождественно самому малому значению  tgMessageId в ТГ-канале или верхнему концу КК в ТГ канале, 
                # граница которого быдла задана условиями настроек по загрузки сообщений из ТГ-канала в itter-переборе  Telethon)
                topEndMessageTbid = max(groupedImgMessages)
                
                print(f"PR_B160 --> topEndMessageTbid = {topEndMessageTbid}")
                
                # АНАЛИЗ верхнего конца КК на предмет правильного завершения КК после окончания цикла скачивания сообщений из ТГ-канала 
                # 1. Анализ на наличие следующего элемента цепочки в общем в скачанных сообщениях в табл 'tg_messages_proceeded'. Или наш верхний конец 
                # КК является конечным на этом завершенном этапе скачивания
                
                
                # Получить список всех tdids табличных id в табл 'tg_messages_proceeded'
                messagesTbids = TelegramManager.tlf.get_all_tbids_from_tg_messages_proceeded_tlf()
                
                
                # Найти те элементы в списке messagesTbids, которые больше , чем topEndMessageTbid
                
                # listOfValsMoreThenGivenVal = [x for x in messagesTbids if x > topEndMessageTbid]
                
                # topEndMessageTbid = 2814
                
                listOfValsMoreThenGivenVal = FunctionsGeneralClass.obtain_list_elements_greater_than_given_val_fgc(messagesTbids, topEndMessageTbid)
                
                print(f"PR_B161 --> listOfValsMoreThenGivenVal = {listOfValsMoreThenGivenVal}")

                # Проанализировать полученный список сравнения всех messagesTbids из табл 'tg_messages_proceeded' в сравнении с заданным верхним  id сообщения
                # максимальной картинки из группы. Если есть большие элементы, то нужно проанализировать самый первый, следующий за самим топовым 
                # topEndMessageTbid в последовательности сообщений , формирующих книжный комплект
                
                # Если полученный лист сообщений. id которых больше топового сообщения из книжного комплекта, будет содержать хоть один элемент, 
                # то этот факт подтвердит, что книжный комплект завершен, так как любой следующий эдлемент уже по умолчанию не входит в группу картинок КК, 
                # которые всегда по умолчанию находятся выше в ТГ ленте, Чем аудио-тома. А значит КК загружен полностью и может представлять КК на следующем этапе
                # Если же никаких элементов в этом остаточном от сравнения списке нет, то из этого следуюет, что существует вероятность, что в ТГ канале остались не 
                # загруженными участники группы описания книги. И значит этот комплект не сожет считатьься доказанно завершенным. И словарб с ним необходимо 
                # удалить из общего списка книжных комплектов listBookComplects
                
                # Если в остаточном списке listOfValsMoreThenGivenVal есть хоть один элемент, то КК завершен и мы пропускаем его для формирования КК для 
                # следующего уровня в табл tg_book_complects_ch_01 и tg_book_complect_volumes_ch_01. Просто ничего не делаем, pass
                if len(listOfValsMoreThenGivenVal) > 0: 
                    pass
                # Если же элементов НЕ существует в остаточном списке listOfValsMoreThenGivenVal, то это значит мы не можем сказать, что КК завершен правильно 
                # и поэтому мы удаляем этот незавершенный книжный комплект из общего списка listBookComplects, который находится в нем последним
                else:
                    pass
                    # ~ https://favtutor.com/blogs/remove-last-element-from-list-python
                    del listBookComplects[-1]
                    

        else:
            pass
            print(f"PR_A820 -->  Не найдены книжные комплекты !!! NOT fOUND")
            
            

        print(f"PR_A867 --> ")
        pp(listBookComplects)
            
        
        print(f"PR_A826 --> END: assemble_book_complects_from_messages_types_sequence()")


        
        return listBookComplects
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # # создать строку с типами
        # typesString = "".join(map(str,messagesTypesSequence))

        # print(f"PR_A820 -->  typesString = {typesString}")
        
        # # Поиск последовательностей начинающихся с 2 (соержащие хоть сколько их внутри) и оканчивающиеся 1 
        # # 1 - это описание книги, 2 - это аудио-том книги. а такая последовательность отражает книжный комплект
        # rExpr = r"(2+1)"
        # bComplects = re.findall(rExpr,typesString)
        
        # # Список для сохранения формируемых словарей с книжным комплектом
        # listBookComplects =  [] 
    
        # # Если найдены последовательности, отражающие суть книжного комплекта, то формируем из них словарь книжного комплекта
        # if bComplects:
            
        #     print(f"PR_A820 -->  mo = {bComplects}")

        #     # Словарь для описания книги
        #     dicTgBookComplectData = {}



        #     # Найденные группы соотвтетсвуют образу книжного комплекта, где 1 - это описание книги, а двойки - это аудио-тома книги
        #     # организовать цикл по образам книжных комплектов по найденным группам в анализируемой строке
        #     for complect in re.finditer(rExpr, typesString):
                
                
        #         # Словарь для аудио-томов книги
        #         dicBookVolumes = {}
                    
                
        #         print(f'PR_A821 --> rExpr: {rExpr} found', complect.start(), complect.end())  
                
        #         # A. Найти id сообщений в списке correspondingMessagesIds, соотвтетсвующих типам из найденной группы, 
        #         # используя стартовый и конечный ндекс в анализируемой строке typesString, которые соотвтетсвуют индексам в списке  correspondingMessagesIds
                
        #         # INI
        #         # табличный id из correspondingMessagesIds в соотвтетсвии по индексу позиции 1, определяемой текущей найденной группой
        #         bookTbId = correspondingMessagesTbIds[complect.end()-1]
                
        #         # Цикл по образам аудио-томов книги 

        #         # for i, volumeInx in enumerate(complect.start(), complect.end()-1):
        #         for i, volumeInx in enumerate(range(complect.end()-2, complect.start()-1, -1)):
                
                    
                
        #             volumeTbId = correspondingMessagesTbIds[volumeInx]
                
        #             dicBookVolumes[i+1] = volumeTbId
                    
        #         print(f"PR_A824 --> dicBookVolumes = {dicBookVolumes}")
                    
                    
                    
                    
        #         # B. Анализ не является ли найденное первое сообщение типа Photo на стыке дальнейших аудио-томов [rExpr = r"(2+1)"], которое 
        #         # в простейшем случае и является описанием книги, не является ли это сообщение одним из группы сообщений-photo из группы
        #         # Если это найденное сообщение прнадлежит группе, то оно не явялется описанием книги, а лишь последним по порядку в альбоме 
        #         # картинкой. Поэтому, если это группа, то надо найти первое сообщение в группе уартинок. Именно оно в этом случае будет являтся
        #         # описанием книги. Индикатором того, Что картинка (или документ) принадлежит группе является не NULL целое число в 
        #         # поле 'messages_grouped_id' в таблице 'tg_message_proceeded_ext'
        #         if TelegramManager.blf.if_tg_message_belongs_to_message_group_objects_blf(bookTbId):
                    
        #             # C. Найти групповой идентификатор текущего сообщения-картинки 
                    
        #             messageGroupedId = TelegramManager.blf.get_tg_message_grouped_id_if_any_by_mssg_tbid_blf (bookTbId)

        #             # D. Найти все сообщения-картинки группы
        #             messagesTbIdsOfGivenGroup = TelegramManager.tlf.obtain_all_messages_ids_with_given_grouped_id_tlf(messageGroupedId)
                    
        #             print(f"PR_B114 --> messagesTbIdsOfGivenGroup = {messagesTbIdsOfGivenGroup}")
                    
        #             # E. Найти сообщение самое первое в группе (то есть с минимальным messageId или ьаксимальной)
                    
        #             # OBSOLETED: caption может быть присвоен любой картинке, а не только первой. Поэтому методика определения главной картинки 
        #             # с надписью меняется
        #             # bookTbId =  max(messagesTbIdsOfGivenGroup)
                    
        #             # E'. Найти какое из сообщений имеет в поле message_text табл tg_message_proceeded_ext описание. Взять минимум текста какой-то. 
        #             # Допустим 30 знаков 
                    
        #             # Основная картинка с описанием книги 
        #             bookMainMessageId = TelegramManager.tlf.find_grouped_photo_message_book_description_tlf(messageGroupedId)
                    
                    
                    
        #             # Если не найдено описание, то значит ? (ничего не значит, потомы что были книги, которые не имели описания. Все было еа фото)
        #             # Поэтому критерий завершения тома нужно искать в анализе рядов 
        #             # если не найдено, То bookMainMessageId = -1
        #             if bookMainMessageId < 0: 
        #                 bookTbId =  max(messagesTbIdsOfGivenGroup)
        #             elif bookMainMessageId > 0:
        #                 bookTbId = bookMainMessageId
                        
        #             bookMainMessageId = bookTbId
                        
                        
        #             print(f"PR_B157 --> bookTbId = {bookTbId}")
                    
        #             # F. Присвоить это сообщение в качестве описания книги
                    
        #             # G. Сохранить группу или список всех других кроме описания картинок в dicTgBookComplectData['group_photo_mssgs']
                
        #         # Если нет альбомного описания книги (нет группы картинок, есть только одна)
        #         else:
        #             messagesTbIdsOfGivenGroup = -1
        #             messageGroupedId = -1
        #             bookMainMessageId = -1
                    
                
                
        #         # ФОРМИРОВАНИЕ КНИЖНОГО КОМПЛЕКТА @@@ Прим: все идентификаторы сообщений в книжном комплекте выражены в табличных id из 
        #         # табл 'tg_messages_proceeded'
        #         #
        #         # # Если сообщение -каринка или документ не групповой, то получаес книжный комплект как обычно ранее было
        #         # id сообщения с описанием книги
        #         dicTgBookComplectData['book'] = bookTbId
        #         # словарь с перечнем томов. индексированным по ключу
        #         dicTgBookComplectData['volumes'] = dicBookVolumes.copy()
                
        #         # Группа картинок , если описание книги - альбомное
        #         if messageGroupedId > 0: # Если есть группа картинок
        #             # Вся найденная группа сообщений - картинок с одним и тем же идентификатором группы messageGroupedId
        #             dicTgBookComplectData['groupedImgMessages'] = messagesTbIdsOfGivenGroup 
        #             # идентификационны id группы
        #             dicTgBookComplectData['groupedId'] = messageGroupedId 
        #             # Основная картинка с описанием книги
        #             dicTgBookComplectData['bookMainMessageId'] = bookMainMessageId 
                

        #         # КОНЕЧНЫЙ СПИСОК, содержащий сформированные книжные комплекты в виде словаря dicTgBookComplectData с двумя 
        #         # элементами: 'book' книги и словарь томов    
        #         listBookComplects.append(dicTgBookComplectData.copy())
                
                
                
                
                
        #     # АНАЛИЗ конца цепочки, если присутствует групповые картинки с описании книги. Если нет группы, то не надо анализировать конец цепочки
        #     # Правильность загрузки комплекта в последнем случае однозначно определяется анализом переключения (2-->1) регулярным выражением
        #     # H. !!! Анализ верхнего конца цепочки ряда книжного комплекта (который обладает меньшим messageId). С этимокончанием могут быть проблемы,
        #     # а именно - неправильно проанализированное завершение книжнрого комплекта. Поэтому надо более тонко проанализировать это окончание 
        #     # книжного тома по следующим критериям: 
        #     #       1. Признаком правильного завершения верхнего по ТГ книжного комплекта может являтся , что следующий за ним сообщение 
        #     #           не входит в группу картинок описаний книги. Значит все групповые картинки загруэенны и значит загружен и весь КК 
        #     #           ПРИМ: это в случае, когда описание книги - это групповой набор картинок с одной основной в них. Но все они находятся под
        #     #           под одним и тем же groupedId. А так же в случае, если следующее за оконцовкой сообщение является каким-то псевдо книгой без томов
        #     #       2. Если следующий за концом сообщение является аудио-томом, то это тоже служит признаком правильного завершения книжного комплекта
        #     #       
        #     #   РЕЗЮМЕ: На данный момент эти два признака определяют завершение книжного комплекта. Если один из них проявляется, то КК считаем правильно  
        #     #       завершенным. В иных случаях (на данный момент) считаем КК не завершенным и он не должен иметь представление в 
        #     #       табл 'tg_book_complects_ch_01' и 'tg_book_complect_volumes_ch_01' . То есть такой КК незавершенный удаляется 
        #     #        из    listBookComplects , подающийся на выход !!!
        #     #
        #     #
        #     #   ПРИМ: !!! Первая часть выше описывает лишь случай, когда скачаны тома и по тем или иным причинам не докачались картинки для группы описания 
        #     #   книги. Но этот алгоритм не описывает случай, когда недозакачены аудио-тома. Например стоит limit на скачивание и он как раз заканчивается
        #     #   посередине группы аудио-томов. Тогад система видит это как завершенный комплект. Хотя на самом деле аудио-тома с ТГ канала закачены 
        #     #   не все. Хотя - НЕЕЕЕТ!!!! Тогда эта последовательность не подпадет под поиск последовательностей по REGEXP. ТАк как не будет правильного
        #     #   переключения с 2 на 1 по типам. А тома всегда идут сначала и заканчиваютсанием, если идти снизу вверх по уменьшению messageId !!!
        #     #
        #     #
            
        #     # K. Найти книжный комплект с самым бОльшим tbid у главного сообщения описания книги  dicTgBookComplectData['book']. 
        #     # ПРИМ: Самый бОльший tbid соотвтетсвует самому меньшему tgMessageId. То есть это крайний книжный комплект сверху в ленте ТГ канала (внизу 
        #     # КК с болшими значениями tgMessageId и с ними все работает однозначно. Проверить нужно только верхний конец последовательности)
            
        #     if messageGroupedId > 0:
            
            
        #         maxDic = max(listBookComplects, key=lambda x: x['book'])
                
        #         # maxDicMainMssgTbid = maxDic['bookMainMessageId']
                
        #         print(f"PR_B159 --> maxDic = {maxDic}")
                
                
        #         # L. В группе картинок найти, если ли еще большее значния tbid, Так как главное сообщение-картинка с описанием сожет быть любая из 
        #         # групповых картинок альбома, а нам надо найти самую крайнюю сверху, конец цепочки сверху ТГ-канала, лпределяющей книжный комплект
        #         # И по анализу которого нам нужно определить признаки праовильного завершения крайнего сверху книжного комплекта
                
                
        #         # Найти максимальный элемент в списке грцпповых картинок-сообщений этого книжного комплекта с макисмальным x['book'] (tbid главного 
        #         # сообщения - описания с картинкой). Этот максимальный  tbid сообщения в группе картинок и есть верхний конец цепочки, который 
        #         # надо исследовать на признаки правильного завершения КК
                
        #         groupedImgMessages = dicTgBookComplectData['groupedImgMessages']
                
                
        #         # ВЕРХНИЙ КОНЕЦ ЦЕПОЧКИ САМОГО КРАЙНЕГО СВЕРХУ КК (это тождественно самому малому значению  tgMessageId в ТГ-канале или верхнему концу КК в ТГ канале, 
        #         # граница которого быдла задана условиями настроек по загрузки сообщений из ТГ-канала в itter-переборе  Telethon)
        #         topEndMessageTbid = max(groupedImgMessages)
                
        #         print(f"PR_B160 --> topEndMessageTbid = {topEndMessageTbid}")
                
        #         # АНАЛИЗ верхнего конца КК на предмет правильного завершения КК после окончания цикла скачивания сообщений из ТГ-канала 
        #         # 1. Анализ на наличие следующего элемента цепочки в общем в скачанных сообщениях в табл 'tg_messages_proceeded'. Или наш верхний конец 
        #         # КК является конечным на этом завершенном этапе скачивания
                
                
        #         # Получить список всех tdids табличных id в табл 'tg_messages_proceeded'
        #         messagesTbids = TelegramManager.tlf.get_all_tbids_from_tg_messages_proceeded_tlf()
                
                
        #         # Найти те элементы в списке messagesTbids, которые больше , чем topEndMessageTbid
                
        #         # listOfValsMoreThenGivenVal = [x for x in messagesTbids if x > topEndMessageTbid]
                
        #         # topEndMessageTbid = 2814
                
        #         listOfValsMoreThenGivenVal = FunctionsGeneralClass.obtain_list_elements_greater_than_given_val_fgc(messagesTbids, topEndMessageTbid)
                
        #         print(f"PR_B161 --> listOfValsMoreThenGivenVal = {listOfValsMoreThenGivenVal}")

        #         # Проанализировать полученный список сравнения всех messagesTbids из табл 'tg_messages_proceeded' в сравнении с заданным верхним  id сообщения
        #         # максимальной картинки из группы. Если есть большие элементы, то нужно проанализировать самый первый, следующий за самим топовым 
        #         # topEndMessageTbid в последовательности сообщений , формирующих книжный комплект
                
        #         # Если полученный лист сообщений. id которых больше топового сообщения из книжного комплекта, будет содержать хоть один элемент, 
        #         # то этот факт подтвердит, что книжный комплект завершен, так как любой следующий эдлемент уже по умолчанию не входит в группу картинок КК, 
        #         # которые всегда по умолчанию находятся выше в ТГ ленте, Чем аудио-тома. А значит КК загружен полностью и может представлять КК на следующем этапе
        #         # Если же никаких элементов в этом остаточном от сравнения списке нет, то из этого следуюет, что существует вероятность, что в ТГ канале остались не 
        #         # загруженными участники группы описания книги. И значит этот комплект не сожет считатьься доказанно завершенным. И словарб с ним необходимо 
        #         # удалить из общего списка книжных комплектов listBookComplects
                
        #         # Если в остаточном списке listOfValsMoreThenGivenVal есть хоть один элемент, то КК завершен и мы пропускаем его для формирования КК для 
        #         # следующего уровня в табл tg_book_complects_ch_01 и tg_book_complect_volumes_ch_01. Просто ничего не делаем, pass
        #         if len(listOfValsMoreThenGivenVal) > 0: 
        #             pass
        #         # Если же элементов НЕ существует в остаточном списке listOfValsMoreThenGivenVal, то это значит мы не можем сказать, что КК завершен правильно 
        #         # и поэтому мы удаляем этот незавершенный книжный комплект из общего списка listBookComplects, который находится в нем последним
        #         else:
        #             pass
        #             # ~ https://favtutor.com/blogs/remove-last-element-from-list-python
        #             del listBookComplects[-1]
                    

        # else:
        #     pass
        #     print(f"PR_A820 -->  Не найдены книжные комплекты !!! NOT fOUND")
            
            

        # print(f"PR_A867 --> ")
        # pp(listBookComplects)
            
        
        # print(f"PR_A826 --> END: assemble_book_complects_from_messages_types_sequence()")


        
        # return listBookComplects
        
        

        








    @staticmethod
    def create_and_record_book_complects_from_tg_downloads (**bkwargs):
        """ 
        TelegramManager
        Сформировать из загруженных из ТГ данных книжные комплекты и записать их в таблицы 'tg_book_complects_ch_01' и 'tg_book_complect_volumes_ch_01'
        Анализ скаченных дынных из таблиц с сообщениями для формирования книжных комплектов, в которых содержаться описание книги с томами в ней и соотвтетсвующие им 
        id сообщений в формате 

        dicTgBookComplectData = {
            
            'book' : 4209,
            'volumes' : {
                            1 : '4210',
                            2 : '4211',
                            3 : '4212',
                            4 : '4213'
                        }
        }
        """
        
        print(f"PR_A658 --> START: create_and_record_book_complects_from_tg_downloads ()")
        
        # D. !!! Обязательно создать защиту от внесения в таблицы tg_messages... повторно сообщения,в предыдущем успешно загруженные. Повторное включение загрузки меняет их 
        # статус на ошибочные. Это искажает общую картину для анализа в будущем !!!
        
        # A. Из таблицы 'tg_messages_proceeded' скачать все записи и проанализировать их на предмет: 
        
        # ПРИМ: цикл анализа записей должен начинаться с конечного сообщения. То есть сначала идут сообщения с болшими message_id 
        
        spps = SqlitePandasProcessorSpeedup(ms.DB_CONNECTION)
        sps = SqliteProcessorSpeedup (ms.DB_CONNECTION)
        blm = BookLibraryManager()
        blf = BookLibraryFuncs()
        tlf = TgLocalFuncs()
        
        # 1. - создать список всех messages_id с типом = 1 (описание и картинка) 
        
        sql = f"SELECT * FROM {ms.TB_MSSGS_PROCEEDED_}"
        
        # # Все сообщения из таблицы 'tg_messages_proceeded' : for SQLite НЕ УДАЛЯТЬ! 
        # dfAllMessages = spps.read_sql_to_df_pandas_SPPS(sql)
        
        # PREV единая цепочка без разделения по источнику . Позже удалить
        # Все сообщения из таблицы 'tg_messages_proceeded' : for mySQL НЕ УДАЛЯТЬ! 
        # dfAllMessages = spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        # РАзделить последовательности по источнику. Каждая анализируемая цепочка типов должна быть унитарна в смысле источника, иначе будут
        #  ошиочные переплетения аудио-томов одного источника с книгами и томами другого !!! ВАЖНО
        # # Получить id установочного активного ТГ-канала
        tgSourceId = blf.get_orig_source_tbid_by_tg_channel_id_blf(ms.channelNameGlob)
        dfAllMessages = tlf.obtain_df_tb_proceeded_types_sequences_by_tg_source_id_tlf(tgSourceId)
        
        
        print(f"PR_B238 --> id источника , по которому добывается цепочка последовательности типов сообщений: {tgSourceId}")
        
        # сообщения соотвтетсвующие описанию книг
        dfAllBooks = dfAllMessages.query('message_type_ref_id == 1')
        
        # Список id сообщений с книгами в таблице 'tg_messages_proceeded'
        listAllBooks = list(dfAllBooks['message_own_id'])
        
        print(f"PR_A261 --> listAllBooks = {listAllBooks}")
        
        # 2. - Создать списки всех messages_id в интервалах между messages_id с типом = 1 (сообщения должны быть типа = 2 (аудил-тома))
        # - Создать списки всех messages_id в интервалах между messages_id с типом = 1 (сообщения должны быть типа = 2 (аудил-тома))
        # - Создать словари типа dicTgBookComplectData, формирующих комплект по одному аудио-изданию. 
        # - Сформировать список из этих словарей
        # Все сообщения , соотвтетсвуюие ацдио-томам книг
        dfAllVolumes = dfAllMessages.query('message_type_ref_id == 2')
        # Список всех id сообщений соотвтетсвуюие ацдио-томам книг
        listAllVolumes = list(dfAllVolumes['message_own_id'])
        
        # print(f"PR_A262 --> listAllVolumes = {listAllVolumes}")
        

        # F. ОЧИСТКА: 2й уровень
        # тех старых комплектов, которые уже зарегестрированы в библиотек LABBA. Удаление реализованных комплектов из 
        # # таблиц tg_book_complects_ch_01 и tg_book_complect_volumes_ch_01
        
        # НАстройка : Флаг Очищать ненужный использованный материал после регистрации книги
        if bkwargs['clearUsedOutDataAfterRegistration']:
            # Удалить  книжные комплекты  изтаблиц 'tg_book_complects_ch_01' и 'tg_book_complect_volumes_ch_01' зарегестрированных книг
            blf.remove_book_complects_for_lib_reistered_books_blf()

        # END F. ОЧИсТКА: 2й уровень
        
        
        
        # A. PREVIOUS НЕ УДАЛЯТЬ
        # listBookComplects = TelegramManager.get_volums_of_book_by_next_book_id (listAllBooks, listAllVolumes)
        

        
        # B. Сформировать книжные комплекты на основе анализа последовательности типов сообщений из табл tg_messages_proceeded
        
        # Последовательность типов сообщений для анализа на формирование книжных комплектов
        messagesTypesSequence = list(dfAllMessages['message_type_ref_id'])
        
        # Последовательность табличных id сообщений, соотвтетсвующая последователльности типов (для последующего сопоставления групп с типами и их индексов в строке 
        # с данной последовательностью для вычисления id сообщений , соотвтетсвующих вычлененным группам типов) из табл 'tg_messages_proceeded'
        correspondingMessagesTbIds = list(dfAllMessages['id'])
        
        # Книжные комплекты на основе табличных ids зависимостях между сообщениями типа описание-photo и аудио-томами
        listBookComplects = TelegramManager.assemble_book_complects_from_messages_types_sequence (messagesTypesSequence, correspondingMessagesTbIds)
        
        print(f"PR_A819 -->")
        pp(listBookComplects)
        
        
        
        
        # TODO: Удалить это определение после коррекции очистительных методов
        # Источник сообщений : ТГ-канал с id из табл 'lib_orig_sources'
        origSourceId = bkwargs['origSourceId']
        
        
        
        
        
        # 3. На основе списка комплектов вносим записи в указанные таблицы
        
        # print(f"PR_A262 --> listBookComplects = {listBookComplects}")
        

        # Текущие даты-время
        dtStringFormat1, currCalDateTime, currUnixTime = FG.get_current_time_format_1_and_2_and_universal_unix()

        print (f"PR_A667 --> listBookComplects_QN = {len(listBookComplects)}")
        
        print (f"PR_B237 --> listBookComplects = {listBookComplects}")
        
        for inx, complect in enumerate(listBookComplects):
            
            # print(f"PR_A665 --> for inx = {inx}")
            
            bookMsgTbId = complect['book']
            dicVolumesTbids = complect['volumes']
            
            # создаем словарь с volumesMessagesIds  заместо volumesMessagesTbids (то есть вставляем вместо значений словаря, 
            # которые сейчас являются табличными id сообщений для аудио-томов, на  ids образующих сообщений ТГ-канала)
            # Это нужно для того, что бы при формировании комплектов не было бы двойственного значения ключа, если бы был только
            # один tgMessageId, который служит ключем только в составе с  щкшпЫщгксуШв
            dicVolumes = { x:tlf.get_tg_messsage_id_by_its_tbid_tlf(y) for x,y in dicVolumesTbids.items() }
            
            
            # В зависимости от книжного комплекта достаем из него origSourceId комплекта и соотвтетсвенные messagesIds
            # Id сообщения соотвтетвующее табличному id сообщения (не забывать, что уникальность идентификации сообщения образуется 
            # композитным ключем : origSourceId и messageId. Либо одним абсолютным индексом табличным id сообщений)
            bookMsgId = tlf.get_tg_messsage_id_by_its_tbid_tlf(bookMsgTbId)
            
            # Текущий id источника сообщения (берется из самого сообщения, уже скачанного)
            currMssgOrigSourceId = tlf.get_messsage_orig_source_id_by_its_tbid_tlf(bookMsgTbId)
            
            
            
            # ОТСЕЧЕНИЕ : 2й уровень 
            # Second Level (формирование книжных комплектов из скачанных с ТГ сообщений)
            # ПРОВЕРКА И ОТСЕЧЕНИЕ НА УРОВНЕ ФОРМИРОВАНИЯ КОМПЛЕКТОВ КНИГ
            # G. Проверить наличие записи с этой книгой в таблице 'tg_book_complects_ch_01'
            
            # Текущий список отсечения. Формируется на базе определения источника текущего сообщения и на базе вычисленного currMssgOrigSourceId 
            # находятся id ТГ-сообщений только этого источника, по которым происходит остечение
            totalRejectMessagesIdsOfFirstLevel = blf.get_reject_messages_ids_list_for_second_level_blf(currMssgOrigSourceId)
                
            print(f"PR_B021 --> SYS LOG: Reject-список -->> {totalRejectMessagesIdsOfFirstLevel}")
            
            # !!!! ОТСЕЧЕНИЕ REJECTOR!!!!    
            # Остечение сообщение от дальнейшей обработки с анализом по сообщениям только от того источника, к каоторому принадлежит текущее сообщение
            ifReject = blf.reject_proccessing_if_in_reject_messages_ids_list_blf(bookMsgId, totalRejectMessagesIdsOfFirstLevel)    
            
            print(f"PR_B022 --> POINT A")

            if ifReject:
                
                print(f"""
                    PR_B023 --> SYS LOG: Книжный комплект, основанный на сообщении с ID = {bookMsgId}, уже  либо был создан и находится в табл 'tg_book_complects_ch_01'. 
                    Либо книга уже зарегестрирована в библиотеке LABBA. Пропускаем цикл
                    """)

                continue
        
        
                # END ОТСЕЧЕНИЕ : 2й уровень 

            
            # Если нет возврата от sql -запроса, то заносим новую запись книжного комплекта
            else:
                pass
                print(f"PR_A305 --> SYS LOG: В таблице 'tg_book_complects_ch_01' нет записи по книге с message_own_id = {bookMsgId}. Вносим соотвтетствующие записи по данному книжноу комплекту")

        
                print(f"PR_A866 --> bookMsgId = {bookMsgId}")
        
                # Создать новую запись в табл tg_book_complects_ch_01
                sql = f"""
                INSERT INTO {ms.TB_TG_BOOK_COMPLECTS_CH_01} 
                (channel_id_ref, book_msg_id, date_reg_calend, date_reg_unix) 
                VALUES ({origSourceId}, {bookMsgId}, '{currCalDateTime}', {currUnixTime})
                """
                
                # ВНЕСТИ новую запись в таблице tg_book_complects_ch_01
                sps.execute_sql_SPS(sql)
                
                # print(f"PR_A266 --> sql = {sql}")
                
                
                # # Получить последний автоинкрементный номер ключевого поля id в таблице. Для SQLite. НЕ УДАЛЯТЬ !
                # lastId = sps.get_last_rowid_from_tb_sps(ms.TB_TG_BOOK_COMPLECTS_CH_01)
                
                # Получить последний автоинкрементный номер ключевого поля id в таблице. Для MySQL. НЕ УДАЛЯТЬ !
                lastId = sps.get_last_inserted_id_in_db_mysql_sps()
                
                print(f"PR_A402 --> lastId = {lastId}")
                
                
                # Цикл по томам текущей книги 
                
                print(f"PR_A865 --> ")
                pp(dicVolumes)
                
                
                # Если есть тома в словаре dicVolumes
                if len(dicVolumes)>0: 
                
                    for volumeOrder, volumeMsgId in dicVolumes.items():
                        
                        # INI
                        # C. Получить название тома по его mssgId
                        
                        # {CURRENT 05-02-2024 23-06}
                        sql = f"""
                        INSERT INTO {ms.TB_TG_BOOK_COMPLECT_VOLUMES_CH_01} 
                        (book_complect_id_ref, volume_msg_id, volume_order, date_reg_calend, date_reg_unix, channel_id_ref) 
                        VALUES ({lastId}, {volumeMsgId}, {volumeOrder}, '{currCalDateTime}', {currUnixTime}, {origSourceId})
                        """
                    
                        print(f"PR_A267 --> sql = {sql}")
                
                        # ВНЕСТИ новую запись в таблице tg_book_complect_volumes_ch_01
                        sps.execute_sql_SPS(sql)

                
        print(f"PR_A659 --> END: create_and_record_book_complects_from_tg_downloads ()")






# #######################  END IV. ПРОЕКТНЫЕ АЛГОРИТМЫ  ========










# #######################   V. ПОЛЕЗНЫЕ МЕТОДЫ  ========




    def get_message_type_in_project_space (self, message):
        """ 
        ЗАГОТОВКА
        Получить тип сообщения из ТГ-канала в пространстве проектного смысла. Их пока 4 типа.
        """
        
        print(f"PR_B099 --> START: get_message_type_in_project_space()")


        # фильтруем только картинки
        if type(message.media) == MessageMediaPhoto:
            
            pass
        
            
            
            print(f"PR_B101 --> Message Text: {message.text}")
            
            # pp(group)
            
            # Дифференциация альбомных, группвых фото от сообщения с одной фото
            if message.grouped_id is not None:
                print(f"PR_B105 --> Message Type: TEXT_WITH_ALBUM_IMAGES_MSSG_")
                print(f"PR_B106 --> message.grouped_id: {message.grouped_id}")
                
                
            else: 
                
                print(f"PR_B091 --> Message Type: TEXT_WITH_IMAGE_MSSG_")
                
        
        

        # Если сообщения является документом (аудио-файл, ... не картинка)
        elif type(message.media) == MessageMediaDocument: # документы кроме картинок
            
            print(f"PR_B092 --> Message Type: DOCUMENT_FILE_MSSG_")
            
            print(f"PR_B102 --> Message Text: {message.text}")



        # все остальные - текстовые (но не факт. Так как могут быть еще альбомы и прочие типы. не забываем, если будем ставить этот фильтр)
        # Считывание текстового сообщения, если есть в текущем сообщении канала (без всяких условий if, считая, что у каждого сообщения может быть текст . Но может и отсутствовать)


        # Если есть ссылка на какое-то сообщение, то это скорее всего декларативное сообщение, говорящее о том, что автор загрузил новые тома или том
        elif 'https://' in message.text:
            
            print(f"PR_B093 --> Message Type: TEXT_WITH_LINK_MSSG_")
            print(f"PR_B103 --> Message Text: {message.text}")
        
        else:
            
            print(f"PR_B094 --> Message Type: TEXT_SIMPLE_MSSG_")
            print(f"PR_B104 --> Message Text: {message.text}")
    

        print(f"PR_B100 --> END: get_message_type_in_project_space()")








    
    

if __name__ == '__main__':#
    pass




    # # ПРОРАБОТКА:
    
    # sql = f"""
    #             SELECT mp.id,mp.message_type_ref_id, mp.channels_ref_id FROM {ms.TB_MSSGS_PROCEEDED_} as mp, {ms.TB_MSSGS_PROCEEDED_EXT_} as mpe
    #             WHERE 
    #                 mpe.message_proceeded_ref_id = mp.id 
    #             GROUP BY mp.channels_ref_id
    # """
    
    # print(sql)
    




















    # # I. ###  ППРОРАБОТКА: Отправка mp3 файла в самом простом виде реализации из документации
    # # ~ https://docs.telethon.dev/en/stable/modules/client.html#telethon.client.uploads.UploadMethods.upload_file
    # # ~ https://github.com/LonamiWebs/Telethon/issues/601  !!!
    
    

    # from telethon import TelegramClient
    # from telethon.tl.types import DocumentAttributeVideo
    
    
    
    # fileRoot = '/media/ak/Transcend1/GENERAL_ARCHIVE_EXTERNAL_DISC_FROM_01_02_2024_CURRENT_MAIN/TELEGRAM_AUDIO_LIBRARIES/CHANNEL_ID_1'

    # # fileName = '19. ждем книгу.mp3'
    # # fileName = '3. Эндшпиль.mp3' # > 50Mb
    # fileName = '3. Endshpil.mp3'
    
    # caption = '3. Endshpil'
    
    
    # fileFullPath = f"{fileRoot}/{fileName}"
    
    
    # # Printing upload progress
    # def callback(current, total):
    #     print('Uploaded', current, 'out of', total,
    #         'bytes: {:.2%}'.format(current / total))
        
        
        
    # chat = 'me' # отправляет сообщзение беримору в Сохраненные 
    # # chat = 'А-библиотека: Фантастика'
    # # chat = 'integra_light'
        
    
    # chatId = -1001811098741
    

    # client = TelegramClient('anon', 20460272, '9e6f44844a41f717e5c035cb0add2984')

    # async def main():
    #     # Now you can use all client methods listed below, like for example...
    #     # await client.send_message(chat, 'Hello to myself!')
        
    #     message = await client.send_file(chat, fileFullPath, progress_callback=callback, 
    #                                     caption=caption, attributes=(DocumentAttributeVideo(0, 0, 0),))
        
        
    #     print(f"PR_A603 --> messageData = {message}")

    # with client:
    #     client.loop.run_until_complete(main())










    # # # # # ПРОРАБОТКА: метода отправки файла-документа в свой канал через клиента, используя весь обьект TelegramManager (не через бота) [А-библиотека: Фантастика] с созданием обьекта класса TelegramManager
    # # # ПРИМ: пока выдает ошибку RuntimeWarning: Enable tracemalloc to get the object allocation traceback (это значит где-то с async или await что-то неправильно, исследовать!!!)



    # auth = {
    #     'api_id' : 20460272,
    #     'api_hash' : '9e6f44844a41f717e5c035cb0add2984',
    #     'session_name' : 'anon', # Название файла с сессией (БД sqlite, если нет прочих настроек по формату сесссии. Хранится в рабочей директории, где manage.py)
    #     'bot_token' : '6982698935:AAFQQdz8uApzejMak2ily8azWVKytfIeuNQ', # тоукен своего бота 
    #     'own_bot_chat_id' : -4104980551, # id своего ТГ чата-бота
    # }
    
    # botToken = '6982698935:AAFQQdz8uApzejMak2ily8azWVKytfIeuNQ'
    
    # tm = TelegramManager(auth)


    # fileRoot = '/media/ak/Transcend1/GENERAL_ARCHIVE_EXTERNAL_DISC_FROM_01_02_2024_CURRENT_MAIN/TELEGRAM_AUDIO_LIBRARIES/CHANNEL_ID_1'

    # fileName = '19. ждем книгу.mp3'
    # # fileName = '3. Эндшпиль.mp3' # > 50Mb
    
    
    # fileFullPath = f"{fileRoot}/{fileName}"

    # # Словарь сообщенияclear
    # messageDic = {
        
    #     'message_type' : 'DOCUMENT_FILE_MSSG_', # Тип сообщения
    #     # 'text' : text,
    #     'file' : fileFullPath,
        
    # }
    
    # # id своего чата, куда мы хотим отправить сообщение messageDic
    # ownChatId = -1001811098741


    # dicThrow = {
        
    #     'ownChatId' : -1001811098741,
    #     'messageDic' : messageDic,
        
    # }
    
    
    
    # dFunc = 'send_message_to_own_channel_through_own_bot_tm_self' 


    # tm.client_dynamic_method_execute_telegram_self(dFunc, **dicThrow)
    
    
    
    
    
    
    
    
    
    
    
    
    
    



    # # # # ПРОРАБОТКА: метода отправки файла-документа в свой канал через бот [А-библиотека: Фантастика] с созданием обьекта класса TelegramManager
    # # ПРИМ: бот не позволяет отправлять файлы больше чем 50Мб


    # auth = {
    #     'api_id' : 20460272,
    #     'api_hash' : '9e6f44844a41f717e5c035cb0add2984',
    #     'session_name' : 'anon', # Название файла с сессией (БД sqlite, если нет прочих настроек по формату сесссии. Хранится в рабочей директории, где manage.py)
    #     'bot_token' : '6982698935:AAFQQdz8uApzejMak2ily8azWVKytfIeuNQ', # тоукен своего бота
    #     'own_bot_chat_id' : -4104980551, # id своего ТГ чата-бота
    # }
    
    # botToken = '6982698935:AAFQQdz8uApzejMak2ily8azWVKytfIeuNQ'
    
    # tm = TelegramManager(auth)

    # fileRoot = '/media/ak/Transcend1/GENERAL_ARCHIVE_EXTERNAL_DISC_FROM_01_02_2024_CURRENT_MAIN/TELEGRAM_AUDIO_LIBRARIES/CHANNEL_ID_1'

    # fileName = '19. ждем книгу.mp3'
    # # fileName = '3. Эндшпиль.mp3' # > 50Mb

    
    # fileFullPath = f"{fileRoot}/{fileName}"
    
    # # Словарь сообщенияclear
    # messageDic = {
        
    #     'message_type' : 'DOCUMENT_FILE_MSSG_', # Тип сообщения
    #     # 'text' : text,
    #     'file' : '/media/ak/Transcend1/GENERAL_ARCHIVE_EXTERNAL_DISC_FROM_01_02_2024_CURRENT_MAIN/TELEGRAM_AUDIO_LIBRARIES/CHANNEL_ID_1/3. Эндшпиль.mp3'
        
    # }
    
    # # id своего чата, куда мы хотим отправить сообщение messageDic
    # ownChatId = -1001811098741

    # # tm.send_message_to_own_channel_through_own_bot_tm_self (ownChatId, messageDic)
    
    
    # dicThrow = {
        
    #     'ownChatId' : -1001811098741,
    #     'messageDic' : messageDic,
        
    # }
    
    
    
    # dFunc = 'send_message_to_own_channel_through_own_bot_tm_self' 


    # # tm.client_dynamic_method_execute_telegram_self(dFunc, **dicThrow)


    # bot = telebot.TeleBot(token = auth['bot_token']) 
    

        
    
    # # with open(file, 'rb') as audio:
        

    # bot.send_document(chat_id=ownChatId, document=open(fileFullPath, 'rb'), timeout=300)





    # # ERROR:
    # # raise SSLError(e, request=request)
    # # requests.exceptions.SSLError: HTTPSConnectionPool(host='api.telegram.org', port=443): Max retries exceeded with url: /bot6982698935:AAFQQdz8uApzejMak2ily8azWVKytfIeuNQ/sendDocument?chat_id=-1001811098741 (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:2426)')))

    # import requests 
    
    # with open( fileFullPath, 'rb') as audio:
    #     payload = {
    #         'chat_id': ownChatId,
    #         'title': 'file.mp3',
    #         'parse_mode': 'HTML'
    #     }
    #     files = {
    #         'audio': audio.read(),
    #     }
        



    #     try:
    #         resp = requests.post(
    #             f"https://api.telegram.org/bot{botToken}/sendAudio",
    #             data=payload,
    #             files=files,
    #             timeout=60).json()


    #     except Exception:
    #         pass















    # # # ПРОРАБОТКА: метода отправки сообщения с картинкой  в свой канал [А-библиотека: Фантастика] с созданием обьекта класса TelegramManager

    # auth = {
    #     'api_id' : 20460272,
    #     'api_hash' : '9e6f44844a41f717e5c035cb0add2984',
    #     'session_name' : 'anon', # Название файла с сессией (БД sqlite, если нет прочих настроек по формату сесссии. Хранится в рабочей директории, где manage.py)
    #     'bot_token' : '6982698935:AAFQQdz8uApzejMak2ily8azWVKytfIeuNQ', # тоукен своего бота
    #     'own_bot_chat_id' : -4104980551, # id своего ТГ чата-бота
    # }
    
    # tm = TelegramManager(auth)
    
    # # Текст
    # text = 'Картинка с <b>мишкой!</b>'
    
    # # Картинка
    # img = '/home/ak/Yandex.Disk/Мишки.jpg' 
    
    
    # # Словарь сообщения
    # messageDic = {
        
    #     'message_type' : 'TEXT_WITH_IMAGE_MSSG_', # Тип сообщения
    #     'text' : text,
    #     'image' : img
        
    # }
    
    # # id своего чата, куда мы хотим отправить сообщение messageDic
    # ownChatId = -1001811098741

    # tm.send_message_to_own_channel_through_own_bot_tm_self (ownChatId, messageDic)









    # # ПРОРАБОТКА: Считывание всего массива сообщений с канала 
    
    

    # client = TelegramClient('anon', 20460272, '9e6f44844a41f717e5c035cb0add2984')
        

    # with client:
    #     client.loop.run_until_complete(TelegramManager.test(client))
















    # # # ПРОРАБОТКА:  отправки сообщения в свой ТГ-бот [Test Group 1]  с созданием обьекта класса TelegramManager
    
    # auth = {
    #     'api_id' : 20460272,
    #     'api_hash' : '9e6f44844a41f717e5c035cb0add2984',
    #     'session_name' : 'anon', # Название файла с сессией (БД sqlite, если нет прочих настроек по формату сесссии. Хранится в рабочей директории, где manage.py)
    #     'bot_token' : '6982698935:AAFQQdz8uApzejMak2ily8azWVKytfIeuNQ', # тоукен своего бота
    #     'own_bot_chat_id' : -4104980551, # id своего ТГ чата-бота
    # }
    
    # tm = TelegramManager(auth)

    # # Словарь сообщения
    # messageDic = {
    #     'message' : 'Привет! Это сообщение от бота прямо сейчас!' # Тип сообщения
    # }

    # # Отправить сообщение
    # tm.send_message_to_own_bot_chat_through_own_bot_tm (messageDic)











    # ПРОРАБОКТА: Создание сообщений в собственном канале (взято из проекта PRJ_027 -> bot1.py)   !!!!!!!!!!!
    
    
    # import telebot
    # from telebot import types

    # bot = telebot.TeleBot(token='6982698935:AAFQQdz8uApzejMak2ily8azWVKytfIeuNQ')

    # channel = '@erwernke'


    # Отправить сообщение в бот
    # bot.send_message(-4104980551, 'Hi! Я наш бот!!!')
    
    # Chat ID  бота: -4104980551


    # # Получить всякие ID и пр. В менеджер засунуть
    # import requests
    # TOKEN = "6982698935:AAFQQdz8uApzejMak2ily8azWVKytfIeuNQ"
    # url = f"https://api.telegram.org/bot{6982698935:AAFQQdz8uApzejMak2ily8azWVKytfIeuNQ}/getUpdates"
    # print(requests.get(url).json())


    # # отправить в канал сообщение с картинкой. Сообщение может быть отформатировано , к примеру, по HTML
    # ID чата канала: -1001811098741
    # img = '/home/ak/Yandex.Disk/Мишки.jpg'
    # text = 'Your <b>profile!</b>'

    # markup = types.InlineKeyboardMarkup(row_width=2)

    # bot.send_photo(-1001811098741, photo = open(img, 'rb'), caption=text, reply_markup = markup, parse_mode='html')




    # # ПРОРАБОТКА: пересылка сообщений из канала в канал НЕ РАБОТАЕТ !!!
    # https://stackoverflow.com/questions/71079062/creating-or-using-a-telegram-bot-that-forward-messages-received-from-a-bot-to-an

    # # bot.forward_message(-1001811098741, -1911157001, 4209) # НЕ работает
    
    # # bot.forward_message(-1001811098741, '@akniga', 4209)


    # from telethon import TelegramClient, events
    # import asyncio
    # import logging
    # logging.basicConfig(level=logging.WARNING)

    # api_id = 20460272 # don't forget to fill this 
    # api_hash = '9e6f44844a41f717e5c035cb0add2984' # don't forget to fill this 

    # client = TelegramClient("anon", api_id, api_hash)
    # client.start()


    # from_chat_id = -1911157001 # don't forget to fill this
    # to_chat_id = -1001811098741


    # async def get_chat_id(title):
    #     async for dialog in client.iter_dialogs():        
    #         if dialog.title == title:        
    #             return dialog.id


    # @client.on(events.NewMessage)
    # async def my_event_handler(event):
    #     chat = await event.get_chat()
    #     if chat.id == from_chat_id:
    #         await client.forward_messages(to_chat_id, event.message)

    # # asyncio.get_event_loop().run_until_complete(get_chat_id("Аудиокниги фантастика"))
    # asyncio.get_event_loop().run_forever()





    # api_id = '20460272'
    # api_hash = '9e6f44844a41f717e5c035cb0add2984'
    # session_name = 'anon'
    
    # channelFromName = 'Аудиокниги фантастика'
    
    # bot = telebot.TeleBot(token='6982698935:AAFQQdz8uApzejMak2ily8azWVKytfIeuNQ')
    

    
    # # finally:
    # #     client.disconnect() # Правильно закрыть клиента ~ https://docs.telethon.dev/en/stable/quick-references/faq.html#what-does-task-was-destroyed-but-it-is-pending-mean


    # bot.forward_message(chat_id='@erwernke',
    #                         from_chat_id='@akniga',
    #                         message_id=4209)




















    # ПРОРАБОТКА: Динамическое подключение импорт классов и методов
    
    
    
    # import importlib.util
    
    # dicMessageData = {
    #     'message_id': 4167, 
    #     'proj_path': None, 
    #     'download_path': None, 
    #     'document_file_name': None, 
    #     'image_file_name': None, 
    #     'message_text': 'Антон Б. Спасибо за 500р\nсообщение "Как и обещал на шаурму))"\nВладимир Х. Спасибо за 300р\nсообщение "ᾑD"', 
    #     'curr_calend_date': None, 
    #     'current_unix_date': None, 
    #     'status': None}


    # file_path = '/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django/telegram_monitor/local_classes/audiobooks_channel_telegram_manager.py'
    # module_name = 'AudiobooksChannelTelegramManager'

    # spec = importlib.util.spec_from_file_location(module_name, file_path)
    # module = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(module)

    # # Verify contents of the module:
    # print(dir(module))

    # # testStr  = "[AAAAAA, BBBBBBB,   CCCCCCCC]"

    # cls = getattr(module, 'AudiobooksChannelTelegramManager') # Получаем класс

    # objCls = cls() # Сздаем обьект класса

    # objCls.analyze_parse_and_save_data_in_messages_of_channel_with_ID_01_tg (dicMessageData) # Выполняем метод класса явным образом (но можно и через поиск метода через его название, если неявным образом)









    # # ПРОРАБОТКА: Получение ссылки канала
    # # https://stackoverflow.com/questions/74927571/how-to-get-telegram-chat-invite-link-using-telethon
    
    
    
    # tm = TelegramManager()
    
    # tm.get_chat_links()
    









    # # # ПРОРАБОТКА !!!! : Первая авторизация для создания сессии  со своим Телеграм-каналом
    # # # НЕ УДАЛЯТЬ !!!!
    
    # # from telethon import TelegramClient

    # api_id = 20460272
    # api_hash = '9e6f44844a41f717e5c035cb0add2984'
    # session_name = 'anon'

    # TelegramManager.auth_for_session(session_name, api_id, api_hash)







    # # II. ###  ПРОРАБОТКА: Организовать сЧитку сообщений с канада и !!! получить message.file.id файлов документов или фотографий
    
    # from telethon import TelegramClient

    # api_id = 20460272
    # api_hash = '9e6f44844a41f717e5c035cb0add2984'
    # botToken = "6982698935:AAFQQdz8uApzejMak2ily8azWVKytfIeuNQ"
    
    # chatId = -1001811098741 # Моя библиотека
    
    # # chatName = 'me'
    # chatName = 'А-библиотека: Фантастика'
    # # sessionName = 'anon'
    # sessionName = 'new_test_delete'

    
    

    # # 'anon' - название файла сессии, который появляется в рабочем катологе проекта
    # client = TelegramClient(sessionName, api_id, api_hash)

    # async def main():
    #     async for message in client.iter_messages(chatName):

    #         print(message.id, message.text)
    #         if message.media:
    #             print('File Name :' + str(message.file.name))
    #             # path = await client.download_media(message.media, "youranypathhere") # <<-- file download, NO LIMIT
    #             # print('File saved to', path)  # printed after download is done
                
    #             message.file.name
                
                
    #             print(f"PR_A601 --> message.file_id = {message.file.id}") # message.file_id = BQADAgAD3EIAAqEh-UpvjOwAAdL--_8C
                
    #             # print(f"PR_A604 --> message.file_id = {message.file.id}")

    # with client:
    #     client.loop.run_until_complete(main())

    # # 





    # # # III. ПРОРАБОТКА: Инициализация чата в сессии
    # # ~ https://stackoverflow.com/questions/52351640/get-telegram-channel-messages-after-an-specific-id-with-telethon
    
    # api_id = 20460272
    # api_hash = '9e6f44844a41f717e5c035cb0add2984'
    # botToken = "6982698935:AAFQQdz8uApzejMak2ily8azWVKytfIeuNQ"
    
    # chatId = -1001811098741 # Моя библиотека
    
    # # chatName = 'me'
    # chatName = 'А-библиотека: Фантастика'
    # sessionName = 'anon'
    
    # ph = '+79967534315'

    # from telethon import functions
    

    # # 'anon' - название файла сессии, который появляется в рабочем катологе проекта
    # client = TelegramClient(sessionName, api_id, api_hash)

    # async def main():
    #     async for message in client.iter_messages(chatId):

    #         print(message.id, message.text)
    #         if message.media:
    #             print('File Name :' + str(message.file.name))
    #             # path = await client.download_media(message.media, "youranypathhere") # <<-- file download, NO LIMIT
    #             # print('File saved to', path)  # printed after download is done
                
    #             message.file.name
                
                
    #             print(f"PR_A601 --> message.file_id = {message.file.id}") # message.file_id = BQADAgAD3EIAAqEh-UpvjOwAAdL--_8C
                
    #             # print(f"PR_A604 --> message.file_id = {message.file.id}")
        
    #     pass
    
    #     # bot = TelegramClient(sessionName, api_id, api_hash).start(bot_token=botToken)
    #     # result = await bot(functions.messages.GetMessagesRequest(id=[message_id]))
    #     # message = result.messages[0]
    #     # print(message.text)
        
    

    # with client:
    #     client.loop.run_until_complete(main())

    # # 





    # # ПРоработка получения сообщений из телеграм канала и их форматов и их распечаток из списка
    
    # # tm = TelegramManager()
    
    # # Паарметры телеграм канала собственного
    # api_id = 20460272
    # api_hash = '9e6f44844a41f717e5c035cb0add2984'
    # limit = 3
        
    # mssgs = TelegramManager.get_channel_chats_messages_stat(api_id, api_hash, limit)
    
    # for mssg in mssgs:
    
    #     # Распечатка параметров обьекта message
    #     # print(f"""
    #     #     \nPR_A034 -->\n 
    #     #     \nmssg_id = {mssg.id}\n
    #     #     \nphoto_id = {mssg.media}\n
    #     #     \n{mssg.message}\n
            
    #     #     """)
        
        
    #     # # Распечатка названий картинки
    #     # print(f"""
    #     #     \PR_A036 -->\n 
    #     #     \nmssg_ph_name = {mssg}\n
    #     #     """)
        
        
    #     # # распечатка для обьектов  messages
    #     # print(f"""
    #     #     \PR_A038 -->\n 
    #     #     \message = {mssg}\n
    #     #     """)
        
    
    
    
    #     # Для текста сообщения
    #     print(f"""
    #         \nPR_A039 --> message = 
    #         \n{mssg.message}\n
    #         """)
    
    
    
    
    
    
    
    
    
    
    
    # ПРОВЕРКА: Работа local Bot API Server 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    