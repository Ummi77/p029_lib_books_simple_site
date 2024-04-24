


# from telegram_monitor.local_classes.audiobooks_channel_telegram_manager import TelegramManager

# from telegram_manager import TelegramManager

import sys
sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')
import settings_bdp_main as ms # общие установки для всех модулей


from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup


from noocube.switch import Switch


from noocube.re_manager import ReManager
# import noocube.re_constants as RC


from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup


from noocube.files_manager import FilesManager

from noocube.pandas_manager import PandasManager
from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup
from noocube.sqlite_pandas_processor_speedup import SqlitePandasProcessorSpeedup


from telegram_monitor.local_classes.book_library_funcs import BookLibraryFuncs

from telegram_monitor.local_classes.tg_local_funcs import TgLocalFuncs


import copy



class AudiobooksChannelTelegramManager():
    """ 
    Класс для  работы с каналами Телеграм, содержащими аудио-книги
    """

    def __init__(self):
        

        self.blf = BookLibraryFuncs()
        self.tlf = TgLocalFuncs()
        self.sps = SqliteProcessorSpeedup(ms.DB_CONNECTION) # Обьект класса SqliteProcessorSpeedup
        self.spps = SqlitePandasProcessorSpeedup(ms.DB_CONNECTION) # Обьект класса SqlitePandasProcessorSpeedup



    @staticmethod
    async def analyze_parse_and_save_data_in_messages_of_channel_with_ID_01_tg(dicMessageData, **tgwargs):
        """ 
        AudiobooksChannelTelegramManager
        Аналитическая функция парсинга сообщений разного типа из канала аудиокниг с ID = 1 из таблицы 'tg_channels' и с 
        названием 'Аудиокниги фантастика'
        chDicMessageData - словарь с данными сообщения в определенном формате по ключам
        SET_100 - маркер настроек из settings.ru (НЕ УДАЛЯТЬ)
        """
        
        print(f"PR_A122 --> START: analyze_parse_and_save_data_in_messages_of_channel_with_ID_01_tg()")
        
        sps = SqliteProcessorSpeedup(ms.DB_CONNECTION)
        
        
        # Смысловые
        
        # Присваивание табличное ID канала из таблицы tg_channels
        channel_ref_id = tgwargs['origSourceId'] # Соотвтетсвуют каналу с названием 'Аудиокниги фантастика'

        message_id = dicMessageData['message_id'] # Собственный ID сообщения в данном канале
        
        mssg_status = dicMessageData['status']  # Статус сообщения стринговое
        
        date_reg_calend = dicMessageData['curr_calend_date']  # Календарная дата регистрации в БД, <string>
        
        date_reg_unix = int(dicMessageData['current_unix_date']) # Соотвтетсвующая календарной дате UNIX-дата <int or real>
    
    
        # INI
        # loadImgAnyway = tgwargs['loadImgAnyway'] # Флаг скачивания картинок, несмотря на то, что система обнаруживает, что сообщение с картинкой и описанием уже было обработано
        # loadDocsAnyway = tgwargs['loadDocsAnyway'] # Флаг скачивания документов, несмотря на то, что система обнаруживает, что сообщение с картинкой и описанием, к которым относится этот документ, уже было обработано

        # параметр настройки типа sql-операции для сохраенния данных в БД
        saveDataExecuteType =  tgwargs['saveDataExecuteType']
        
        
        # ДИФФЕРЕНЦИАЦИЯ СООБЩЕНЙИ ПО ТИПУ
        # Разнос сообщений по таблицам и типам зависит от присвоенных значений в переменные: mssg_type_id и tbMssgsMain и mssgType 
        # (пока в стринговом виде типа для переключателя Switch)
    
        # I. Если ячейка словаря 'image_file_name' не пустая, то это значит, что сообщение содержит картинку и возможно описание к ней текстом
        if dicMessageData['image_file_name'] is not None: 
            
            
            
            # Групповое  id сообщения, если есть (либо None,  либо цифра типа message.grouped_id: 13690994442196138)
            messageGroupId = dicMessageData['messages_grouped_id']
            
            
            # Тип соообщения из табл 'tg_message_types' TODO: Переделать не на имя, а на id типа сообщения из таблд. иначе любое изменение будет давать ошибки
            mssgType = 'TEXT_WITH_IMAGE_MSSG_' # Название типа
            mssg_type_id = 1 # id типа
            
            
            print(f"PR_A395 --> SYS LOG: обрабатываемое сообщение из чата ТГ канала классифицировано как 'TEXT_WITH_IMAGE_MSSG_' (Сообщение с картинкой и текстом)")
            
            # N. Получение ID статуса из таблицы 'tg_message_proc_statuses' 
            # O. Присваивание вычесленного типа сообщения по таблице tg_message_types по результатам направления хода программы в этот if
            mssg_status_id = ms.DIC_MESSAGE_STATUSES_CH_ID_01[mssg_status]

            
                    
            # Название основной, характеристической таблицы для проанализированных сообщений данного типа
            tbMssgsMain = 'tg_messages_proceeded'
            


        # II. Если ячейка словаря 'audio_file_name' не пустая, то это значит, что сообщение содержит какой-то документ-файл (скорее всего аудио-том книги)
        elif dicMessageData['document_file_name'] is not None: 
            
            
            # Групповое  id сообщения, если есть (либо None,  либо цифра типа message.grouped_id: 13690994442196138)
            messageGroupId = dicMessageData['messages_grouped_id']
            

            print(f"PR_A396 --> SYS LOG: обрабатываемое сообщение из чата ТГ канала классифицировано как 'DOCUMENT_FILE_MSSG_' (Сообщение с файлом-документом)")

            
            # N. Получение ID статуса из таблицы 'tg_message_proc_statuses' 
            mssg_status_id = ms.DIC_MESSAGE_STATUSES_CH_ID_01[mssg_status]
                


            # S. АНАЛИЗ расширения файла скаченного документа !!! 
            
            print(f"PR_B222 --> document_file_name = {dicMessageData['document_file_name']}")
            
            fExt = FilesManager.get_file_extension_from_file_path_fm (dicMessageData['document_file_name'])
            
            print(f"PR_B223 --> fExt = {fExt}")
            
            # Если расширение скачанного файла документа разрешено в качестве аудио-формата из списка  ms.AUDIO_VOLUMES_ALLOWED_EXTS, тогда файл 
            # допускается для дальнейшей регистрации в табл 'tg_messages_proceeded' для книг и их томов. Иначе сообщение регестрируется в 
            # табл 'tg_auxilary_messages_proceeded' как не нужное
            
            # Регистрация как соотвтетсвующего аудио-тому книги документа в табл 'tg_messages_proceeded'. Регистрация определяется таблицей и типом
            if fExt in ms.AUDIO_VOLUMES_ALLOWED_EXTS:
                
                mssgType = 'DOCUMENT_FILE_MSSG_' # Название типа
                
                # Присваивание вычесленного типа сообщения 'DOCUMENT_FILE_MSSG_' по таблице tg_message_types 
                mssg_type_id = 2 

                # Название таблицы для регистрации проанализированных сообщений данного типа
                tbMssgsMain = 'tg_messages_proceeded'
            
            # Регистрация как ненужное сообщение в табл 'tg_auxilary_messages_proceeded'
            else:
                
                mssgType = 'DOCUMENT_FILE_MSSG_WRONG_EXT' # Название типа
                
                # Присваивание вычесленного типа сообщения 'DOCUMENT_FILE_MSSG_WRONG_EXT' по таблице tg_message_types 
                mssg_type_id = 7 

                # Название таблицы для регистрации проанализированных сообщений данного типа
                tbMssgsMain = 'tg_auxilary_messages_proceeded'
                
                

            

            
            
        # Оставшиеся сообщения - либо просто информационные, либо декларативные (последние указывают на то, что автором были загружены новые аудио-тома существующих книг с ссылкой на эти книги)
        
        # iii. Вычленение декларативного информационного сообщения     
        elif 'https://' in dicMessageData['message_text']: # Если есть ссылка на какое-то сообщение, то это скорее всего декларативное сообщение, говорящее о том, что автор загрузил новые тома или том



            # Анализ ссылки. Ссылка может быть декларативной и информационной. От этого зависит тип сообщения
            message_text = dicMessageData['message_text']
            
            # URL в декларативном вспомогательном нформационном сообщении
            url_in_message = ReManager.find_url_in_string(message_text)
            print(f"PR_A590 --> SYS LOG: URL в сообщении : {url_in_message}")
            
            # ID сообщения, который был изменен автором (скорее всего - добавлен ожидаемый том или тома кники, расположенной по этому ID), 
            # вычленяемого из ссылки на сообщение, в котором произведены, возможно, изменения (а именно - добалвен ожидаемый аудио-том книги исключительно в данном канале)
            # В другом канале скорее всего будет совершенно другой парсинг всего и поэтому надо данный алгоритм анализа ввести в зависимость от заданного канала (кассетный подход)                
            parts = url_in_message.split('/')
            
            print(f"PR_A591 --> parts = {parts}")
            
            lastLinkSection = parts[-1].strip(' ()') # очищаем от ошибочных символов. которые встречаются в практике
            

            # Проверить последний сегмент ссылки. Если чисто цифра, то ВОЗМОЖНО (но не факт) - это декларативная ссылка
            # Иначе - Точно не декларативная, а значит информационная ссылка
            if lastLinkSection.isdigit() and len(lastLinkSection) > 3 and len(lastLinkSection) < 6: 
                pass
                print(f"PR_A592 --> SYS LOG: Ссылка {url_in_message} в сообщении с очень большой вероятностью является декларативной")
            
                mssgType = 'TEXT_WITH_LINK_MSSG_'
                
                print(f"PR_A397 --> SYS LOG: обрабатываемое сообщение из чата ТГ канала классифицировано как 'TEXT_WITH_LINK_MSSG_' (Деларативное текстовое сообщение,  с ссылкой  https в тексте)")

                
                mssg_status_id = 'NULL'
                
                # O. Присваивание вычесленного типа сообщения по таблице tg_message_types
                mssg_type_id = 3 # 'TEXT_WITH_LINK_MSSG_'
                
                # Название основной, характеристической таблицы для проанализированных сообщений
                tbMssgsMain= 'tg_auxilary_messages_proceeded'
                
                
            
            
            else:
                print(f"PR_A593 --> SYS LOG: Ссылка {url_in_message} в сообщении НЕ является декларативной. Это информационная ссылка")

                mssgType = 'TEXT_SIMPLE_MSSG_'
                
                print(f"PR_A594 --> SYS LOG: обрабатываемое сообщение из чата ТГ канала классифицировано как 'TEXT_SIMPLE_MSSG_' (Обычное текстовое сообщение)")

                
                mssg_status_id = 'NULL'
                
                # O. Присваивание вычесленного типа сообщения по таблице tg_message_types
                mssg_type_id = 4 # 'TEXT_SIMPLE_MSSG_'
                
                # Название основной, характеристической таблицы для проанализированных сообщений
                tbMssgsMain = 'tg_auxilary_messages_proceeded'



            
        
        # iv. ОСтавшиеся информационные сообщения, которые, как выходит, остаются только просто информативными и которые нам ничего не дают и не являются декларативными
        else:
            
            mssgType = 'TEXT_SIMPLE_MSSG_'
            
            print(f"PR_A398 --> SYS LOG: обрабатываемое сообщение из чата ТГ канала классифицировано как 'TEXT_SIMPLE_MSSG_' (Обычное текстовое сообщение)")

            
            mssg_status_id = 'NULL'
            
            # O. Присваивание вычесленного типа сообщения по таблице tg_message_types
            mssg_type_id = 4 # 'TEXT_SIMPLE_MSSG_'
            
            # Название основной, характеристической таблицы для проанализированных сообщений
            tbMssgsMain = 'tg_auxilary_messages_proceeded'
        
        # INI
        # Параметр с id маркера текущей вытяжки из табл 'tg_samples_markers'. Этот id появляется перед циклом вытяжки сообщений по заданной сэмплу сообщений
        # Перед циклом: async for message in client.iter_messages(channeChatName, **msgKwargs): [в модуле telegram_manager.py ]
        currSampleId = tgwargs['currSampleId']

        # B. 
        # Внести в БД данные по обработанному сообщению данного сектора анализатора данных обработканных сообщений
        sql = f"""
                    INSERT INTO {tbMssgsMain} 
                    (message_own_id, message_proc_status_ref_id, message_type_ref_id, channels_ref_id, date_reg_calend, date_reg_unix, tg_sample_id) 
                    VALUES ({message_id}, {mssg_status_id}, {mssg_type_id}, {channel_ref_id}, '{date_reg_calend}', {date_reg_unix}, {currSampleId})
        """ 
        
        # Запрос на UPDATE, если флаги загрузок loadImgAnyway или loadDocsAnyway = True (то есть приказывающие загрузить или обновить с загрузкой, 
        # если уже была регистрация сообщения, но без загрузки)
        # ПРИМ: В данном случае пока меняем только статус, который после успешной загрузки картинки или документа станет другим (??? ПРОВЕРИТЬ ВСЕ)
        sqlUpdate = f"""UPDATE {tbMssgsMain}  SET 
                        message_proc_status_ref_id =  {mssg_status_id} 
                        WHERE message_own_id = {message_id}
                    """
        
        # print(f"PR_A155 --> sql = {sql}")
        # print(f"PR_A321 --> sqlUpdate = {sqlUpdate}")
        
        # Выполнение SQL-запроса для вставки данных в главные таблицы обработанных сообщений (без расширений _ext)
        # SQL EXECUTE: 
        
        inserttedFlag = False # Флаг успешной реализации INSERT  запроса
        
        try: 
            
            # C. Анализ параметра настройки типа выполнения sql запроса на сохранение данных после загрузки сообщения
            if '_INSERT_' in saveDataExecuteType: # Для вставки новых данных
            
                print(f"PR_A349 --> START EXECUTE SQL _INSERT_")
                sps.execute_sql_SPS(sql)
                print(f"""PR_A320 --> SYS SQL LOG: В таблицы 'tg_messages_proceeded' или 'tg_auxilary_messages_proceeded' внесена запись по sql-запросу:\n
                    sql = {sql}""")
                inserttedFlag = True # Флаг создания новой записи в таблице
                updateSuccessFlag = False # Флаг успешного апдейта
                
                idTbUpdated = -1 # id  для sql - update. если не update. то = -1
                
            elif '_UPDATE_' in saveDataExecuteType: # Для обновления уже существующих данных по записи
                
                pass
                print(f"PR_A882 --> START EXECUTE SQL _UPDATE_")
                sps.execute_sql_SPS(sqlUpdate)
                
                print(f"""PR_A883 --> SYS SQL LOG: В таблицах 'tg_messages_proceeded' или 'tg_auxilary_messages_proceeded' внесена изменения в существующих записях  по sql-запросу:\n
                    sql = {sqlUpdate}""")
            
                inserttedFlag = False # Флаг создания новой записи в таблице
                
                # D. Получить табличное id записи , в которой проведен UPDATE в текущей табл tbMssgsMain 
                # (их может быть 2 варианта, см.выше) : tg_messages_proceeded или tg_auxilary_messages_proceeded. Но структура у них единая
                
                sql_ = f"SELECT id FROM {tbMssgsMain} WHERE message_own_id = {message_id}"
                idTbUpdated = sps.get_result_from_sql_exec_proc_sps(sql_)[0]
                
                
                updateSuccessFlag = True # Флаг успешного апдейта
                
        except Exception as err:
            print(f"""PR_A394 --> SYS SQL LOG: SQL EXEUTION ERROR!!! {err}""")
            print(f"""PR_A120 --> SYS SQL LOG: SQL EXEUTION ERROR!!! Возможно, запись противоречит запрету по уникальному индексу колонки в таблицах 'tg_messages_proceeded' или 'tg_auxilary_messages_proceeded'\n
                sqlError = {sql}""")
            
            inserttedFlag = False # Флаг создания новой записи в таблице
            updateSuccessFlag = False # Флаг успешного апдейта
            
            # Пока не удалять !!!
            # # Исполняем запрос на UPDATE, если флаги загрузок loadImgAnyway или loadDocsAnyway = True (то есть приказывающие загрузить или обновить с загрузкой, 
            # # если уже была регистрация сообщения, но без загрузки)
            # if loadImgAnyway or loadDocsAnyway:
            #     try:
            #         sps.execute_sql_SPS(sqlUpdate)
                    
            #         print(f"PR_A322 --> SYS LOG: sqlUpdate реализован успешно:\n sqlUpdate = {sqlUpdate}")
                    
            #     except:
            #         pass
            #         print(f"PR_A323 --> SYS LOG: sqlUpdate ERROR!!!!\n sqlUpdateError = {sqlUpdate}")
                    
        print(f"PR_A892 --> updateSuccessFlag = {updateSuccessFlag}")
                    
        if inserttedFlag or updateSuccessFlag: # Если предыдущий запрос INSERT прошел успешно или операция UPDATE выполнена
            
            
            # Если была операция INSERT. то нужно получить последний id автоинкремента таблицы
            if inserttedFlag:
            
                # Получить последний ID в таблице tg_messages_proceeded (что бы иметь этот ключ для созданя записи в расширении этой таблицы в tg_message_proceeded_ext)
                print(f"PR_A401 --> START SELECT SQL")

                # # Для SQLite НЕ УДАЛЯТЬ
                # sql = f"SELECT rowid from {tbMssgsMain} order by ROWID DESC limit 1"
                
                # Для MySQL
                sql = f"SELECT LAST_INSERT_ID()"

                res = sps.get_result_from_sql_exec_proc_sps(sql)
                tgmpLastId = res[0] # Последний ID в таблице tg_messages_proceeded (tgmp)
                print(f"PR_A116 --> Последний row_id или lastId = {tgmpLastId}")
            
            else:
                tgmpLastId = -1
            
            # TODO: Изменить переключатель. Сделать дифференциацию не по имени, а по  id  типа (что бы не зависело от изменении названия типа)    
            # R. Внести или изменить конкретные данные в таблице - РАСШИРЕНИЕ tg_message_proceeded_ext или в tg_auxilary_message_proceeded_ext, 
            # после первичной обработки сообщения
            for case in Switch(mssgType):
                
                
                if case('TEXT_WITH_IMAGE_MSSG_'): 

                    print(f"PR_A339 --> DEBUG LOG: mssgType = TEXT_WITH_IMAGE_MSSG_")

                    
                    # Смысловая инициализация переменных из возвращенного словаря с данными по обработке сообщения
                    message_proceeded_ref_id = tgmpLastId
                    message_text = dicMessageData['message_text']
                    message_img_loded_path = dicMessageData['download_path']
                    message_img_name = dicMessageData['image_file_name']
                    
                    sql = f"""
                                INSERT INTO {ms.TB_TG_MESSAGE_PROCEEDED_EXT}
                                (message_proceeded_ref_id, message_text, message_img_loded_path, message_img_name, messages_grouped_id, channels_ref_id_ext, message_own_id_ext) 
                                VALUES ({message_proceeded_ref_id}, '{message_text}', '{message_img_loded_path}', '{message_img_name}', {messageGroupId}, {channel_ref_id}, {message_id})
                    """
                    
                    sqlUpdate = f""" 
                            UPDATE {ms.TB_TG_MESSAGE_PROCEEDED_EXT} SET 
                            message_text = '{message_text}', message_img_loded_path = '{message_img_loded_path}', message_img_name = '{message_img_name}', 
                            messages_grouped_id = {messageGroupId},  channels_ref_id_ext = {channel_ref_id}, message_own_id_ext = {message_id}
                            WHERE message_proceeded_ref_id = {idTbUpdated}
                    """
                    
                    print(f"PR_A893 -->  sqlupdate = {sqlUpdate}")
                    
                    # # SQL EXECUTE: 
                    # try: 
                    #     sps.execute_sql_SPS(sql)
                    # except:
                    #     print(f"PR_A117 --> SQL EXEUTION ERROR!!! Возможно, запись противоречит запрету по уникальному индексу колонки в таблице")
                        
                        
                    
                    
                    break
                
                
                if case('DOCUMENT_FILE_MSSG_'): 
                    
                    print(f"PR_A352 --> DEBUG LOG: mssgType = DOCUMENT_FILE_MSSG_")

                    
                            
                    # Смысловая инициализация переменных из возвращенного словаря с данными по обработке сообщения с типом 'DOCUMENT_FILE_MSSG_'
                    message_proceeded_ref_id = tgmpLastId
                    # message_text = dicMessageData['message_text']
                    message_document_loded_path = dicMessageData['download_path']
                    message_document_name = dicMessageData['document_file_name']
                    message_document_size = int(dicMessageData['document_file_size'])
                    
                    sql = f"""
                                INSERT INTO {ms.TB_TG_MESSAGE_PROCEEDED_EXT} 
                                (message_proceeded_ref_id, message_document_loded_path, message_document_name, message_document_size, messages_grouped_id, channels_ref_id_ext, message_own_id_ext) 
                                VALUES ({message_proceeded_ref_id}, '{message_document_loded_path}', '{message_document_name}', {message_document_size}, {messageGroupId}, {channel_ref_id}, {message_id})
                    """
                    
                    sqlUpdate = f""" 
                            UPDATE {ms.TB_TG_MESSAGE_PROCEEDED_EXT} SET 
                            message_document_loded_path = '{message_document_loded_path}', message_document_name = '{message_document_name}', message_document_size = '{message_document_size}', 
                            messages_grouped_id = {messageGroupId}, channels_ref_id_ext = {channel_ref_id}, message_own_id_ext = {message_id}
                            WHERE message_proceeded_ref_id = {idTbUpdated}
                    """
                    
                    
                    print(f"PR_A156 --> sql = {sql}")
                    
                    # # SQL EXECUTE: 
                    # try: 
                    #     sps.execute_sql_SPS(sql)
                    # except:
                    #     print(f"PR_A142 --> SQL EXEUTION ERROR!!! Возможно, запись противоречит запрету по уникальному индексу колонки в таблице")
                        

                    break
                
                
                if case('TEXT_WITH_LINK_MSSG_'): 
                    
                    
                    print(f"PR_A353 --> DEBUG LOG: mssgType = TEXT_WITH_LINK_MSSG_")

                    
                    # Смысловая инициализация переменных из возвращенного словаря с данными по обработке сообщения
                    auxilaty_message_proceeded_ref_id = tgmpLastId
                    message_text = dicMessageData['message_text']
                            
                    # URL в декларативном вспомогательном нформационном сообщении
                    url_in_message = ReManager.find_url_in_string(message_text)
                    print(f"PR_A112 --> SYS LOG: URL в декларативном сообщении : {url_in_message}")
                    
                    # ID сообщения, который был изменен автором (скорее всего - добавлен ожидаемый том или тома кники, расположенной по этому ID), 
                    # вычленяемого из ссылки на сообщение, в котором произведены, возможно, изменения (а именно - добалвен ожидаемый аудио-том книги исключительно в данном канале)
                    # В другом канале скорее всего будет совершенно другой парсинг всего и поэтому надо данный алгоритм анализа ввести в зависимость от заданного канала (кассетный подход)                
                    parts = url_in_message.split('/')
                    
                    print(f"PR_A355 --> parts = {parts}")
                    
                    parentMessageId = parts[-1].strip(' ()') # очищаем от ошибочных символов. которые встречаются в практике
                    
                    
                    # D. Ссылка может содержать в конце номер сообщения - тогда это декларативное сообщение, как-то связанное с предыдущимы сообщениями
                    # Если ссылка не содержит номера в конце, то это не декларативное сообщение, а просто инфоративная ссылка и сообщение нужно записывать в обычное сообщение
                    
                    
                    parentMessageId = int(parentMessageId)
                    print(f"PR_A114 --> parentMessageId = {parentMessageId}\n")
                            
                    sql = f"""
                                INSERT INTO {ms.TB_TG_AUXILARY_MSSGS_PROCEEDED_EXT_} 
                                (auxilary_message_proceeded_ref_id, message_text, url_in_message, parent_id_in_url) 
                                VALUES ({auxilaty_message_proceeded_ref_id}, '{message_text}', '{url_in_message}', {parentMessageId} )
                    """
                    
                    
                    sqlUpdate = f""" 
                            UPDATE {ms.TB_TG_AUXILARY_MSSGS_PROCEEDED_EXT_} SET 
                            message_text = '{message_text}', url_in_message = '{url_in_message}', parent_id_in_url = '{parentMessageId}'
                            WHERE auxilary_message_proceeded_ref_id = {idTbUpdated}
                    """
                    
                    
                    break
                
                
                if case('TEXT_SIMPLE_MSSG_'): 
                    pass
                if case('DOCUMENT_FILE_MSSG_WRONG_EXT'): 
                    
                    print(f"PR_A354 --> DEBUG LOG: mssgType = TEXT_SIMPLE_MSSG_")

                    
                    # Смысловая инициализация переменных из возвращенного словаря с данными по обработке сообщения
                    auxilaty_message_proceeded_ref_id = tgmpLastId
                    message_text = dicMessageData['message_text']
                    
                    sql = f"""
                                INSERT INTO {ms.TB_TG_AUXILARY_MSSGS_PROCEEDED_EXT_} 
                                (auxilary_message_proceeded_ref_id, message_text) 
                                VALUES ({auxilaty_message_proceeded_ref_id}, '{message_text}')
                    """
                    
                    
                    print(f"PR_A894 -->  sql = {sql}")
                    
                    
                    sqlUpdate = f""" 
                            UPDATE {ms.TB_TG_AUXILARY_MSSGS_PROCEEDED_EXT_} SET 
                            message_text = '{message_text}' 
                            WHERE auxilary_message_proceeded_ref_id = {idTbUpdated}
                    """
                    
                    print(f"PR_A895 -->  sqlUpdate = {sqlUpdate}")
                    
                    break
                
                
                if case(): # default
                    print('Другое число')
                    break
                
                
            print(f"PR_A891 --> saveDataExecuteType = {saveDataExecuteType}")
                
                
            # SQL EXECUTE: 
            try: 
                
                # C. Анализ параметра настройки типа выполнения sql запроса на сохранение данных после загрузки сообщения
                if '_INSERT_' in saveDataExecuteType: # Для вставки новых данных
                    
                    print(f"PR_A350 --> START EXECUTE SQL")
                    sps.execute_sql_SPS(sql)
                    print(f"""PR_A319 --> SYS SQL LOG: В таблицы расширений 'tg_message_proceeded_ext' или 'tg_auxilary_messages_proceeded_ext' внесена запись по sql-запрос:\n sql = {sql}""")
                        
                elif '_UPDATE_' in saveDataExecuteType: # Для обновления уже существующих данных по записи
                    
                    print(f"PR_A884 --> START EXECUTE SQL _UPDATE_")
                    sps.execute_sql_SPS(sqlUpdate)
                    
                    print(f"""PR_A885 --> SYS SQL LOG: В таблицах 'tg_messages_proceeded' или 'tg_auxilary_messages_proceeded' внесена изменения в существующих записях  по sql-запросу:\n
                        sql = {sqlUpdate}""")
                                
                        
                        
            except Exception as err:
                print(f"""PR_A121 --> SYS SQL LOG: SQL EXEUTION ERROR!!! Возможно, запись противоречит запрету по уникальному индексу колонки в таблицах 'tg_message_proceeded_ext' или 'tg_auxilary_messages_proceeded_ext'\n 
                    sqlError = {sql}""")
                print(f"PR_A351 --> ERROR: {err}")
                
                # # Исполняем запрос на UPDATE, если флаги загрузок loadDocsAnyway = True (то есть приказывающие загрузить или обновить с загрузкой, 
                # # если уже была регистрация сообщения, но без загрузки)
                # if loadImgAnyway or loadDocsAnyway:
                #     try:
                #         sps.execute_sql_SPS(sqlUpdate)
                        
                #         print(f"PR_A324 --> SYS LOG: sqlUpdate реализован успешно:\n sqlUpdate = {sqlUpdate}")
                        
                #     except:
                #         pass
                #         print(f"PR_A325 --> SYS LOG: sqlUpdate ERROR!!!!\n sqlUpdateError = {sqlUpdate}")
                
                

        print(f"PR_A123 --> END: analyze_parse_and_save_data_in_messages_of_channel_with_ID_01_tg()")








    @staticmethod
    def get_lists_of_messages_ids_differenciated_by_type_and_status_from_proceeded_main_tables_for_channel_id_01_actgm (**tgwargs):
        """ 
        AudiobooksChannelTelegramManager
        Суффикс actgm - AudiobooksChannelTelegramManager
        
        Считать из характеристических или основных таблиц с корнем '...proceeded...' списки message_own)_ids по всем типам сообщений и их статусов.
        Дифференциейтед по типу и статусу (6 списков наданный момент)
        Специфический: Считать из таблиц, связанных с канадом с ID=1, в которые занесены данные сообщений из канала с ID = 1 из таблицы 'tg_channels'
        """
        
        # INI
        # табличное id источника (ТГ-канала) в  табл 'lib_orig_sources' ( должен быть динамическим)
        origSourceId = tgwargs['origSourceId']
        
        dicRes = {} # словарь для результата по спискам дифференцированных данных по статусц обработанных сообщений

        sps = SqliteProcessorSpeedup(ms.DB_CONNECTION)

        #   'IMAGE_DOWNLOADED_' (загруженные успешно сообщения с картинками, имеющие статус status_type_id = 1) , 
        sql = f'SELECT message_own_id FROM {ms.TB_MSSGS_PROCEEDED_}  WHERE message_type_ref_id=1 AND message_proc_status_ref_id=1 AND channels_ref_id = {origSourceId}'
        listMssgsTextImgsTypeLoadedFull = sps.get_result_from_sql_exec_proc_sps(sql) # Список ID-сообщений типа текст-картинка загруженные полностью
        # Если  res = -1, то это значит, что в списке нет значений и он должен быть равен просто []
        if isinstance(listMssgsTextImgsTypeLoadedFull, int):
            listMssgsTextImgsTypeLoadedFull = []
        # print(f"PR_A128 --> 'IMAGE_DOWNLOADED_' type messages procceded in channel: listMssgsTextImgsTypeLoadedFull = {listMssgsTextImgsTypeLoadedFull}")
        dicRes['IMAGE_DOWNLOADED_'] = listMssgsTextImgsTypeLoadedFull 
        
        #   'IMAGE_DOWNLOADING_PROHIBITED_BY_FLAG_' (загружены текстовые сообщения типа  'мообщения с картинками', но картинки не скачаны, так как флагом было запрещено, имеющие статус status_type_id = 3)
        sql = f'SELECT message_own_id FROM {ms.TB_MSSGS_PROCEEDED_} WHERE message_type_ref_id=1 AND message_proc_status_ref_id=3 AND channels_ref_id = {origSourceId}'
        listMssgsTextImgsTypeFobidenDownloadIds = sps.get_result_from_sql_exec_proc_sps(sql) # Список ID-сообщений типа текст-картинка : загружены текстовые сообщения, но запрещена загрузка картинок из сообщения
        # Если  res = -1, то это значит, что в списке нет значений и он должен быть равен просто []
        if isinstance(listMssgsTextImgsTypeFobidenDownloadIds, int):
            listMssgsTextImgsTypeFobidenDownloadIds = []
        # print(f"PR_A129 --> 'IMAGE_DOWNLOADING_PROHIBITED_BY_FLAG_' type messages procceded in channel: listMssgsTextImgsTypeFobidenDownloadIds = {listMssgsTextImgsTypeFobidenDownloadIds}")
        dicRes['IMAGE_DOWNLOADING_PROHIBITED_BY_FLAG_'] = listMssgsTextImgsTypeFobidenDownloadIds
        
        
        # и 'IMAGE_DOWNLOADING_ERROR_' (Произошла какая-то ошибка при загрузке сообщений типа текст-картинки, имеющие статус status_type_id = 2)
        sql = f'SELECT message_own_id FROM {ms.TB_MSSGS_PROCEEDED_} WHERE message_type_ref_id=1 AND message_proc_status_ref_id=2 AND channels_ref_id = {origSourceId}'
        listMssgsTextImgsTypeErrorDownloadIds = sps.get_result_from_sql_exec_proc_sps(sql) # Список ID-сообщений типа текст-картинка : загружены текстовые сообщения, но запрещена загрузка картинок из сообщения
        # Если  res = -1, то это значит, что в списке нет значений и он должен быть равен просто []
        if isinstance(listMssgsTextImgsTypeErrorDownloadIds, int):
            listMssgsTextImgsTypeErrorDownloadIds = []
        # print(f"PR_A130 --> 'IMAGE_DOWNLOADING_ERROR_' type messages procceded in channel: listMssgsTextImgsTypeErrorDownloadIds = {listMssgsTextImgsTypeErrorDownloadIds}")
        dicRes['IMAGE_DOWNLOADING_ERROR_'] = listMssgsTextImgsTypeErrorDownloadIds
        
        
        
        
        # для сообщений - документов типа 'DOCUMENT_FILE_MSSG_' (type_message_id = 2): 
        # 'DOCUMENT_DOWNLOADED_' (документ-файл загружен успешно, имеющие статус status_type_id = 4) 
        sql = f'SELECT message_own_id FROM {ms.TB_MSSGS_PROCEEDED_} WHERE message_type_ref_id=2 AND message_proc_status_ref_id=4 AND channels_ref_id = {origSourceId}'
        listMssgsDocumentTypeDownloadFullIds = sps.get_result_from_sql_exec_proc_sps(sql) # Список ID-сообщений типа текст-картинка : загружены текстовые сообщения, но запрещена загрузка картинок из сообщения
        # Если  res = -1, то это значит, что в списке нет значений и он должен быть равен просто []
        if isinstance(listMssgsDocumentTypeDownloadFullIds, int):
            listMssgsDocumentTypeDownloadFullIds = []
        # print(f"PR_A131 --> 'DOCUMENT_DOWNLOADED_' type messages procceded in channel: listMssgsDocumentTypeDownloadFullIds = {listMssgsDocumentTypeDownloadFullIds}")
        dicRes['DOCUMENT_DOWNLOADED_'] = listMssgsDocumentTypeDownloadFullIds


        
        # 'DOCUMENT_DOWNLOADING_PROHIBITED_BY_FLAG_' (загрузка файла-документа была запрещена флагом загрузки доекментов-файлов, имеющие статус status_type_id = 6)
        sql = f'SELECT message_own_id FROM {ms.TB_MSSGS_PROCEEDED_} WHERE message_type_ref_id=2 AND message_proc_status_ref_id=6 AND channels_ref_id = {origSourceId}'
        listMssgsDocumentTypeFobidenDownloadIds = sps.get_result_from_sql_exec_proc_sps(sql) # Список ID-сообщений типа текст-картинка : загружены текстовые сообщения, но запрещена загрузка картинок из сообщения
        # Если  res = -1, то это значит, что в списке нет значений и он должен быть равен просто []
        if isinstance(listMssgsDocumentTypeFobidenDownloadIds, int):
            listMssgsDocumentTypeFobidenDownloadIds = []
        # print(f"PR_A132 --> 'DOCUMENT_DOWNLOADING_PROHIBITED_BY_FLAG_' type messages procceded in channel: listMssgsDocumentTypeFobidenDownloadIds = {listMssgsDocumentTypeFobidenDownloadIds}")
        dicRes['DOCUMENT_DOWNLOADING_PROHIBITED_BY_FLAG_'] = listMssgsDocumentTypeFobidenDownloadIds





        # и 'DOCUMENT_DOWNLOADING_ERROR_' (Произошла какая-то ошибка при загрузке документов-файлов, имеющие статус status_type_id = 5)
        sql = f'SELECT message_own_id FROM {ms.TB_MSSGS_PROCEEDED_} WHERE message_type_ref_id=2 AND message_proc_status_ref_id=5 AND channels_ref_id = {origSourceId}'
        listMssgsDocumentTypeErrorDownloadIds = sps.get_result_from_sql_exec_proc_sps(sql) # Список ID-сообщений типа текст-картинка : загружены текстовые сообщения, но запрещена загрузка картинок из сообщения
        # Если  res = -1, то это значит, что в списке нет значений и он должен быть равен просто []
        if isinstance(listMssgsDocumentTypeErrorDownloadIds, int):
            listMssgsDocumentTypeErrorDownloadIds = []
        # print(f"PR_A133 --> 'DOCUMENT_DOWNLOADING_ERROR_' type messages procceded in channel: listMssgsDocumentTypeErrorDownloadIds = {listMssgsDocumentTypeErrorDownloadIds}")

        dicRes['DOCUMENT_DOWNLOADING_ERROR_'] = listMssgsDocumentTypeErrorDownloadIds
        
        
        
        # Список всех ID обычных и декларативных сообщений, зарегестрированных в табл 'tg_auxilary_messages_proceeded'
        sql = f'SELECT message_own_id FROM {ms.TB_AUXILARY_MSSGS_PROCEEDED_} WHERE channels_ref_id = {origSourceId}'
        listMssgsSimpleAndDeclarativeDownloadIds = sps.get_result_from_sql_exec_proc_sps(sql) # Список ID-сообщений типа текст-картинка : загружены текстовые сообщения, но запрещена загрузка картинок из сообщения

        # Если  res = -1, то это значит, что в списке нет значений и он должен быть равен просто []
        if isinstance(listMssgsSimpleAndDeclarativeDownloadIds, int):
            listMssgsSimpleAndDeclarativeDownloadIds = []
            
        dicRes['DECLARATIVE_AND_SIMPLE_'] = listMssgsSimpleAndDeclarativeDownloadIds
        
        
        
        
        return dicRes






    @staticmethod
    def get_lists_of_rejecting_messages_actgm (messageOrigSourceId):
        """ 
        AudiobooksChannelTelegramManager
        Проанализировать и создать списки отсечения по разным аспектам
        Это могут быть типы сообщений, которые не подлежат обработке, или сообщения, которые уже сыграли свою роль и на их базе уже 
        образованые необходимые сущности, либо сообщения, которые уже были успешно скаченны в БД , и т.д.
        
        messageOrigSourceId - В зависимости от источника сообщений нужно выдать списки осечений. Это базируется на том, что общим сквозным ключем
        по всем сущностям, базирующимся на их образующих оригинальных сообщений, является ключ UNIQUE (origSourceId, messageId)
        Поэтому для правильного отсечения сообщений списки должны быть в разрезе именно их origSourceId. Ids сообщений из других
        источников нас не интересует и они, даже, могут совпадать с анализируемым messageId, но при этом этот фактор не имеет значения, так 
        как общий сувозной ключ состоит из двух значений: origSourceId, messageId
        
        RET: Возвращает словарь с ключами : 
        
            IMAGE_DOWNLOADED_ - успешно скачанные сообщения типа PHOTO  с описание книги
            IMAGE_DOWNLOADING_PROHIBITED_BY_FLAG_ - сообщения, скачанные в рамках дебагинга и не имеющих реальных физически скачанных обьектов типа PHOTO  
                                                    с описание книги (описание считывается, а картинка - нет)
            
            IMAGE_DOWNLOADING_ERROR_ - сообщения с картинкой и описанием книги, скачанные с ошибкой и поэтому не являющимися действенынми
            
            DOCUMENT_DOWNLOADED_ - успешно скачанные сообщения типа аудио-файла  или аудио-тома книги
            
            DOCUMENT_DOWNLOADING_PROHIBITED_BY_FLAG_ - сообщения, скачанные в рамках дебагинга, но реально не скачивающих аудио-файла и поэтому
                                                не являющимися действенынми
                                                
            DOCUMENT_DOWNLOADING_ERROR_ - сообщения типа аудио-файл, скачанных с ошибкой
            
            DECLARATIVE_AND_SIMPLE_ - сообщения, которые по типу не являются ни описанием книги с картинкой, ни аудио-файлом представляющим аудио-том книги
            
            
        """
        
        # INI
        # табличное id источника (ТГ-канала) в  табл 'lib_orig_sources' ( должен быть динамическим)
        # origSourceId = tgwargs['origSourceId']
        
        dicRes = {} # словарь для результата по спискам дифференцированных данных по статусц обработанных сообщений

        sps = SqliteProcessorSpeedup(ms.DB_CONNECTION)

        #   'IMAGE_DOWNLOADED_' (загруженные успешно сообщения с картинками, имеющие статус status_type_id = 1) , 
        sql = f'SELECT message_own_id FROM {ms.TB_MSSGS_PROCEEDED_}  WHERE message_type_ref_id=1 AND message_proc_status_ref_id=1 AND channels_ref_id = {messageOrigSourceId}'
        listMssgsTextImgsTypeLoadedFull = sps.get_result_from_sql_exec_proc_sps(sql) # Список ID-сообщений типа текст-картинка загруженные полностью
        # Если  res = -1, то это значит, что в списке нет значений и он должен быть равен просто []
        if isinstance(listMssgsTextImgsTypeLoadedFull, int):
            listMssgsTextImgsTypeLoadedFull = []
        # print(f"PR_A128 --> 'IMAGE_DOWNLOADED_' type messages procceded in channel: listMssgsTextImgsTypeLoadedFull = {listMssgsTextImgsTypeLoadedFull}")
        dicRes['IMAGE_DOWNLOADED_'] = listMssgsTextImgsTypeLoadedFull 
        
        #   'IMAGE_DOWNLOADING_PROHIBITED_BY_FLAG_' (загружены текстовые сообщения типа  'мообщения с картинками', но картинки не скачаны, так как флагом было запрещено, имеющие статус status_type_id = 3)
        sql = f'SELECT message_own_id FROM {ms.TB_MSSGS_PROCEEDED_} WHERE message_type_ref_id=1 AND message_proc_status_ref_id=3 AND channels_ref_id = {messageOrigSourceId}'
        listMssgsTextImgsTypeFobidenDownloadIds = sps.get_result_from_sql_exec_proc_sps(sql) # Список ID-сообщений типа текст-картинка : загружены текстовые сообщения, но запрещена загрузка картинок из сообщения
        # Если  res = -1, то это значит, что в списке нет значений и он должен быть равен просто []
        if isinstance(listMssgsTextImgsTypeFobidenDownloadIds, int):
            listMssgsTextImgsTypeFobidenDownloadIds = []
        # print(f"PR_A129 --> 'IMAGE_DOWNLOADING_PROHIBITED_BY_FLAG_' type messages procceded in channel: listMssgsTextImgsTypeFobidenDownloadIds = {listMssgsTextImgsTypeFobidenDownloadIds}")
        dicRes['IMAGE_DOWNLOADING_PROHIBITED_BY_FLAG_'] = listMssgsTextImgsTypeFobidenDownloadIds
        
        
        # и 'IMAGE_DOWNLOADING_ERROR_' (Произошла какая-то ошибка при загрузке сообщений типа текст-картинки, имеющие статус status_type_id = 2)
        sql = f'SELECT message_own_id FROM {ms.TB_MSSGS_PROCEEDED_} WHERE message_type_ref_id=1 AND message_proc_status_ref_id=2 AND channels_ref_id = {messageOrigSourceId}'
        listMssgsTextImgsTypeErrorDownloadIds = sps.get_result_from_sql_exec_proc_sps(sql) # Список ID-сообщений типа текст-картинка : загружены текстовые сообщения, но запрещена загрузка картинок из сообщения
        # Если  res = -1, то это значит, что в списке нет значений и он должен быть равен просто []
        if isinstance(listMssgsTextImgsTypeErrorDownloadIds, int):
            listMssgsTextImgsTypeErrorDownloadIds = []
        # print(f"PR_A130 --> 'IMAGE_DOWNLOADING_ERROR_' type messages procceded in channel: listMssgsTextImgsTypeErrorDownloadIds = {listMssgsTextImgsTypeErrorDownloadIds}")
        dicRes['IMAGE_DOWNLOADING_ERROR_'] = listMssgsTextImgsTypeErrorDownloadIds
        
        
        
        
        # для сообщений - документов типа 'DOCUMENT_FILE_MSSG_' (type_message_id = 2): 
        # 'DOCUMENT_DOWNLOADED_' (документ-файл загружен успешно, имеющие статус status_type_id = 4) 
        sql = f'SELECT message_own_id FROM {ms.TB_MSSGS_PROCEEDED_} WHERE message_type_ref_id=2 AND (message_proc_status_ref_id=4 OR message_proc_status_ref_id=7) AND channels_ref_id = {messageOrigSourceId}'
        listMssgsDocumentTypeDownloadFullIds = sps.get_result_from_sql_exec_proc_sps(sql) # Список ID-сообщений типа текст-картинка : загружены текстовые сообщения, но запрещена загрузка картинок из сообщения
        # Если  res = -1, то это значит, что в списке нет значений и он должен быть равен просто []
        if isinstance(listMssgsDocumentTypeDownloadFullIds, int):
            listMssgsDocumentTypeDownloadFullIds = []
        # print(f"PR_A131 --> 'DOCUMENT_DOWNLOADED_' type messages procceded in channel: listMssgsDocumentTypeDownloadFullIds = {listMssgsDocumentTypeDownloadFullIds}")
        dicRes['DOCUMENT_DOWNLOADED_'] = listMssgsDocumentTypeDownloadFullIds
        
        print(f"PR_A968 --> dicRes['DOCUMENT_DOWNLOADED_'] = {dicRes['DOCUMENT_DOWNLOADED_']}")


        
        # 'DOCUMENT_DOWNLOADING_PROHIBITED_BY_FLAG_' (загрузка файла-документа была запрещена флагом загрузки доекментов-файлов, имеющие статус status_type_id = 6)
        sql = f'SELECT message_own_id FROM {ms.TB_MSSGS_PROCEEDED_} WHERE message_type_ref_id=2 AND message_proc_status_ref_id=6 AND channels_ref_id = {messageOrigSourceId}'
        listMssgsDocumentTypeFobidenDownloadIds = sps.get_result_from_sql_exec_proc_sps(sql) # Список ID-сообщений типа текст-картинка : загружены текстовые сообщения, но запрещена загрузка картинок из сообщения
        # Если  res = -1, то это значит, что в списке нет значений и он должен быть равен просто []
        if isinstance(listMssgsDocumentTypeFobidenDownloadIds, int):
            listMssgsDocumentTypeFobidenDownloadIds = []
        # print(f"PR_A132 --> 'DOCUMENT_DOWNLOADING_PROHIBITED_BY_FLAG_' type messages procceded in channel: listMssgsDocumentTypeFobidenDownloadIds = {listMssgsDocumentTypeFobidenDownloadIds}")
        dicRes['DOCUMENT_DOWNLOADING_PROHIBITED_BY_FLAG_'] = listMssgsDocumentTypeFobidenDownloadIds





        # и 'DOCUMENT_DOWNLOADING_ERROR_' (Произошла какая-то ошибка при загрузке документов-файлов, имеющие статус status_type_id = 5)
        sql = f'SELECT message_own_id FROM {ms.TB_MSSGS_PROCEEDED_} WHERE message_type_ref_id=2 AND message_proc_status_ref_id=5 AND channels_ref_id = {messageOrigSourceId}'
        listMssgsDocumentTypeErrorDownloadIds = sps.get_result_from_sql_exec_proc_sps(sql) # Список ID-сообщений типа текст-картинка : загружены текстовые сообщения, но запрещена загрузка картинок из сообщения
        # Если  res = -1, то это значит, что в списке нет значений и он должен быть равен просто []
        if isinstance(listMssgsDocumentTypeErrorDownloadIds, int):
            listMssgsDocumentTypeErrorDownloadIds = []
        # print(f"PR_A133 --> 'DOCUMENT_DOWNLOADING_ERROR_' type messages procceded in channel: listMssgsDocumentTypeErrorDownloadIds = {listMssgsDocumentTypeErrorDownloadIds}")

        dicRes['DOCUMENT_DOWNLOADING_ERROR_'] = listMssgsDocumentTypeErrorDownloadIds
        
        
        
        # Список всех ID обычных и декларативных сообщений, зарегестрированных в табл 'tg_auxilary_messages_proceeded'
        sql = f'SELECT message_own_id FROM {ms.TB_AUXILARY_MSSGS_PROCEEDED_} WHERE channels_ref_id = {messageOrigSourceId}'
        listMssgsSimpleAndDeclarativeDownloadIds = sps.get_result_from_sql_exec_proc_sps(sql) # Список ID-сообщений типа текст-картинка : загружены текстовые сообщения, но запрещена загрузка картинок из сообщения

        # Если  res = -1, то это значит, что в списке нет значений и он должен быть равен просто []
        if isinstance(listMssgsSimpleAndDeclarativeDownloadIds, int):
            listMssgsSimpleAndDeclarativeDownloadIds = []
            
        dicRes['DECLARATIVE_AND_SIMPLE_'] = listMssgsSimpleAndDeclarativeDownloadIds
        
        
        
        
        return dicRes









    # def reject_analizators_first_level_for_all_channels_actm (self):
    #     """
    #     Анализатор - Усекатель для всех каналов для уровня 1
    #     Уровень 1: это табл уровня 'tg_messages_proceeded' и 'tg_messages_proceeded_ext'
    #     """



        
    #     # АНАЛИЗАТОР I 
        
    #     # Анализируем на предмет соотвтетсвия рядов в таблицах 'tg_messages_proceeded' и 'tg_messages_proceeded_ext' между собой
        
    #     dfTgProceeded = self.spps.read_table_auto_sql_to_df_mysql_spps(ms.TB_MSSGS_PROCEEDED_)
        
    #     dfTgProceededExt = self.spps.read_table_auto_sql_to_df_mysql_spps(ms.TB_MSSGS_PROCEEDED_EXT_)

    #     x = set(dfTgProceeded['id'])
        
    #     y = set(dfTgProceededExt['message_proceeded_ref_id'])

    #     # tbids сообщений, которые по каким-то причинам (пока неустановленным) не получили свой ряд расширение в табл 'tg_messages_proceeded_ext'
    #     diffTbidsList = list(set(x) - set(y))
        
    #     print(f"PR_B263 --> diffTbidsList = {diffTbidsList}")
        
    #     if len(diffTbidsList) > 0:
        
    #         # Удалить эти сообщения из табл 'tg_messages_proceeded'
            
    #         inDiffTupleSql = self.sps.transform_list_valuews_to_sql_string_for_tuple_inside_sps(diffTbidsList)
            
    #         sql = f"DELETE FROM {ms.TB_MSSGS_PROCEEDED_} WHERE id in ({inDiffTupleSql})"
            
    #         print(f"PR_B264 --> sql = {sql}")
            
    #         self.sps.execute_sql_SPS(sql)

    #     # END АНАЛИЗАТОР I 
        
        
    #     # АНАЛИЗАТОР II
        
    #     # Поиск и анализ сообщений-картинок, следующих одна за другой, с текстом в них (обязательно). Но которые имеют grouped_id = -1,
    #     # Либо один имеет другой нет. В общем случае - имют разные grouped id, если они больще нуля, либо один или оба имеют 
    #     # grouped_id = -1. Тогда удалятся должен тот, который имеет меньший  message_id. Причем, этот анализ идет исключительно 
    #     # по выборке по каждому унмтарному источнику этих сообщений (то есть нужно организовать цикл по всем источникам)
        
    #     # Список id всех источников
    #     allSources = self.blf.get_all_books_orig_sources_ids_blf()
        
    #     # список tbids сообщений для переноса из тбалиц 'tg_messages_proceeded' в таблицы 'tg_auxilary_messages_proceeded'
    #     tbidsForTransferToAuxilarList = []
                
    #     for origSource in  allSources:
            
            
    #         # Полный фрейм с данными из таблиц 'tg_messages_proceeded' и 'tg_messages_proceeded_ext'. Действует на любые источники 
    #         # сообщений либо их смесь
    #         dfFullProcceededBySource = self.tlf.get_df_full_dta_tbs_procceeded_by_sourcr_id_tlf(origSource)
    #         # Индексируем одинаково названные колонки
    #         dfFullProcceededBySource = PandasManager.index_duplicated_name_columns_in_df_universal(dfFullProcceededBySource)
            
            
    #         print(f"\n PR_B273--> @@@@@@@@ currorigSource = {origSource}\n")
            
    #         # typeDfSequence = list(dfFullProcceededBySource['message_type_ref_id'])
            
    #         # print(f"PR_B274--> ## typeDfSequence = {typeDfSequence}")
            
    #         # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfFullProcceededBySource,False,colsIndxed = True, marker="PR_B265 --> colList of dfFullProcceededBySource")
                
    #         # Цикл по рядам dfFullProcceededBySource
    #         # ПРИМ: Итерация идет в таком порядке, что снаяла идут сообщения с больщими messageId, как и нужно. Это соотвтетсвует 
    #         # рассмотрению ленты сообщений в ТГ снизу вверх (сначала идут самые последние сообщение. Выще - болеее ранние с меньшими messageID)
    #         # Имеем ввиду , что при этом порядке рассмотрения для поиска смычки описания и аудио-тома будет всегда переключение последователльности
    #         # типа сообщения с 2 на 1 (2 -> 1). Это переключение и является качественным индикатором для определения Книжного комплекта, который 
    #         # состоит из картинки (или картинок) с описанием в одной из них и непосредственно за ним следующими группой (или одним) аудио-томов
    #         for index, row in dfFullProcceededBySource.iterrows():

    #             # print(f"\n PR_B267 --> Индекс ряда или цикла: {index}\n")
                
    #             # Тип сообщения по текущему ряду фрейма
    #             # messageId = row['message_own_id']
                
    #             # print(f"PR_B269 --> messageId = {messageId}")
            
    #             # пропускаем первый цикл, что бы появились регрессивные данные по предыдущему ряду, что бы сравнивать
    #             if index == 0: 

    #                 continue
                
    #             # tbid текущего сообщения в таблице 'tg_messages_proceeded'
    #             tbidCurr = row['id']
                
    #             print(f"PR_B266 --> Текущий tbidCurr = {tbidCurr}")
                
    #             # Тип сообщения по текущему ряду фрейма
    #             messageTypeRefIdCurr = row['message_type_ref_id']

                
    #             # print(f"PR_B268 --> messagesGroupedIdCurr = {messagesGroupedIdCurr}")
            
            
    #             # БЛОК АНАЛИЗА 
                
    #             # 1. Сравниваем значение текущего типа сообщения с типом предыдущего сообщения (в предшествующем ряду фрейма)
    #             # Всегда будем из текущего значения вычитать предыдущее
                
    #             messageTypeRefIdPrev = dfFullProcceededBySource['message_type_ref_id'].iloc[index-1]
                
    #             # print(f"PR_B267 --> messageTypeRefIdCurr = {messageTypeRefIdCurr}")
    #             # print(f"PR_B272 --> messageTypeRefIdPrev = {messageTypeRefIdPrev}")
                
    #             diffTypes = messageTypeRefIdCurr - messageTypeRefIdPrev
                
    #             print(f"PR_B276 --> {index} Разница меэжду текущим и предыдущим типом сообщения. diffTypes = {diffTypes}")
                
    #             # ПРИМ: 
    #             # a/ Если разница diffTypes = -1  (Это значит переключение [2 -> 1], переключение последней картинки из группы описания или просто одна картинка с описание)
    #             # Это так же значит, что предыдущее сообщение tbid - это самый первый том после последней картинки в группе описания (или один файл описания)
                
    #             # b/ Если diffTypes = 0, это значит, что предыдущим было сообщение с таким же типом, как и текущее (это может быть как том, так и одна из картинок 
    #             # в группе описания книги)
                
    #             # c/ Если diffTypes = 1, то это означает, что предыдущим сообщением был последний аудио-том книги. И после него снова пошла какая -то картинка ,
    #             # которая можкт быть как первой картинкой в описании следующей новой книги, так и псевдо-описанием (ккое-то сообщений с картинкой)
                
    #             # e/ Если diffTypes= 0, а текущий тип сообщения аудио-книга, то это означает, что текущее сообщение скорее всего яаляется продлжением группы 
    #             # аудио-томов книги. Но тем ни менее, проверяем по идентификатору группы. Эти группы по идее должны быть равны. если нет, какое-то из сообщений
    #             # наверняка является затесавшимся осколком. Тут надо дальше анализировать
                
                
    #             # В данном анализаторе [АНАЛИЗАТОР II] мы вычисляем псевдо-книги, то есть пункт d/ !!!
                
    #             # Ветка d/ Если diffTypes = 0 и текущий тип сообщения = 1, это значит что в предыдущем цикле была картинка и сейчас в текущем цикле - тоже картинка
    #             # Тогда необходимо сравнить их идентификаторы групп. Если группы разные, то это означает, что текущее сообщение-картинка является псевдо-описанием книги
    #             # и его надо перенести в 'tg_auxilary_messages_proceeded'. Этот анализ является универсальным для всех источников.
    #             # Для дополнительного контроля по sourceId = 2 можно проверить наличие ссылки, которая в данном источнике никогда (?) не встречается в описании
    #             # книги, но встречается в различных псевдо-сообщениях картинках. Переносится картинка с меньшим tbid или с меньшим messageId, то есть текущая по циклу
    #             # Кроме того, если идентификатор группы предыдущей картинки = -1, это означает, что картинка-описание текущей книги - вообще не групповая и можно 
    #             # сразу смело переносить текущую картинку как псевдо. Так как без перехода (2 -> 1) любая картинка с текстом не может являтся описанием книги, если до 
    #             #  до нее была тоже картинка !!!
    #             if diffTypes == 0 and messageTypeRefIdCurr == 1:
                
    #                 # Идентификатор группы сообщения по текущему ряду фрейма
    #                 messagesGroupedIdCurr = row['messages_grouped_id']
    #                 # Идентификатор группы сообщения по предыдущему ряду фрейма
    #                 messagesGroupedIdPrev = dfFullProcceededBySource['messages_grouped_id'].iloc[index-1]
                    
    #                 if messagesGroupedIdPrev == -1 or messagesGroupedIdPrev != messagesGroupedIdCurr:
                        
    #                     print(f"PR_B277--> SYS LOG: Сообщение с tbid = {tbidCurr} внесено в список на перемещение в таблицы 'tg_auxilary_messages_proceeded'")
                        
    #                     # Вносим текущее сообщение в список на перенос в таблицы Auxilaries 
    #                     tbidsForTransferToAuxilarList.append(tbidCurr)
                



    #             # END БЛОК АНАИЗА 
                
    #     print(f"Результат Анализатора II. ")
    #     print(f"PR_B278--> SYS LOG: Список tbids сообщений в табл 'tg_messages_proceeded', которые будут перемещены в таблицы регистрации вспомогательных сообщений \n {tbidsForTransferToAuxilarList}")
            
            
    #     # НЕ УДАЛЯТЬ    
    #     # ПЕРЕНОС сообщений в списке   tbidsForTransferToAuxilarList  из таблиц 'tg_messages_proceeded' в таблицы 'tg_auxilary_messages_proceeded'
        
    #     # # 1. Сначала копируем (создаем) записи в из главной табл 'tg_messages_proceeded' в табл 'tg_auxilary_messages_proceeded' 
        
    #     # inListsql = self.sps.transform_list_valuews_to_sql_string_for_tuple_inside_sps(tbidsForTransferToAuxilarList)
        
        
        
    #     # Через IN не получится. надо через for


    #     # # Цикл по  tbidsForTransferToAuxilarList
        
    #     # for msgeTbid in tbidsForTransferToAuxilarList:

    #     #     sql = f"""
    #     #                 INSERT INTO {ms.TB_AUXILARY_MSSGS_PROCEEDED_} 
    #     #                 VALUES (
    #     #                     channels_ref_id,
    #     #                     message_own_id,
    #     #                     message_type_ref_id,
    #     #                     message_proc_status_ref_id,
    #     #                     date_reg_calend,
    #     #                     date_reg_unix,
    #     #                     date_executed_calend,
    #     #                     date_executed_unix,
    #     #                     tg_sample_id
    #     #                 )
    #     #                 SELECT 
    #     #                     channels_ref_id,
    #     #                     message_own_id,
    #     #                     message_type_ref_id,
    #     #                     message_proc_status_ref_id,
    #     #                     date_reg_calend,
    #     #                     date_reg_unix,
    #     #                     date_executed_calend,
    #     #                     date_executed_unix,
    #     #                     tg_sample_id
    #     #                 FROM {ms.TB_MSSGS_PROCEEDED_} 
    #     #                 WHERE id = {msgeTbid}
    #     #     """
        
    #     #     print(f"PR_B279-->  sql = {sql}")
            
    #     #     try: 
    #     #         # self.sps.execute_sql_SPS(sql)
    #     #         print(f"PR_B280 --> SYS LOG: из табл 'tg_messages_proceeded' в табл 'tg_auxilary_messages_proceeded' перенесена запись с tbid = {msgeTbid}")
                
    #     #         # автоинкрементное id последней вставки
    #     #         lastId = self.sps.get_last_inserted_id_in_db_mysql_sps()
                
    #     #     except Exception as err:
    #     #         print(f"PR_B281 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
    #     #         print(f"PR_B282 --> SYS LOG: ERRORR !!! {err}")


        
    #     #     # Получить текст сообщения из 'tg_message_proceeded_ext'
            
    #     #     sql = f"SELECT message_text FROM {ms.TB_MSSGS_PROCEEDED_EXT_} WHERE message_proceeded_ref_id = {msgeTbid}"
            
    #     #     mssgText = self.sps.get_result_from_sql_exec_proc_sps(sql)
            
    #     #     print(f"PR_B283--> mssgText = {mssgText}")
        
        
    #         # 2. Копируем (создаем) записи из главной табл 'tg_message_proceeded_ext' в главную табл 'tg_auxilary_messages_proceeded_ext'
            
            
    #         # sql2 = f"""
    #         #             INSERT INTO {ms.TB_AUXILARY_MSSGS_PROCEEDED_EXT_} 
    #         #             VALUES (
    #         #                 message_proceeded_ref_id,
    #         #                 message_text,
    #         #             )
    #         #             SELECT 
    #         #                 auxilary_message_proceeded_ref_id,
    #         #                 message_text
    #         #             FROM {ms.TB_MSSGS_PROCEEDED_EXT_} 
    #         #             WHERE message_proceeded_ref_id IN ({inListsql})
    #         # """
            
    #         # print(f"PR_B279-->  sql = {sql1}")
            
        
        
        
    #     # 3. Удалить записи в зависимой табл 'tg_message_proceeded_ext'
    #     # 4. Удалить записи из главной табл 'tg_messages_proceeded'
            
            

            
            
            
            
            
    #     # END АНАЛИЗАТОР II    

                







    def analyzers_I_II_III_logic_wrong_messages_first_lv_actm(self, analisysExelist = []):
        """ 
        Поиск и анализ сообщений-картинок, следующих одна за другой, с текстом в них (обязательно). Но которые имеют grouped_id = -1,
        Либо один имеет другой нет. В общем случае - имют разные grouped id, если они больще нуля, либо один или оба имеют 
        grouped_id = -1. Тогда удалятся должен тот, который имеет меньший  message_id. Причем, этот анализ идет исключительно 
        по выборке по каждому унмтарному источнику этих сообщений (то есть нужно организовать цикл по всем источникам)
        
        analisysExelist - список номеров видов анализа, которые запускаются в методе [1,2,3] (на данный момент 3 вида анализа)
        
        Анализ I: Анализ рядов в табл 'tg_messages_proceeded', которые не имеют расширения в табл 'tg_messages_proceeded_ext' 
        (то есть бракованные сообщения по умолчанию)
        
        Анализ II: Поиск псевдо-книг методом сравнения различия идентификатора групп у сообщений с типом id = 1, когда идентификатор считается правильным у 
        того сообщения, который непосредственно соприкасается с первым аудио-томом. А отличные от него ИГ указывают на то, что сообщение является псевдо-книгой
        сообщения. которые воспринимаются системой как псевдо-книги. картинки с текстом, стоящие в цепочке наряду с картинками описания
        книги. не входящие в группу описания книги 
        
        Возвращает список вычесленных системой сообщений с возможной логической ошибкой. Ошибки подразумевают псевдо-книги. Однако, 
        система не может сама решить какого рода эти ошибки. МОжет быть псевдо-книга, а может быть нормальное описание книги, но по каким-то 
        причинам не сохранены ее аудио-тома (эта возможность была выявлена путем практики - иногда почему-то могуь аудио-тома, которые
        скачаны системой, н опочему-то не зафиксированы в БД. Это и создает необходимость на данный моент участие человеческого фактора
        в классификации этих ошибок)
        
        Анализ III. Поиск осколочных томов в верхнем конце цепочки типов. Принцип: если аудио-тома (тип id = 2) в верхнем конце цепочки (верхний конец - это
        те сообщения, у которых меньший messageId) не соприкасаются с сообщением типа 1 (описанием книги), то эти аудио-тома не могут образовать книжный 
        комплект и должны быть удалены из таблиц первого уровня tg_procceeded
        
        RET: Возвращает списки по каждому виду анализа отдельно (analys1List, analys2List, analys3List)
        """
        
        print(f"PR_B292--> START: analyzers_I_II_III_logic_wrong_messages_first_lv_actm()")


        # Список id всех источников
        allSources = self.blf.get_all_books_orig_sources_ids_blf()
        
        # Пустой вид анализа, вставка для соотвтетсвия номеров анализа в тапле на выходе
        analys0List = []
        
        analys1List = []
        
        if 1 in analisysExelist:
            
            # БЛОК АНАЛИЗА I
            # Анализ рядов в табл 'tg_messages_proceeded', которые не имеют расширения в табл 'tg_messages_proceeded_ext' 
            # (то есть бракованные сообщения по умолчанию)
            
            
            dfTgProceeded = self.spps.read_table_auto_sql_to_df_mysql_spps(ms.TB_MSSGS_PROCEEDED_)
            
            dfTgProceededExt = self.spps.read_table_auto_sql_to_df_mysql_spps(ms.TB_MSSGS_PROCEEDED_EXT_)

            x = set(dfTgProceeded['id'])
            
            y = set(dfTgProceededExt['message_proceeded_ref_id'])

            # tbids сообщений, которые по каким-то причинам (пока неустановленным) не получили свой ряд расширение в табл 'tg_messages_proceeded_ext'
            analys1List = list(set(x) - set(y))
            
            print(f"PR_B263 --> diffTbidsList = {analys1List}")
            
            # Пока не удалять
            # if len(diffTbidsList) > 0:
            
            #     # Удалить эти сообщения из табл 'tg_messages_proceeded'
                
            #     inDiffTupleSql = self.sps.transform_list_valuews_to_sql_string_for_tuple_inside_sps(diffTbidsList)
                
            #     sql = f"DELETE FROM {ms.TB_MSSGS_PROCEEDED_} WHERE id in ({inDiffTupleSql})"
                
            #     print(f"PR_B264 --> sql = {sql}")
                
            #     self.sps.execute_sql_SPS(sql)

            # END БЛОК АНАЛИЗА I
        else:
            analys1List = []

        
        # список tbids сообщений для переноса из тбалиц 'tg_messages_proceeded' в таблицы 'tg_auxilary_messages_proceeded'
        analys2List = []
        
        analys3List = []
        
                
        
        for origSource in  allSources:
            
            
            # Полный фрейм с данными из таблиц 'tg_messages_proceeded' и 'tg_messages_proceeded_ext'. Действует на любые источники 
            # сообщений либо их смесь
            dfFullProcceededBySource = self.tlf.get_df_full_dta_tbs_procceeded_by_source_id_tlf(origSource)
            # Индексируем одинаково названные колонки
            dfFullProcceededBySource = PandasManager.index_duplicated_name_columns_in_df_universal(dfFullProcceededBySource)
            
            
            print(f"\n PR_B288--> @@@@@@@@ currorigSource = {origSource}\n")
            
            # typeDfSequence = list(dfFullProcceededBySource['message_type_ref_id'])
            
            # print(f"PR_B274--> ## typeDfSequence = {typeDfSequence}")
            
            # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfFullProcceededBySource, True, colsIndxed = True, marker="PR_B265 --> colList of dfFullProcceededBySource")
                
            if 2 in analisysExelist:
                # БЛОК АНАЛИЗА II
                # Анализ II: Поиск псевдо-книг методом сравнения различия идентификатора групп у сообщений с типом id = 1, когда идентификатор считается правильным у 
                # того сообщения, который непосредственно соприкасается с первым аудио-томом. А отличные от него ИГ указывают на то, что сообщение является псевдо-книгой
                # сообщения. которые воспринимаются системой как псевдо-книги. картинки с текстом, стоящие в цепочке наряду с картинками описания
                # книги. не входящие в группу описания книги 
                
                # Цикл по рядам dfFullProcceededBySource
                # ПРИМ: Итерация идет в таком порядке, что снаяла идут сообщения с больщими messageId, как и нужно. Это соотвтетсвует 
                # рассмотрению ленты сообщений в ТГ снизу вверх (сначала идут самые последние сообщение. Выще - болеее ранние с меньшими messageID)
                # Имеем ввиду , что при этом порядке рассмотрения для поиска смычки описания и аудио-тома будет всегда переключение последователльности
                # типа сообщения с 2 на 1 (2 -> 1). Это переключение и является качественным индикатором для определения Книжного комплекта, который 
                # состоит из картинки (или картинок) с описанием в одной из них и непосредственно за ним следующими группой (или одним) аудио-томов
                for index, row in dfFullProcceededBySource.iterrows():

                    # print(f"\n PR_B267 --> Индекс ряда или цикла: {index}\n")
                    
                    # Тип сообщения по текущему ряду фрейма
                    # messageId = row['message_own_id']
                    
                    # print(f"PR_B269 --> messageId = {messageId}")
                
                    # пропускаем первый цикл, что бы появились регрессивные данные по предыдущему ряду, что бы сравнивать
                    if index == 0: 
                        
                        
                        continue
                    
                    # tbid текущего сообщения в таблице 'tg_messages_proceeded'
                    tbidCurr = row['id']
                    
                    # print(f"PR_B289 --> Текущий tbidCurr = {tbidCurr}")
                    
                    # Тип сообщения по текущему ряду фрейма
                    messageTypeRefIdCurr = row['message_type_ref_id']

                    
                    # print(f"PR_B268 --> messagesGroupedIdCurr = {messagesGroupedIdCurr}")
                
                
                    
                    
                    # 1. Сравниваем значение текущего типа сообщения с типом предыдущего сообщения (в предшествующем ряду фрейма)
                    # Всегда будем из текущего значения вычитать предыдущее
                    
                    messageTypeRefIdPrev = dfFullProcceededBySource['message_type_ref_id'].iloc[index-1]
                    
                    # print(f"PR_B267 --> messageTypeRefIdCurr = {messageTypeRefIdCurr}")
                    # print(f"PR_B272 --> messageTypeRefIdPrev = {messageTypeRefIdPrev}")
                    
                    # АНАЛИЗ II
                    diffTypes = messageTypeRefIdCurr - messageTypeRefIdPrev 
                    
                    # print(f"PR_B290 --> {index} Разница меэжду текущим и предыдущим типом сообщения. diffTypes = {diffTypes}")
                    
                    # ПРИМ: 
                    # a/ Если разница diffTypes = -1  (Это значит переключение [2 -> 1], переключение последней картинки из группы описания или просто одна картинка с описание)
                    # Это так же значит, что предыдущее сообщение tbid - это самый первый том после последней картинки в группе описания (или один файл описания)
                    
                    # b/ Если diffTypes = 0, это значит, что предыдущим было сообщение с таким же типом, как и текущее (это может быть как том, так и одна из картинок 
                    # в группе описания книги)
                    
                    # c/ Если diffTypes = 1, то это означает, что предыдущим сообщением был последний аудио-том книги. И после него снова пошла какая -то картинка ,
                    # которая можкт быть как первой картинкой в описании следующей новой книги, так и псевдо-описанием (ккое-то сообщений с картинкой)
                    
                    # e/ Если diffTypes= 0, а текущий тип сообщения аудио-книга, то это означает, что текущее сообщение скорее всего яаляется продлжением группы 
                    # аудио-томов книги. Но тем ни менее, проверяем по идентификатору группы. Эти группы по идее должны быть равны. если нет, какое-то из сообщений
                    # наверняка является затесавшимся осколком. Тут надо дальше анализировать
                    
                    
                    # В данном анализаторе [АНАЛИЗАТОР II] мы вычисляем псевдо-книги, то есть пункт d/ !!!
                    
                    # Ветка d/ Если diffTypes = 0 и текущий тип сообщения = 1, это значит что в предыдущем цикле была картинка и сейчас в текущем цикле - тоже картинка
                    # Тогда необходимо сравнить их идентификаторы групп. Если группы разные, то это означает, что текущее сообщение-картинка является псевдо-описанием книги
                    # и его надо перенести в 'tg_auxilary_messages_proceeded'. Этот анализ является универсальным для всех источников.
                    # Для дополнительного контроля по sourceId = 2 можно проверить наличие ссылки, которая в данном источнике никогда (?) не встречается в описании
                    # книги, но встречается в различных псевдо-сообщениях картинках. Переносится картинка с меньшим tbid или с меньшим messageId, то есть текущая по циклу
                    # Кроме того, если идентификатор группы предыдущей картинки = -1, это означает, что картинка-описание текущей книги - вообще не групповая и можно 
                    # сразу смело переносить текущую картинку как псевдо. Так как без перехода (2 -> 1) любая картинка с текстом не может являтся описанием книги, если до 
                    #  до нее была тоже картинка !!!
                    if diffTypes == 0 and messageTypeRefIdCurr == 1:
                    
                        # Идентификатор группы сообщения по текущему ряду фрейма
                        messagesGroupedIdCurr = row['messages_grouped_id']
                        # Идентификатор группы сообщения по предыдущему ряду фрейма
                        messagesGroupedIdPrev = dfFullProcceededBySource['messages_grouped_id'].iloc[index-1]
                        
                        if messagesGroupedIdPrev == -1 or messagesGroupedIdPrev != messagesGroupedIdCurr:
                            
                            # print(f"PR_B291--> SYS LOG: Сообщение с tbid = {tbidCurr} внесено в список на перемещение в таблицы 'tg_auxilary_messages_proceeded'")
                            
                            # Вносим текущее сообщение в список на перенос в таблицы Auxilaries 
                            analys2List.append(tbidCurr)
                    
                # END БЛОК АНАЛИЗА II
                
                
                
            else:
                analys2List = []
                
            if 3 in analisysExelist:
                # БЛОК АНАЛИЗА III
                # Анализ III. Поиск осколочных томов в верхнем конце цепочки типов. Принцип: если аудио-тома (тип id = 2) в верхнем конце цепочки (верхний конец - это
                # те сообщения, у которых меньший messageId) не соприкасаются с сообщением типа 1 (описанием книги), то эти аудио-тома не могут образовать книжный 
                # комплект и должны быть удалены из таблиц первого уровня tg_procceeded
                
                    
                # Переворачиваем фрейм
                for index, row in dfFullProcceededBySource[::-1].iterrows() :
                    
                    if index == 0: 
                        
                        messageTypeRefIdFirst = row['message_type_ref_id']
                        
                        # Если верхний конец цепочки начинается с аудио-тома, это значит, что эти аудио-тома уже никак не смогут учавствовать в создании 
                        # книжного комплекта. Поэтому в этом случае включаем анализ цепочки до следующего переключения (2 -> 1). и найденные аудио-тома удалить
                        # Когда наступит переключение - анализ завершен. Так же анализ не нужен, если верхняя цепочка начинается с какой-либо картинки с типом = 1
                        if messageTypeRefIdFirst == 2:
                            
                            
                            tbidCurr = row['id']
                            
                            # Вносим tbid сообщения в список ошибочных сообщений
                            analys3List.append(tbidCurr)
                            
                            continue
                            
                        
                        else:
                            # Завершение анализа
                            break
                        
                        
                    messageTypeRefIdCurr = row['message_type_ref_id']
                    
                    
                    if messageTypeRefIdCurr == 2:
                        
                        
                        tbidCurr = row['id']
                        
                        # Вносим tbid сообщения в список ошибочных сообщений
                        analys3List.append(tbidCurr)
                    
                    else:
                        
                        break

                print(f"PR_B303 --> analys3List = {analys3List}")
                
                # END БЛОК АНАИЗА III
                
            else:
                analys3List = []
                
        # Добавляем список анализа 3        
        # analys2List +=  analys3List       
                
        # print(f"Результат Анализатора II. ")
        # print(f"PR_B278--> SYS LOG: Список tbids сообщений в табл 'tg_messages_proceeded', которые будут перемещены в таблицы регистрации вспомогательных сообщений \n {listOfLogicErrorsMessagesTbids}")
            
            
            
            
        print(f"PR_B293--> END: analyzer_II_logic_wrong_messages_first_lv_actm()")

            
        return analys0List, analys1List, analys2List, analys3List







if __name__ == '__main__':
    pass





    # ПРОРАБОТКА:
    
    aubtm = AudiobooksChannelTelegramManager()
    
    listOfLogicErrorsMessagesTbids = aubtm.analyzer_II_logic_wrong_messages_first_lv_actm()
    
    print(f"PR_B287--> listOfLogicErrorsMessagesTbids = {listOfLogicErrorsMessagesTbids}")
    
    
    
    
    
    
    
    
    
    







    # # Настройка авторизации на свой Телеграм-канал для подключения возможностей взаимодействовать с програмным кодом
    # auth = {
    #     'api_id' : 20460272,
    #     'api_hash' : '9e6f44844a41f717e5c035cb0add2984',
    #     'session_name' : 'anon', # Название файла с сессией (БД sqlite, если нет прочих настроек по формату сесссии. Хранится в рабочей директории, где manage.py)
    # }


    # aubtm = AudiobooksChannelTelegramManager(auth)










