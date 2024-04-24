# Динамическое подключение settings_bdp_main в корне проекта
import sys
sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')
import settings_bdp_main as ms # общие установки для всех модулей
import settings_tg as ts

from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup
from noocube.sqlite_pandas_processor_speedup import SqlitePandasProcessorSpeedup
# # from noocube.django_view_manager import DjangoViewManager
from noocube.bonds_main_manager_speedup import BondsMainManagerSpeedup
from noocube.funcs_general_class import FunctionsGeneralClass

from telegram_monitor.local_classes.tg_local_funcs import TgLocalFuncs

from telegram_monitor.local_classes.tg_chat_messages_parsers import TgChatMessagesParsers

from noocube.pandas_manager import PandasManager

# from telegram_monitor.

import noocube.funcs_general as FG

from telegram_monitor.local_classes.book_library_funcs import BookLibraryFuncs

from noocube.files_manager import FilesManager

from beeprint import pp


from  telegram_monitor.local_classes.audiobooks_channel_telegram_manager import AudiobooksChannelTelegramManager

from noocube.switch import Switch

import numpy as np

from noocube.html_manager import HTMLSiteManager

from telegram_monitor.local_classes.tg_pyrogram_manager import TgPyrogramManager
from pyrogram.types import InputMediaPhoto, InputMediaVideo, InputMediaAudio


from telegram_monitor.local_classes.tg_render_manager import TgRenderManager





class BookLibraryManager ():
    """ 
    Модуль отвечающий за работу с библиотекой книг
    """


    def __init__(self, **dicTrough):
        self.db_uri = f"sqlite:///{ms.DB_CONNECTION.dataBase}" # Pandas по умолчанию работает через SQLAlchemy и может создавать сама присоединение к БД по формату адреса URI (см. в документации SQLAlchemy)
        self.db_connection = ms.DB_CONNECTION
        self.sps = SqliteProcessorSpeedup(self.db_connection) # Обьект класса SqliteProcessorSpeedup
        self.spps = SqlitePandasProcessorSpeedup(self.db_connection) # Обьект класса SqlitePandasProcessorSpeedup
        self.bmms = BondsMainManagerSpeedup(self.db_connection)
        self.tlf = TgLocalFuncs()
        # self.request = request
        self.dicTrough = dicTrough
        
        self.blf = BookLibraryFuncs()



    # НЕ УДАЛЯТЬ ПОКА. Необходимо скопировать описания
    def prepare_and_set_ilbn_to_alfa_book_row_based_on_book_id_lfdb_blm(self, bookId, xGroup, yGroup):
        """ 
        BookLibraryManager
        Присвоить книге все необходимые  группы литеров (группы литеров xGroup, yGroup, zGroup). Литер-группа zGroup является отображением 
        уникального индивидуального номера книги (который в свою очередь является автоинкрементным ключем таблицы в поле 'id')
        zGroup - это стринг из 10 разрядов нулей, где справа разряды замещаются идентификатором-ключем книги в автоинкрементном поле 'id' таблицы 'lib_books_alfa'
        xGroup и yGroup - пока эти литеры являются 3х разрядовыми стрингами с нулями (в далльнейшем они будут нести какую-то смысловую составляющую)
        А так же этот метод формирует из гропп-литеров конечный уникальный индивидуальный серийный номер книги в библиотек ILBN (Individual Library Book Number) 
        в поле 'final_ilbn'  талицы lib_books_alfa
        Все литеры и окончательный ILBN прописываются в только что созданной новой записи регистрации книги в таблице 'lib_books_alfa' в записи с id = bookId (которая
        является id только что созданной записи в таблице при регистрации новой книге в  BIBLIO)
        ПРИМ: литеры для групп xGroup и yGroup передаются пока в параметрах (потом, возможно, они будут формироваться автоматом, когда станет понятен их 
        потенциальный смысл)
        """
        print(f"PR_A278 --> START: prepare_and_set_ilbn_to_alfa_book_row_based_on_book_id_lfdb_blm()")

        # Сформировать литеральные группы идентификационного номера книги и сохранить их в других полях, обозначающих группы
        # xGroup = '000'
        # yGroup = '000'
        zLiterGroupZeroIni = '0000000000'
        
        # # Получить литер стринговой группы z в идентификаторе
        zLiterGroup = FunctionsGeneralClass.replace_right_end_of_string_with_diigit_fragment_fgc (zLiterGroupZeroIni, bookId)
        
        # ILBN final
        newIlbn = f"{xGroup}-{yGroup}-{zLiterGroup}"
        
        # A. Обновить значение zLiterGroup, xLiterFroup and yLiterGroup в новой созданной записи в табл 'lib_book_serial_ilbn' заданными текущими форматами
        
        sql = f"UPDATE {ms.TB_LIB_BOOKS_ALFA} SET liter_group_z = '{zLiterGroup}', liter_group_y = '{xGroup}', liter_group_x ='{yGroup}', final_ilbn = '{newIlbn}' WHERE id = {bookId} "
        
        print(f"PR_A214 --> SYS LOG: Сформирован и присвоен новый серийный идентификационный номер для книги с ID = {bookId} в табл 'lib_books_alfa' ")
        
        self.sps.execute_sql_SPS(sql)
        
        print(f"PR_A279 --> END: prepare_and_set_ilbn_to_alfa_book_row_based_on_book_id_lfdb_blm()")

        
        return newIlbn
        



    def extend_new_alfa_book_with_data_blm (self, newAlfaBookId, dicFullBookData, **bkwargs):
        """ 
        BookLibraryManager
        Создать запись в таблице 'lib_books_alfa_ext' с 'books_alfa_id' равным ID новой книге, созданной в таблице 'lib_books_alfa' и 
        наполнить ее всеми известными данными о регестрируемой книге, находящимися в словаре данных книги dicRegisterBookData
        
        newAlfaBookId - это новый id книги, созданной в табл 'lib_books_alfa', и которое нужно расширить данынми в таблице one-to-one 'lib_books_alfa_ext',
        которые нужно заполнить из словаря dicRegisterBookData
        
        dicRegisterBookData - словарь данных книги, который получен из анализа скачанных сообщений по книге из ТГ канала
        
        """
        
        print(f"PR_A280 --> START: extend_new_alfa_book_with_data_blm()")

        
        # print(f"PR_A229 --> newAlfaBookId = {newAlfaBookId}")
        
        # INI
        

        
        
        # словарь с набором данных по описанию книги в ТГ и данных при ее скачивании с ТГ канала
        dicTgRegisterBookData = dicFullBookData['tgChatData']
        
        # Словарь с распарсенными обьектами описания книги
        dicDescrParsing = dicFullBookData['descrParsingData']
        
        # Данные по текущему комплекту книги, на базе которого производится регистрация книги !!!
        dicTgBookComplectData = bkwargs['dicTgBookComplectData']
        
        # Источник текущего книжного комплекта, на базе которого производится регистрация книги
        origSourceId = dicTgBookComplectData['origSourceId']

        
        # G. Внести категории и зарегестрировать книгу по категориям в таблице lib_books_categories 
        # Пока заготовка
        categId = self.check_if_category_exists_and_insert_if_not_to_lib_categories_blm (newAlfaBookId, dicDescrParsing)
        
        
        
        # C. Внести автора и зарегестрировать книгу в таблице lib_books_authors {_ВНЕСЕНИЕ_АВТОРА_В_БД_}
        
        # C.1. Проверить наличие данного автора в таблице 'lib_authors'. Если нет такого автора, то вставить ег ов таблицу и вернуть его id (нового втавленного автора)
        # Если автор найден в таблице 'lib_authors' , то вернуть его id
        # Если несколько авторов с такой фамилией, то сообщить об этом и потребовать ОПЕРАТОРА дя решения неоднозначной проблемы (в этом случае вернуть 
        # authorId = None)
        
        
        
        if 'authorSecondname' in dicDescrParsing and len(dicDescrParsing['authorSecondname']) > 0:
            authorId = self.check_author_by_secondname_and_insert_if_there_is_no_blm(dicDescrParsing) 
        else:
            authorId = None
        
        
        # C.2. В зависимости от возвращения authorId из проверки автора в таблице 'lib_authors' выполнить действия
            # Если вернули число, то это ознаает, что автора найден или внесен и потом найден и возвращает его ID в табл 'lib_authors' 
            # А если None, то это означает. что надйено несколько авторов с заданной фамилией и система требует дальнейшего вмешательство 
            # (может требует вмешательсво оператора)
            
            
        # Если получили какое-то конкретное значение author_id, то это означает. что надо вставить и зарегестрировать автора книги и книгу 
        # в таблицу 'lib_books_authors' {CURRENT_POINT 04-02-2024 !!! }
        if not authorId: 
            pass
            print(f"""PR_A247 --> SYS LOG: Система не определила автора. Книга зарегестрирована не до конца. Необходимо закончить регистрацию, присвоив автора 
                для этой книги Книге  присвоен статус - незаконченная регистрация по автору. Продолжаем заполнение данных книги в таблице расширения книги""")
            
            bookstatus = 2 # UNREGISTERED_DUE_AUTHOR
            self.add_new_alfa_book_status(newAlfaBookId, bookstatus) 
        
        else:
            pass
            print(f"PR_A290 --> SYS LOG: Автор книги найден с author_id = {authorId}. Продолжаем заполнение данных книги в таблице расширения книги")
            
            
            # B. Создать запись в таблице 'lib_books_alfa_ext' с 'books_alfa_id' равным ID новой книге и наполнить ее всеми
            # известными данными о регестрируемой книге, находящимися в словаре данных книги dicRegisterBookData и в словаре парсинга dicDescrParsing
            
            #PARS
            dicInsertData = {
                'book_alfa_id' : newAlfaBookId,
                'author_id' : authorId,
                'bool_orig_source_id' : origSourceId,
                    }
            
            # Вставить связку IDs автора и книги в таблицу регистрации связей многие-ко-многим 'lib_books_authors'
            self.sps.insert_record_to_tb_with_many_to_many_relation (ms.TB_LIB_BOOKS_AUTHORS, dicInsertData)

        
                # ini НЕ УДАЛЯТЬ ПОКА!!!
        # dicRegisterBookData :
        # """  
        #             'id': 499, 
        #             'channels_ref_id': 1, 
        #             'message_own_id': 4209, 
        #             'message_type_ref_id': 1, 
        #             'message_proc_status_ref_id': 3, 
        #             'date_reg_calend': '03-02-2024 13:51:50', 
        #             'date_reg_unix': 1706968310.0, 
        #             'date_executed_calend': None, 
        #             'date_executed_unix': None, 
        #             'message_proceeded_ref_id': 507, 

        #             'message_text': 'Герой Земли. Алексей Губарев\n\n#губарев #космическаяфантастика #попаданцы\n\nПоддержать канал (Сбербанк) 4276600049341072\n\nГоворят, сапёр ошибается один раз. Подрыв вражеского фугаса отправил меня, Андрея Базилевского, в небытиё.\nОчнулся в герметичной капсуле, стремительно несущейся в космосе. На предплечье высокотехнологичный наруч, а безэмоциональный голос ИИ твердит прямо в ухо:\n– Для погашения долга перед корпорацией вы отправлены в зону А-1.\nИнструкции получите после приземления.\nКакого лешего?!\nАрмейский юмор, самоирония, и проклятая, чтоб её, аномалия, где даже укус насекомого может изменить тебя. Изменить не в лучшую сторону.\nА тут ещё странный шёпот…\nХочешь выжить? Плати!\nИ почему в аномалии постоянно попадаются следы, оставленные соотечественниками?\nЧтец: #Курнаев Сергей #Троицкий Олег', 

        #             'message_img_loded_path': 'None', 
        #             'message_img_name': '4209_msg_photo_03_02_2024_13_51_50.jpg', 
        #             'message_document_loded_path': None, 
        #             'message_document_name': None, 
        #             'message_document_size': nan, 
        #             'book_language': 1
        # """
        
        
        
        

        
        # J. Внести диктора и зарегестрировать книгу в таблице lib_books_narrators {_ВНЕСЕНИЕ_ ДИКТОРА_В_БД_}
        
        # J.1. Проверить наличие данного диктора в таблице 'lib_narrators'. Если нет такого диктора, то вставить его в таблицу и вернуть его id (нового втавленного диктора)
        # Если диктор найден в таблице 'lib_narrators' , то вернуть его id
        # Если несколько дикторов с такой фамилией, то сообщить об этом и потребовать ОПЕРАТОРА для решения неоднозначной проблемы (в этом случае вернуть 
        # narratorId = None)
        
        
        print(f"PR_A731 --> dicDescrParsing = \n{dicDescrParsing}")
        
        # narratorId = self.check_narrator_by_secondname_and_insert_if_there_is_no_blm(dicDescrParsing)       
        
        
        if 'narratorSecondname' in dicDescrParsing and len(dicDescrParsing['narratorSecondname']) > 0:
            narratorId = self.check_narrator_by_secondname_and_insert_if_there_is_no_blm(dicDescrParsing) 
        else:
            narratorId = None
        
        # J.2. В зависимости от возвращения narratorId из проверки диктора в таблице 'lib_narrators' выполнить действия
            # Если вернули число, то это ознаает, что диктора найден или внесен и потом найден и возвращает его ID в табл 'lib_narrators' 
            # А если None, то это означает. что надйено несколько дикторов с заданной фамилией и система требует дальнейшего вмешательство 
            # (может требует вмешательсво оператора)
            
            
        # Если получили какое-то конкретное значение narrator_id, то это означает. что надо вставить и зарегестрировать диктора книги и книгу 
        # в таблицу 'lib_books_narrators' {CURRENT_POINT 04-02-2024 !!! }
        if not narratorId: 
            
            print(f"""PR_A729 --> SYS LOG: Система не определила диктора. Книга зарегестрирована не до конца. Необходимо закончить регистрацию, присвоив диктора 
                для этой книги Книге  присвоен статус - незаконченная регистрация по диктору. Продолжаем заполнение данных книги в таблице расширения книги""")
            
            bookstatus = 4 # UNREGISTERED_DUE_NARRATOR
            self.add_new_alfa_book_status(newAlfaBookId, bookstatus) 
        
        else:
            pass
            print(f"PR_A730 --> SYS LOG: Диктор книги найден с narrator_id = {narratorId}. Продолжаем заполнение данных книги в таблице расширения книги")
            
            
            # B. Создать запись в таблице 'lib_books_alfa_ext' с 'books_alfa_id' равным ID новой книге и наполнить ее всеми
            # известными данными о регестрируемой книге, находящимися в словаре данных книги dicRegisterBookData и в словаре парсинга dicDescrParsing
            
            #PARS
            dicInsertData = {
                'book_alfa_id' : newAlfaBookId,
                'narrator_id' : narratorId,
                'bool_orig_source_id' : origSourceId,
                    }
            
            # Вставить связку IDs автора и книги в таблицу регистрации связей многие-ко-многим 'lib_books_authors'
            self.sps.insert_record_to_tb_with_many_to_many_relation (ms.TB_LIB_BOOKS_NARRATORS, dicInsertData)
        
        
                
                
        # D. Создать запись в таблице 'lib_books_alfa_ext' и наполнить ее всеми известными данными
        
        print(f"PR_A311 --> dicFullBookData = {dicFullBookData}")
        
        # SQL_INI 
        booksAlfaId = newAlfaBookId # 'books_alfa_id' ID созданной новой книги из табл 'lib_books_alfa', котрую нужно расширить всеми необходимыми данными в табл lib_books_alfa_ext
        bookTitle = dicDescrParsing['bookTitle'] # 'book_title' Название книги
        bookDescription = dicDescrParsing['description'] # 'book_description' Описание книги
        # Путь к картинке книги (это все в формате только данного канала CH_01 'Аудиокниги фагьастика'. В форматах других канадов может быть совсем другой 
        # формат и может быть несколько картинок в описании книги или вообще не быть)
        bookImgName = dicTgRegisterBookData['message_img_name'] # 'book_img'
        
        dateIssueCalend = '' # 'date_issue_calend' Дата выпуска первого тома книги (этих данных может и не существовать)
        dateIssueUnix = None # 'date_issue_unix' Это конвертация календарной даты date_issue_calend в числовой формат, что бы можно было осуществлять поиск с условиями по дате выпуска
        
        languageId = dicTgRegisterBookData['book_language'] # 'language_id' Язык книги
        
        serialId = None # 'serial_id' Название сериала книги
        
        languageRelationId = None # 'language_relation_id' Рекурсиваня связь с зарегестрированной книгой, тождественной этой, но на другом языке
        
        dateissuedcalend = dicDescrParsing['dateissuedcalend']
        
        bookMessageId = dicTgRegisterBookData['message_own_id'] 
        
        # Если есть календарнаядата издания, то перевести ее в UNIX формат для поискоа потом
        if dateissuedcalend != "NULL": # "NULL" для этого поля - дефолт словаря
            pass
        
        
        
        sql = f"""
        INSERT INTO {ms.TB_LIB_BOOKS_ALFA_EXT} 
        (
            books_alfa_id,
            book_title,
            language_id,
            book_description,
            date_issue_calend,
            book_message_id,
            book_orig_source_id
            
            
            ) 
        VALUES (
        {booksAlfaId},
        '{bookTitle}',
        {languageId},
        '{bookDescription}',
        '{dateissuedcalend}',
        {bookMessageId},
        {origSourceId}
        
        
        )
        """
        
        # print(f"PR_A237 --> sql = {sql}")


        try:
            self.sps.execute_sql_SPS(sql)
            
            print(f"PR_A295 --> SYS LOG: Внесена расширяющая запись в таблицу 'lib_books_alfa_ext' для альфа-книги по запросу : \n{sql}")
            
        except Exception as err:
            print(f"PR_A238 --> SYS LOG: Не внесена запись в таблицу 'lib_books_alfa_ext' по запросу : \n{sql}")
            
            sys.exit(err)
            
            
            
            
        # M. Проанализировать , является ли образующее описание книги сообщение-картинка является группой.
        # Если является,  то найти все картинки-сообщения группы этог сообщения, создать записи с ними в табл  'lib_book_images'
        # и присвоить эти созданные картинки книге с alfaId
        
        # Id сообщений описания текущего книжного комплекта
        bookMessageId = dicTgBookComplectData['book']
        
        print(f"PR_B118 --> bookMessageId = {bookMessageId}")
        
        # origSourceId = self.blf.get_book_source_id_by_alfa_id_blf(booksAlfaId)
        
        # 
        # Текцший табличный id сообщения-картинки регестрируемой и присваиваемой текущей книге, которую регестриуем
        messageTbID = self.blf.get_tg_proceed_tbid_by_message_id_and_source_id_blf(origSourceId, bookMessageId)
        
        
        
        
        # Определить образующее описание книги сообщение в книжном коплекте является ли групповым? То есть 
        # если оно принадлежит, то просто является первым в группе картинок, которые так же относятся к описанию книги 
        # и их нужно присвоить текущему описанию книги. 
        if self.blf.if_tg_message_belongs_to_message_group_objects_blf(messageTbID):
            
            
            # Получить идентификатор группы groupedId , исользуя сообщение с описанием книги, которое является доказанно групповым
            messageGroupedId = self.blf.get_tg_message_grouped_id_if_any_by_mssg_tbid_blf(messageTbID)
            
            print(f"PR_B115 --> messageGroupedId = {messageGroupedId}")
            
            # Получить все картинки-сообщения, принадлежащие группе с идентификатором = messageGroupedId
            
            messagesTbIdsOfGivenGroup = self.tlf.obtain_all_messages_ids_with_given_grouped_id_tlf(messageGroupedId)
            
            print(f"PR_B116 --> messagesTbIdsOfGivenGroup = {messagesTbIdsOfGivenGroup}")
            
            
            # Цикл по группе картинок, которые все надо присвоить текущей создаваемой книге с альфа-id = booksAlfaId
            for messagePhotoGroupTbid in messagesTbIdsOfGivenGroup:
                
                # print(f"PR_B116 --> POINT B")
            
                # Поулчаем данные для присваивания картинки к регестрируемой книге по сообщению по его 
                # табличному id = messagePhotoGroupTbid
                
                # # id источника текущего сообщения
                # mssgSourceId = self.tlf.get_messsage_orig_source_id_by_its_tbid_tlf(messagePhotoGroupTbid)
                
                # # id текущего сообщения в ТГ-канале
                # tgMessageId = self.tlf.get_tg_messsage_id_by_its_tbid_tlf(messagePhotoGroupTbid)
                
                # Данные по текущей регестрируемой еартинке-сообщению из табл 'tg_messages_proceeded' и 'tg_message_proceeded_ext'
                tlf = TgLocalFuncs()
                dicTgMessageData = tlf.get_dic_tg_book_data_by_tbid_tlf(messagePhotoGroupTbid)
                
                print(f"PR_B122 --> dicTgBookData = ")
                pp(dicTgMessageData)
                
                # Создать запись по регестрируемой картинке в табл 'lib_book_images'  и присвоить картинку книге в табл 'lib_books_images'
                self.blf.assign_image_to_being_registered_alfa_book_blf (booksAlfaId, dicTgMessageData, **bkwargs)
                
                
            
        # Если - не групповая, то все происходит как и раньше и присваивается всего одна, основная картинка к описанию к книге 
        else:
            # H. EXECUTE SQL!!! Занести картинки книги в таблицу 'lib_book_images' и 'lib_books_images'
            # self.blf.assign_image_to_given_alfa_book_blf (booksAlfaId, bookImgName, **bkwargs)
            
            # Данные по текущей регестрируемой еартинке-сообщению из табл 'tg_messages_proceeded' и 'tg_message_proceeded_ext'
            dicTgMessageData = self.tlf.get_dic_tg_book_data_by_tbid_tlf(messageTbID)
            
            print(f"PR_B133 --> dicTgBookData = ")
            pp(dicTgMessageData)
        
            # Создать запись по регестрируемой картинке в табл 'lib_book_images'  и присвоить картинку книге в табл 'lib_books_images'
            self.blf.assign_image_to_being_registered_alfa_book_blf (booksAlfaId, dicTgMessageData, **bkwargs)
            
    
        
            


        # E. Простаавить статус книги ЗАРЕГЕСТРИРОВАНА
        bookstatus = 1 # REGISTERED
        self.add_new_alfa_book_status(newAlfaBookId, bookstatus) 
        
        print(f"PR_A281 --> END: extend_new_alfa_book_with_data_blm()")

        



    
    def register_new_book_in_libba_blm (self, dicFullBookData, **bkwargs):
        """ 
        BookLibraryManager
        Создание новой книги в библиотеке на основе словаря книги с данными по ней
        dicFullBookData - словарь со всеми необходимыми данными по книге для ее создании и регистрации в библиотеке BIBLIO
        
        """
        print(f"PR_A276 --> START: register_new_book_in_biblio_blm()")
        
        
        #INI
        
        # origSourceId = bkwargs['origSourceId'] # соотвтетсвует ТГ каналу "Аудиокниги фантастика" из таблицы 'lib_orig_sources'

        # A. Создать новую пустую запись в Альфа-книге (таблица 'lib_books_alfa'), для того, что бы получить уникальный идентификационный номер книги, который
        # равен автоинкременту по ключу таблицы в поле 'id'
        
        dtStringFormat1, currCalDateTime, currUnixTime = FG.get_current_time_format_1_and_2_and_universal_unix()
        
        # INI
        # Тип создания сущности книги и томов. Задается во View: register_book_complects_in_libba ()
        bookCreationType = bkwargs['bookCreationType']

        # Получить новый идентификационный уникальный номер для присваивания новой книге
        sql = f"INSERT INTO {ms.TB_LIB_BOOKS_ALFA} (date_reg_calend, date_reg_unix, btype_creation_id) VALUES ('{currCalDateTime}', {currUnixTime}, {bookCreationType})" 
        
        
        try:
        
            self.sps.execute_sql_SPS(sql)
            
        except Exception as err:
            
            print(f"PR_A423 --> SYS LOG: ERROR !!! while INSERT in table '{ms.TB_LIB_BOOKS_ALFA}': {err}")
        
        
        
        
        # Получить последний автоинкрементный номер ключевого поля id в таблице lib_books_alfa
        newBookId = self.sps.get_last_inserted_id_in_db_mysql_sps()
        
        print(f"PR_A212 --> SYS LOG: Создана альфа-запись для регистрации новой книги в таблице {ms.TB_LIB_BOOKS_ALFA} с ID =  {newBookId}")
        
        
        # B. Присвоить книге все необходимые  группы литеров (группы литеров xGroup, yGroup, zGroup). Литер-группа zGroup является отображением 
        # уникального индивидуального номера книги (который в свою очередь является автоинкрементным ключем таблицы в поле 'id')
        # zGroup - это стринг из 10 разрядов нулей, где справа разряды замещаются идентификатором-ключем книги в автоинкрементном поле 'id' таблицы 'lib_books_alfa'
        # xGroup и yGroup - пока эти литеры являются 3х разрядовыми стрингами с нулями (в далльнейшем они будут нести какую-то смысловую составляющую)
        # А так же этот метод формирует из гропп-литеров конечный уникальный индивидуальный серийный номер книги в библиотек ILBN (Individual Library Book Number) 
        # в поле 'final_ilbn'  талицы lib_books_alfa
        # Все литеры и окончательный ILBN прописываются в только что созданной новой записи регистрации книги в таблице lib_books_alfa
        # pars
        xGroup = '000'
        yGroup = '000'
        self.prepare_and_set_ilbn_to_alfa_book_row_based_on_book_id_lfdb_blm(newBookId, xGroup, yGroup)
        
        
        # C. Расширить новую созданную книгу в таблице 'lib_books_alfa' всеми данными из словаря данных регистрируемой книги dicRegisterBookData. 
        # Создать запись в таблице 'lib_books_ext', которая является расширением альфа-книги , и прописать в ней все необходимые данные по регестрируемой 
        # книге из словаря dicRegisterBookData
        self.extend_new_alfa_book_with_data_blm (newBookId, dicFullBookData, **bkwargs)
        

        print(f"PR_A277 --> END: register_new_book_in_biblio_blm()")
        
        return newBookId

        
        


    def check_if_category_exists_and_insert_if_not_to_lib_categories_blm (self, bookAlfaId, dicDescrParsing):
        """ 
        Проверить существует категория и вставить, если не существует
        ПРИМ: Так как категории будут переименовываться, то нужно будет создать таблицу ассоциаций изначальных и переименованных категорий. Таблица ассоциаций
        может быть многие-ко-многим. То есть категория измененная - одна, а исходные названия категорий в разных каналах может быть разная, но переименовываться
        они будут кк одной категории в сотвтетсвии с этой таблицой
        Переименование категорий и заполнение этой таблице должны производиться в специальном редакторе переименований. ПРОДУМАТЬ
        """

        # print(f"PR_A910 --> bookAlfaId = {bookAlfaId}")
        
        
        # print(f"PR_A913 -->  dicDescrParsing")
        
        # pp(dicDescrParsing)
        
        # bookMessageId  регестрируемой книги
        bookMessageId = dicDescrParsing['message_own_id']
        
        # print(f"PR_A911 --> bookMessageId = {bookMessageId}")
        

        categories = dicDescrParsing['categories']
        
        # print(f"PR_A675 --> categories = {categories}")
        
        
        
        # Цикл по категориям 
        
        for categ in categories:
            
            
            print(f"PR_A916 --> [{bookMessageId}] : for categ in categories")
            
            # # Получить списки существующих категорий и переводов категорий в переводчике категорий из таблиц 'lib_categories' и 'lib_book_categories_vocabulary'
            # listExistsCategories, listExistsCategoriesVocabulary = self.blf.obtain_lists_of_lib_categories_and_categ_translations_in_vocabulary_blf()
            # print(f"PR_A923 --> listExistsCategories = {listExistsCategories}")
            # print(f"PR_A924 --> listExistsCategoriesVocabulary = {listExistsCategoriesVocabulary}")


            # A. Првоерить наличие такой категории сначала в табл lib_categories. Если найдено, то присвоить этот categId по данной книге в таблицу 
            # lib_books_categories
            # if PandasManager.if_value_exists_in_df_column_values_static(dfCategories, 'category', categ):
            
            # очистка
            categ = categ.strip(' ')
            
            if self.spps.if_value_exists_in_tb_given_column_auto_sql_df_spps(ms.TB_LIB_CATEGORIES, 'category', categ):
            
                print(f"PR_A676 --> SYS LOG: В таблице lib_categories найдено значение категории  {categ} (из парсинга для новой книги с mssgId = {bookMessageId}). Присваиваем книге данную категорию")
                
                df = self.spps.read_table_auto_sql_to_df_mysql_spps (ms.TB_LIB_CATEGORIES)
                
                categoryId = PandasManager.get_val_of_column_cell_by_val_of_key_column_stat_pandas(df, 'category', categ, 'id')
                
                
            # B. Если не найдено в A. , то ищем в табл lib_book_categories_vocabulary. Если в тут найдено значение, то тоже имеем id из поля categ_id и 
            # присваиваем lib_books_categories
            elif self.spps.if_value_exists_in_tb_given_column_auto_sql_df_spps(ms.TB_LIB_BOOK_CATEGORIES_VOCABILARY, 'categ_translate', categ):
            
                print(f"PR_A677 --> SYS LOG: В таблице lib_book_categories_vocabulary найдено значение категории  {categ} (из парсинга для новой книги с mssgId = {bookMessageId}). Присваиваем книге данную категорию")
            
                df = self.spps.read_table_auto_sql_to_df_mysql_spps (ms.TB_LIB_BOOK_CATEGORIES_VOCABILARY)
                
                categoryId = PandasManager.get_val_of_column_cell_by_val_of_key_column_stat_pandas(df, 'categ_translate', categ, 'categ_id')
            
            
            # C. Если не найдены в обоих таблицах, значит вносим эту новую категорию в таблицу lib_categories. Получаем новый id и присваиваем 
            # !!! EXECUTE INSERT to lib_books_categories new category
            else: 
                
                print(f"PR_A678 --> SYS LOG: В таблицах lib_categories и lib_book_categories_vocabulary НЕ найдено значение категории  {categ} (из парсинга для новой книги с mssgId = {bookMessageId}). Создаем новую категорию и присваиваем ее")
                
                categoryId = self.blf.create_new_category_in_tb_lib_categories_blf (categ)
        
        
        
            # D. Вставить запись по текущей распознанной категории книги в таблицу lib_books_categories ->> book_alfa_id <-> category_id, присваиявая этим книге 
            # данную категорию
            # !!! EXECUTE INSERT to lib_books_categories new category
            self.blf.assign_the_category_to_the_book_blf (bookAlfaId, categoryId)
        
        
        



    def check_author_by_secondname_and_insert_if_there_is_no_blm (self, dicDescrParsing ):
        """ 
        Входной параметр - словарь парсинга с данынми по книге, включая имяи фамилие автора
        Проверить наличие автора в таблице 'lib_authors'. Если такого автора нет, то внести  его в таблицу. Вернуть author_id.
        Елси автора с такой фамилией нет. то внести его в БД в таблицу 'lib_authors'
        Если авторов по фамилии несколько. то сообщить об этом и больше ничего не делать
        """

        print(f"PR_A282 --> START: check_author_by_secondname_and_insert_if_there_is_no_blm()")

        # INI
        authorSecondname = dicDescrParsing['authorSecondname']
        authorFirstname = dicDescrParsing['authorFirstname']
        # authorFullName = f"{authorFirstname} {authorFirstname}"
        
        sql = f"SELECT * FROM {ms.TB_LIB_AUTHORS} WHERE author_second_name = '{authorSecondname}' "
        
        print(f"PR_A240 --> sql = {sql}")
        
        
        # # df из sql-запроса по табл 'lib_authors' с заданной фамилией автора. for SQLite
        # dfAuthorsByGivenSurname = self.spps.read_sql_to_df_pandas_SPPS(sql)
        
        # df из sql-запроса по табл 'lib_authors' с заданной фамилией автора. for MySQL
        dfAuthorsByGivenSurname = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        
        rowsQn = len(dfAuthorsByGivenSurname) # Кол-во рядов в фрейме
        
        # C.2. В зависимости от кол-ва рядов выполняем разные алгоритмы, связанные с внесением автороа в БД 
        
        
        
        # Если кол-во рядов в фрейме = 0, то это значит этого автора (поиск был по фамилии) - нет в таблице 'lib_authors'. Значит надо внести этого автора
        if rowsQn == 0:
            
            # print(f"PR_A242 --> Автор {authorFullName} не найден в таблице авторов 'lib_authors'")
            
            # TODO: {FUNCS} создать метод внесения автора в таблицу 'lib_authors'
            
            # Вставить нового автора в таблицу 'lib_authors'
            authorId = self.blf.insert_new_author_to_book_library_db_blf(authorFirstname, authorSecondname)
            
            print(f"PR_A245 --> authorId = {authorId}")

                
        # Если кол-во рядов во фрейме = 1, то это значит, что данный автор уже присутствует в таблице  'lib_authors'.
        # В этом случае автора вносить не надо, а надо просто взять его id из таблицы, что бы далее присвоить книге этого автора в таблицу 'lib_books_authors' (зарегестрировать)
        elif rowsQn == 1: 

            # Получить словарь по единственному ряду фрейма
            dic = PandasManager.get_dict_from_df_with_only_one_row_stat_pm(dfAuthorsByGivenSurname)
            
            # print(f"PR_A244 --> dic = {dic}")
            
            # ID автора в таблице 'lib_authors'
            authorId = dic['id']
            
            print(f"PR_A246 --> authorId = {authorId}")
            
                    
        
        # Если в фрейме поиска по фамилии автора больше, чем один ряд, то это значит, что есть несколько авторов с одной и той же фамилией. и необходимо 
        # вмешательство опреатора. Это надо внести в Log проекта. что бы потом обработать в ручную данную книгу в смысле автора
        else: 
            pass
            print(f"PR_A294 --> SYS LOG: В таблице 'lib_authors' найдено несколько авторов с одной и той же фамилией. необходимо вмешательство оператора")
        
            authorId = None
            
            
            
        # C.3.  Если authorId НЕ None, значит вставляем (регестрируем) книг-автора в таблице 'lib_books_authors' {CURrENT 03-02-2024 !!!}
        
        if authorId: # Если authorId НЕ None
            pass
        else:
            pass
            
            
        print(f"PR_A283 --> END: extend_new_alfa_book_with_data_blm()")


        print(f"PR_A293 --> END: check_author_by_secondname_and_insert_if_there_is_no_blm()")


            
        return authorId
    
    
    
    
    
    
    
    def check_narrator_by_secondname_and_insert_if_there_is_no_blm (self, dicDescrParsing ):
        """ 
        Входной параметр - словарь парсинга с данынми по книге, включая имяи фамилие диктора
        Проверить наличие диктора в таблице 'lib_narrators'. Если такого диктора нет, то внести  его в таблицу. Вернуть narrator_id.
        Елси диктора с такой фамилией нет. то внести его в БД в таблицу 'lib_narrators'
        Если диктора по фамилии несколько. то сообщить об этом и больше ничего не делать
        """

        print(f"PR_A722 --> START: check_narrator_by_secondname_and_insert_if_there_is_no_blm()")

        # INI
        narratorSecondName = dicDescrParsing['narratorSecondname']
        narratorFirstName = dicDescrParsing['narratorFirstname']
        # authorFullName = f"{authorFirstname} {authorFirstname}"
        
        sql = f"SELECT * FROM {ms.TB_LIB_NARRATORS} WHERE narrator_second_name = '{narratorSecondName}' "
        
        # # df из sql-запроса по табл 'lib_authors' с заданной фамилией автора. for SQLite
        # dfAuthorsByGivenSurname = self.spps.read_sql_to_df_pandas_SPPS(sql)
        
        # df из sql-запроса по табл 'lib_narrator' с заданной фамилией диктора. for MySQL
        dfNarratorsByGivenSurname = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        
        rowsQn = len(dfNarratorsByGivenSurname) # Кол-во рядов в фрейме
        
        # C.2. В зависимости от кол-ва рядов выполняем разные алгоритмы, связанные с внесением диктора в БД 
        
        print(f"PR_A723 --> rowsQn = {rowsQn}")
        
        # Если кол-во рядов в фрейме = 0, то это значит этого диктора (поиск был по фамилии) - нет в таблице 'lib_narrators'. Значит надо внести этого  диктора
        if rowsQn == 0:
            
            # print(f"PR_A242 --> Автор {authorFullName} не найден в таблице авторов 'lib_authors'")
            
            # TODO: {FUNCS} создать метод внесения автора в таблицу 'lib_authors'
            
            # Вставить нового автора в таблицу 'lib_authors'
            narratorId = self.blf.insert_new_narrator_to_book_library_db_blf(narratorFirstName, narratorSecondName)
            
            print(f"PR_A724 --> narratorId = {narratorId}")

                
        # Если кол-во рядов во фрейме = 1, то это значит, что данный автор уже присутствует в таблице  'lib_authors'.
        # В этом случае автора вносить не надо, а надо просто взять его id из таблицы, что бы далее присвоить книге этого автора в таблицу 'lib_books_authors' (зарегестрировать)
        elif rowsQn == 1: 

            # Получить словарь по единственному ряду фрейма
            dic = PandasManager.get_dict_from_df_with_only_one_row_stat_pm(dfNarratorsByGivenSurname)
            
            # print(f"PR_A244 --> dic = {dic}")
            
            # ID автора в таблице 'lib_authors'
            narratorId = dic['id']
            
            print(f"PR_A725 --> narratorId = {narratorId}")
            
                    
        
        # Если в фрейме поиска по фамилии автора больше, чем один ряд, то это значит, что есть несколько авторов с одной и той же фамилией. и необходимо 
        # вмешательство опреатора. Это надо внести в Log проекта. что бы потом обработать в ручную данную книгу в смысле автора
        else: 
            pass
            print(f"PR_A726 --> SYS LOG: В таблице 'lib_narrators' найдено несколько дикторов с одной и той же фамилией. необходимо вмешательство оператора")
        
            narratorId = None
            
            
            
        # C.3.  Если narratorId НЕ None, значит вставляем (регестрируем) книг-дикторав таблице 'lib_books_narrators' {CURrENT 03-02-2024 !!!}
        
        if narratorId: # Если narratorId НЕ None
            pass
        else:
            pass
            
            
        print(f"PR_A728 --> END: check_narrator_by_secondname_and_insert_if_there_is_no_blm()")


            
        return narratorId
    
    

    
    def if_book_title_exists_already (self, bookTitle):
        """ 
        Проверить существует ли название книги в таблице 'lib_books_alfa_ext'
        """
        
        print(f"PR_A275 --> START: if_book_title_exists_already()")

        
        sql = f"SELECT * FROM {ms.TB_LIB_BOOKS_ALFA_EXT} WHERE book_title = '{bookTitle}' "
        
        
        # # Для SQLite
        # df = self.spps.read_sql_to_df_pandas_SPPS(sql)
        
        # Для MySQL
        df = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        
        
        rowsQn = len(df) # Кол-во рядов в фрейме

        # print(f"PR_A250 --> rowsQn = {rowsQn}")
        
        # Если кол-во рядов в фрейме = 0, то это значит 
        if rowsQn == 0:
            
            return False
                
        # Если кол-во рядов во фрейме > 0, то это значит, 
        else : 
            return True
        
        
    
    def get_author_data_by_author_id (self, authorId):
        """ 
        Поулчить данные по автору по его id в таблице 'lib_authors'
        """
        
        print(f"PR_A285 --> START: get_author_data_by_author_id()")

        
        sql = f"SELECT * FROM {ms.TB_LIB_AUTHORS} WHERE id = {authorId}"
        
        print(f"PR_A258 --> sql = {sql}")
        
        df = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        print(f"PR_A257 --> df = {df}")
        
        rowsQn = len(df) # Кол-во рядов в фрейме. НЕ УДАЛЯТЬ, пригодится в будущем
        
        if rowsQn > 0:
        
            dicAuthor = PandasManager.get_dict_from_df_with_only_one_row_stat_pm (df)
            
        else:
            dicAuthor = -1
            
        print(f"PR_A286 --> END: get_author_data_by_author_id()")

        
        return dicAuthor
        
        
        
    def get_authors_of_book_with_given_title (self, bookTitle):
        """ 
        Получить авторов книги по ее названию
        """
        
        print(f"PR_A287 --> START: get_authors_of_book_with_given_title()")

        
        bookId = self.get_book_id_by_book_title (bookTitle)
        
        sql = f"SELECT * FROM {ms.TB_LIB_BOOKS_AUTHORS} WHERE book_alfa_id = {bookId}"
        
        df = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        rowsQn = len(df) # Кол-во рядов в фрейме. НЕ УДАЛЯТЬ, пригодится в будущем
        
        if rowsQn == 0: 
            pass
        elif rowsQn == 1: # Если автор у книги один
            
            # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(df, True, marker="PR_A256 --> df")
        
            authorId = PandasManager.get_cell_val_by_row_inx_and_col_name(df, 0, 'author_id')
            
            dicAuthor = self.get_author_data_by_author_id (authorId)
            
            
            
        else:
            pass
        
        
        print(f"PR_A288 --> END: get_authors_of_book_with_given_title()")

        
        return dicAuthor
        
        
        
    def get_book_id_by_book_title (self, bookTitle):
        """ 
        Получить id книги по ее названию
        """
        
        sql = f"SELECT * FROM {ms.TB_LIB_BOOKS_ALFA_EXT} WHERE book_title = '{bookTitle}' "
        
        df = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        rowsQn = len(df) # Кол-во рядов в фрейме. НЕ УДАЛЯТЬ, пригодится в будущем
        
        bookId = PandasManager.get_cell_val_by_row_inx_and_col_name(df, 0, 'books_alfa_id')
        
        return bookId
        
        
    

    
        
    
    
    
    def check_if_book_registered_already (self, dicCheckData):
        """ 
        Проверить зарегестрирована ли такая книга уже.
        Проверка на данный момент ведется по названию книги и фамилии ее автора (авторов)
        Данные к проверке dicCheckData = {
            'authorSecondname' : '...',
            'bookTitle' : '...'
        }
        
        """
        
        print(f"PR_A274 --> START: check_if_book_registered_already()")

        
        bookTitleCheck = dicCheckData['bookTitle']
        authorSecondnameCheck = dicCheckData['authorSecondname']
        
        # 1. Проверка по названию книги 
        
        # ПРИМ: TODO: !!! Если в таблице альфа случайно в результате ошибки присутствует книга с названием, зарегестрирован ее автор с одним именем,
        # И заводится новая книга с таким же названием, но другим автором, то система всегда будет сообщать, что книга другая. То есть анализ не 
        # доходит до следующей книги, которая уже была введена с таким же названием, но другим автором. То есть код будет всегда выдавать, что 
        # книга есть по названию, но автор - другой и будет снова регестрировать ее. ИСПРАВИТЬ
        # По сути получается этот метод вообще не работает правильно и не выполняет своих задач !!! 
        
        
        # TODO: еще одно условие - эта проверка может проверять только книжные комплекты, НЕ комплекты томов. А значит, на данный момент, комплкты томов 
        #  должны регестрироваться без этой проверки. То есть те записи, которые в поле alfa-таблицы в поле 'parent_id' имеет какое-то целочисленное
        # значение идут на регистрацию напрямую без проверки этой. ПРИМ: В будущем, возможно, нужно придумать фильтры проверки и для книжных комплектов,
        # но сейчас работаем пока так как описано выше
        
        # этот метод должен проверять список ВСЕХ книг с одним и тем же названием, а не только первую попавшуюся !!!
        # и , возможно, с разными авторами. И среди них всех сверять новую книгу !!! {РЕШЕНИЕ}
        if self.if_book_title_exists_already(bookTitleCheck): # Если True, то название существует 
            pass
            print(f"PR_A251 --> SYS LOG: При проверке ругистрации книги найдена книга с таким же названием: '{bookTitleCheck}'")
            
            # Так как название книги уже существует, проверяем автора книги с таким же названием
            bookId = self.get_book_id_by_book_title(bookTitleCheck)
            print(f"PR_A252 --> SYS LOG: ID найденной зарегестрированной книги : {bookId}")
            
            dicAuthor = self.get_authors_of_book_with_given_title(bookTitleCheck)
            
            # Найденная фамилия автора книги, с которой совпали названия в поиске по названию
            authorSecondname = dicAuthor['author_second_name']
            
            
            if authorSecondnameCheck == authorSecondname : # Если фамилии одинаковы, то значит эта та же самая книга
                print(f"PR_A254 --> SYS LOG: Фамилия автора совпадает с автором книги '{bookTitleCheck}', уже зарегестрированной в базе. Книгу НЕ надо регистрировать")
                return True
            
            else: # Если фамилии НЕ одинаковы, то значит это - другая книга
                print(f"PR_A255 --> SYS LOG: Фамилия автора НЕ совпадает с автором книги '{bookTitleCheck}', уже зарегестрированной в базе. Значит книгу можно регистрировать")
                return False
        
        
        else: # Если False, то название не существует 
            print(f"PR_A253 --> SYS LOG: В базе НЕ найдена книга с таким же названием: '{bookTitleCheck}'. Книгу можно регистрировать")
            return False
        
        
        
        
    
    def get_full_book_data_by_chat_mssg_id_for_CH1 (self, chatMssgId, mssgSourceId):
        """ 
        Получить словарь с полным набором данных по книге, включая данные по парсингу и данные при первичном анализе и загрузке книги с ТГ канала
        Внутри него содержатся (на данный момент) два словаря 
        dicFullBookData['tgChatData'] - словарь с набором данных по описанию книги в ТГ и данных при ее скачивании с ТГ канала
        dicFullBookData['descrParsingData'] - словарь с данными о книге после парсинга ее описания из сообщения в ТГ
        """
        
        print(f"PR_A271 --> START: get_full_book_data_by_chat_mssg_id_for_CH1()")
        
        # Данные по книге в виде словаря: {fieldName : fieldData}
        
        print(f"PR_A308 --> chatMssgId = {chatMssgId}")

        
        dicRegisterBookData = self.tlf.get_dic_book_data_by_chat_message_id_tlf(chatMssgId)
        
        print(f"PR_A914 --> dicRegisterBookData")
        pp(dicRegisterBookData)
        
        # Добавить язык книги в словарь данных книги
        # TODO: Этот параметр должен формироваться на уровне анализа и скачивания с ТГ канала
        dicRegisterBookData['book_language'] = 1 # Русский 
        
        
        
        
        
        # ПАРСИНГ
        # A. Сформировать словарь с полным набором данных по книге, включая данные по парсингу и данные при первичном анализе и загрузке книги с ТГ канала
        
        # Словарь с полным набором данных по книге
        dicFullBookData = {}
        # словарь с данными о книге после парсинга ее описания из сообщения в ТГ
        bookMessageDescriptionCh01 = dicRegisterBookData['message_text'] # Описание книги в оригинале с канала CH_1 ('Аудиокниги фантастика')
        
        
        # переключатель кассеты алгоритма парсинга
        for case in Switch(mssgSourceId):
            
            # Парсинг для ТГ канала с id = 1 / -1001911157001  'Аудиокниги фантастика'
            if case(1): 
                dicFullBookData['descrParsingData'] = TgChatMessagesParsers.parse_book_descr_from_cannel_chat_01_stat_bpm(bookMessageDescriptionCh01)
                break
            
            # Парсинг для ТГ канала с id = 2 / -1001894592463  'Любимая Книга в Дорогу' 
            if case(2): 
                dicFullBookData['descrParsingData'] = TgChatMessagesParsers.parse_book_descr_from_cannel_chat_02_stat_bpm(bookMessageDescriptionCh01)
                break

            if case(): # default
                print('Другое число')
                break
            
            
        
        
        
        
        
        # EBD ПАРСИНГ
        
        
        
        
        # присвоить mssgId словарю с данными по парсингу описания книги message_own_id
        dicFullBookData['descrParsingData']['message_own_id'] = dicRegisterBookData['message_own_id']
        
        # словарь с набором данных по описанию книги в ТГ и данных при ее скачивании с ТГ канала
        dicFullBookData['tgChatData'] = dicRegisterBookData
        
        print(f"PR_A272 --> END: get_full_book_data_by_chat_mssg_id_for_CH1()")

        
        return dicFullBookData
            

        
        

    
    
    
    
    
    



# #######################   II. ВСПОМОГАТЕЛЬНЫЕ  ===============================

    def clear_all_books_records_ties_and_reset_alfa_book_register(self):
        """ 
        BookLibraryManager
        Очистить все записи связанные с регистрацией новых книг и Обнулить регистр таблицы lib_books_alfa выпусков ILBN в БД
        """
        
        # Очистить все записи связанные с регистрацией новых книг и Обнулить регистр таблицы lib_books_alfa выпусков ILBN в БД
        
        # 'lib_books_alfa'
        self.sps.clear_tb_and_reset_autoincrement_to_zero(ms.TB_LIB_BOOKS_ALFA) 
        # 'lib_books_alfa_ext'
        self.sps.clear_tb_and_reset_autoincrement_to_zero(ms.TB_LIB_BOOKS_ALFA_EXT) 
        # 'lib_books_authors'
        self.sps.clear_tb_and_reset_autoincrement_to_zero(ms.TB_LIB_BOOKS_AUTHORS) # а табл 'lib_authors' обнулять НЕ НАДО
        'lib_books_statuses'
        self.sps.clear_tb_and_reset_autoincrement_to_zero(ms.TB_LIB_BOOKS_STATUSES) 
        
        'lib_book_audio_volumes'
        self.sps.clear_tb_and_reset_autoincrement_to_zero(ms.TB_LIB_BOOK_AUDIO_VOLUMES) 
        
        'lib_volumes_volume_statuses' #- очистка статусов [многие-ко-многим] по томам книги
        self.sps.clear_tb_and_reset_autoincrement_to_zero(ms.TB_LIB_VOLUMES_VOLUME_STATUSES) 
        
        'lib_book_images'
        self.sps.clear_tb_and_reset_autoincrement_to_zero(ms.TB_LIB_BOOK_IMAGES) 

        'lib_books_images'
        self.sps.clear_tb_and_reset_autoincrement_to_zero(ms.TB_LIB_BOOKS_IMAGES) 

        






    def trucate_tables_for_book_complects_mysql(self):
        """ 
        BookLibraryManager
        Очистить все записи с обнулением autoincrement field в таблицах бд mysql 'tg_book_complects_ch_01' и 'tg_book_complect_volumes_ch_01'
        """

        # 'tg_book_complect_volumes_ch_01'
        self.sps.truncate_table_mysql_sps(ms.TB_TG_BOOK_COMPLECT_VOLUMES_CH_01) 
        # 'tg_book_complects_ch_01'
        self.sps.truncate_table_mysql_sps(ms.TB_TG_BOOK_COMPLECTS_CH_01) 






    def trucate_tables_for_all_books_records_ties_with_alfa_book_register_mysql(self):
        """ 
        BookLibraryManager
        Очистить все записи связанные с регистрацией новых книг и Обнулить регистр таблицы lib_books_alfa выпусков ILBN в БД
        """
        
        # Очистить все записи связанные с регистрацией новых книг и Обнулить регистр таблицы lib_books_alfa выпусков ILBN в БД
        
        # 'lib_books_alfa'
        self.sps.truncate_table_mysql_sps(ms.TB_LIB_BOOKS_ALFA) 
        # 'lib_books_alfa_ext'
        self.sps.truncate_table_mysql_sps(ms.TB_LIB_BOOKS_ALFA_EXT) 
        # 'lib_books_authors'
        self.sps.truncate_table_mysql_sps(ms.TB_LIB_BOOKS_AUTHORS) # а табл 'lib_authors' обнулять НЕ НАДО
        'lib_books_statuses'
        self.sps.truncate_table_mysql_sps(ms.TB_LIB_BOOKS_STATUSES) 
        
        'lib_book_audio_volumes'
        self.sps.truncate_table_mysql_sps(ms.TB_LIB_BOOK_AUDIO_VOLUMES) 
        
        'lib_volumes_volume_statuses' #- очистка статусов [многие-ко-многим] по томам книги
        self.sps.truncate_table_mysql_sps(ms.TB_LIB_VOLUMES_VOLUME_STATUSES) 
        
        'lib_book_images'
        self.sps.truncate_table_mysql_sps(ms.TB_LIB_BOOK_IMAGES) 

        'lib_books_images'
        self.sps.truncate_table_mysql_sps(ms.TB_LIB_BOOKS_IMAGES) 

        
        
        
        
    def trncate_all_repositories_load_registration_tables(self):
        """ 
        Очистить и обнулить таблицы регистрации выгрузки сообщений 'lib_reposit_books_registr_1' , 'lib_reposit_audio_volumes_registr_1', 
        'lib_books_loaded_to_repositories' и 'lib_audio_volumes_loaded_to_repositories'
        
        # TODO: Использовать цикл по ids репозиториев для автоматизации очистки массива регистрационных таблиц
        # Использовать заготовку blf.get_sll_tg_type_repositories_ids()
        """
        
        # 'lib_audio_volumes_loaded_to_repositories'
        self.sps.truncate_table_mysql_sps(ms.TB_LIB_AUDIO_VOLUMES_LOADED_TO_REPOSITORIES) 
        
        # 'lib_books_loaded_to_repositories' #- очистка статусов [многие-ко-многим] по томам книги
        self.sps.truncate_table_mysql_sps(ms.TB_LIB_BOOKS_LOADED_TO_REPOSITORIES) 
        
        # #'lib_reposit_audio_volumes_registr_1'
        self.sps.truncate_table_mysql_sps(ms.TB_LIB_REPOSIT_AUDIO_VOLUMES_REGISTR_1) 

        # S'lib_reposit_books_registr_1'
        self.sps.truncate_table_mysql_sps(ms.TB_LIB_REPOSIT_BOOKS_REGISTR_1) 

        
        # 'lib_reposit_audio_volumes_registr_2'
        self.sps.truncate_table_mysql_sps(ms.TB_LIB_REPOSIT_AUDIO_VOLUMES_REGISTR_2) 

        # 'lib_reposit_books_registr_2'
        self.sps.truncate_table_mysql_sps(ms.TB_LIB_REPOSIT_BOOKS_REGISTR_2) 

        
        
        
        


    def trucate_registered_book_authors(self):
        """ 
        Очистить и обнулить счетчик в таблице  lib_authors, где хранятся зарегестрированные авторы книг 
        """
        'lib_authors'
        self.sps.truncate_table_mysql_sps(ms.TB_LIB_AUTHORS) 
        


    def trucate_registered_book_narrators(self):
        """ 
        Очистить и обнулить счетчик в таблице  lib_narrators, где хранятся зарегестрированные дикторы книг 
        """
        'lib_narrators'
        self.sps.truncate_table_mysql_sps(ms.TB_LIB_NARRATORS) 
        

    def truncate_lib_books_narrators_blm (self):
        """ 
        Очистить таблицу lib_books_narrators
        """
        
        self.sps.truncate_table_mysql_sps(ms.TB_LIB_BOOKS_NARRATORS) 





    def trucate_tb_lib_categories(self):
        """ 
        Очистить и обнулить счетчик в таблице  lib_categories
        """

        try: 
            self.sps.truncate_table_mysql_sps(ms.TB_LIB_CATEGORIES) 
            print(f"PR_A707 --> SYS LOG: Удалены записи и обнулена таблица 'lib_categories'")
            
        except Exception as err:
            print(f"PR_A708 --> SYS LOG: При выполнении запроса произошла ошибка иа таблица 'lib_categories' не очищена от записей!!!")
            print(f"PR_A709 --> SYS LOG: ERRORR !!! {err}")
            


    def trucate_tb_lib_books_categories(self):
        """ 
        Очистить и обнулить счетчик в таблице  lib_books_categories
        """

        try: 
            self.sps.truncate_table_mysql_sps(ms.TB_LIB_BOOKS_CATEGORIES)
            print(f"PR_A699 --> SYS LOG: Удалены записи и обнулена таблица 'lib_books_categories'")
            
        except Exception as err:
            print(f"PR_A700 --> SYS LOG: При выполнении запроса произошла ошибка иа таблица 'lib_books_categories' не очищена от записей!!!")
            print(f"PR_A701 --> SYS LOG: ERRORR !!! {err}")
            



    def trucate_tb_lib_book_categories_vocabulary(self):
        """ 
        Очистить и обнулить счетчик в таблице  lib_book_categories_vocabulary
        """
        
        try: 
            self.sps.truncate_table_mysql_sps(ms.TB_LIB_BOOK_CATEGORIES_VOCABILARY)
            print(f"PR_A702 --> SYS LOG: Удалены записи и обнулена таблица 'lib_book_categories_vocabulary'")
            
        except Exception as err:
            print(f"PR_A703 --> SYS LOG: При выполнении запроса произошла ошибка иа таблица 'lib_book_categories_vocabulary' не очищена от записей!!!")
            print(f"PR_A704 --> SYS LOG: ERRORR !!! {err}")
            
            
        
        

    def trucate_tg_samples_markers(self):
        """ 
        Очистить и обнулить счетчик в таблице  tg_samples_markers
        """
        
        try: 
            self.sps.truncate_table_mysql_sps(ms.TB_TG_SAMPLES_MARKERS)
            print(f"PR_A766 --> SYS LOG: Удалены записи и обнулена таблица 'tg_samples_markers'")
            
        except Exception as err:
            print(f"PR_A767 --> SYS LOG: При выполнении запроса произошла ошибка иа таблица 'tg_samples_markers' не очищена от записей!!!")
            print(f"PR_A768 --> SYS LOG: ERRORR !!! {err}")
            
            





    def trucate_tbl_lib_objects_removed(self):
        """ 
        Очистить и обнулить таблицу удаленных обьектов lib_objects_removed
        """
        
        try: 
            self.sps.truncate_table_mysql_sps(ms.TB_LIB_OBJECTS_REMOVED)
            print(f"PR_A804 --> SYS LOG: Удалены записи и обнулена таблица 'lib_objects_removed'")
            
        except Exception as err:
            print(f"PR_A805 --> SYS LOG: При выполнении запроса произошла ошибка иа таблица 'lib_objects_removed' не очищена от записей!!!")
            print(f"PR_A806 --> SYS LOG: ERRORR !!! {err}")
            
            









# #######################  END II. ВСПОМОГАТЕЛЬНЫЕ  ===============================




# #######################   III. ПРОСТЕЙЦШИЕ  ===============================

    # def insert_new_author_to_book_library_db (self, authorFirstname, authorSecondname):
    #     """ 
    #     Вставить нового автора в таблицу 'lib_authors'
    #     """
        
    #     authorFullName = f"{authorFirstname} {authorSecondname}" # Полное имя автора
        
    #     sql = f"""INSERT INTO {ms.TB_LIB_AUTHORS} (author_first_name, author_second_name, author_full_name) 
    #                 VALUES ('{authorFirstname}','{authorSecondname}', '{authorFullName}')
    #             """
    #     # Внести данные по автору в таблицу 'lib_authors'
    #     # TODO: сделать try в самом методе self.sps.execute_sql_SPS()
    #     try:
    #         self.sps.execute_sql_SPS(sql)
    #         print(f"PR_A243 --> SYS LOG: Автор {authorFullName} внесен в таблицу автоматически")
            
            
    #         # Получить Id последней внесенной записи в табл 'lib_authors', которая будет соответствовать автору обрабатываемой книги. for mysql
    #         newAuthorId = self.sps.get_last_inserted_id_in_db_mysql_sps ()
            
    #         print(f"PR_A424 --> SYS LOG: newAuthorId = {newAuthorId}")
                
    #     except Exception as err:
    #         print(f"PR_A241 --> SYS LOG: В результате !!! ОШИБКИ !!! автор не внесен в таблицу 'lib_authors' по запросу : \n{sql}")
            
    #         print(f"PR_A425 --> SYS LOG: Exception -> {err}")
            
    #         newAuthorId = -1
            
    #         # TODO: Ввести систему логов в текстовые файлы. Их форматы
    #         # Внести в проектный лог, что по этой книге и этому файлу не внесен автор. в дальнейшем, чтобы эти логи показывали, где надо вмешаться на уровне оператора библиотеки
            
    #     # # Получить Id последней внесенной записи в табл 'lib_authors', которая будет соответствовать автору обрабатываемой книги. for sqlite
    #     # authorId = self.sps.get_last_rowid_from_tb_sps (ms.TB_LIB_AUTHORS)

    #     return newAuthorId
    
        
        




        
        
        
        
        
        
        
        
        
        
        
    def add_new_alfa_book_status (self, bookId, bookStatus):
        """ 
        OBSOLETED: Использовать assign_the_status_to_the_book_blf()
        Добавить новый статус bookStatus для книги c id = bookId в таблице 'lib_books_alfa'
        """
        print(f"PR_A291 --> START: add_new_alfa_book_status()")

        dicInsertData = {
            'book_alfa_id' : bookId,
            'book_status_id' : bookStatus
        }
        self.sps.insert_record_to_tb_with_many_to_many_relation(ms.TB_LIB_BOOKS_STATUSES, dicInsertData)

        
        print(f"PR_A249 -->  SYS DB LOG: присвоен новый статус {bookStatus} для книги с id = {bookId}")

        print(f"PR_A292 --> END: add_new_alfa_book_status()")




# #######################  END III. ПРОСТЕЙЦШИЕ    ===============================



    def get_list_book_audio_volums_by_own_mssg_id(self, bookMssgId, **bkwargs):
        """ 
        получить список списков со значениями данных book_audio_volums_by_own_mssg_id
        """
        
        # C. Регистрация аудио-томов книги
        
        sql = f"""
        SELECT * FROM 
                {ms.TB_TG_BOOK_COMPLECT_VOLUMES_CH_01} AS bcv, 
                {ms.TB_MSSGS_PROCEEDED_} AS mp, 
                {ms.TB_MSSGS_PROCEEDED_EXT_} AS mpe,
                {ms.TB_TG_BOOK_COMPLECTS_CH_01} AS bc
            WHERE 
                mp.id = mpe.message_proceeded_ref_id AND bcv.volume_msg_id = mp.message_own_id AND bc.id = bcv.book_complect_id_ref AND bc.book_msg_id = {bookMssgId}
        """
        
        
        # print(f"PR_A371 --> sql = {sql}")
    
        listBookVolumes = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        # dfBookVolumes = self.spps.read_sql_to_df_pandas_SPPS(sql)
        
        # dicBookVolumes = PandasManager.read_df_with_one_row_to_dic_stat_pm(dfBookVolumes)
        
        return listBookVolumes



    def get_list_of_dicts_book_audio_volums_by_own_mssg_id(self, bookMssgId, **bkwargs):
        """ 
        Получить список словарей с данными book_audio_volums, где ключами являются названия полей в фрейме, а значениями - значения полей в фрейме по колонкам фрейма
        """
        
        # C. Регистрация аудио-томов книги
        
        sql = f"""
        SELECT * FROM 
                {ms.TB_TG_BOOK_COMPLECT_VOLUMES_CH_01} AS bcv, 
                {ms.TB_MSSGS_PROCEEDED_} AS mp, 
                {ms.TB_MSSGS_PROCEEDED_EXT_} AS mpe,
                {ms.TB_TG_BOOK_COMPLECTS_CH_01} AS bc
            WHERE 
                mp.id = mpe.message_proceeded_ref_id AND bcv.volume_msg_id = mp.message_own_id AND bc.id = bcv.book_complect_id_ref AND bc.book_msg_id = {bookMssgId}
        """
        
        

        
        # # Для SQLite
        # df = self.spps.read_sql_to_df_pandas_SPPS(sql)
        
        # Для MySQL
        dfBookVolumes = self.spps.read_sql_to_df_pandas_mysql_spps(sql)

        
        
        # Список словарей, соотыеттсвующих каждому ряду заданного фрейма, где ключами являются названия полей фрейма (которые тождественны названию полей исходной 
        # таблицы)
        listDfRowsDicts = PandasManager.read_multiple_rows_df_to_list_of_row_dictionaries_stat_pm(dfBookVolumes)
        
        # dfBookVolumes = self.spps.read_sql_to_df_pandas_SPPS(sql)
        
        # dicBookVolumes = PandasManager.read_df_with_one_row_to_dic_stat_pm(dfBookVolumes)
        
        return listDfRowsDicts



    def register_book_complects_in_libba (self, **bkwargs):
        """ 
        Сформировать из проанализированных и альтернативно скаченных из ТГ данных (из таблиц 'tg_proceeded_...') по сообщениям из чата книжные комплекты 
        и записать их в таблицы 'tg_book_complects_ch_01' и 'tg_book_complect_volumes_ch_01'
        """
        
        
        # INI CLASSES

        # tlf = TgLocalFuncs()
        # blm = BookLibraryManager()
        # sps = SqliteProcessorSpeedup(ms.DB_CONNECTION)
        
        # Условия ограничения по выборке из книжных комплектов для их регистрации в LIB DB
        if 'setSampleConditions' in bkwargs:
            setSampleConditions = bkwargs['setSampleConditions']
            
        # Условие ограничения по message-ids
        condListMessagesIds = setSampleConditions['ids']
        
            
        

        # flagRegVolumesAnyway = True # Флаг прохождения алгоритма регистрации аудио-томов книг в любом случае. невзирая даже на то. что книга уже зарегестрирована

        # Кол-во циклов при разработке. Несмотря на любые установки, будет произведен только debugCycleQn циклов при считывании и обработке книг
        # Если debugCycleQn = -1 , то система не реагирует на этот флаг вообще
        debugCycleQn = bkwargs['debugCycleQn'] 
        
        
        # INI
        
        dtStringFormat1, dtStringFormat2, universUnix = FG.get_current_time_format_1_and_2_and_universal_unix()

        
        # id ТГ источника  из таблицы 'lib_orig_sources'.
        origSourceId = bkwargs['origSourceId'] 
        
        # D. Получить словрь отсечений по спискам ids сообщений, по которым уже состоялась регистрация книг и их аудио-томов в разрезах по 
        # оригинальным источникам этих сообщений (другими словами, сгруппированными по  id ТГ-каналов в таблице 'lib_orig_sources')

        # формат словаря для набора сообющений в чате. которая формирует комплект сообщений, составляющий описание книги и ее аудио-тома
        # dicTgBookComplectData = {
            
        #     'book' : 4209,
        #     'volumes' : {
        #                     1 : '4210',
        #                     2 : '4211',
        #                     3 : '4212',
        #                     4 : '4213'
        #                 }
        # }
        
        
        # F. Организовать цикл по книжным комплектам из таблицы 'tg_book_complect_volumes_ch_01' , предварительно сформировав для каждого цикла словарь комплекта формата 
        
        # Если есть условия по фильтрации книжных комплектов по message_ids для описаний книг
        if condListMessagesIds and condListMessagesIds != -1 :
        
            # Замещаем квадратные скобки листа на круглые, необходимые для sql
            sql = f"SELECT * FROM {ms.TB_TG_BOOK_COMPLECTS_CH_01} WHERE book_msg_id IN {condListMessagesIds}".replace('[', '(').replace(']', ')')
            
        else:
            
            sql = f"SELECT * FROM {ms.TB_TG_BOOK_COMPLECTS_CH_01}"
            
            
        print(f"PR_A907 --> SYS LOG: Набор книжных комплектов описывается этим sql-запросом по книгам комплектов \n{sql}")
        
        # Книжные комплекты, найденные в таблице tg_book_complects_ch_01
        tgBookComplects = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        
        # Если есть элементы в списке возврата от запроса sql
        if not isinstance(tgBookComplects, int):
        
        
            # Цикл по книжным комплектов для их регистрации в библиотеке Labba
            for inx, bookComplectRow in enumerate(tgBookComplects):
                
                
                # FORMAT: bookComplectRow = [1, 4513, 1, '20-03-2024 13:26:29', 1710940000.0]
                
                # INI
                # Id исходного ТГ-сообщения соотвтетсвующего текущему описанию книги в книжном комплекте
                bookMessageId = bookComplectRow[1]
                origSourceId = bookComplectRow[2]
                
                print(f"PR_A374 --> SYS LOG: for cycle inx = {inx} and for bookMessageId = {bookMessageId}")
                
                # Ограничение на кол-во циклов (установочный ограничительный параметр для дебагинга)
                if debugCycleQn > 0 and inx > debugCycleQn - 1:
                    
                    print(f"PR_A372 --> Ограничение по кол-ву циклов debugCycleQn для разработки = {debugCycleQn}. Прерываем цикл for... , так как этот предел достигнут. for inx = {inx}")
                    break
                



                # C. ОТСЕЧЕНИЕ книжных комплектов уже прошедших регистрацию в библиотеке LIB
                
                #TODO: Переделать отсечение по всем sourcesIds, а н е по одному
                
                # print(f"PR_A951 --> bookComplectRow = {bookComplectRow}")
                
                # Получить общий список messagesIds всех типов, зарегестрированных в библиотеке
                listLibMessagesIdsDone, listWrongBookDescrMessagesIds, listBookDescrIdsWhereEvenOneVolumeFasWrongStatus = self.blf.get_reject_messages_ids_list_for_third_level_blf(origSourceId)
                    
                print(f"PR_A975 --> SYS LOG: Reject-список -->> {listLibMessagesIdsDone}")
                
                # !!!! ОТСЕЧЕНИЕ REJECTOR!!!!    
                # Остечение сообщение от дальнейшей обработки с анализом по сообщениям только от того источника, к каоторому принадлежит текущее сообщение
                # ifReject = self.blf.reject_proccessing_if_in_reject_messages_ids_list_blf(bookMessageId, totalRejectMessagesIdsForThirdLevel)    
                

                
                print(f"PR_A958 --> POINT A")

                if bookMessageId in listLibMessagesIdsDone:
                    
                    print(f"""PR_B051 --> SYS LOG: Книга на базе комплекта из сообщения с ID = {bookMessageId} уже зарегестрирована в библиотек LIB. 
                                Пропускаем цикл """)
                                

                    continue
                
                # END C. ОТСЕЧЕНИЕ книжных комплектов уже прошедших регистрацию в библиотеке LIB
                
                
                elif bookMessageId in listWrongBookDescrMessagesIds:
                
                    print(f"""PR_B052 --> SYS LOG: Книга на базе комплекта из сообщения с ID = {bookMessageId}  в описании с картинкой имеет ошибочный статус в табл 'tg_messages_proceeded'. Пропускаем цикл
                                Проверить таблицу недозагрузок и дозагрузить !!!
                                """)

                    continue
                
                
                
                
                elif bookMessageId in listBookDescrIdsWhereEvenOneVolumeFasWrongStatus:
                
                    print(f"""PR_B053 --> SYS LOG: у Книги на базе комплекта из сообщения с ID = {bookMessageId} есть один или несколько аудио-томов с ошибочным статусом недозагрзки. 
                                Пропускаем цикл. Проверить таблицу недозагрузок и дозагрузить аудио-тома книги.
                                """)

                    continue
                
                

                # END C. ОТСЕЧЕНИЕ





                
                # INI
                # bkwargs = {}
                bookRefId = bookComplectRow[0]
                bookMsgId = bookComplectRow[1]
                bookTitle = self.tlf.get_book_title_by_tg_message_id(bookMsgId)
                
                
                
                print(f"""PR_A270 --> SYS LOG: START: Обработка следующего книжного комплекта с message_own_id = {bookMsgId} с названием : {bookTitle}
                    \nfor loop in tgBookComplects, CYCLE: bookComplectrow = {bookComplectRow}""")
                
            
                # сформировать словарь комплекта
                
                sql = f"SELECT * FROM {ms.TB_TG_BOOK_COMPLECT_VOLUMES_CH_01} WHERE book_complect_id_ref = {bookRefId}"
                
                print(f"PR_A310 --> sql = {sql}")
                
                bookComplectVolumes = self.sps.get_result_from_sql_exec_proc_sps(sql)
                
                print(f"PR_A309 --> bookcomplectVolumes = {bookComplectVolumes}")
                
                
                # Анализ: Если в комплекте есть название книги и нет аудио-томов, то тут две вероятности: 1. Автор канала еще не успел выгрузить тома,
                # а книга является последним сообщением-книгой  в ТГ канале. 2. Перед этим сообщением-книгой было фиктивное сообщение-книга. распознанное 
                # системой как книга, но таковой не являющимся (это скорее всего какой-то новый тип сообщения. типа картинка с описанием. но не являющийся
                # описанием книги) TODO: придумать решение в ходе реализации проекта
                # qnVolums = len(bookComplectVolumes)
                
                
                
                # и ФОРМИРУЕМ словрь аудио-томов для книги на базе результатов запроса
                if not isinstance(bookComplectVolumes, int):
                    bVolumes = {x[3] : x[2] for x in bookComplectVolumes}
                    
                else:
                    bVolumes = {}
                
                
                
                
                # сформировать словарь комплекта. x[3] - соотвтетсвуют полю 'volume_order' в возвращенном элементе списка списков bookComplectVolumes
                # x[4] - 'volume_msg_id' . Из табл 'tg_book_complect_volumes_ch_01'
                dicTgBookComplectData = {
                    'book' : bookMsgId,
                    'volumes' : bVolumes,
                    'origSourceId' : bookComplectRow[2]
                }
                
                # print(f"PR_A269 --> dicTgBookComplectData = {dicTgBookComplectData}")
                
                


                # ПРОВЕСТИ ОБРАБОТКУ И АНАЛИЗ каниги на основе словаря комплекта

                # INI
                # bookMsgId = dicTgBookComplectData['book']
                
                # volumes = dicTgBookComplectData['volumes']
                # volumsQn = len(volumes) # кол-во томов у книги



                # ПАРСИНГ ДАННЫХ 
                # A. Получить словарь с полным набором данных по книге, включая данные по парсингу и данные при первичном анализе и загрузке книги с ТГ канала
                dicFullBookData = self.get_full_book_data_by_chat_mssg_id_for_CH1 (bookMessageId, origSourceId)    
                
                print(f"PR_A908 --> bookMsgId = {bookMsgId}")
                print(f"PR_A909 --> ")
                pp(dicFullBookData)

                
                # НЕ УДАЛЯТЬ !!!
                # # B. Предварительная ПРОВЕРКА НАЛИЧИЯ уже зарегестрированной книги в библиотеке {CHECK REGISTRATION}
                # #INI
                # bookTitle = dicFullBookData['descrParsingData']['bookTitle']
                # authorSecondname = dicFullBookData['descrParsingData']['authorSecondname']
                # #PAR
                # dicCheckData = {
                #             'bookTitle' : bookTitle,
                #             'authorSecondname' : authorSecondname
                #         }
                
                # # Проверить наличие книги по двум параметрам : название книги и ее автор. Если совпадает, то на данный момент считаем, что книга уже зарегестрирована
                # ifRegistered = self.check_if_book_registered_already (dicCheckData)
                
                # Блокировка проверки. На этом этапе решено не проверять книгжный комплект на наличие регистрации в библиотеке. Так как алгоритм провекри еще не точен
                # Эта проверка будет на качественном уровне выделять цветом те книги, которые система поситает уже присутствуют. Плюс, учитывая, что могут 
                # быть продолжения у книги в виде группы аудио-томов, которой может предшествовать описание книги, подобное альфа-описанию, то система отсекала бы
                # эти продолжения одной и той же книги. Поэтому на данном этапе пропускаем все книги к регистрации и анализируем их уже на уровне библиотеи в 
                # полу - автоматическом режиме, то есть на базе этой проверки ряды с книгами будут выделятся цветом . Те. которые система посчитает уже ранее зарегестрированными 
                ifRegistered = False
                # print(f"PR_A223 --> dic = {dicBookData}")
                
                if ifRegistered: # Если уже зарегестрирована
                    pass
                    # print(f"PR_A259 --> SYS LOG: Эта книга {dicCheckData['bookTitle']} с автором {dicCheckData['authorSecondname']} уже есть в базе, поэтому не регистрируем ее")
                else:
                    # print(f"PR_A260 --> SYS LOG: Этой книги {dicCheckData['bookTitle']} с автором {dicCheckData['authorSecondname']} НЕТ в базе, поэтому регистрируем ее")
                
                
                
                
                    # TODO: На этом этапе можно провести проверку фиктивности книжного комплекта. Если книга есть, а аудио-томов у нее нет, то это означает 
                    # книга - фиктивная и ее моэно удалить
                    
                    bkwargs['dicTgBookComplectData'] = dicTgBookComplectData

                    # Зарегестрировать новую книгу в библиотеке
                    newAlfaBookId = self.register_new_book_in_libba_blm(dicFullBookData, **bkwargs)
                    
                
                
                    # D. Проверить, обновить или ЗАРЕГЕСТРИРОВАТЬ АУДИО-ТОМА !!! точлько что зарегестрированного описания книги с AlfaId = newAlfaBookId
                    
                    # получить спискок данных об аудил-томах книги
                    listDfRowsDictsBookVolumes = self.get_list_of_dicts_book_audio_volums_by_own_mssg_id(bookMsgId)
                    
                    print(f"PR_A373 --> listBookVolumes = {listDfRowsDictsBookVolumes}")
                    
                    # Цикл по томам книги
                    for volume in listDfRowsDictsBookVolumes:
                        
                        # INI
                        
                        print(f"PR_A377 --> volume = {volume}")
                        
                        volumeFileName = volume['message_document_name']
                        
                        volumeOrder = volume['volume_order']

                        volumeMssgId = volume['volume_msg_id']
                        
                        print(f"PR_A378 --> volumeMssgId = {volumeMssgId}") 
                        
                        # INI
                        # Тип создания сущности книги и томов. Задается во View: register_book_complects_in_libba ()
                        bookCreationType = bkwargs['bookCreationType']
                        
                        
                        
                        # A. Анализ названия файла , вычленение смысловой части и запись ее в поле 'volume_title'
                        parts = volumeFileName.split('_')
                        volumeTitle = parts[0]
                                
                        # # НЕ УДАЛЯТЬ
                        # # Проверить, зарегестрирован ли такой том уже у книги
                        # # ПРИМ: Нужна ли тут эта проверка. Кажется она избыточна, так как на прошлых этапах производятся отсечения . Проанализировать точнее 
                        # # похоже. что эта проверка тривиальна и не нужна
                        # sql = f"SELECT * FROM {ms.TB_LIB_BOOK_AUDIO_VOLUMES} WHERE volume_file_name = '{volumeFileName}' AND books_alfa_id = {newAlfaBookId}"
                    
                        # # Проверить, есть ли запись в таблице с названием = volumeName
                        # ifVolNameExists = self.sps.if_select_result_exists_sps(sql)
                        
                        # print(f"PR_A379 --> Наличие в таблице 'lib_book_audio_volumes'  записи в поле с названием {volumeFileName} ifVolNameExists = {ifVolNameExists}")
                        
                        # АНАЛИЗ
                        
                        # Если запись с таким названием существует, значит такой том на уровне как минимум информационной записи существуует
                        # TODO: Ввести статус тома
                        
                        # Пока блокируем этупроверку.
                        ifVolNameExists = False
                        
                        # Если запись с таким названием тома уже зарегестрирована и существует, то либо мы пропускаем цикл, либо. в зависимости от декларативного флага,
                        # все - равно обновляем все тома (volumes) книги, так как они могли измениться за счет того. что автор канала загрузил в пустышки 
                        # выпущенные тома и их названия уже стали другими и их нужно обновить.(???) Вернее, пустышки со стандартынми названиями могли быть 
                        # заменены другими названиями (но тогда и их названия не будет. вобщем - продумать). пока делаем UPDATE томов, если стоит флаг : проанализировать по любому
                        if ifVolNameExists: 
                            
                            pass
                        
                        # Если не существует, то вставляем информационную запись с названием тома книги
                        else:
                            
                            pass
                        
                            sql = f"""
                                        INSERT INTO {ms.TB_LIB_BOOK_AUDIO_VOLUMES} 
                                            (
                                                books_alfa_id, 
                                                volume_file_name, 
                                                volume_order, 
                                                date_reg_calend, 
                                                date_reg_unix, 
                                                volume_message_id, 
                                                btype_creation_id,
                                                source_id,
                                                volume_title
                                            )
                                        VALUES 
                                        (
                                            {newAlfaBookId}, 
                                            '{volumeFileName}', 
                                            {volumeOrder}, 
                                            '{dtStringFormat2}', 
                                            {universUnix}, 
                                            {volumeMssgId}, 
                                            {bookCreationType},
                                            {origSourceId},
                                            '{volumeTitle}'
                                        )
                                    """
                                    
                            # print(f"PR_A376 --> sql = {sql}")
                            
                            
                            
                            

                            
                            
                            try:
                            
                                print(f"PR_A380 --> START EXECUTE SQL")
                                
                                self.sps.execute_sql_SPS(sql)
                                
                                
                                print(f"PR_A382 --> SYS LOG: В таблицу 'lib_book_audio_volumes' внесена запись по sql: \n {sql}")
                                
                                
                                
                                newValumeId = self.sps.get_last_inserted_id_in_db_mysql_sps()
                                
                                
                                print(f"PR_A427 --> SYS LOG: newValumeId = {newValumeId}")
                                
                                
                                
                                
                            except Exception as err:
                                
                                print(f"PR_A426 --> SYS LOG: ERROR !!! Ошибка при вставке в таблицу 'lib_book_audio_volumes': {err}")
                            
                                newValumeId = -1
                                
                                sys.exit(err)
                                            
                                            
                            
                            
                            
                            
                            
                            
                            # J. Проставить статусы для записанного тома книги
                            # А именно, что как мнимум прописана информация по тому книги
                            # по факту тнфрмация загруэена. но не загружен сам файл в директроию первичной загрузки
                            
                            
                            # 1. Проставление статуса информационной загрузки в БД тома книги
                            
                            volumeStatus = 1 # -> 'VOLUME_INFOR_INSERTED'
                            
                            sql = f"INSERT INTO {ms.TB_LIB_VOLUMES_VOLUME_STATUSES} (book_volume_id, volume_status_id) VALUES ({newValumeId}, {volumeStatus})"
                            

                            
                            
                            
                            try:
                            
                                print(f"PR_A381 --> START EXECUTE SQL")
                                
                                self.sps.execute_sql_SPS(sql)
                                
                                print(f"PR_A383 --> SYS LOG: В таблицу 'lib_volumes_volume_statuses' внесена запись по sql: \n {sql}")
                                
                            except Exception as err:
                                
                                print(f"Произошла !!! ОШИБКА !!! В результате INSERT запроса: \n {sql} ")
                                
                                print(f"PR_A428 --> SYS LOG: ERROR !!! {err}")
                                
                                sys.exit(err)
                            
                            
                            

                            
            # B. Присвоить жанры книги и категории 
            
            # G. После успешной регистрации можно ОИСТИТЬ таблицы с книжными комплектами и сгруженными сообщениями в tg_procceeded






    def update_book_description_img_blm (self, bookAlfaId, updFileName):
        """ 
        Обновить картинку в описании книги (со страницы редактирования книжного комплекта, http://127.0.0.1:6070/telegram_monitor/edit_book_complect?alfa_id=1)
        updFileName - название файла для обновления в описании книги
        bookAlfaId - главное id книги
        ПРИМ: Есть два ограничения целостности на проектном уровне. 1. Любые картинки, которые присваиваются к книгам в любом варианте и которые хранятся 
        в Хранилище картинок для книг библиотеки, должны быть с уникальным названием. То есть они сами по себе являются ключами. И их всегда можно найти 
        по названию в Хранилище методами фалового поиска. 2. Хранилище картинок может быть любым и в любом проекта или на сервере, где могут быть разные 
        абсолютные пути к нему. Единственное ограничение для хранилища - это название секции в пути при любых раскладах, который называется маркером хранилища и 
        этот сегмент будет называтся 'lib_books_images'. Начиная с этого сегмента, который считается началом Хранилища, могут быть любые вариации директорий и 
        поддиректорий, в которых могут хранится любые имиджевые файлы, но с уникальными названим=ями. Координатами файла в Хранилище и в БД явялеются: название
        файла и его относительный путь, начиная с маркера Хранилища (не включая его). 
        """
        
        # Получить абсолютный путь для редактируемого относительного пути файла, который описывается чеециями-доменами пути файла с правого конца
        # Относительный остаток с правого конца передан из модуля редактирования : fileNameEditPartialLast
        
        # С. Провести поиск заданного нового файла-картинки к описанию книги в хранилище картинок к книгам
        
        # INI
        # Хранилище картинок для книг в файловом пространистве проекта
        bookImgStorage = ms.LIB_BOOK_IMAGE_STORAGE
        # Маркер-секция, которая считается началом Хранилища картинок библиотеки
        imgStorageMarker = ms.IMAGE_STORAGE_MARKER
        
        listFiles = FilesManager.find_file_in_dir_by_name_recursively(bookImgStorage, updFileName)

        # Кол-во в резйльтате по поиску файлов в подмножестве хранилища картинок
        listFilesQn = len(listFiles)
        
        print(f"PR_A451 --> listFilesQn = {listFilesQn}")
        
        # Если файл найден и он единственный
        if listFilesQn == 1:
            
            print(f"PR_A464 --> SYS LOG: В подмножестве суб-директорий хранилища картинок для книг найден файл с названием '{updFileName}', который надо присвоить книге с alfaId = {bookAlfaId}")

            # E. Присвоить файл editedFileName книге с alfaId = bookAlfaId
            
            # 1/ Поиск найденного файла-картинки из Хранилища картинок в таблице lib_book_images , в таблице, где регистрируются все картинки по книгам
            
            # Словарь с результатами поиска по названию файла из таблицы lib_book_images
            dicBookImgSearched = self.blf.search_file_in_lib_book_images_tb_blf(updFileName)
            
            # Кол-во в словаре (должно быть либо 1, либо 0)
            dicBookImgSearchedQn = len(dicBookImgSearched)
            
            # 2/ В зависимости от того найден или не найден файл картинки в табл lib_book_images дифференцируем действия
            
            # Если название файла найдено в табл lib_book_images (то есть этот файл уже зарегестрирован), то присваеваем его id в записи по заданнйо книги в 
            # таблице  lib_books_images
            if dicBookImgSearchedQn == 1: 
                pass
                print(f"\nPR_A472 --> SYS LOG: В таблице lib_books_images найдена регистрация файла с названием '{updFileName}'\n")
                
                # Получить id файла с заданынм названием редактируемого файла, регистрация которого обнаружена в табл lib_books_images
                imgFileId = self.blf.get_id_of_img_file_from_lib_book_images_by_file_name(updFileName)
                
                print(f"PR_A474 --> newImgFileId = {imgFileId}")
                

            # Если название файла НЕ найдено в табл lib_book_images (то есть этот файл НЕ зарегестрирован), то необходимо его зарегестрировать 
            # в табл lib_books_images  и далее присвоить его id книге в табл lib_books_images
            else:
                
                # INI
                # Полный путь редактируемого и загруженного в Хранилище файла (который ранее найден в рекурсивном поиске по Хранилищу картинок книг)
                editedFileFullPath = str(listFiles[0])
            
                print(f"\nPR_A465 --> SYS LOG: Файл с названием '{updFileName}' НЕ зарегестрирован в таблице 'lib_book_images'. Необходимо его зарегестрировать и далее присвоить его  id книге c alfaId = {bookAlfaId} в табл  'lib_books_images'")
                print(f"PR_A466 --> SYS LOG: Регестрируем файл '{editedFileFullPath}' в таблице 'lib_book_images', вычислив его относительный с правого конца путь в Хранилище картинок\n")

                
                # F.  Получить относительный путь редактируемого файла с правого конца до начала абсолютного пути Хранилища картинок книг
                relRightPath = FilesManager.get_relative_right_path_from_full_file_path_by_given_section_name_fm (editedFileFullPath, imgStorageMarker)
                
                
                # G. Зарегестрировать название файла и его относительную директорию справа в табл lib_books_images

                # EXECUTE SQL !!!
                print(f"PR_A471 --> SYS LOG: Выполнение INSERT запроса ")
                
                imgFileId = self.blf.insert_new_image_to_lib_book_images_tb_blf(updFileName, relRightPath)
                
                print(f"PR_A467 --> imgFileId = {imgFileId}")
        
        
        
            # G. Присвоить для книги с заданным alfa_id  в таблице lib_books_images id файла картинки в поле 'book_image_id' текущтй id редактируемого файла,
            # который равен imgFileId
            # EXECUTE UPDATE SQL !!!
            self.blf.update_book_with_alfa_id_assign_img_with_reg_id_blf (bookAlfaId, imgFileId)
            
            print(f"\nPR_A476 --> SYS LOG: Книге с alfaId = {bookAlfaId} присвоена картинка к описанию с id регистрации картинки = {imgFileId}")
        
        
        
        # Если найден не один, а несколько файлов с таким названием, то необходимо удалить все, кроме одного, так как принято, что названия файлов в 
        # подмножестве хранилища картинок и которые используются для описания книг,  должны быть уникальными !!!
        # TODO: Проработать
        elif listFilesQn > 1:
            pass
            print(f"PR_A473 --> SYS LOG: В хранилище картинок к книгам найдены фалы с одинаковыми названиями {updFileName}. Название фала для книг должны быть уникальны. Необходимо свести наличие фалов с одинаковым названием к одному!!!")
        
        
        # Если не найдена ни одна картинка с подобным названием в подмножестве хранилища картинок, то необходимо выполнить ряд действий ниже
        elif listFilesQn < 1:
            pass
        

        
            # TODO: Сделать эту проверку на уровне AJAX с выводом  popup-окна с обьяснением действий без перезагрузки страницы
            print(f"\nPR_A462 --> SYS LOG: В подмножестве суб-директорий хранилища картинок для книг не найден ни один файл с названием '{updFileName}'")
            print(f"PR_A463 --> SYS LOG: 1. Необходимо загрузить этот файл в любой существующий или вновь созданный суб-директорий хранилища картинок и повторить сохранение редактирования с этой картинкой: \n\t'{bookImgStorage}'\n")
            # D. 
        
            
            
        # если такой картинки не найдено, то ссобщить, что либо не загружена, либо ошибка в названии
        else:
            pass    
            
            
            
            
            







    @staticmethod
    def prepare_out_data_block_dressed_for_book_authors_with_checkboxes_v1 (**dicThrough):
        """ 
        BookLibraryManager
        Организовать создание и оформление выходного словаря для списка всех авторов с чек-боксами для выбора для модуля редактирования книги
        VIEWS: edit_book_complect
        """
        
        print(f"PR_A513 --> START: prepare_html_code_for_edit_table_redactor_mysql_sdm()")

        blf = BookLibraryFuncs()
        
        # INI
        # bookAlfaId , если задана книга (если задана книга, то надо в списке авторов сделать checked по авторам для этой книги)
        # Если книга не задана, то список авторов выдается без выделения каких-либо авторов
        if 'bookAlfaId' in dicThrough:
            bookAlfaId = dicThrough['bookAlfaId']
        else:
            bookAlfaId = None
            
        # if 'ulClass' in dicThrough:
        #     ulClass = dicThrough['ulClass']
        # else:
        #     ulClass = ''
            
        # A. Если задан bookAlfaId книги, то находим список ids авторов этой книги, что бы выделить их checkboxes в выводимом списке
        if bookAlfaId:
            listBookAuthorsIds = blf.get_authors_ids_of_book_by_alfa_id(bookAlfaId)
        else:
            listBookAuthorsIds = -1
            
        print(f"PR_A512 --> listBookAuthors = {listBookAuthorsIds}")
        
        
        # Если фрейм пустой. то он будет передан в виде -1
        if isinstance(dicThrough['df'], int): 
            outDataBlock = f'Ничего не найдено'
        # иначе - создаем html код со списком чек-боксов по всем авторам. Если задана книга, то авторов этой книги в этом списке необходимо выделить checked
        else:
            
            outDataBlock = '''
                    <ul>
                '''
            
            for inx, row in dicThrough['df'].iterrows():
                
                # INI
                
                authorRegId = row['id']
                authorFullName = row['author_full_name']
                authFirstName = row['author_first_name']
                authSecondName = row['author_second_name']
            
                checked =''
                
                # Если задана была конкретная книга, то для нее получен список  ids авторов. Для них чек-боксы нужно выделить как checked
                if not isinstance(listBookAuthorsIds, int)  :

                    if authorRegId in listBookAuthorsIds:
                        checked = 'checked'
            
                    # JS155^^ - вывод на редактирование автора при нажатии на его ФИО в блоке редактирования авторов
                    outDataBlock += f'''
                                <li>
                                <input type="checkbox" firstn = "{authFirstName}" scndn = "{authSecondName}"  class="chb_book_authors" name="book_authors_{authorRegId}" value="{authorRegId}" {checked}>
                                <span class=".edit_li_chbox_author_fio" firstn = "{authFirstName}" scndn = "{authSecondName}" auth_id = "{authorRegId}">
                                {authorFullName}
                                </span>
                                </li>
                                '''


                # Если НЕ задана никакия книга (то авторы выводятся все без checked)
                else: 
                    outDataBlock += f'''
                            <li>
                            <input type="checkbox" firstn = "{authFirstName}" scndn = "{authSecondName}" class="chb_book_authors" name="book_authors_{authorRegId}" value="{authorRegId}">
                            <span class="edit_li_chbox_author_fio" firstn = "{authFirstName}" scndn = "{authSecondName}" auth_id = "{authorRegId}">
                            {authorFullName}
                            </span>
                            </li>
                        '''



            outDataBlock += "</ul>"
            
            
            # (???)
            dicThrough['htmlAuthorListBlock'] = outDataBlock 
            
            
        print(f"PR_A514 --> END: prepare_html_code_for_edit_table_redactor_mysql_sdm()")
        
        return outDataBlock















    @staticmethod
    def prepare_out_data_block_for_book_narrators_with_checkboxes (**dicThrough):
        """ 
        BookLibraryManager
        Организовать создание и оформление выходного словаря для списка всех дикторов с чек-боксами для выбора для модуля редактирования книги
        VIEWS: edit_book_complect
        """
        
        print(f"PR_A720 --> START: prepare_out_data_block_for_book_narrators_with_checkboxes()")

        blf = BookLibraryFuncs()
        
        # INI
        # bookAlfaId , если задана книга (если задана книга, то надо в списке авторов сделать checked по авторам для этой книги)
        # Если книга не задана, то список авторов выдается без выделения каких-либо авторов
        if 'bookAlfaId' in dicThrough:
            bookAlfaId = dicThrough['bookAlfaId']
        else:
            bookAlfaId = None
            
        print(f"PR_B404 --> bookAlfaId = {bookAlfaId}")
            
        # A. Если задан bookAlfaId книги, то находим список ids авторов этой книги, что бы выделить их checkboxes в выводимом списке
        if bookAlfaId:
            listBookNarratorsIds = blf.get_narrators_ids_of_book_by_alfa_id(bookAlfaId)
        else:
            listBookNarratorsIds = None
            
        print(f"PR_A722 --> listBookNarratorsIds = {listBookNarratorsIds}")
        
        
        # Если фрейм пустой. то он будет передан в виде -1
        if isinstance(dicThrough['df'], int): 
            outDataBlock = f'Ничего не найдено'
        # иначе - создаем html код со списком чек-боксов по всем авторам. Если задана книга, то авторов этой книги в этом списке необходимо выделить checked
        else:
            
            PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dicThrough['df'], True, colsIndxed = False, marker="PR_B413 --> df" )
            
            outDataBlock = '<ul class="list">'
            
            for inx, row in dicThrough['df'].iterrows():
                
                # INI
                narratorRegId = row['id']
                narratorFullName = row['narrator_full_name']
                narratorFirstName = row['narrator_first_name']
                narratorSecondName = row['narrator_second_name']
                
                print(f"PR_B414 --> narratorFirstName = {narratorFirstName}")
                
                # Перевести значение None в пустую строку '' TODO: НАдо сделать, что бы в фрейме не было None, а было NULL
                if narratorFirstName == None:
                    narratorFirstName = ''
                    
                print(f"PR_B415 --> narratorFirstName = {narratorFirstName}")
            
                checked =''
                
                # Если задана была конкретная книга, то для нее получен список  ids авторов. Для них чек-боксы нужно выделить как checked
                if listBookNarratorsIds and not isinstance(listBookNarratorsIds, int):

                    if narratorRegId in listBookNarratorsIds:
                        checked = 'checked'
                        
                    # JS162^^ - При нажатии на span ФИО  запустить редактирование данного ликтора
                    outDataBlock += f'''
                            <li>
                            <input type="checkbox" firstn = "{narratorFirstName}" scndn = "{narratorSecondName}"  class="chb_book_narrators" name="book_narrators_{narratorRegId}" value="{narratorRegId}" {checked}>
                            <span class="spn_li_narrator" firstn = "{narratorFirstName}" scndn = "{narratorSecondName}" narrator_tbid="{narratorRegId}"> 
                            {narratorFullName}
                            </span>
                            </li>
                    '''


                # Если НЕ задана никакия книга (то авторы выводятся все без checked)
                else: 
                    outDataBlock += f'''
                            <li>
                            <input type="checkbox" firstn = "{narratorFirstName}" scndn = "{narratorSecondName}" class="chb_book_narrators" name="book_narrators_{narratorRegId}" value="{narratorRegId}">
                            <span class="spn_li_narrator" firstn = "{narratorFirstName}" scndn = "{narratorSecondName}" narrator_tbid="{narratorRegId}">
                            {narratorFullName}
                            </span>
                            </li>
                    '''



            outDataBlock += "</ul>"
            
            
            # (???)
            dicThrough['htmlNarratorListBlock'] = outDataBlock 
            
            
        print(f"PR_A721 --> END: prepare_out_data_block_for_book_narrators_with_checkboxes()")
        
        return outDataBlock










    @staticmethod
    def prepare_html_list_for_repositories_checkboxes_checked_for_source_blm (origSourceId = None, ulClass = 'list_repositories'):
        """ 
        BookLibraryManager
        Сформировать html-список всех репозиториев с выделением присвоенных для заданного источника, если  источник задан. Без выделения - если не задан
        ulClass -  название класса для <ul>
        VIEWS: 
        """
        
        print(f"PR_B445 --> START: prepare_html_block_for_repositories_checkboxes_with_source_checked_analisys_blm()")

        blf = BookLibraryFuncs()
        
        print(f"PR_B465 --> origSourceId = {origSourceId}")
        
        # INI

        # A. Если задан bookAlfaId книги, то находим список ids авторов этой книги, что бы выделить их checkboxes в выводимом списке
        if origSourceId:
            listRepositoriesIdsForSource = blf.get_repositories_ids_of_orig_source_id(origSourceId)
        else:
            listRepositoriesIdsForSource = None
            
        print(f"PR_B447 --> listRepositoriesIdsForSource = {listRepositoriesIdsForSource}")
        
        # Список Id всех репозиториев
        dfAllRepositories = blf.get_df_all_lib_repositories_data_blf()
        
        # Сотрировка фрейма по названию репозитория ASC
        dfAllRepositories = dfAllRepositories.sort_values(by=['repository'])
        

        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dicThrough['df'], True, colsIndxed = False, marker="PR_B451 --> df" )
        
        # ФОРМИРОВАНИЕ html-кода списка
        htmlDataBlock = f'<ul class="{ulClass}">'
        
        for inx, row in dfAllRepositories.iterrows():
            
            # INI
            repositId = row['id']
            repositName = row['repository']
            repositTgId = row['repository_tg_id']
            repositTgNick = row['reposit_nick']
            
            print(f"PR_B448 --> repositName = {repositName}")
            
            # # Перевести значение None в пустую строку '' TODO: НАдо сделать, что бы в фрейме не было None, а было NULL
            # if narratorFirstName == None:
            #     narratorFirstName = ''
                
            # print(f"PR_B449 --> narratorFirstName = {narratorFirstName}")
        
            checked =''
            
            # Если задана была конкретная книга, то для нее получен список  ids авторов. Для них чек-боксы нужно выделить как checked
            if listRepositoriesIdsForSource and not isinstance(listRepositoriesIdsForSource, int):

                if repositId in listRepositoriesIdsForSource:
                    checked = 'checked'
                    

            htmlDataBlock += f"""
                    <li>
                    <input type="checkbox"  class="chb_assigned_repositories" name="" value="{repositId}" {checked}>
                    <span class="spn_li_repositories"  reposit_id="{repositId}" title="{repositTgNick}/{repositTgId}"> 
                    {repositName}
                    </span>
                    </li>
            """


        htmlDataBlock += "</ul>"
            
        # END ФОРМИРОВАНИЕ html-кода списка

            
        print(f"PR_B450 --> END: prepare_html_block_for_repositories_checkboxes_with_source_checked_analisys_blm()")
        
        return htmlDataBlock







    @staticmethod
    def prepare_html_list_for_repositories_checkboxes_checked_for_lib_book_blm (bookAlfaId = None, ulClass = 'list_repositories'):
        """ 
        BookLibraryManager
        Сформировать html-список всех репозиториев с выделением чекбоксов, присвоенных для заданной книги, если книга задана. 
        Без выделения по чекбоксам - если не задана
        ulClass -  название класса для <ul>
        VIEWS: 
        """
        
        print(f"PR_B481 --> START: prepare_html_list_for_repositories_checkboxes_checked_for_lib_book_blm()")

        blf = BookLibraryFuncs()
        
        print(f"PR_B483 --> origSourceId = {bookAlfaId}")
        
        # INI

        # A. Если задан bookAlfaId книги, то находим список tbids целевых репозиториев для этой книги, что бы выделить их checkboxes в выводимом списке
        if bookAlfaId:
            listRepositoriesIdsForSBook = blf.get_repositories_ids_of_given_lib_book_id(bookAlfaId)
        else:
            listRepositoriesIdsForSBook = None
            
        print(f"PR_B484 --> listRepositoriesIdsForSBook = {listRepositoriesIdsForSBook}")
        
        # Список Id всех репозиториев
        dfAllRepositories = blf.get_df_all_lib_repositories_data_blf()
        
        # Сотрировка фрейма по названию репозитория ASC
        dfAllRepositories = dfAllRepositories.sort_values(by=['repository'])
        

        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dicThrough['df'], True, colsIndxed = False, marker="PR_B451 --> df" )
        
        # ФОРМИРОВАНИЕ html-кода списка
        htmlDataBlock = f'<ul class="{ulClass}">'
        
        for inx, row in dfAllRepositories.iterrows():
            
            # INI
            repositId = row['id']
            repositName = row['repository']
            repositTgId = row['repository_tg_id']
            repositTgNick = row['reposit_nick']
            
            print(f"PR_B485 --> repositName = {repositName}")
            
            # # Перевести значение None в пустую строку '' TODO: НАдо сделать, что бы в фрейме не было None, а было NULL
            # if narratorFirstName == None:
            #     narratorFirstName = ''
                
            # print(f"PR_B449 --> narratorFirstName = {narratorFirstName}")
        
            checked =''
            
            # Если задана была конкретная книга, то для нее получен список  ids авторов. Для них чек-боксы нужно выделить как checked
            if listRepositoriesIdsForSBook and not isinstance(listRepositoriesIdsForSBook, int):

                if repositId in listRepositoriesIdsForSBook:
                    checked = 'checked'
                    

            htmlDataBlock += f"""
                    <li>
                    <input type="checkbox"  class="chb_assigned_repositories" name="" value="{repositId}" {checked}>
                    <span class="spn_li_repositories"  reposit_id="{repositId}" title="{repositTgNick}/{repositTgId}"> 
                    {repositName}
                    </span>
                    </li>
            """


        htmlDataBlock += "</ul>"
            
        # END ФОРМИРОВАНИЕ html-кода списка

            
        print(f"PR_B482 --> END: prepare_html_list_for_repositories_checkboxes_checked_for_lib_book_blm()")
        
        return htmlDataBlock
















    @staticmethod
    def prepare_html_list_for_all_orig_sources_simple_blm (ulClass = 'list_orig_sources'):
        """ 
        BookLibraryManager
        Сформировать простой html-список всех оригинальных источников из табл 'lib_orig_sources' 
        VIEWS: 
        """
        blf = BookLibraryFuncs()
        
        # Фрейм с данными по всем источникам
        dfOrigSources = blf.get_df_all_books_orig_sources_ids_blf()
        
        # Сотрировка фрейма по названию иcточника ASC
        dfOrigSources = dfOrigSources.sort_values(by=['orig_source'])

        # ФОРМИРОВАНИЕ html-кода списка
        htmlDataBlock = f'<ul class="{ulClass}">'

        for inx, row in dfOrigSources.iterrows():
            
            sourceId = row['id']
            sourceName = row['orig_source']
            sourceNick = row['tg_channel_nick']
            sourceTgId = row['tg_channel_id']

            # JS165^^ - операции при нажатии на название источника в модлуе присвоения репозиториев источнику 
            htmlDataBlock += f"""
                    <li>
                    <span class="spn_li_orig_source"  orig_source_id="{sourceId}" title="{sourceNick}/{sourceTgId}"> 
                    {sourceName}
                    </span>
                    </li>
            """

        htmlDataBlock += "</ul>"    

        # END ФОРМИРОВАНИЕ html-кода списка
        
        
        return htmlDataBlock
    
    
    
    
    


    @staticmethod
    def prepare_code_block_for_book_ststuses_with_checkboxes (**dicThrough):
        """ 
        BookLibraryManager
        Получить блок с html-кодами для полного массива суцществующих статусов книги из табл lib_book_statuses с чек-боксами для выбора, обернутых формой 
        с заданными фиксированными параметрами
        """
        
        print(f"PR_A521 --> START: prepare_code_block_for_book_ststuses_with_checkboxes_v1()")

        blf = BookLibraryFuncs()
        
        # INI
        # bookAlfaId , если задана книга (если задана книга, то надо в списке статусов сделать checked по статусам для этой книги)
        # Если книга не задана, то список статусов выдается без выделения каких-либо статусов
        if 'bookAlfaId' in dicThrough:
            bookAlfaId = dicThrough['bookAlfaId']
        else:
            bookAlfaId = None
            
        # A. Если задан bookAlfaId книги, то находим список ids статусов этой книги из табл lib_books_statuses, что бы выделить их checkboxes в выводимом списке
        if bookAlfaId:
            listBookStatusesIds = blf.get_list_of_statuses_ids_for_book_with_given_alfa_id(bookAlfaId)
        else:
            listBookStatusesIds = None
            
        # print(f"PR_A523 --> listBookAuthors = {listBookAuthorsIds}")
        
        
        # Если фрейм пустой. то он будет передан в виде -1
        if isinstance(dicThrough['df'], int): 
            outDataBlock = f'Ничего не найдено'
        # иначе - создаем html код со списком чек-боксов по всем статусам. Если задана книга, то статусы этой книги в этом списке необходимо выделить checked
        else:
            
            outDataBlock = '<form id="form_save_book_chosen_statuses" action="http://127.0.0.1:6070/telegram_monitor/save_book_statuses_choosen">\n<ul>'
            
            for inx, row in dicThrough['df'].iterrows():
                
                # INI
                
                bookStatusId = row['id']
                bookStatusName = row['book_status']

            
                checked =''
                
                # Если задана была конкретная книга, то для нее получен список  ids статусов. Для них чек-боксы нужно выделить как checked
                if listBookStatusesIds:

                    if bookStatusId in listBookStatusesIds:
                        checked = 'checked'
            
                    outDataBlock += f'\n<li><p><input type="checkbox" status_name = "{bookStatusName}"  class="chb_book_statuses" name="book_status_{bookStatusId}" value="{bookStatusId}" {checked}>{bookStatusName}</p></li>'


                # Если НЕ задана никакия книга (то авторы выводятся все без checked)
                else: 
                    outDataBlock += f'\n<li><p><input type="checkbox" status_name = "{bookStatusName}"  class="chb_book_statuses" name="book_status_{bookStatusId}" value="{bookStatusId}">{bookStatusName}</p></li>'


            outDataBlock += "\n</ul>\n</form>"
            
            
            dicThrough['htmlBookStatusesListBlock'] = outDataBlock 
            
            
        print(f"PR_A522 --> END: prepare_code_block_for_book_ststuses_with_checkboxes_v1()")
        
        return outDataBlock







    @staticmethod
    def prepare_code_block_for_book_categories_with_checkboxes (**dicThrough):
        """ 
        BookLibraryManager
        Получить блок с html-кодами для полного массива суцществующих категорий книги из табл lib_categories с чек-боксами для выбора, обернутых формой 
        с заданными фиксированными параметрами
        """
        
        print(f"PR_A628 --> START: prepare_code_block_for_book_categories_with_checkboxes()")

        blf = BookLibraryFuncs()
        
        # INI
        # bookAlfaId , если задана книга (если задана книга, то надо в списке статусов сделать checked по категориям для этой книги)
        # Если книга не задана, то список статусов выдается без выделения каких-либо категорий
        if 'bookAlfaId' in dicThrough:
            bookAlfaId = dicThrough['bookAlfaId']
        else:
            bookAlfaId = None
            
        # A. Если задан bookAlfaId книги, то находим список ids категорий этой книги из табл lib_books_statuses, что бы выделить их checkboxes в выводимом списке
        if bookAlfaId:
            listBookCategoriesIds = blf.get_list_of_categories_ids_for_book_with_given_alfa_id(bookAlfaId)
        else:
            # The code `listBookCategoriesIds` appears to be a variable name in Python. It suggests
            # that it might be used to store a list of book category IDs. However, without seeing the
            # actual code where this variable is defined and used, it is difficult to provide a more
            # specific explanation.
            listBookCategoriesIds = []
            
        # print(f"PR_A523 --> listBookAuthors = {listBookAuthorsIds}")
        
        
        # Если фрейм пустой. то он будет передан в виде -1
        
        
        # PARS
        df = dicThrough['df']   
        
        keyValFieldsList = ['id', 'category']
        
        kwargs = {
            
            'ulClass' : 'list',
            'liMarker' : 'js149' # JS149^^ - Подгружение вторичного блока редактирования выбранной (нажатой категории)
        }
            
            
        hm =  HTMLSiteManager()    
        
        outDataBlock = hm.prepare_ul_checkbox_list_hm(df, keyValFieldsList, listBookCategoriesIds, **kwargs)
        
            
            
        dicThrough['htmlBookCategoriesListBlock'] = outDataBlock 
            
            
        print(f"PR_A629 --> END: prepare_code_block_for_book_categories_with_checkboxes()")
        
        return outDataBlock


    def test(self):
        
        print(f"PR_A960 --> START: test()")






    @staticmethod
    def prepare_html_categories_block_three_columns_with_checkboxes (dicThrough):
        """ 
        BookLibraryManager
        Для VIEW: book_categories_editor - редактирование категорий книг в общем
        Получить блок с html-кодами для полного массива суцществующих категорий из табл lib_categories с чек-боксами для выбора, обернутых формой 
        с заданными фиксированными параметрами. В 3 колонки
        JS148^^
        """
        
        print(f"PR_B347 --> START: prepare_html_categories_block_three_columns_with_checkboxes()")
        
        
        # print(f"PR_B349 --> dicThrough = {dicThrough}")
            
        # PARS
        
        df = dicThrough['df']   
        
        keyValFieldsList = ['id', 'category']
        
        kwargs = {
            
            'ulClass' : 'list',
            'liMarker' : 'js148'
        }
            
            
        hm =  HTMLSiteManager()    
        
        outDataBlock = hm.prepare_ul_checkbox_list_hm(df, keyValFieldsList, **kwargs)
            
            
        # print(f"PR_B351 --> dicThrough['htmlCategoriesBlock'] = {dicThrough['htmlCategoriesBlock']}")
            
            
        print(f"PR_B348 --> END: prepare_html_categories_block_three_columns_with_checkboxes()")
        
        return outDataBlock






    def get_categories_list_with_chbox_for_given_alfa_book_blm (self, alfaId, ):
        
        print(f"PR_B357 --> START: get_categories_list_for_given_alfa_book_blm()")







        print(f"PR_B358 --> END: get_categories_list_for_given_alfa_book_blm()")







    def messages_proccessing_rejector (self, messageSourceId, messageId, enterPoint, flagLoadImgAnyway = False):
        """ 
        Алгоритм анализа сообщений и сущностей, связанных с ними, на предмет отсечения от дальнейшего процессинга
        На разных уровнях сообщения и сущности отсекаются в зависимости от разных причин, в частности от того, были ли они уже успешно обработаны 
        системой, соотвтетсвует ли их тип для дальнейшего процессинга и т.д.
        В целом отсечения производятся на 3х этапах: на этапе скачивания сообщений из ТГ-канала, на этапе перевода скачанных сообщений в книжные
        комплдекты и на этапе регистрации книжных комплектов в библиотеке LABBA
        
        !!! Кроме того, реджектор при обращении к нему производит анализ всех сообщений, скаченных с ошибкой в таблицах tg_proceeded на самом
        первичном этапе во View: analyze_and_download_messages_from_ch_id_01(). И удаляет их из таблиц, что бы они не препятсвовали скачиванию
        в следующий раз ошибочно-скачанных сообщений снова (иначе ошибочно скаченные сообщения будут отсекатся и так и останутся не обработанными)
        
        messageId - id сообщения в ТГ канале, который является книго- или аулио-том образующим (но в перспективе может быть любым id из любого источника)
        messageSourceId - изначальный источник, к которому принадлежит сообщение с  id = messageId (определяется в табл 'lib_orig_sources')
        enterPoint - условный маркер входа реджектора: 'TG_MESSAGE_LOADING', 'BOOK_COMPLECTS_FORMATING', 'BOOK_COMPLECTS_REGISTRATION_IN_LABBA'
        flagLoadImgAnyway  - флаг , который обходит все ограничения по отсечению и принуждает закаивать сообщения, даже , если они входят в списки отсечения
        sourceId - источник сообщения
        
        Так же отсечение производится на разных фильтрах или типах:
        
            # 1. отсечение на фильтрах уже скачанных сообщений без ошибок, находящихся в таблицах tb_proceeded. Плюс отсечение по типам сообщений на этом же уровне
            # Проверяем наличие данного ID, а так же статус этого ID в таблице проанализированных сообщений 'tg_messages_proceeded' и 'tg_auxilary_messages_proceeded'.
            # Если данное сообщение с ID существует в полях 'message_own_id' в этих таблицах и статус его в таблице 'tg_messages_proceeded' (если оно принадлежит таблице)
            # если статус сообщения равен 'IMAGE_DOWNLOADED_' (или type_id = 1) для сообщений с картинками, или 'DOCUMENT_DOWNLOADED_' (type_id = 4), то это сообщение 
            # пропускаем в цикле по сообщениям for.
            
            # 2. Отсечение на фильтрах зарегестрированных книг и томов
            # Общий список ids сообщений, обоих типов Photo и Audio, которые уже выполнили свою роль и на базе их были образованы и зарегестрированы
            # книги и их томы в библиотеке LABBA или Lib. Эти сообщения с заданного канала уже не надо скачивать
            # Дополнительный механизм отсечения - это удаленные , по тем или иным причинам, сущности на базе сообщений в модулях lib
            # Еще один механизм отсечения - это отсечение уже скчанных и находящихся сообщений в таблицах tg_proceeded. И четвертый, по умолчанию отсекаются 
            # сообщения, типы которых не Photo и Audio (на данный момент. В будущем этот ряд может быть увеличен)
            
            # 3. Отсечение на фильтрах удаленных сообщений в Lib-пространстве. Удаленные по тем или иным причинам книги или аудио-тома находятся в таблице 
            # 'lib_objects_removed'. Если они встречаются - их тоже отсекаем
            
            
        Точки отсечения в проекте:
        
        1. telegram_monitor/local_classes/telegram_manager.py --> download_media_telegram_self() -->> async for message in client.iter_messages() --> ~ Ln 365
        2. 
        3.
        
            
            
        RET: Возвращаетя True или False. Если True, то  messageId подпадает под отсечение, так как находится в общем списке 
        отчесения listGeneralMessageRejection и флаг flagLoadImgAnyway не принуждает обойти отсечение и все-равно пропустить сообщений 
        для дальнейшей обработки
        """
        
        print(f"PR_A955 --> START: messages_proccessing_rejector()")
        
        # INI
        

        
        # списки ids сообщений отсечения по разным аспектам и в разрезе messageSourceId - источника анализируемого сообщения
        listsMessagesIdsBySource =  AudiobooksChannelTelegramManager.get_lists_of_rejecting_messages_actgm (messageSourceId)
        
        

        # общий список ids сообщений, обоих типов Photo и Audio, которые уже выполнили свою роль и на базе их были образованы и зарегестрированы
        # книги и их томы в библиотеке LABBA или Lib
        listLibMessagesIdsDoneBySource = self.blf.obtain_lib_books_and_volumes_given_source_messages_ids_done_blf (messageSourceId)
        
        


        
        
        
        # B. Получить общий список тех сообщений, Которые необходимо удалить из таблиц tg_procceded (те, которые были скачаны с 
        # ошибкой и которые в следующих подходах могли бы заблокировать анализ, так как они типа есть, но они на самом деле скачаны с ошибкой
        # и не действительны)
        

        # 3. TODO: ОТСЕЧЕНИЕ НА УРОВНЕ УДАЛЕННЫХ ПО КАКИМ-ТО ПРИЧИНАМ СУЩНОСТЕЙ НА БАЗЕ РАНЕЕ СКАЧАННЫХ СООБЩЕНИЙ , и которые храняться в 
        # таблице-урне 'lib_objects_removed' 



        # IV. Аналитика и исполнение 


        # В зависимости от точки применения подключаем механизмы определенных реджекторов


        for case in Switch(enterPoint):
            
            
            # Точка 1: telegram_monitor/local_classes/telegram_manager.py --> download_media_telegram_self() 
            # -->> async for message in client.iter_messages() --> ~ Ln 365
            if case('TG_MESSAGE_LOADING'): 
                
                print(f"PR_A969 --> Вход по точке отсечения : TG_MESSAGE_LOADING")
                
                # A. Получить общий список ids сообщений в разрезе  id оригинальноги источника сообщений, по которому будет произведен анализ 
                # на отсечение текущего сообщения для дальнейшей обработки (то есть текущиее сообщений, найдя себя в этих списках, отсекается от 
                # дальнейшей обработки). Этот список - для данной точки входа
                
                listGeneralMessageRejectionBySource = (
                                listsMessagesIdsBySource['IMAGE_DOWNLOADED_'] 
                                + listsMessagesIdsBySource['DOCUMENT_DOWNLOADED_'] 
                                + listsMessagesIdsBySource['DECLARATIVE_AND_SIMPLE_'] 
                                + listLibMessagesIdsDoneBySource
                            )
                
                # Проверка текущего message_id для скачивания в списках отсечения и ОТСЕЧЕНИЕ !!! через continue
                if (
                    
                    # 1. ОТСЕЧЕНИЕ НА УРОВНЕ ПЕРВИНОГО СКАЧИВАНИЯ СООБЩЕНИЙ И АНАЛИЗА УЖЕ СУЩЕСТВУЮЩИХ СООБЩЕНИЙ В таблицах tg_proceeded_...
                    messageId in listGeneralMessageRejectionBySource
                    and not flagLoadImgAnyway # Флаг скачивания картинок, несмотря на то, что система обнаруживает, что сообщение с картинкой и описанием уже было обработано
                    ): # списки ID считанных в БД простых и декларративных сообщений
                    
                    print(f"PR_A952 --> SYS LOG: Сообщение с id = {messageId} подпадает под отсечение, так как входит в общий список отсечения \n{listGeneralMessageRejectionBySource}")
                    
                    ret = True
                    
                # Если  messageId не входит в список  listGeneralMessageRejection и флаг  flagLoadImgAnyway = True (то есть флаг говорит, что не важно все, 
                # пропустить messageId на дальнейшую обработку)
                else:
                    
                    print(f"PR_A953 --> SYS LOG: Сообщение с id = {messageId} НЕ подпадает под отсечение, так как НЕ входит в общий список отсечения \n{listGeneralMessageRejectionBySource} и флаг flagLoadImgAnyway = {flagLoadImgAnyway} не принуждает пропустить сообщение для дальнейшей обработки")

                    
                    ret = False
                
                break
            
            # Точка 2:
            if case('BOOK_COMPLECTS_FORMATING'): 
                pass
                break
            
            # Точка 3:
            if case('BOOK_COMPLECTS_REGISTRATION_IN_LABBA'): 
                pass
                break


            if case(): # default
                print('Другое')
                break
            
            
        print(f"PR_A956 --> END: messages_proccessing_rejector()")

            
        return ret






    def clear_tg_proceeded_tables_from_messages_with_given_statuses_blm (self, givenStatuses : list):
        """ 
        Очистить таблицу tg_messages_proceeded  от сообщений со статусами, заданных в списке givenStatuses
        Идентификация записей производится по ключу 'id' (автоинкрементный табличный id)
        
        """
        
        print(f"PR_A973 --> START: clear_tg_proceeded_tables_from_messages_with_given_statuses_blm()")

        # Получить ids сообщений из табл tg_messages_proceeded, которые имеют неправильный статус
        listWrongMessagesTbIds = self.tlf.get_tg_procceded_messages_tbids_with_given_statuses_tlf(givenStatuses)
        
        print(f"PR_A971 --> listWrongMessagesTbIds = {listWrongMessagesTbIds}")
        
        # если есть результат
        if not isinstance(listWrongMessagesTbIds, int):
        
            for tbId in listWrongMessagesTbIds:
            
                # Удалить сообщение с 'message_own_id' = mssgId
                self.tlf.delete_from_tg_messages_procceded_by_tbid_tlf(tbId)
                
        else: 
            print(f'PR_A972 --> SYS LOG: В таблице tg_messages_proceeded не найдены сообщения с ошибочными статусами, подлежащими удалению')

        print(f"PR_A974 --> END: clear_tg_proceeded_tables_from_messages_with_given_statuses_blm()")









    def load_registered_book_complect_to_own_tg_repository_blm (self, bookAlfaId, chatStorage, **parsTrough):
        """ 
        Выгрузить  зарегестрированный в библиотеке книжный комплект на свой ТГ репозиторий и зарегестрировать в БД
        выгрузки сущностей (как картинок для описания книги, так и ее аудио-тома)
        TODO: Сделать декомпозицию кода метода !
        TODO: Сделать что бы только один раз формировались списки сущностей для выгрузке по одной и той же книге. 
        Пока что каждый раз формируются списки, если книга отправляется в разные предписанные репозитории книги
        """

        # INI
        
        bookPublishDic = parsTrough['bookPublishDic']
        
        # Название фала картинки для описания книги
        fileImgName = bookPublishDic['bookImages'][0]
        
        bookImages = bookPublishDic['bookImages']
        
        bookImages = bookPublishDic['bookImages']
        
        # j/ Выгрузить аудио - тома в Хранилище аудио-томов в случае, если выбран вариант оотдельного хранения аудио-томов в отдельном чате. Ссылки на эти тома нужно вставить в тело описания книги !!!
        # сообщения с описанием книги

        # n/ Проверить наличие в табл регистрации , выгружалась ли уже описание текущей книги в заданный ТГ канал. Проверку наличия выгрузки выполнить 
        # в таблице 'lib_reposit_books_registr_<repositId>' по уникальному индексу (book_alfa_id и book_continue_part). book_continue_part -
        # дает возможность создавать продолжения книги. Задавать book_continue_part всегда. 0 - для первой начальной части книги !!!

        # g/ RENDERING описания книги на базе макета CH_MESSAGE_FOR_BOOK_DESCR_01 с разметкой для сообщения 
        # с описанием книги и необходимых атрибутов из данных по книжному комплекту 

        # print(f"PR_B206 --> bookPublishDic = ")
        # pp(bookPublishDic)
        
        # Название фала картинки для описания книги
        fileImgName = bookPublishDic['bookImages'][0]
        
        print(f"PR_B207 --> fileImgName = {fileImgName}")
        
        # Проверить наличие картинки для описания книги. Если нет - то вызвать ошибку в системе. Если картинка найдена в Хранилище, то сформировать 
        # полный путь к файлу картинки 
        uploadImgFullPath = TgPyrogramManager.prepare_book_img_file_path_by_img_name_tpm(fileImgName)
        
        # RENDERING !!!:  макета CH_MESSAGE_FOR_BOOK_DESCR_01 с необходимой разметкой текста для формирвоания сообщения с описанием книги и картинкой для обложки
        # В резудьтате получаем текст сообщения для параметра Caption для отправки сообщения типа 'Photo' в среде фреймворка Pyrogram
        finalBookDescr = TgRenderManager.render_template_for_ch_book_descr_message(ts.ABIBLIOT_TYPE_PHOTO_TEMPLATE, bookPublishDic)
        
        # PARS INI
        # uploadImgFullPath = uploadImgFullPath
        kwargs = {
            'caption' : finalBookDescr, # отформатированный и заполненный текст для сообщения типа 'Photo' в Pyrogram
        }

        # # ОТПРАВИТЬ картинку с описанием в ТГ-канал, идентифицируемый  через: chat
        # retMessageData = TgPyrogramManager.send_photo_tpm(chatStorage, uploadImgFullPath, **kwargs)
        
        # print(f"PR_B209 --> dicBooksPublishData = ")
        # pp(dicBooksPublishData)
        
        # ОТПРАВИТЬ книгу с группой картинок и аудио-томами. К главной картинке должно быть присоединено описание 
        
        # Подготовить список отправляемых группой сущностей с их настроенными параметрами
        
        listMediaGroup = []
        
        # A. Подготовка списка группы картинок (пока только картинок, но в принципе можно присоединять к группе любые сущности следующих типов:
        # InputMediaPhoto, InputMediaVideo, InputMediaAudio and InputMediaDocument)
        
        # Формируем список картинок в необходимом для Pyrogram формате на базе списка картинок из dicBooksPublishData['bookImages']
        # ПРИМ: в списке может быть и одна картинка. Через этот фактор можно обьединить отправку с одной картинкой и групповой. Просто делаем все - групповыми
        
        # Получить картинку альфа-книги по ее   message_id
        mainImgMessageId = bookPublishDic['bookData']['book_message_id']
        # Название главной картинки книги 
        bookMainImageName = self.blf.get_book_image_name_by_alfa_id_and_message_id_blf (bookAlfaId, mainImgMessageId)
        
        print(f"PR_B210 --> bookImageName = {bookMainImageName}")
        
        
        # ФОРМИРОВАНИЕ списка сущностей для Pyrogram
        for grImage in bookImages:
            
            uploadImgFullPath = TgPyrogramManager.prepare_book_img_file_path_by_img_name_tpm(grImage)
            
            print(f"PR_B211 --> uploadImgFullPath = {uploadImgFullPath}")
        
            # Проверить не является ли текущая картинка - главнйо каринкой книги, где должно располагаться описание (caption)
            # Если равны, то это главная каринка книги и именно ей нужно проставить описание и прочие атрибуты. если необходимо
            if grImage == bookMainImageName:
                pass
                captionPar = finalBookDescr
            else :
                captionPar = ''
        
            # Группа Pyrogram сущностей в списке 
            listMediaGroup.append(InputMediaPhoto(uploadImgFullPath, caption = captionPar))
        

        retMessageData = TgPyrogramManager.send_media_group_tpm(chatStorage, listMediaGroup, **kwargs)

        print(f"PR_B227 --> SYS LOG: Возврат после отправки сообщения с описанием альфа-книги: {bookAlfaId} \n {retMessageData} ")
        
        print(f"PR_B230 --> QN в возврате = {len(retMessageData)}")
        
        # print(f"PR_A925 --> retMessage")
        # pp(retMessageData)
        
        messageId = retMessageData[0].id
        
        print(f"PR_A925 --> messageId = {messageId}")
        
        # newMssgId = retMessageData
        
        # print(f"SYS LOG: В ТГ-канал: {chatStorage} загружены сообщения типа 'Photo', которое теперь имеют ids = {retMessageData}")
            
        # k/ Зафиксировать в БД все необходимые данные при успешном завершении загрузки книжного комплекта (репозитории выгруженных книг) 
        # Необходимо для несколькиих целей. В чстности для составления ссылок на будущем публичном сайте библиотек. 
        
        # PARS
        
        repositoryId = 1 # А-библиотека: Фантастика - Хранилище
        bookContinuePart = None # Продолжение уже существующей ранее книги (Пока не проработаны принциаы и алгоритмы)
        bookSerialsPart = None # Часть сериала книги (если книга относится к серии книг) (Пока не проработаны принциаы и алгоритмы)
        messageTypeId = self.tlf.get_tg_mssg_type_id_by_name_tlf('TEXT_WITH_IMAGE_MSSG_')
        
        libBookData = {
            'bookAlfaId' : bookAlfaId,
            'repositoryId' : repositoryId, 
            'bookContinuePart' : bookContinuePart,
            'bookSerialsPart' : bookSerialsPart,
            'messageTypeId' : messageTypeId, 
            'fileImgName' : fileImgName,
            # 'bookImages' : bookImages,
            
        }
        
        kwargs = {
            
            'libBookData' : libBookData, # Данные по текущей книге
            # 'retMssgLoadData' : retMessageData, # Возвращаемые данные, возвращаемые после загрузки сообщения в канал
        }
        

        #   ЗАРЕГЕСТРИРОВАТЬ выгруз картинки или группы картинок

        print(f"PR_B224 --> Тут регистрация выгруженных картинок")

        # # Зарегестрировать данные по выгруженному сообщению с картинкой и описанием книги в табл 'lib_reposit_books_registr_1' (<-- зависит от repositoryId)
        # # lastBookReposRegId - id новой созданной записи в таблице 'lib_reposit_books_registr_' с индексом текущего репозитория repositoryId (ТГ канала, куда загружается сообщение)
        # Цикл по списку ответов с ТГ-канала, куда было выгружено описание книги (с возможной группой картинок). От кол-ва картинок в группе зависит и 
        # кол-во ответов . Каждая картинка - это отдельное выгруженное сообщение
        for inx, retData in enumerate(retMessageData):
        
            print(f"PR_B231 --> Текущий ответ из группы отвтеов после выгрузки книги на ТГ канал. индекс в группе: {inx} \n{retData}")
        
            # print(f"PR_B232 --> retData.id  = {retData.id}")

            # Картинка, соотвтетсвующая текущему ответу с ТГ-канала, после закачивания на него сообщения
            imgName = bookImages[inx]
            # Табличный id текущей картинки в табл 'lib_book_images'
            imageLibTbid = self.blf.get_image_id_by_its_name_blf (imgName)
            
            kwargs['imageLibTbid'] = imageLibTbid

            newBookReposRegId = self.blf.register_repository_loaded_book_descr_message_data_blf(retData, **kwargs)

        # g/ Подготовить и отправить сообщения со всеми томами книги под ее описанием [!!! НЕ УДАЛЯТЬ]

        # INI
        # Диретория хранилища скаченных аудио-томов
        storageRoot = ms.TG_DOWNLOAD_PRIME_STORAGE
        dicAlfaBookVolumes = self.blf.get_lib_alfa_books_volumes_dic_for_given_lib_book_blf(bookAlfaId, indexDuplicated = True)
        dicBookVolumesTitles = self.blf.get_dic_book_volumes_titles_and_its_ids_by_alfa_id_blf(bookAlfaId)

        # Сформировать вхродную медиа-группу по всем томам книги (в том случае, когда мы хотим загружать аудио-тома группой под опиcанием книги)
        listMediaGroupForAudio = []
        # Счетчик накопления сообщений в группе (что бы не превысить 10)
        k = 0
        # Счетчик общих циклов для нахождения завершения цикла. По этому сигналу надо отправить группу на загрузку, даже если кол-во в группе не достигло 10
        m = len(dicAlfaBookVolumes) # Кол-во элементов в словаре
        
        # Отсортировать словарь по ключу в обратном порядке
        
        dKeys = list(dicAlfaBookVolumes.keys())
        
        dKeys.sort(reverse=True)
        
        dicAlfaBookVolumesSortedDesc = {i: dicAlfaBookVolumes[i] for i in dKeys}
        
        
        print(f"PR_B258 --> dicAlfaBookVolumes = {dicAlfaBookVolumes}")
        
        for volumeId, volumeName in dicAlfaBookVolumesSortedDesc.items():
            
            k += 1
            m -= 1
            
            print(f"PR_B257 --> Цикл накопления аудио-томов. inx = {k}")
            
            volumeFullPath = f"{storageRoot}/{volumeName}"
            
            # Если аудио-том имеет значение в поле 'volume_title'  и если в словаре не стоит в значении None (после корявого преобразования NULL в None), 
            # то прописываем значение title в caption - параметр
            if dicBookVolumesTitles[volumeId] and dicBookVolumesTitles[volumeId] != 'None' and dicBookVolumesTitles[volumeId] != None:
                listMediaGroupForAudio.append(InputMediaAudio(volumeFullPath, title = dicBookVolumesTitles[volumeId], caption = ""))
            else:
                listMediaGroupForAudio.append(InputMediaAudio(volumeFullPath))
            
            print(f"PR_A941 --> listMediaGroupForAudio = {listMediaGroupForAudio}")

            # Накапливаем в группу не более 10 томов ()
            if k < 10 and m > 0  :
                continue

            print(f"PR_B228 --> SYS LOG: Отправка аудио-томов альфа-книги: {bookAlfaId}.")


            # ОТПРАВКА ГРУППЫ С АУДИО-ТОМАМИ КНИГИ !!!
            # ВЫГРУЗИТЬ !!! сформированную медиа-группу (в том случае, когда мы хотим загружать аудио-тома группой под опичанием книги) 
            # TODO: try ..
            listRetMssgLoadData = TgPyrogramManager.send_media_group_tpm (chatStorage, listMediaGroupForAudio)
            
            # print(f"PR_A943 --> retMessage")
            # pp(retMessageData)
            print(f"PR_B229 --> SYS LOG: Возврат после отправки сообщения с аудио-томами книги: {bookAlfaId} \n {listRetMssgLoadData} ")
            
            # INI
            repositoryId = 1 # А-библиотека: Фантастика - Хранилище
            messageTypeId = self.tlf.get_tg_mssg_type_id_by_name_tlf('DOCUMENT_FILE_MSSG_')
            
            # Данные из библиотеки по книге - аудио-тому 
            libBookVolumeData = {
                
                # id регистрации книги в табл 'lib_reposit_books_registr_<RepositId>', соотвтетсвующей текущему репозиторию (текущему своему ТГ-каналу), 
                # связывающий эту медиа-группу с регистрацией книги-описания по реферальному полю FOREIGN KEY 'reposit_book_ref_id'
                
                'repositoryId' : repositoryId,
                'messageTypeId' : messageTypeId,
                'bookAlfaId' : bookAlfaId,
                'dicAlfaBookVolumes' : dicAlfaBookVolumes, # словарь с названиями файлов аудио-томов текущей книги с заданным bookAlfaId
                'dicBookVolumesTitles' : dicBookVolumesTitles, # словарь с заголовками к аудио-томам (Caption) заданной книги
            }
            
            # PARS
            
            kwargs = {
                
                'libBookVolumeData' : libBookVolumeData, # Данные из библиотеки по книге - аудио-тому 
                'listRetMssgLoadData' : listRetMssgLoadData, # возвратные данные после загрузки медиа-группы в ТГ-канал
            }

            # # ЗАРЕГЕСТРИРОВАТЬ тома
            
            print(f"PR_B225 --> Тут регистрация выгруженных томов аудио")

            # # Зарегестрировать данные о сообщении в виде медиа-группы с аудио-томами книги, выгруженной в свой заданный ТГ канал (репозиторий)
            # # Цикл по списку аудио-томов с внесением данных в БД производится внутри регистрационного метода по медиа-группе
            self.blf.register_repository_loaded_book_media_group_audio_volume_message_data_blf(**kwargs)
            
            # Обнуление списка накопления томов 
            listMediaGroupForAudio = []
            # Обнуление счетчика циклов накопления
            k = 0

        print(f"PR_B259 --> m = {m}")
        
        print(f"PR_A944 --> listRetMssgLoadData[0].id = {listRetMssgLoadData[0].audio.file_id}")



        # # i/ Зафиксировать в БД все необходимые данные при успешном завершении загрузки книжного комплекта (репозитории выгруженных книг) 
        # # Необходимо для несколькиих целей. В чстности для составления ссылок на будущем публичном сайте библиотек. 
        

        # # j/ Удаление из канала тоже 
        # # должно проводится с соблюдением целостности системы. То есть удалять в ручном режиме - нельзя. Только через программу, которая будет 
        # # удалять все зафиксированные в БД записи, связанные с удаляемыми обьектами из ТГ !!!  
    
    
    
    



    def load_registered_book_complect_to_assigned_list_of_repositories_blm (self, bookAlfaId, listBookAssignedRepositoriesTbids, **parsTrough):
        """ 
        Выгрузить зарегестрированный книжный комплект во все собственные, предписанные для данной книги, ТГ-репозитории (каналы)
        """


        for reposiTbid in listBookAssignedRepositoriesTbids:

            # PARS
            
            # Получить ID целевого ТГ-канала (репозитория)
            repositTgChId = self.blf.get_repositorty_tg_channel_id_by_its_tbid_blf(reposiTbid)
            
            # Присвоить параметру целевой отправки текущий ID ТГ-канала
            chatStorage = repositTgChId
            

            

            self.load_registered_book_complect_to_own_tg_repository_blm (
                    bookAlfaId, 
                    chatStorage, # ID ТГ канала
                    **parsTrough
                )
        
            print(f"PR_B473 --> LOG SYS: В свой ТГ-канал с ID = {chatStorage} выгружен одобренный к публикации зарегестрированный КК с bookAlfaId = {bookAlfaId}")






    def obtain_book_assigned_repositories_blm (self, bookAlfaId):
        """ 
        Получить предписанные для книги целевые репозитории.
        Эти репозитории определяются последовательн опо иерархии. Сначала анализируется табл 'lib_books_assigned_repositories'.
        Если в этой табл не найдены настройки по предписанным репозиториям, то тогда анализируется более общая табл настроек по целевым репозиториям, 
        базируясь на настройках Источник книги -> Предписанные репозитории для оригинального источника в табл 'lib_sources_assigned_repositories'
        """


        # АНАЛИЗ книги и его источника для определения на какой канал выгружать сообщение с этой книгой
        # Принципы: Сначала проверяется табл 'lib_books_assigned_repositories' и находится целевой репозиторий
        #   для данной книги. Если в этой таблице нет данных, то целевой репозиторий ищется в табл 'lib_sources_assigned_repositories'
        # После вычисления целевого репозитирия в зависимости от этого перенастраивается параметр в send_media_group_tpm()
        # который отвечает за то, куда будет выгружено сообщение


        bookTargetRepositories = []
        
        # A. Анализ табл 'lib_books_assigned_repositories' 
        
        sql = f"SELECT repository_id FROM {ms.TB_LIB_BOOKS_ASSIGNED_REPOSITORIES} WHERE book_alfa_id = {bookAlfaId}"
        
        #СПИСОК ЦЕЛЕВЫХ РЕПОЗИТОРИЕВ
        bookTargetRepositories = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        # END A. Анализ табл 'lib_books_assigned_repositories' 
        
        # Если есть предписания в табл 'lib_books_assigned_repositories' - отправить по всем репозиториям
        if not isinstance(bookTargetRepositories, int): 
            
            print(f"PR_B474 --> SYS LOG: В табл 'lib_books_assigned_repositories' найдены предписания по целевым репозиториям для книги с alfaIs = {bookAlfaId}. \nСписок предписанных репозиториев: {bookTargetRepositories}")
            


        # Если в табл 'lib_books_assigned_repositories' нет предписаний для текущей книги по целевым репозиторием, то
        # получаем дефолтные предписания по репозиториям из табл 'lib_sources_assigned_repositories', 
        # основанные на изначальных настройках источника книги и предписанных этому источнику репозиториев (которые
        # должны обязательно присутствовать, которые обладают более низкой иерархией и которые можно назвать дефолтными)
        # ПРИМ: Если нет дефолтных предписаний по ТГ-источнику книги и целевого репозитория для этого канала, то тогда книга 
        # - никуда НЕ отправляется, пока не будут проставлены предписания по репозитириям в самой книге в табл 'lib_books_assigned_repositories'
        else:
            # B. Анализ табл 'lib_sources_assigned_repositories'  для получения предписаний по репозиториям для книги , исходящих 
            # из настроек Источник -> предписанные репозитории

            # Оригинальный источник текущей книги
            bookSourceId = self.blf.get_book_source_id_by_alfa_id_blf(bookAlfaId)
            
            sql = f"SELECT repository_id FROM {ms.TB_LIB_SOURCES_ASSIGNED_REPOSITORIES} WHERE orig_source_id = {bookSourceId}"

            # СПИСОК ЦЕЛЕВЫХ РЕПОЗИТОРИЕВ, предписанны из настроек Источник  -> целевые репозитории из табл 'lib_sources_assigned_repositories'
            # ПРИМ: Эти настройки проставляются в ручную в VIEW: set_source_repositories_editor() : 
            # ~ http://127.0.0.1:6070/telegram_monitor/set_source_repositories_editor
            bookTargetRepositories = self.sps.get_result_from_sql_exec_proc_sps(sql)
            
            # END B. Анализ табл 'lib_sources_assigned_repositories'  для получения предписаний по репозиториям для книги , исходящих 
            
            # Если есть предписания в табл 'lib_sources_assigned_repositories' - отправить по всем репозиториям
            if not isinstance(bookTargetRepositories, int): 
                
                print(f"PR_B475 --> SYS LOG: В табл 'lib_sources_assigned_repositories' найдены предписания по целевым репозиториям для книги с alfaIs = {bookAlfaId}. \nСписок предписанных репозиториев: {bookTargetRepositories}")


            # Если не найдены целевые репозитории ни в табл 'lib_books_assigned_repositories' , ни в табл 'lib_sources_assigned_repositories'
            else:
                print(f"SYS LOG: В таблицах 'lib_books_assigned_repositories' и 'lib_sources_assigned_repositories' НЕ НАЙДЕНЫ предписания по целевым репозиториям для источника c id = {bookSourceId}  \nи далее для книги c alfaId = {bookAlfaId}. Поэтому книжный комплект НЕ БЫЛ ВЫГРУЖЕН ни в один репозиторий ")


        return bookTargetRepositories












if __name__ == '__main__':
    pass


    # # # # ПРОРАБОТКА: TODO: Перевести все в методы !!! {CURRENT 06-02-2024 12:41}
    # # регистрации новой книги в библиотеке с источником документов и описания в файловом репозитории скаченных файлов из каннала ТГ и 
    # # соотвтетсвенных таблиц с данными по скаченным сообщениям из ТГ канала

    # # 


    # # A. Входными параметрами на данный момент являются ID сообщений, который содержат описание книги с картинкой и прилагающиеся к ней айдио-тома
    # # TODO:Сделать автоматическое определение из таюлиц скачанных сообщений комплексы, состоящие из описания книги и ее аудио-тома !!!
    
    # """ 
    #     4213 - 4. ГЗ. Лидер.mp3
    #     4212 - 3. ГЗ. Пират.mp3
    #     4211 - 2. ГЗ. Элита.mp3
    #     4210 - 1. ГЗ. Невольник.mp3
    #     4209 - картинка и описание книги Герой земли
    # """


    # # {CURRENT 05-02-2024 23-16}
    
    # # INI CLASSES

    # tlf = TgLocalFuncs()
    # blm = BookLibraryManager()
    # sps = SqliteProcessorSpeedup(ms.DB_CONNECTION)
    
    
    # # PARS
    
    # flagRegVolumesAnyway = True # Флаг прохождения алгоритма регистрации аудио-томов книг в любом случае. невзирая даже на то. что книга уже зарегестрирована

    # # Кол-во циклов при разработке. Несмотря на любые установки, будет произведен только debugCycleQn циклов при считывании и обработке книг
    # # Если debugCycleQn = -1 , то система не реагирует на этот флаг вообще
    # debugCycleQn = -1 
    
    
    # # INI
    
    # dtStringFormat1, dtStringFormat2, universUnix = FG.get_current_time_format_1_and_2_and_universal_unix()


    # # формат словаря для набора сообющений в чате. которая формирует комплект сообщений, составляющий описание книги и ее аудио-тома
    # # dicTgBookComplectData = {
        
    # #     'book' : 4209,
    # #     'volumes' : {
    # #                     1 : '4210',
    # #                     2 : '4211',
    # #                     3 : '4212',
    # #                     4 : '4213'
    # #                 }
    # # }
    
    
    # # F. Организовать цикл по книжным комплектам из таблицы 'tg_book_complect_volumes_ch_01' , предварительно сформировав для каждого цикла словарь комплекта формата 
    # """ 
    # dicTgBookComplectData = {
        
    #     'book' : 4209,
    #     'volumes' : {
    #                     1 : '4210',
    #                     2 : '4211',
    #                     3 : '4212',
    #                     4 : '4213'
    #                 }
    # }
    # """
    
    # sql = f"SELECT * FROM {ms.TB_TG_BOOK_COMPLECTS_CH_01}"
    
    # tgBookComplects = sps.get_result_from_sql_exec_proc_sps(sql)
    
    
    
    # for inx, bookComplectRow in enumerate(tgBookComplects):
        
        
    #     print(f"PR_A374 --> SYS LOG: for cycle inx = {inx}")
        
        
    #     if debugCycleQn > 0 and inx > debugCycleQn - 1:
            
    #         print(f"PR_A372 --> Ограничение по кол-ву циклов debugCycleQn для разработки = {debugCycleQn}. Прерываем цикл for... , так как этот предел достигнут. for inx = {inx}")
    #         break
        

        
    #     # INI
    #     bkwargs = {}
    #     bookRefId = bookComplectRow[0]
    #     bookMsgId = bookComplectRow[1]
    #     bookTitle = tlf.get_book_title_by_tg_message_id(bookMsgId)
        
    #     origSourceId = 1 # соотвтетсвует ТГ каналу "Аудиокниги фантастика" из таблицы 'lib_orig_sources'
        
    #     bkwargs['origSourceId'] = origSourceId # соотвтетсвует ТГ каналу "Аудиокниги фантастика" из таблицы 'lib_orig_sources'
        
    #     print(f"""PR_A270 --> SYS LOG: START: Обработка следующего книжного комплекта с message_own_id = {bookMsgId} с названием : {bookTitle}
    #         \nfor loop in tgBookComplects, CYCLE: bookComplectrow = {bookComplectRow}""")
        
    
    #     # сформировать словарь комплекта
        
    #     sql = f"SELECT * FROM {ms.TB_TG_BOOK_COMPLECT_VOLUMES_CH_01} WHERE book_complect_id_ref = {bookRefId}"
        
    #     print(f"PR_A310 --> sql = {sql}")
        
    #     bookComplectVolumes = sps.get_result_from_sql_exec_proc_sps(sql)
        
    #     print(f"PR_A309 --> bookcomplectVolumes = {bookComplectVolumes}")
        
        
    #     # Анализ: Если в комплекте есть название книги и нет аудио-томов, то тут две вероятности: 1. Автор канала еще не успел выгрузить тома,
    #     # а книга является последним сообщением-книгой  в ТГ канале. 2. Перед этим сообщением-книгой было фиктивное сообщение-книга. распознанное 
    #     # системой как книга, но таковой не являющимся (это скорее всего какой-то новый тип сообщения. типа картинка с описанием. но не являющийся
    #     # описанием книги) TODO: придумать решение в ходе реализации проекта
    #     qnVolums = len(bookComplectVolumes)
        
        
        
        
        
    #     # сформировать словарь комплекта. x[3] - соотвтетсвуют полю 'volume_order' в возвращенном элементе списка списков bookComplectVolumes
    #     # x[4] - 'volume_msg_id' . Из табл 'tg_book_complect_volumes_ch_01'
    #     dicTgBookComplectData = {
    #         'book' : bookMsgId,
    #         'volumes' : {x[3] : x[2] for x in bookComplectVolumes}
    #     }
        
    #     print(f"PR_A269 --> dicTgBookComplectData = {dicTgBookComplectData}")



    #     # ПРОВЕСТИ ОБРАБОТКУ И АНАЛИЗ каниги на основе словаря комплекта

    #     # INI
    #     bookMsgId = dicTgBookComplectData['book']
        
    #     volumes = dicTgBookComplectData['volumes']
    #     volumsQn = len(volumes) # кол-во томов у книги



        
    #     # A. Получить словарь с полным набором данных по книге, включая данные по парсингу и данные при первичном анализе и загрузке книги с ТГ канала
    #     dicFullBookData = blm.get_full_book_data_by_chat_mssg_id_for_CH1 (bookMsgId)    

        
    #     # B. Предварительная ПРОВЕРКА НАЛИЧИЯ уже зарегестрированной книги в библиотеке {CHECK REGISTRATION}
    #     #INI
    #     bookTitle = dicFullBookData['descrParsingData']['bookTitle']
    #     authorSecondname = dicFullBookData['descrParsingData']['authorSecondname']
    #     #PAR
    #     dicCheckData = {
    #                 'bookTitle' : bookTitle,
    #                 'authorSecondname' : authorSecondname
    #             }
        
    #     # Проверить наличие книги по двум параметрам : название книги и ее автор. Если совпадает, то на данный момент считаем, что книга уже зарегестрирована
    #     ifRegistered = blm.check_if_book_registered_already (dicCheckData)
        

    #     # print(f"PR_A223 --> dic = {dicBookData}")
        
    #     if ifRegistered: # Если уже зарегестрирована
    #         print(f"PR_A259 --> SYS LOG: Эта книга {dicCheckData['bookTitle']} с автором {dicCheckData['authorSecondname']} уже есть в базе, поэтому не регистрируем ее")
    #     else:
    #         print(f"PR_A260 --> SYS LOG: Этой книги {dicCheckData['bookTitle']} с автором {dicCheckData['authorSecondname']} НЕТ в базе, поэтому регистрируем ее")
        
        
    #         # Зарегестрировать новую книгу в библиотеке
    #         newAlfaBookId = blm.register_new_book_in_libba_blm(dicFullBookData, **bkwargs)
            
        
        
    #         # D. Проверить, обновить или зарегестрировать аудио-тома книги
            
    #         # получить спискок данных об аудил-томах книги
    #         listDfRowsDictsBookVolumes = blm.get_list_of_dicts_book_audio_volums_by_own_mssg_id(bookMsgId)
            
    #         print(f"PR_A373 --> listBookVolumes = {listDfRowsDictsBookVolumes}")
            
    #         # Цикл по томам книги
            
    #         for volume in listDfRowsDictsBookVolumes:
                
    #             # INI
                
    #             print(f"PR_A377 --> volume = {volume}")
                
    #             volumeFileName = volume['message_document_name']
                
    #             print(f"PR_A378 --> volumeFileName = {volumeFileName}") 
                
                
            
    #             # Проверить, зарегестрирован ли такой том уже у книги
                
    #             sql = f"SELECT * FROM {ms.TB_LIB_BOOK_AUDIO_VOLUMES} WHERE volume_file_name = '{volumeFileName}'"
            
    #             # Проверить, есть ли запись в таблице с названием = volumeName
    #             ifVolNameExists = sps.if_select_result_exists_sps(sql)
                
    #             print(f"PR_A379 --> Наличие в таблице 'lib_book_audio_volumes'  записи в поле с названием {volumeFileName} ifVolNameExists = {ifVolNameExists}")
                
    #             # АНАЛИЗ
                
    #             # Если запись с таким названием существует, значит такой том на уровне как минимум информационной записи существуует
    #             # TODO: Ввести статус тома
                
    #             # Если запись с таким названием тома уже зарегестрирована и существует, то либо мы пропускаем цикл, либо. в зависимости от декларативного флага,
    #             # все - равно обновляем все тома (volumes) книги, так как они могли измениться за счет того. что автор канала загрузил в пустышки 
    #             # выпущенные тома и их названия уже стали другими и их нужно обновить.(???) Вернее, пустышки со стандартынми названиями могли быть 
    #             # заменены другими названиями (но тогда и их названия не будет. вобщем - продумать). пока делаем UPDATE томов, если стоит флаг : проанализировать по любому
    #             if ifVolNameExists: 
                    
    #                 pass
                
    #             # Если не существует, то вставляем информационную запись с названием тома книги
    #             else:
                    
    #                 pass
                
    #                 sql = f"""
    #                             INSERT INTO {ms.TB_LIB_BOOK_AUDIO_VOLUMES} 
    #                                 (
    #                                     books_alfa_id, volume_file_name, date_reg_calend, date_reg_unix
    #                                 )
    #                             VALUES 
    #                             (
    #                                 {newAlfaBookId}, '{volumeFileName}', '{dtStringFormat2}', {universUnix}
    #                             )
    #                         """
                            
    #                 # print(f"PR_A376 --> sql = {sql}")
                    
                    
    #                 print(f"PR_A380 --> START EXECUTE SQL")
                    
    #                 sps.execute_sql_SPS(sql)
                    
                    
    #                 print(f"PR_A382 --> SYS LOG: В таблицу 'lib_book_audio_volumes' внесена запись по sql: \n {sql}")
                    
                    
    #                 newValumeId = sps.get_last_rowid_from_tb_sps(ms.TB_LIB_BOOK_AUDIO_VOLUMES)
                    
                    
    #                 # J. Проставить статусы для записанного тома книги
    #                 # А именно, что как мнимум прописана информация по тому книги
    #                 # по факту тнфрмация загруэена. но не загружен сам файл в директроию первичной загрузки
                    
                    
    #                 # 1. Проставление статуса информационной загрузки в БД тома книги
                    
    #                 volumeStatus = 1 # -> 'VOLUME_INFOR_INSERTED'
                    
    #                 sql = f"INSERT INTO {ms.TB_LIB_VOLUMES_VOLUME_STATUSES} (book_volume_id, volume_status_id) VALUES ({newValumeId}, {volumeStatus})"
                    
    #                 print(f"PR_A381 --> START EXECUTE SQL")
                    
    #                 sps.execute_sql_SPS(sql)
                    
    #                 print(f"PR_A383 --> SYS LOG: В таблицу 'lib_volumes_volume_statuses' внесена запись по sql: \n {sql}")

                    
    #                 # PARS
                    
    #                 # Подтверждение загрузки данных скаченного файла в относительной директории (на данынй момент в : 
    #                 # /home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django/telegram_monitor/static/telegram_monitor/audio_books/books_img_downloaded/ch_1
                    
                    
                    
            
            

        
        
    





























