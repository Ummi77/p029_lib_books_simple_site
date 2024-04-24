

import sys
sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')
import settings_bdp_main as ms # общие установки для всех модулей

from noocube.pandas_manager import PandasManager
from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup
from noocube.sqlite_pandas_processor_speedup import SqlitePandasProcessorSpeedup
from beeprint import pp
from noocube.files_manager import FilesManager
import noocube.funcs_general as FG
from telegram_monitor.local_classes.tg_local_funcs import TgLocalFuncs
from telegram_monitor.local_classes.stractures import LibUniqueMessage

from noocube.switch import Switch

# from noocube.funcs_general_class import FunctionsGeneralClass



# Глобальные обьекты для этого модуля



class BookLibraryFuncs ():
    """ 
    Методы для библиотеки книг
    """
    
    
    def __init__(self): 

        self.sps = SqliteProcessorSpeedup(ms.DB_CONNECTION) # Обьект класса SqliteProcessorSpeedup
        self.spps = SqlitePandasProcessorSpeedup(ms.DB_CONNECTION) # Обьект класса SqlitePandasProcessorSpeedup
        self.tlf = TgLocalFuncs()
    


    def get_alfa_book_data_by_tg_chat_message_id_blf (self, origSourceId, bookMssgId):
        """  
        Получить данные по книге из библиотеки LIBBA по id источника оригинала и id сообщения в ТГ канале
        """
        
        print(f"PR_A344 --> START: get_dic_book_data_by_chat_message_id_tlf()")

        sql = f"SELECT *  FROM {ms.TB_LIB_BOOKS_ALFA}, {ms.TB_LIB_BOOKS_ALFA_EXT} WHERE {ms.TB_LIB_BOOKS_ALFA}.id = {ms.TB_LIB_BOOKS_ALFA_EXT}.books_alfa_id"



        df = self.spps.read_sql_to_df_pandas_SPPS(sql)
        
        df = PandasManager.index_duplicated_name_columns_in_df(df)
        
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(df, True, printFull = True, marker='PR_A347 --> ')

        
        # Комплексный ключ идентификации нужного ряда в фрейме
        listOfKeyVals = [ 
            {'key' : 'book_message_id', 'val' : bookMssgId },
            {'key' : 'book_orig_source_id', 'val' : origSourceId },
        ]
        
        # print(f"PR_A369 --> listOfKeyVals = {listOfKeyVals}")
        
        # Конвертировать один ряд фрейма , взятый по значению в поле-ключе, в словрь
        dicBookData = PandasManager.read_df_row_to_dic_by_multiple_key_val_stat_pm (df, listOfKeyVals)
        
        # print(f"PR_A346 --> dic = {dicBookData}")
        
        print(f"PR_A345 --> END: get_dic_book_data_by_chat_message_id_tlf()")

        
        return dicBookData
    
    
    
    
    def get_alfa_book_data_by_alfa_id (self, bookAlfaId):
        """  
        OBSOLETED: use get_lib_book_full_data_by_alfa_id_as_dic_blf()
        
        Получить данные по книге из библиотеки LIBBA по book_alfa_id
        
        RET:
        
        dicBookData = 
        {
            'id': 5, 
            'liter_group_z': '0000000005', 
            'liter_group_y': '000', 
            'liter_group_x': '000', 
            'final_ilbn': '000-000-0000000005', 
            'date_reg_calend': '05-03-2024 15:42:04', 
            'date_reg_unix': 1709650000.0, 
            'id_1': 5, 
            'books_alfa_id': 5, 
            'book_title': 'Звездная месть', 
            'book_description': '\r\n\r\n ХХV век. Мощь земной цивилизации безгранична. Ее космический флот может уничтожить любую нечеловеческую расу в отдельности и все их вместе взятые. Однако, в своем могуществе Земля не замечает нависшей над ней чудовищной угрозы Вторжения Извне, с которой человечеству еще никогда не приходилось сталкиваться. Надвигающийся апокалипсис может предотвратить космодесантник-смертник, младенцем найденный в анабиозной капсуле на краю вселенной...\r\n', 
            'book_message_id': 4390, 
            'book_orig_source_id': 1, 
            'date_issue_calend': 'NULL', 
            'date_issue_unix': None, 
            'language_id': 1, 
            'serial_id': None, 
            'language_relation_id': None}

        """
        
        print(f"PR_A370 --> START: get_dic_book_data_by_chat_message_id_tlf()")

        sql = f"SELECT *  FROM {ms.TB_LIB_BOOKS_ALFA}, {ms.TB_LIB_BOOKS_ALFA_EXT} WHERE {ms.TB_LIB_BOOKS_ALFA}.id = {ms.TB_LIB_BOOKS_ALFA_EXT}.books_alfa_id AND books_alfa_id = {bookAlfaId}"

        print(f"PR_A912 --> sql = {sql}")
        
        # # Для SQLite
        # df = self.spps.read_sql_to_df_pandas_SPPS(sql)
        
        # Для MySQL
        df = self.spps.read_sql_to_df_pandas_mysql_spps(sql)

        
        
        df = PandasManager.index_duplicated_name_columns_in_df(df)
        
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(df, True, printFull = True, marker='PR_A347 --> ')

        # print(f"PR_A369 --> listOfKeyVals = {listOfKeyVals}")
        
        # Конвертировать один ряд фрейма , взятый по значению в поле-ключе, в словрь
        dicBookData = PandasManager.read_df_with_one_row_to_dic_stat_pm (df)
        
        # print(f"PR_A346 --> dic = {dicBookData}")
        
        print(f"PR_A371 --> END: get_dic_book_data_by_chat_message_id_tlf()")
        
        return dicBookData
        
    
    
    
    
    
    def get_book_message_id_by_alfa_id_blf (self, bookAlfaId):
        """ 
        Получить bookMessagId книги с alfaId
        """
        
        bookMessageId = self.get_alfa_book_data_by_alfa_id (bookAlfaId)['book_message_id']
        
        return bookMessageId
    
    
    
    
    def get_book_source_id_by_alfa_id_blf (self, bookAlfaId):
        """ 
        Получить bookSourceId книги с alfaId
        """
        
        bookSourceId = self.get_alfa_book_data_by_alfa_id (bookAlfaId)['book_orig_source_id']
        
        return bookSourceId
    
    
    

    
    
    
    
    def get_book_original_source_tg_channel_id_by_tbid_blf(self, origSourceTblId):
        """ 
        Получить id entity (ТГ-канала) исходного источника образующего сообщения по табличному id из табл  'lib_orig_sources'
        """
        
        sql = f"SELECT tg_channel_id FROM {ms.TB_LIB_ORIG_SOURCES} WHERE id = {origSourceTblId}"
        
        origSourceTgChannelid = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return origSourceTgChannelid[0]
    
    
    
    
    
    
    
    def get_alfa_book_id_by_orig_src_and_tg_msg_id_blf (self, origSourceId, bookMssgId):
        """ 
        Получить id альфа-книги по id ее источника и id сообщения в ТГ канале с описанием этой книги 
        """
        
        dicBookData = self.get_alfa_book_data_by_tg_chat_message_id_blf(origSourceId, bookMssgId)
        
        alfaBookId = dicBookData['books_alfa_id']
        
        return alfaBookId
        
        

    
    
    
    
    
    def get_source_orig_tg_link_blf (self, sourceId):
        """ 
        Получить сылку на канал , определяемый его id в табл 'lib_orig_sources'
        """

        sql = f"SELECT tg_channel_link FROM {ms.TB_LIB_ORIG_SOURCES} WHERE id = {sourceId}"
        
        sourctLink = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return sourctLink[0]
        
        


    def get_book_statuses_by_alfa_id (self, bookAlfaId) :
        """ 
        Получить список статусов книги 
        """
        
        sql = f"SELECT * FROM {ms.TB_LIB_BOOKS_STATUSES}, {ms.TB_LIB_BOOK_STATUSES} WHERE {ms.TB_LIB_BOOKS_STATUSES}.book_status_id = {ms.TB_LIB_BOOK_STATUSES}.id AND book_alfa_id = {bookAlfaId}"
        
        listBookStatuses = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return listBookStatuses
    
    
    
    
    def get_book_categories_by_alfa_id (self, bookAlfaId) :
        """ 
        Получить список категорий книги 
        """
        
        sql = f"SELECT * FROM {ms.TB_LIB_BOOKS_CATEGORIES}, {ms.TB_LIB_CATEGORIES} WHERE {ms.TB_LIB_BOOKS_CATEGORIES}.category_id = {ms.TB_LIB_CATEGORIES}.id AND book_alfa_id = {bookAlfaId}"
        
        listBooksCategories = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return listBooksCategories
    
    
    
    # def get_list_book_statuses_ids_by_alfa_id (self, bookAlfaId) :
    #     """ 
    #     Получить список ids статусов книги 
    #     TEMP: listBookStatuses = [[1, 1, 1, 'REGISTERED']]
    #         PR_A553 --> listBookStatuses = [[1, 1, 1, 'REGISTERED']]
    #         PR_A553 --> listBookStatuses = [[4, 1, 1, 'REGISTERED']]
    #         PR_A553 --> listBookStatuses = [[3, 1, 1, 'REGISTERED']]
    #         PR_A553 --> listBookStatuses = [[5, 1, 1, 'REGISTERED']]
    #         PR_A553 --> listBookStatuses = [[6, 1, 1, 'REGISTERED']]
    #         PR_A553 --> listBookStatuses = [[2, 1, 1, 'REGISTERED']]

    #     """
        
    #     listBookStatuses = self.get_book_statuses_by_alfa_id(bookAlfaId)
        
    #     listBookStatusesIds = [x for x in listBookStatuses]
        
    #     return listBookStatusesIds
    
    



    def get_book_genres_by_alfa_id (self, bookAlfaId) :
        """ 
        Получить список жанров книги 
        """
        
        sql = f"SELECT * FROM lib_books_genres, lib_genres WHERE lib_books_genres.genre_id = lib_genres.id AND book_alfa_id = {bookAlfaId}"
        
        listBookGenres = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return listBookGenres




    # def get_book_categories_by_alfa_id (self, bookAlfaId) :
    #     """ 
    #     Получить список категорий книги 
    #     """
        
    #     sql = f"SELECT * FROM lib_books_categories, lib_categories WHERE lib_books_categories.category_id = lib_categories.id AND book_alfa_id = {bookAlfaId}"
        
    #     listBookCategories = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
    #     return listBookCategories





    def get_lib_book_complex_data_by_alfa_id (self, bookAlfaId) :
        """ 
        Получить набор многих данных по книге: списки авторов, статусов, жанров. категорий
        """
        
        dicBookcomplexData = {
            
            'listBookAuthors' : self.get_authors_of_book_by_alfa_id(bookAlfaId),
            'listBookStatuses' : self.get_book_statuses_by_alfa_id(bookAlfaId),
            'listBookGenres' : self.get_book_genres_by_alfa_id(bookAlfaId),
            'listBookCategories' : self.get_book_categories_by_alfa_id(bookAlfaId),
            'listBookDescrImgs' : self.get_book_descr_images_by_alfa_id(bookAlfaId),
            'full_descript_data' : self.get_alfa_book_data_by_alfa_id(bookAlfaId)  

        }

        return dicBookcomplexData




    def get_book_descr_images_by_alfa_id (self, bookAlfaId):
        """ 
        OBSOLETED: use get_book_descr_image_name_for_photo_mssg_type_by_alfa_id()
        Получить список картинок, принадлежащих описанию книги по bookAlfaId
        """
        
        
        sql = f"SELECT * FROM {ms.TB_LIB_BOOKS_IMAGES}, {ms.TB_LIB_BOOK_IMAGES} WHERE lib_books_images.book_image_id = lib_book_images.id AND book_alfa_id = {bookAlfaId}"
        
        print(f"PR_A368 --> sql = {sql}")
        
        listBookDescrImgs = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        listBookDescrImgs = [x[-2] for x in listBookDescrImgs]
        
        return listBookDescrImgs




    def get_book_descr_images_by_alfa_id_for_book_object_creation_blf (self, bookAlfaId):
        """ 
        OBSOLETED: use get_df_book_descr_images_by_alfa_id_for_book_object_creation_blf [03-04-2024]
        Получить список картинок, принадлежащих описанию книги по bookAlfaId  для использования при создании обьекта книги
        """
        
        
        sql = f"SELECT * FROM {ms.TB_LIB_BOOKS_IMAGES}, {ms.TB_LIB_BOOK_IMAGES} WHERE lib_books_images.book_image_id = lib_book_images.id AND book_alfa_id = {bookAlfaId}"
        
        print(f"PR_A368 --> sql = {sql}")
        
        listBookDescrImgs = self.sps.get_result_from_sql_exec_proc_sps(sql)
        

        return listBookDescrImgs




    def get_df_book_descr_images_by_alfa_id_for_book_object_creation_blf (self, bookAlfaId):
        """ 
        Получить список картинок, принадлежащих описанию книги по bookAlfaId  для использования при создании обьекта книги
        """
        
        
        sql = f"SELECT * FROM {ms.TB_LIB_BOOKS_IMAGES}, {ms.TB_LIB_BOOK_IMAGES} WHERE lib_books_images.book_image_id = lib_book_images.id AND book_alfa_id = {bookAlfaId}"
        
        print(f"PR_A368 --> sql = {sql}")
        
        dfBookDescrImgs = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        

        return dfBookDescrImgs










    def get_our_repositories_where_book_downloaded_to_by_alfa_id_blf (self, bookAlfaId):
        """ 
        Получить список наших репозиториев, в которые книга была выгружена
        """
        
        
        sql = f"SELECT * FROM {ms.TB_LIB_BOOKS_LOADED_TO_REPOSITORIES}, {ms.TB_LIB_REPOSITORIES} WHERE {ms.TB_LIB_BOOKS_LOADED_TO_REPOSITORIES}.repository_id = {ms.TB_LIB_REPOSITORIES}.id AND book_alfa_id = {bookAlfaId}"
        
        print(f"PR_A368 --> sql = {sql}")
        
        listBookDRepositoriesDownloadedTo = self.sps.get_result_from_sql_exec_proc_sps(sql)
        

        return listBookDRepositoriesDownloadedTo









    def get_book_descr_image_name_for_photo_mssg_type_by_alfa_id (self, bookAlfaId):
        """ 
        OBSOLETED: [31-03-2024] use get_book_images_names_dic_in_lib_by_alfa_id()
        Получить картинку, принадлежащих описанию книги по bookAlfaId в сообщении типа: PHOTO (где всегда присвоена только не более одной картинки)
        """
        
        
        sql = f"SELECT image_name FROM {ms.TB_LIB_BOOKS_IMAGES} as lbsi, {ms.TB_LIB_BOOK_IMAGES} as lbi WHERE lbsi.book_image_id = lbi.id AND book_alfa_id = {bookAlfaId}"
        
        # print(f"PR_A368 --> sql = {sql}")
        
        imgName = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        
        return imgName[0]






    def get_book_images_names_dic_in_lib_by_alfa_id_blf (self, bookAlfaId):
        """ 
        NEW: 31-03-2024
        Получить  словарь картинок, принадлежащих описанию книги по bookAlfaId в формате : Словарь tg_message_id -> image_name
        ПРИМ: для картинок в библиотеке однозначным ключем могут выступать несколько ключей : 
        bookAlfaId - tg_message_id, tg_message_id - orig_source_id, само название картинки уникально и tbid табл 'lib_book_images'
        """
        
        
        sql = f"SELECT image_name, tg_message_id FROM {ms.TB_LIB_BOOKS_IMAGES} as lbsi, {ms.TB_LIB_BOOK_IMAGES} as lbi WHERE lbsi.book_image_id = lbi.id AND book_alfa_id = {bookAlfaId}"
        
        # print(f"PR_A368 --> sql = {sql}")
        
        # bookImagesnames = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        # Словарь tg_message_id -> image_name
        dicAlfaBookImagesNames = self.spps.read_sql_to_dic_like_group_by_mysql_spps(sql, 'tg_message_id', 'image_name')
        
        # # Избавляемся от списка в названии файла
        dicAlfaBookImagesNames = {x:y[0] for x, y in  dicAlfaBookImagesNames.items()}
            
    
        
        return dicAlfaBookImagesNames





    def get_book_image_name_by_alfa_id_and_message_id_blf (self, bookAlfaId, messageId ):
        """ 
        NEW: 31-03-2024
        Получить название картинки книги по id альфа-книги и по messageId картинки
        """
        
        dicAlfaBookImagesNames = self.get_book_images_names_dic_in_lib_by_alfa_id_blf(bookAlfaId)
        
        bookImageName = dicAlfaBookImagesNames[messageId]
        
        return bookImageName
        
        














    def assign_image_to_given_alfa_book_blf (self, bookAlfaId, imgName, **bkwargs):
        """ 
        OBSOLETED: Использовать assign_image_to_being_registered_alfa_book_blf() более оптимальный вариант метода с параметром dicTgBookData ниже
        Присвоить картинку к книге. Внести ее в две таблицы 'lib_book_images' и 'lib_books_images'
        relDir -  относителльынй директорий, начиная с принятого стандартным директория 'books_images' (в любом проекте на любом сервере или PC)
        """
        print(f"PR_A356 --> START: assign_image_to_given_alfa_book_blf()")
        
        
        # Относительный диреторий после принятого стандартом 'books_images' (который должен быть в любом проекте на любом сревере или PC)
        # В данном случае задается в INI части VIEW в ручном режиме 
        
        
        # print(f"PR_A457 --> bkwargs = {bkwargs}")
        
        relImgDir = bkwargs['relImgDir']
        
        
        sql = f"iNSERT INTO {ms.TB_LIB_BOOK_IMAGES} (image_name, relative_subdir) VALUES ('{imgName}', '{relImgDir}')"
        
        # SQL EXECUTE: 
        flagInserted = False
        try: 
            print(f"PR_A358 --> START EXECUTE SQL")
            self.sps.execute_sql_SPS(sql)
            # print(f"""PR_A319 --> SYS SQL LOG: В таблицы расширений 'tg_message_proceeded_ext' или 'tg_auxilary_messages_proceeded_ext' внесена запись по sql-запрос:\n sql = {sql}""")
            flagInserted = True
        except Exception as err:
            print(f"""PR_A359 --> SYS SQL LOG: SQL EXEUTION ERROR!!! \n  sqlError = {sql}""")
            
            print(f"PR_A360 --> ERROR: {err}")
            flagInserted = False
    
    
        if flagInserted: # Если предыдущий запрос INSERT прошел успешно
            # # Получить последний ID в таблице tg_messages_proceeded (что бы иметь этот ключ для созданя записи в расширении этой таблицы в tg_message_proceeded_ext)
            # sql = f"SELECT rowid from {ms.TB_LIB_BOOK_IMAGES} order by ROWID DESC limit 1"
            
            # res = self.sps.get_result_from_sql_exec_proc_sps(sql)
            
            lastId = self.sps.get_last_inserted_id_in_db_mysql_sps()
            print(f"PR_A361 --> Последний row_id или lastId = {lastId}")

            dicInsertData = {
                'book_alfa_id' : bookAlfaId,
                'book_image_id' : lastId
            }

            try:
                
                print(f"PR_A362 --> START EXECUTE SQL")
                self.sps.insert_record_to_tb_with_many_to_many_relation(ms.TB_LIB_BOOKS_IMAGES, dicInsertData)
                
            except Exception as err:
                print(f"""PR_A363 --> SYS SQL LOG: SQL EXEUTION ERROR!!! \n  sqlError = {sql}""")
                
                print(f"PR_A364 --> ERROR: {err}")
        
        # print(f"PR_A249 -->  SYS DB LOG: присвоен новый статус {bookStatus} для книги с id = {bookId}")

        print(f"PR_A357 --> END: assign_image_to_given_alfa_book_blf()")





    def assign_image_to_being_registered_alfa_book_blf (self, bookAlfaId, dicTgGroupMessageData, **bkwargs):
        """ 
        Создать запись по регестрируемой картинке в табл 'lib_book_images'  и присвоить картинку книге в табл 'lib_books_images'
        dicTgGroupMessageData - Словарь с данными сообщения из ТГ-канала из табл 'tg_messages_proceeded' и 'tg_message_proceeded_ext'
        relDir -  относителльынй директорий, начиная с принятого стандартным директория 'books_images' (в любом проекте на любом сервере или PC)
        RET: Возвращает id созданной картинки в табл 'lib_book_images' 
        """
        print(f"PR_B124 --> START: assign_image_to_being_registered_alfa_book_blf()")
        
        

        
        # INI
        
        
        # Относительный диреторий после принятого стандартом 'books_images' (который должен быть в любом проекте на любом сревере или PC)
        # В данном случае задается в INI части VIEW в ручном режиме 
        
        relImgDir = bkwargs['relImgDir']
        
        # Текущая регестрируемая шрупповая картинка-сообщение
        imgName = dicTgGroupMessageData['message_img_name']
        imgSourceId = dicTgGroupMessageData['channels_ref_id'] # id Источника ТГ-канала картинки
        imgTgMessageId = dicTgGroupMessageData['message_own_id'] # id сообщения текущей регистрируемой картинки
        
        
        
        sql = f"""INSERT INTO {ms.TB_LIB_BOOK_IMAGES} 
        (image_name, relative_subdir, orig_source_id, tg_message_id) 
        VALUES ('{imgName}', '{relImgDir}', {imgSourceId}, {imgTgMessageId})"""
        
        # SQL EXECUTE: 
        flagInserted = False
        try: 
            print(f"PR_B125 --> START EXECUTE SQL")
            self.sps.execute_sql_SPS(sql)
            # print(f"""PR_A319 --> SYS SQL LOG: В таблицы расширений 'tg_message_proceeded_ext' или 'tg_auxilary_messages_proceeded_ext' внесена запись по sql-запрос:\n sql = {sql}""")
            flagInserted = True
        except Exception as err:
            print(f"""PR_B126 --> SYS SQL LOG: SQL EXEUTION ERROR!!! \n  sqlError = {sql}""")
            
            print(f"PR_B127 --> ERROR: {err}")
            flagInserted = False
    
    
        if flagInserted: # Если предыдущий запрос INSERT прошел успешно
            # # Получить последний ID в таблице tg_messages_proceeded (что бы иметь этот ключ для созданя записи в расширении этой таблицы в tg_message_proceeded_ext)
            # sql = f"SELECT rowid from {ms.TB_LIB_BOOK_IMAGES} order by ROWID DESC limit 1"
            
            # res = self.sps.get_result_from_sql_exec_proc_sps(sql)
            
            lastId = self.sps.get_last_inserted_id_in_db_mysql_sps()
            print(f"PR_B128 --> Последний row_id или lastId = {lastId}")

            dicInsertData = {
                'book_alfa_id' : bookAlfaId,
                'book_image_id' : lastId
            }

            try:
                
                print(f"PR_B129 --> START EXECUTE SQL")
                self.sps.insert_record_to_tb_with_many_to_many_relation(ms.TB_LIB_BOOKS_IMAGES, dicInsertData)
                
            except Exception as err:
                print(f"""PR_B130 --> SYS SQL LOG: SQL EXEUTION ERROR!!! \n  sqlError = {sql}""")
                
                print(f"PR_B131 --> ERROR: {err}")
        
        # print(f"PR_A249 -->  SYS DB LOG: присвоен новый статус {bookStatus} для книги с id = {bookId}")

        print(f"PR_B132 --> END: assign_image_to_being_registered_alfa_book_blf()")
        
        return lastId














    def get_lib_alfa_books_volumes_dic (self):
        """ 
        Получить словарь альфа-книг и их аудио-томов с расширениями
        """
        
        print(f"PR_A440 --> START: get_lib_alfa_books_volumes_dic()")
        
        # сформировать словарь с аудио-томами альфа-книг LABBA для передачи в сквозной словарь и для формирования дополнительного расчетного поля с перечнем
        # айдио-томов . соотвтетствующих книжному комплекту в выходной таблице
        
        sql = f"""SELECT * FROM 
                        {ms.TB_LIB_BOOKS_ALFA} as lba, 
                        {ms.TB_LIB_BOOK_AUDIO_VOLUMES} as lbav
                    WHERE 
                        lbav.books_alfa_id = lba.id
        """
        
        # 
        
        
        
        dfBookVolumes = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        print(f"PR_A416 --> dfBookVolumes = \n{dfBookVolumes}")
        
        # PARS
        colPrime = 'books_alfa_id' # Название колонки, которая будет являтся ключем в словаре
        colVal = 'volume_file_name' #  Название колонки, по которой значения добавляются в список, который является значением в словаре по ключу
        
        dicAlfaBookVolumes = PandasManager.read_df_col_as_list_to_diсtionary_by_col_prime (dfBookVolumes, colPrime, colVal)
        
        
        print(f"PR_A441 --> END: get_lib_alfa_books_volumes_dic()")


        return dicAlfaBookVolumes
    
    
    
    

    def get_lib_alfa_books_volumes_dic_for_given_lib_book_blf (self, bookAlfaId, indexDuplicated = False):
        """ 
        Получить словарь для заданной альфа-книги и их аудио-томов с расширениями
        RET FORMAT:
        dicAlfaBookVolumes = {
            1: 'Подвиньтесь. Подвиньтесь_ch1_gsmefai_gr1_audio_volume.mp3',
            2: 'Подвиньтесь. Подвиньтесь2_ch1_gsmefai_gr1_audio_volume.mp3',
            ...
            }
            
        ПРИМ: get_dic_book_volumes_names_and_its_ids_by_alfa_id_blf() повторяет эту функцию ? Проверить и одну из них удалить
            
        """
        
        print(f"PR_A440 --> START: get_lib_alfa_books_volumes_dic()")
        
        # сформировать словарь с аудио-томами альфа-книг LABBA для передачи в сквозной словарь и для формирования дополнительного расчетного поля с перечнем
        # айдио-томов . соотвтетствующих книжному комплекту в выходной таблице
        
        sql = f"""SELECT * FROM 
                        {ms.TB_LIB_BOOKS_ALFA} as lba, 
                        {ms.TB_LIB_BOOK_AUDIO_VOLUMES} as lbav
                    WHERE 
                        lbav.books_alfa_id = lba.id AND 
                        lbav.books_alfa_id = {bookAlfaId}
        """
        
        # 
        
        
        
        dfBookVolumes = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        
        
        if indexDuplicated:
            # переименования (индексации) одинаковых по названию колонок
            dfBookVolumes = PandasManager.index_duplicated_name_columns_in_df_universal(dfBookVolumes)
            
            
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfBookVolumes, True, colsIndxed = True, marker = "PR_A942 --> dfBookVolumes")
            
            
        print(f"PR_A416 --> dfBookVolumes = \n{dfBookVolumes}")
        
        # PARS
        colPrime = 'id_1' # Название колонки, которая будет являтся ключем в словаре
        colVal = 'volume_file_name' #  Название колонки, по которой значения добавляются в список, который является значением в словаре по ключу
        
        dicAlfaBookVolumes = PandasManager.read_df_cols_by_colPrime_as_diсtionary_for_alternative_ties (dfBookVolumes, colPrime, colVal, asList = False)
        
        
        print(f"PR_A441 --> END: get_lib_alfa_books_volumes_dic()")


        return dicAlfaBookVolumes
    
    
    
    
    
    def get_book_volumes_tbids_list_by_alfa_id_blf (self, bookAlfaId):
        """ 
        Получить  табличные  ids аудио-томов книги по ее alfaId
        """
        
        sql = f"""SELECT lbav.books_alfa_id, lbav.id FROM 
                        {ms.TB_LIB_BOOKS_ALFA} as lba, 
                        {ms.TB_LIB_BOOK_AUDIO_VOLUMES} as lbav
                    WHERE 
                        lbav.books_alfa_id = lba.id AND 
                        lbav.books_alfa_id = {bookAlfaId}
        """
        
        print(f"PR_B082 --> sql = {sql}")
        
        listBookAudioVolumesTbids = self.sps.get_result_from_sql_exec_proc_sps(sql)
    
    
        return listBookAudioVolumesTbids
    
    
    
    
    
    
    def get_lib_books_volumes_by_alfa_id (self, bookAlfaId):
        """ 
        OBSOLETED: использовать get_df_lib_books_volumes_by_alfa_id_through_df_blf () для получения данных, а не индексы в списках, так как 
        изменения в таблицах меняют индексы и соотвттетсвенно меняют данные, получаемые через индексы в списках
        Получить список списков аудио-томов с расширениями , принадлежащие книге с id = bookAlfaId
        """
        
        print(f"PR_A778 --> START: get_lib_books_volumes_by_alfa_id()")
        
        # сформировать словарь с аудио-томами альфа-книг LABBA для передачи в сквозной словарь и для формирования дополнительного расчетного поля с перечнем
        # айдио-томов . соотвтетствующих книжному комплекту в выходной таблице
        
        sql = f"""SELECT * FROM 
                        {ms.TB_LIB_BOOKS_ALFA} as lba, 
                        {ms.TB_LIB_BOOK_AUDIO_VOLUMES} as lbav
                    WHERE 
                        lbav.books_alfa_id = lba.id AND lbav.books_alfa_id = {bookAlfaId}
        """
        
        # 
        listBookVolumes = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        print(f"PR_A815 --> listBookVolumes = {listBookVolumes}")
        

        print(f"PR_A779 --> END: get_lib_books_volumes_by_alfa_id()")


        return listBookVolumes
    
    
    
    
    
    
    
    
    
    
    
    def get_df_lib_books_volumes_by_alfa_id_through_df_blf (self, bookAlfaId):
        """ 
        OBSOLITED: Frame тоже устарел. Теперь получаем значения в виде словаря с ключами <?> и значений по заданному полю
                    Use: 
        Получить список списков аудио-томов с расширениями , принадлежащие книге с id = bookAlfaId, используя фрейм, а не результат sps.get_result_from_sql_exec_proc_sps
        чтобы изменения в таблице не влияло на дальнейшие получения данных (раньше использовались индексы для получаемого списка. что бы получить данные. этот подход-
        ошибочен, так как изменения в таблице изменяют индексы в списке получаемых запросов к бд)
        """
        
        print(f"PR_A828 --> START: get_df_lib_books_volumes_by_alfa_id_through_df_blf()")
        
        # сформировать словарь с аудио-томами альфа-книг LABBA для передачи в сквозной словарь и для формирования дополнительного расчетного поля с перечнем
        # айдио-томов . соотвтетствующих книжному комплекту в выходной таблице
        
        sql = f"""SELECT * FROM 
                        {ms.TB_LIB_BOOKS_ALFA} as lba, 
                        {ms.TB_LIB_BOOK_AUDIO_VOLUMES} as lbav
                    WHERE 
                        lbav.books_alfa_id = lba.id AND lbav.books_alfa_id = {bookAlfaId}
        """
        
        # 
        dfBookVolumes = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        # print(f"PR_A829 --> dfBookVolumes = \n{dfBookVolumes}")
        

        print(f"PR_A830 --> END: get_df_lib_books_volumes_by_alfa_id_through_df_blf()")


        return dfBookVolumes
    
    
    
    
    
    def get_list_books_volumes_by_alfa_id_through_df_blf (self, bookAlfaId):
        """ 
        NEW : 29-03-2024
        Получить словарь аудио-томов с расширениями , принадлежащие книге с id = bookAlfaId, используя фрейм, а не результат sps.get_result_from_sql_exec_proc_sps
        чтобы изменения в таблице не влияло на дальнейшие получения данных (раньше использовались индексы для получаемого списка. что бы получить данные. этот подход-
        ошибочен, так как изменения в таблице изменяют индексы в списке получаемых запросов к бд)
        """
        
        print(f"PR_B175 --> START: get_list_books_volumes_by_alfa_id_through_df_blf()")
        
        # сформировать словарь с аудио-томами альфа-книг LABBA для передачи в сквозной словарь и для формирования дополнительного расчетного поля с перечнем
        # айдио-томов . соотвтетствующих книжному комплекту в выходной таблице
        
        sql = f"""SELECT volume_message_id, volume_file_name FROM 
                        {ms.TB_LIB_BOOKS_ALFA} as lba, 
                        {ms.TB_LIB_BOOK_AUDIO_VOLUMES} as lbav
                    WHERE 
                        lbav.books_alfa_id = lba.id AND lbav.books_alfa_id = {bookAlfaId}
                    ORDER BY lbav.volume_order
        """
        
        # 
        # listBookVolumesNames = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        dicBookMssgIdVolumesNames = self.spps.read_sql_to_dic_like_one_to_one_tie_spps(sql, 'volume_message_id', 'volume_file_name', True)
        
        print(f"PR_B339 --> listBookVolumesNames = {dicBookMssgIdVolumesNames}")


        print(f"PR_B176 --> END: get_list_books_volumes_by_alfa_id_through_df_blf()")


        return   dicBookMssgIdVolumesNames

    
    
    
    
    def get_list_books_volumes_titles_by_alfa_id_through_df_blf (self, bookAlfaId):
        """ 
        NEW : 06-04-2024
        Получить словарь  тайтлов аудио-томов с расширениями , принадлежащие книге с id = bookAlfaId, используя фрейм, а не результат sps.get_result_from_sql_exec_proc_sps
        чтобы изменения в таблице не влияло на дальнейшие получения данных (раньше использовались индексы для получаемого списка. что бы получить данные. этот подход-
        ошибочен, так как изменения в таблице изменяют индексы в списке получаемых запросов к бд)
        """
        
        print(f"PR_B340 --> START: get_list_books_volumes_titles_by_alfa_id_through_df_blf()")
        
        # сформировать словарь с аудио-томами альфа-книг LABBA для передачи в сквозной словарь и для формирования дополнительного расчетного поля с перечнем
        # айдио-томов . соотвтетствующих книжному комплекту в выходной таблице
        
        sql = f"""SELECT volume_message_id, volume_title FROM 
                        {ms.TB_LIB_BOOKS_ALFA} as lba, 
                        {ms.TB_LIB_BOOK_AUDIO_VOLUMES} as lbav
                    WHERE 
                        lbav.books_alfa_id = lba.id AND lbav.books_alfa_id = {bookAlfaId}
                    ORDER BY lbav.volume_order
        """
        
        # 
        # listBookVolumesNames = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        dicBookMssgIdVolumesNames = self.spps.read_sql_to_dic_like_one_to_one_tie_spps(sql, 'volume_message_id', 'volume_title', True)
        
        print(f"PR_B341 --> listBookVolumesNames = {dicBookMssgIdVolumesNames}")


        print(f"PR_B342 --> END: get_list_books_volumes_titles_by_alfa_id_through_df_blf()")


        return   dicBookMssgIdVolumesNames

    
    
    
    
    
    
    
    def get_lib_book_volumes_tg_messages_ids_blf (self, bookAlfaId):
        """ 
        Получить список  ids сообщений, скачанных с ТГ-канала, соотвтетсвующих аудио-томам книги с заданным bookAlfaId
        """
        
        listBookVolumes = self.get_lib_books_volumes_by_alfa_id(bookAlfaId)
        
        listBVolumesMssgsIds = [x[-2] for x in listBookVolumes]
        
        
        return listBVolumesMssgsIds
    
    
    
    # def get_book_volumes_names_by_alfa_id_blf (self, bookAlfaId):
    #     """ 
    #     Получить список  названий аудио-томов файлов заданной книги bookAlfaId
    #     """
        
    #     print(f"PR_B172 --> START: get_book_volumes_names_by_alfa_id_blf()")
        
    #     listBookVolumes = self.get_list_books_volumes_by_alfa_id_through_df_blf(bookAlfaId)
        
    #     print(f"PR_B174 --> listBookVolumes = {listBookVolumes}")
        
    #     print(f"PR_B173 --> END: get_book_volumes_names_by_alfa_id_blf()")

    #     return listBookVolumes
    
    
    
    
    def get_dic_book_volumes_names_and_its_ids_by_alfa_id_blf (self, bookAlfaId):
        """ 
        Получить словарь ids аудио-томов и  их названий файлов по заданной книги bookAlfaId
        
        
        ПРИМ: Функия get_lib_alfa_books_volumes_dic_for_given_lib_book_blf() - повторяет эту функцию ? Проверить
        """
        
        dfBookVolumes = self.get_df_lib_books_volumes_by_alfa_id_through_df_blf(bookAlfaId)

        # print(f"PR_A827 --> dfBookVolumes = \n{dfBookVolumes}")
        
        # После раздуплицирования id необходимые порядковые id аудио-томов из табл lib_book_audio_volumes превращаются в 'id_1'
        dfBookVolumes = PandasManager.index_duplicated_name_columns_in_df(dfBookVolumes)
        
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfBookVolumes, True, colsIndxed = True, marker = "PR_A827", printFull = True)
        
        dicBookVolumesNames = PandasManager.get_dict_from_df_with_key_col_name_and_val_col_name_pbf(dfBookVolumes, 'id_1', 'volume_file_name')
        
        return dicBookVolumesNames
    
    
    
    
    
    def get_dic_book_volumes_titles_and_its_ids_by_alfa_id_blf (self, bookAlfaId):
        """ 
        Получить словарь ids аудио-томов и  их titles по заданной книги bookAlfaId
        """
        
        dfBookVolumes = self.get_df_lib_books_volumes_by_alfa_id_through_df_blf(bookAlfaId)

        # print(f"PR_A827 --> dfBookVolumes = \n{dfBookVolumes}")
        
        # После раздуплицирования id необходимые порядковые id аудио-томов из табл lib_book_audio_volumes превращаются в 'id_1'
        dfBookVolumes = PandasManager.index_duplicated_name_columns_in_df(dfBookVolumes)
        
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfBookVolumes, True, colsIndxed = True, marker = "PR_A827", printFull = True)
        
        dicBookVolumesTitles = PandasManager.get_dict_from_df_with_key_col_name_and_val_col_name_pbf(dfBookVolumes, 'id_1', 'volume_title')
        
        return dicBookVolumesTitles
    
    
    
    
    
    def get_dic_book_volume_cls_objects_by_alfa_id_blf (self, bookAlfaId, **bvParams):
        """ 
        Получить словарь с обьектами класса BookVolume, содержащие все необходимые данные для аудио-томов  по заданной книги bookAlfaId
        """
        
        dfBookVolumes = self.get_df_lib_books_volumes_by_alfa_id_through_df_blf(bookAlfaId)

        # print(f"PR_A827 --> dfBookVolumes = \n{dfBookVolumes}")
        
        # После раздуплицирования id необходимые порядковые id аудио-томов из табл lib_book_audio_volumes превращаются в 'id_1'
        dfBookVolumes = PandasManager.index_duplicated_name_columns_in_df(dfBookVolumes)
        
        # Заменить пустые значения в коолнке 'volume_title' стрринговой пустотой (иначе идут потом глюки со словарем и темплейтингов в Джаного, 
        # где вместо путоты Джанго выдает 'None' для пустых значений в ловаре)
        # https://www.geeksforgeeks.org/python-pandas-dataframe-fillna-to-replace-null-values-in-dataframe/
        
        dfBookVolumes["volume_title"].fillna("", inplace = True)
        
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfBookVolumes, True, colsIndxed = True, marker = "PR_A827", printFull = True)
        
        # PARS
        # Путь к классу и название класса
        objClassFullData = {
            
            'classFullPath' : bvParams['classFullPath'],
            'className' : 'LibBookVolume'
        }
        
        # Ключ
        keyColName = 'id_1'
        
        dicBookVolumeObjects = PandasManager.get_dict_from_df_of_class_objects_with_key_col_name_and_cols_vals_names_pm (
            dfBookVolumes, 
            objClassFullData, 
            keyColName
            )
        
        # dicBookVolumesTitles = PandasManager.get_dict_from_df_with_key_col_name_and_val_col_name_pbf(dfBookVolumes, 'id_1', 'volume_title')
        
        # print(f"PR_A834 --> dicBookVolumeObjects = {dicBookVolumeObjects}")
        

        return dicBookVolumeObjects
    
    
    
    
    
    
    
    
    
    

    def isBookHasAudioVolumes(self, bookAlfaId):
        """ 
        Имеет ли книга аудил-тома
        """
        
        listBookVolumes = self.get_lib_books_volumes_by_alfa_id(bookAlfaId)
        
        if not isinstance(listBookVolumes, int) and len(listBookVolumes) > 0:

            return True
        else:
            return False
        
    
    



    def get_lib_alfa_books_volumes_dic_sliced_with_keys_list (self, tupleKeys : tuple):
        """ 
        Получить словарь альфа-книг и их аудио-томов с расширениями, отфильтрованный по набору ключей по полю lbav.books_alfa_id (alfaId)
        """
        
        
        # сформировать словарь с аудио-томами альфа-книг LABBA для передачи в сквозной словарь и для формирования дополнительного расчетного поля с перечнем
        # айдио-томов . соотвтетствующих книжному комплекту в выходной таблице
        
        print(f"PR_A612 --> tupleKeys = {tupleKeys}")
        
        if len(tupleKeys) == 1:
            tupleKeys = f"({tupleKeys[0]})"
        
        sql = f"""SELECT * FROM 
                        {ms.TB_LIB_BOOKS_ALFA} as lba, 
                        {ms.TB_LIB_BOOK_AUDIO_VOLUMES} as lbav
                    WHERE 
                        lbav.books_alfa_id = lba.id AND 
                        lbav.books_alfa_id IN {tupleKeys}
        """
        
        # print(f"PR_A416 --> sql = {sql}")
        
        
        
        dfBookVolumes = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        # PARS
        colPrime = 'books_alfa_id' # Название колонки, которая будет являтся ключем в словаре
        colVal = 'volume_file_name' #  Название колонки, по которой значения добавляются в список, который является значением в словаре по ключу
        
        dicAlfaBookVolumes = PandasManager.read_df_col_as_list_to_diсtionary_by_col_prime (dfBookVolumes, colPrime, colVal)
        

        return dicAlfaBookVolumes







    # def get_source_links_dic_sliced_with_mssg_ids_list (self, tupleKeys : tuple):
    #     """ 
    #     Получить словарь ссылок на источник в зависимости от tbid сообщения
    #     """

    #     print(f"PR_B296 --> tupleKeys = {tupleKeys}")



    #     sql = f"SELECT "










    def get_authors_of_book_by_alfa_id (self, bookAlfaId):
        """ 
        Получить  список авторов заданнйо книги (полных данных в виде списка списков со всеми атрибутами из обьединенных таблиц lib_books_authors и lib_authors )
        RET:[[1, 1, 1, 'Сергей', 'Казанцев', 'Казанцев Сергей']]
        """
        
        sql = f"SELECT * FROM {ms.TB_LIB_BOOKS_AUTHORS}, {ms.TB_LIB_AUTHORS} WHERE lib_books_authors.author_id = lib_authors.id AND book_alfa_id = {bookAlfaId}"
        
        listBookAuthors = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return listBookAuthors
    
    
    
    def get_authors_united_line_for_book_by_alfa_id (self, bookAlfaId):
        """ 
        Получить  тектовую строку авторов заданной книги через запятую (полных данных в виде списка списков со всеми атрибутами из обьединенных таблиц lib_books_authors и lib_authors )
        RET:
        """
        
        sql = f"SELECT author_full_name FROM {ms.TB_LIB_BOOKS_AUTHORS}, {ms.TB_LIB_AUTHORS} WHERE lib_books_authors.author_id = lib_authors.id AND book_alfa_id = {bookAlfaId}"
        
        listBookAuthors = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if not isinstance(listBookAuthors, int):
            lineAuthors = (', ').join(listBookAuthors)
        else:
            lineAuthors = ''
        
        return lineAuthors
    
    
    
    def get_author_fio_by_id_blf(self, aouthorId):
        """ 
        Получить ФИО автора по его  id в табл 'lib_authors'
        """
        
        sql = f"SELECT author_full_name FROM {ms.TB_LIB_AUTHORS} WHERE id = {aouthorId}"
        
        authorFIO = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return authorFIO[0]
    
    
    
    
    
    def get_narrator_fio_by_id_blf(self, narratorId):
        """ 
        Получить ФИО диктора по его  id в табл 'lib_narrators'
        """
        
        sql = f"SELECT narrator_full_name FROM {ms.TB_LIB_NARRATORS} WHERE id = {narratorId}"
        
        narratorFIO = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return narratorFIO[0]
    
    
    
    
    
    
    
    
    
    def get_authors_ids_of_book_by_alfa_id (self, bookAlfaId):
        """ 
        Получить список регистрационных id авторов , присвоенных заданной книге 
        """
        # Список списков с полными данными по авторам заданной книги (со всеми атрибутами из обьединенных таблиц lib_books_authors и lib_authors)
        listBookAuthors = self.get_authors_of_book_by_alfa_id(bookAlfaId)
        
        # Получить одномерный список ids авторов книги
        
        if not isinstance(listBookAuthors, int):
            
            # Получить одномерный список ids авторов книги
            listBookAuthorsIds = [x[2] for x in listBookAuthors]
            
        else:
            listBookAuthorsIds = -1
        
        
        
        # print(f"PR_A515 --> listBookAuthorsIds = {listBookAuthorsIds}")
        
        return listBookAuthorsIds
    
    

    
    
    
    def get_narrators_of_book_by_alfa_id (self, bookAlfaId):
        """ 
        Получить  список дикторов заданной книги (полных данных в виде списка списков со всеми атрибутами из обьединенных таблиц lib_books_narrators и lib_narrators )
        RET:[[1, 1, 1, 'Сергей', 'Казанцев', 'Казанцев Сергей']]
        """
        
        sql = f"SELECT * FROM {ms.TB_LIB_BOOKS_NARRATORS}, {ms.TB_LIB_NARRATORS} WHERE lib_books_narrators.narrator_id = lib_narrators.id AND book_alfa_id = {bookAlfaId}"
        
        listBookNarrators = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return listBookNarrators
    
    
    
    def get_narrators_ids_of_book_by_alfa_id (self, bookAlfaId):
        """ 
        Получить список регистрационных id дикторов , присвоенных заданной книге 
        """
        # Список списков с полными данными по дикторам заданной книги (со всеми атрибутами из обьединенных таблиц lib_books_narrators и lib_narrators)
        listBookNarrators = self.get_narrators_of_book_by_alfa_id(bookAlfaId)
        
        if not isinstance(listBookNarrators, int):
            
            # Получить одномерный список ids авторов книги
            listBookNarratorsIds = [x[2] for x in listBookNarrators]
            
        else:
            listBookNarratorsIds = -1
            
            
        # print(f"PR_A515 --> listBookNarratorsIds = {listBookNarratorsIds}")
        
        return listBookNarratorsIds
    
    
    
    
    
    
    
    def get_repositories_ids_of_orig_source_id(self, sourceId):
        """ 
        Получить список tbids своих репозиториев, присвоенных заданному источнику
        """
    
        sql = f"SELECT repository_id FROM {ms.TB_LIB_SOURCES_ASSIGNED_REPOSITORIES} WHERE orig_source_id = {sourceId}"
        
        print(f"PR_B466 --> sql = {sql}")
        
        repositTbids = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        
        return repositTbids
    
    
    
    
    
    
    
    def get_repositories_ids_of_given_lib_book_id(self, bookAlfaId):
        """ 
        Получить список tbids своих репозиториев, присвоенных заданному источнику
        """
    
        sql = f"SELECT repository_id FROM {ms.TB_LIB_BOOKS_ASSIGNED_REPOSITORIES} WHERE book_alfa_id = {bookAlfaId}"
        
        print(f"PR_B486 --> sql = {sql}")
        
        repositTbids = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        
        return repositTbids
    
    
    
    
    
    
    
    
    
    
    def get_list_of_statuses_ids_for_book_with_given_alfa_id (self, bookAlfaId):
        """ 
        Получить  список  id статусов, присвоенных заданной книге  
        """
        
        # Список списков с полными данными по статусам заданной книги (со всеми атрибутами из обьединенных таблиц lib_books_ststuses и lib_book_statuses)
        listBookStatuses = self.get_book_statuses_by_alfa_id(bookAlfaId)
        
        # Получить одномерный список ids статусов книги
        listBookStatusesIds = [x[2] for x in listBookStatuses]
        
        return listBookStatusesIds
    
    
    
    def get_list_of_categories_ids_for_book_with_given_alfa_id (self, bookAlfaId):
        """ 
        Получить  список  id категорий, присвоенных заданной книге  
        """
        
        # Список списков с полными данными по категориям заданной книги (со всеми атрибутами из обьединенных таблиц lib_categories и lib_book_categories)
        listBookCategories = self.get_book_categories_by_alfa_id(bookAlfaId)
        
        print(f"PR_A631 --> listBookCategories = {listBookCategories}")
        
        if isinstance(listBookCategories, int):
            listBookCategoriesIds = -1
        else:
            # Получить одномерный список ids категорий книги
            listBookCategoriesIds = [x[2] for x in listBookCategories]
        
        return listBookCategoriesIds
    
    
    
    
    
    
    def get_all_registered_authors_dic_with_full_names_blf(self):
        """ 
        Получить массив всех зарегестрированных в таблице lib_authors авторов книг в виде словаря с ключами  id  и полем 'author_full_name'
        """
        
        sql = f"""SELECT id, author_full_name FROM  {ms.TB_LIB_AUTHORS}"""
        
        dicAllRegisteredAuthors = self.spps.read_sql_to_dic_like_group_by_spps (sql, 'id', 'author_full_name') 

        return dicAllRegisteredAuthors
    
    
    
    
    
    def get_all_registered_authors_df_blf(self):
        """ 
        Получить фрейм со всеми зарегестрированными в таблице lib_authors авторами книг
        """
        
        sql = f"""SELECT * FROM  {ms.TB_LIB_AUTHORS}"""
        
        dfAllRegisteredAuthors = self.spps.read_sql_to_df_pandas_mysql_spps (sql) 

        return dfAllRegisteredAuthors
    
    
    
    
    def get_all_registered_narrators_df_blf(self):
        """ 
        Получить фрейм со всеми зарегестрированными в таблице lib_narrators дикторами книг
        """
        
        sql = f"""SELECT * FROM  {ms.TB_LIB_NARRATORS}"""
        
        dfAllRegisteredNarrators = self.spps.read_sql_to_df_pandas_mysql_spps (sql) 

        return dfAllRegisteredNarrators
    
    
    
    
    
    
    
    def get_book_statuses_df_blf(self):
        """ 
        Получить фрейм со стстусами книг из таблицы lib_book_statuses 
        """
        
        sql = f"""SELECT * FROM  {ms.TB_LIB_BOOK_STATUSES}"""
    
        dfBookStatuses = self.spps.read_sql_to_df_pandas_mysql_spps (sql) 

        return dfBookStatuses





    def get_lib_book_statuses_dic (self):
        """ 
        Получить словарь существующих статусов книг из таблицы lib_book_statuses
        """
        
        sql = f"""SELECT * FROM  {ms.TB_LIB_BOOK_STATUSES}"""
        
        dicBookStatuses = self.spps.read_sql_to_dic_like_group_by_spps (sql, 'id', 'book_status') 
        
        # выводим из списка 
        dicBookStatuses = {key: val[0] for key, val in dicBookStatuses.items()}
        
        return dicBookStatuses
    
    
    
    
    
    # def get_lib_book_categories_dic (self):
    #     """ 
    #     Получить словарь существующих категорий для книг из таблицы lib_book_statuses
    #     """
        
    #     sql = f"""SELECT * FROM  {ms.TB_LIB_BOOK_STATUSES}"""
        
    #     dicBookStatuses = self.spps.read_sql_to_dic_like_group_by_spps (sql, 'id', 'book_status') 
        
    #     # выводим из списка 
    #     dicBookStatuses = {key: val[0] for key, val in dicBookStatuses.items()}
        
    #     return dicBookStatuses
    
    
    
    
    
    
    
    
    def get_book_status_id_by_status_name_blf (self, bookStatusName):
        """ 
        Получить id статуса из табл lib_book_statuses по его названию
        """
        
        sql = f"SELECT id FROM {ms.TB_LIB_BOOK_STATUSES} WHERE book_status = '{bookStatusName}'"
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return res[0]




    def filter_alfa_book_ids_by_status_blf (self, statusId):
        """ 
        отфильтровать книги по заданному статусу
        """

        sql = f"SELECT book_alfa_id FROM {ms.TB_LIB_BOOKS_STATUSES}  WHERE book_status_id = {statusId}"
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        print(f"PR_A565 --> res = {res}")
        
        return res
    
    
    
    
    
    def get_book_categories_df_blf(self):
        """ 
        Получить фрейм со категоряими книг из таблицы lib_categories 
        """
        
        sql = f"""SELECT * FROM  {ms.TB_LIB_CATEGORIES}"""
    
        dfBookCategories = self.spps.read_sql_to_df_pandas_mysql_spps (sql) 

        return dfBookCategories


    
    
    
    def get_category_name_by_id_blf(self, categId):
        """ 
        Получить название категории из табл lib_categories по его id
        """
        
        sql = f"SELECT category FROM {ms.TB_LIB_CATEGORIES} WHERE id = {categId}"
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return res[0]
    
    
    
    
    
    
    
    
    def get_all_book_categories_dic (self):
        """ 
        OBSOLETED: Неправилльно выполнен и назван метод !!!
        Получить словарь существующих категорий книг из таблицы lib_categories
        """
        
        sql = f"""SELECT * FROM  {ms.TB_LIB_BOOK_STATUSES}"""
        
        dicBookStatuses = self.spps.read_sql_to_dic_like_group_by_spps (sql, 'id', 'book_status') 
        
        # выводим из списка 
        dicBookStatuses = {key: val[0] for key, val in dicBookStatuses.items()}
        
        return dicBookStatuses
    
    

    
    
    def filter_alfa_book_ids_by_except_status_blf (self, statusId):
        """ 
        отфильтровать книги , исключая книги с заданным статусом statusId
        """

        sql = f"SELECT id FROM {ms.TB_LIB_BOOKS_ALFA} WHERE id NOT IN (SELECT book_alfa_id FROM {ms.TB_LIB_BOOKS_STATUSES} WHERE book_status_id={statusId})"
        
        listAlfaIdsExceptgivenStatus = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        # print(f"PR_A565 --> res = {listAlfaIdsExceptgivenStatus}")
        
        return listAlfaIdsExceptgivenStatus
    
    
    



    def obtain_alfa_books_ids_approved_to_public(self) -> list:
        """ 
        Получить список ids книг. которые одобрены для публикации в соц-каналах
        """
        
        satausApprovedName = 'ALLOWED_TO_PUBLIC'
        
        statusId = self.get_book_status_id_by_status_name_blf(satausApprovedName)
        
        booksApprovedToPublicIds : list | int = self.filter_alfa_book_ids_by_status_blf(statusId)
        
        return booksApprovedToPublicIds





    # def get_df_alfa_book_ids_by_status_blf (self, statusId):
    #     """ 
    #     отфильтровать книги по статусу в таблице lib_books_statuses
    #     """

    #     sql = f"SELECT book_alfa_id FROM {ms.TB_LIB_BOOKS_STATUSES}  WHERE book_status_id = {statusId}"
        
    #     res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
    #     return res









    def get_lib_alfa_books_authors_dic (self):
        """ 
        Получить словарь книги-авторы
        """

        
        sql = f"""SELECT * FROM 
                    {ms.TB_LIB_BOOKS_AUTHORS} as lba, 
                    {ms.TB_LIB_AUTHORS}  as la
                    WHERE 
                    lba.author_id = la.id
        """
        
        # print(f"PR_A416 --> sql = {sql}")
        
        # PARS_DESCR:
        'book_alfa_id' # Название колонки, которая будет являтся ключем в словаре
        'author_full_name' #  Название колонки, по которой значения добавляются в список, который является значением в словаре по ключу
        
        dicAlfaBookAuthors = self.spps.read_sql_to_dic_like_group_by_spps (sql, 'book_alfa_id', 'author_full_name') 
        
        return dicAlfaBookAuthors






    def get_lib_alfa_books_authors_dic_filtered_by_keys_list (self, tupleKeys):
        """ 
        Получить словарь книги-авторы, отфильтрованный по набору ключей по полю book_alfa_id (alfaId)
        """
        
        # сформировать словарь с аудио-томами альфа-книг LABBA для передачи в сквозной словарь и для формирования дополнительного расчетного поля с перечнем
        # айдио-томов . соотвтетствующих книжному комплекту в выходной таблице
        
        # Избавляемя от запятой в тапле с сингулярным набором (если один элемент - конвертация в тапбл идет с запятой)
        if len(tupleKeys) == 1:
            tupleKeys = f"({tupleKeys[0]})"
        
        if len(tupleKeys) > 0 :
        
            sql = f"""SELECT * FROM 
                        {ms.TB_LIB_BOOKS_AUTHORS} as lba, 
                        {ms.TB_LIB_AUTHORS}  as la
                        WHERE 
                        lba.author_id = la.id AND 
                        book_alfa_id IN {tupleKeys}
            """
            
            # print(f"PR_A444 --> sql = {sql}")
            
            # PARS_DESCR:
            'book_alfa_id' # Название колонки, которая будет являтся ключем в словаре
            'author_full_name' #  Название колонки, по которой значения добавляются в список, который является значением в словаре по ключу
            
            dicAlfaBookAuthors = self.spps.read_sql_to_dic_like_group_by_spps (sql, 'book_alfa_id', 'author_full_name') 
            
        else: 
            dicAlfaBookAuthors = -1
        

        return dicAlfaBookAuthors





    def get_lib_books_statuses_dic_filtered_by_keys_list (self, tupleKeys):
        """ 
        Получить словарь книги-статусы, отфильтрованный по набору ключей по полю book_alfa_id (alfaId)
        """
        
        # сформировать словарь с аудио-томами альфа-книг LABBA для передачи в сквозной словарь и для формирования дополнительного расчетного поля с перечнем
        # айдио-томов . соотвтетствующих книжному комплекту в выходной таблице
        
        if len(tupleKeys) > 0 :
        
            sql = f"""SELECT * FROM 
                        {ms.TB_LIB_BOOKS_STATUSES} as lbss, 
                        {ms.TB_LIB_BOOK_STATUSES}  as lbs
                        WHERE 
                        lbss.book_status_id = lbs.id AND 
                        book_alfa_id IN {tupleKeys}
            """
            
            # print(f"PR_A444 --> sql = {sql}")
            
            # PARS_DESCR:
            'book_alfa_id' # Название колонки, которая будет являтся ключем в словаре
            'book_status' #  Название колонки, по которой значения добавляются в список, который является значением в словаре по ключу
            
            dicAlfaBookStatuses = self.spps.read_sql_to_dic_like_group_by_spps (sql, 'book_alfa_id', 'book_status') 
            
        else: 
            dicAlfaBookStatuses = -1
        

        return dicAlfaBookStatuses




    def get_lib_books_statuses_ids_dic_filtered_by_keys_list (self, tupleKeys):
        """ 
        Получить словарь книги-id статусов, отфильтрованный по набору ключей по полю book_alfa_id (alfaId)
        """
        
        # сформировать словарь с аудио-томами альфа-книг LABBA для передачи в сквозной словарь и для формирования дополнительного расчетного поля с перечнем
        # айдио-томов . соотвтетствующих книжному комплекту в выходной таблице
        
        if len(tupleKeys) > 0 :
        
            sql = f"""SELECT * FROM 
                        {ms.TB_LIB_BOOKS_STATUSES} as lbss, 
                        {ms.TB_LIB_BOOK_STATUSES}  as lbs
                        WHERE 
                        lbss.book_status_id = lbs.id AND 
                        book_alfa_id IN {tupleKeys}
            """
            
            # print(f"PR_A444 --> sql = {sql}")
            
            # PARS_DESCR:
            'book_alfa_id' # Название колонки, которая будет являтся ключем в словаре
            'book_status' #  Название колонки, по которой значения добавляются в список, который является значением в словаре по ключу
            
            dicAlfaBookStatuses = self.spps.read_sql_to_dic_like_group_by_spps (sql, 'book_alfa_id', 'book_status_id') 
            
        else: 
            dicAlfaBookStatuses = -1
        

        return dicAlfaBookStatuses






    def get_lib_books_categories_dic_filtered_by_keys_list (self, tupleKeys):
        """ 
        Получить словарь книги-категории, отфильтрованный по набору ключей по полю book_alfa_id (alfaId)
        """
        
        
        if len(tupleKeys) > 0 :
        
            sql = f"""SELECT * FROM 
                        {ms.TB_LIB_BOOKS_CATEGORIES} as lbsc, 
                        {ms.TB_LIB_CATEGORIES}  as lbc
                        WHERE 
                        lbsc.category_id = lbc.id AND 
                        book_alfa_id IN {tupleKeys}
            """
            
            # print(f"PR_A444 --> sql = {sql}")
            
            # PARS_DESCR:
            'book_alfa_id' # Название колонки, которая будет являтся ключем в словаре
            'category' #  Название колонки, по которой значения добавляются в список, который является значением в словаре по ключу
            
            dicAlfaBookStatuses = self.spps.read_sql_to_dic_like_group_by_spps (sql, 'book_alfa_id', 'category') 
            
        else: 
            dicAlfaBookStatuses = -1
        

        return dicAlfaBookStatuses




    def get_lib_books_narrators_dic_filtered_by_keys_list (self, tupleKeys):
        """ 
        Получить словарь книги-дикторы, отфильтрованный по набору ключей по полю book_alfa_id (alfaId)
        """
        
        
        if len(tupleKeys) > 0 :
        
            sql = f"""SELECT * FROM 
                        {ms.TB_LIB_BOOKS_NARRATORS} as lbsn, 
                        {ms.TB_LIB_NARRATORS}  as lbn
                        WHERE 
                        lbsn.narrator_id = lbn.id AND 
                        book_alfa_id IN {tupleKeys}
            """
            
            # print(f"PR_A444 --> sql = {sql}")
            
            # PARS_DESCR:
            'book_alfa_id' # Название колонки, которая будет являтся ключем в словаре
            'narrator_full_name' #  Название колонки, по которой значения добавляются в список, который является значением в словаре по ключу
            
            dicAlfaBookNarrators = self.spps.read_sql_to_dic_like_group_by_spps (sql, 'book_alfa_id', 'narrator_full_name') 
            
        else: 
            dicAlfaBookNarrators = -1
        

        return dicAlfaBookNarrators









    def obtain_books_source_tg_chat_nicks_dic_filtered_by_keys_list (self, tupleAlfaIds):
        """ 
        Получить словарь ников телеграм-чатов, с которых изначально были скачены книги со списком id в tupleAlfaIds, в виде словаря, где ключами являются
        id книг
        """
        
        # сформировать словарь с аудио-томами альфа-книг LABBA для передачи в сквозной словарь и для формирования дополнительного расчетного поля с перечнем
        # айдио-томов . соотвтетствующих книжному комплекту в выходной таблице
        
        if len(tupleAlfaIds) > 0 :
        
            sql = f"""
                SELECT books_alfa_id, tg_channel_nick FROM {ms.TB_LIB_BOOKS_ALFA_EXT} as lbae,{ms.TB_LIB_ORIG_SOURCES} as los 
                WHERE 
                lbae.book_orig_source_id = los.id AND
                los.orig_source_type_id = 1 AND
                lbae.books_alfa_id IN {tupleAlfaIds}
            """
            
            # print(f"PR_A587 --> sql = {sql}")
            
            # PARS_DESCR:
            'book_alfa_id' # Название колонки, которая будет являтся ключем в словаре
            'author_full_name' #  Название колонки, по которой значения добавляются в список, который является значением в словаре по ключу
            
            dicAlfaBookStatuses = self.spps.read_sql_to_dic_like_one_to_one_tie_spps (sql, 'books_alfa_id', 'tg_channel_nick') 
            
            print(f"PR_A588 --> dicAlfaBookStatuses = {dicAlfaBookStatuses}")
            
        else: 
            dicAlfaBookStatuses = -1
        

        return dicAlfaBookStatuses






    def search_file_in_lib_book_images_tb_blf (self, fileName):
        """
        Поиск файла-картинки в таблице lib_book_images, где регистрируются все картинки по книгам
        
        RET:  словарь с найденными значениями по заданынм полям в виде ключа и значений словаря
        """
        
        sql = f"SELECT * FROM lib_book_images WHERE image_name LIKE '%{fileName}%'"
        
        # Словарь с результатами поиска по названию файла из таблицы lib_book_images
        dicBookImgSearched = self.spps.read_sql_to_dic_like_group_by_spps(sql, 'id', 'image_name')
        
        return dicBookImgSearched






    def insert_new_image_to_lib_book_images_tb_blf (self, newFileImgName, fileRelRightPath):
        """ 
        Вставить (зарегестрировать) новую картинку для книг в таблице lib_book_images и вернуть его новый id в таблице
        fileRelRightPath -  относительный участок пути файла справа без названия самого файла, начиная с какой-то определенной суб-диреткории в его полном пути
        """
        
        # G. Зарегестрировать название файла и его относительную директорию справа в табл lib_books_images
        
        sql = f"INSERT INTO {ms.TB_LIB_BOOK_IMAGES} (image_name, relative_subdir) VALUES ('{newFileImgName}', '{fileRelRightPath}')"

        try: 
            print(f"PR_A469 --> SYS LOG: Выполнение INSERT запроса \n{sql}")

            self.sps.execute_sql_SPS(sql)
            
            # Получить id новой зарегестрированнйо картинки в табл lib_books_images
            imgNewId = self.sps.get_last_inserted_id_in_db_mysql_sps() 
                
        except Exception as err:
            
            print(f"PR_A470 --> SYS LOG: В результате выполнения INSERT запроса произошла !!! ОШИБКА !!! : \n{sql}")
            
            imgNewId = err
        
        return imgNewId





    def get_id_of_img_file_from_lib_book_images_by_file_name (self, fileName):
        """ 
        Найти id файла-картинки из табл lib_book_images по его названию, если он там есть
        """
        
        dicBookImgSearched = self.search_file_in_lib_book_images_tb_blf(fileName)
        
        imgFileId = list(dicBookImgSearched)[0]
        
        return imgFileId






    def update_book_with_alfa_id_assign_img_with_reg_id_blf (self, bookAlfaId, imgRegId):
        """ 
        Присвоить к описанию книги с bookAlfaId зарегестрированную в таблице lib_book_images картинку с ее регистрационным там id = imgRegId
        """

        sql = f"UPDATE {ms.TB_LIB_BOOKS_IMAGES} SET book_image_id = {imgRegId} WHERE book_alfa_id = {bookAlfaId}"
        
        
        # EXECUTE SQL !!!
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"\nPR_A476 --> SYS LOG: Произведен успешный UPDATE запрос \n{sql}")
            
        except Exception as err:
        
            print(f"\nPR_A475 --> SYS LOG: В результате UPDATE  запроса произошла !!! ОШИБКА !!! \n{sql}\n")
        
        
    
    
    
    
    
    def update_image_file_name_for_lib_book_blf (self, tgMessagePhotoId, bookImgFileName):
        """ 
        Обновить названия файла для картинки книги по id d ТГ сообщения tgMessagePhotoId, на базе которого создавалась книга
        RET: id редактируемой картинки в таблице 'lib_book_images'
        """
    

        # Список  ids картинок, присвоенных книге в таблице 'lib_books_images'
        listBookImageIds = self.get_lib_book_assigned_images_ids_by_its_tg_message_id(tgMessagePhotoId)
        
        # Разница, если несколько картинок и, если - одна
        if not isinstance(listBookImageIds, int):
            imgId = listBookImageIds[0]
        else:
            imgId = listBookImageIds
        
        # Обновить в таблице 'lib_book_images' значение в поле 'image_name' (название файла картинки без пути)
        
        sql = f"UPDATE {ms.TB_LIB_BOOK_IMAGES} SET image_name = '{bookImgFileName}' WHERE id = {imgId}"
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_A898 --> SYS LOG: Успешно выполнен UPDATE запрос \n{sql}")
            
        except Exception as err:
            print(f"PR_A899 --> SYS LOG: При выполнении запроса произошла !!! ОШИБКА !!!: \n{sql}")
            print(f"PR_A900 --> SYS LOG: ERRORR !!! {err}")
            
        return imgId








    def update_lib_audio_volume_file_name_by_message_id_tlf (self, volumeFileName, volumeMessageId):
        """ 
        Изменить название айдио-файла по ключу id сообщения айдио-тома
        """

        sql = f"UPDATE {ms.TB_LIB_BOOK_AUDIO_VOLUMES} SET volume_file_name = '{volumeFileName}' WHERE volume_message_id = {volumeMessageId}"
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_A902 --> SYS LOG: Успешно выполнен UPDATE запрос \n{sql}")
            
        except Exception as err:
            print(f"PR_A903 --> SYS LOG: При выполнении запроса произошла !!! ОШИБКА !!!: \n{sql}")
            print(f"PR_A904 --> SYS LOG: ERRORR !!! {err}")












    
    
    
    def get_lib_book_assigned_images_ids_by_its_tg_message_id (self, tgBookDescrMessageId):
        """ 
        Поулчить список (или один)  ids картинок, присвоенных альфа-книге по id сообщения, соотвтетсвующего описанию, на основе которого создавалась альфа-книга
        
        """
    
    
        sql = f""" 
    
            SELECT lbi.id FROM 
            
                    {ms.TB_LIB_BOOKS_ALFA} as lba,
                    {ms.TB_LIB_BOOKS_ALFA_EXT} as lbae,
                    {ms.TB_LIB_BOOKS_IMAGES} as lbsi,
                    {ms.TB_LIB_BOOK_IMAGES} as lbi
                    
            WHERE 
            
                    lba.id = lbae.books_alfa_id AND 
                    lbsi.book_alfa_id = lba.id AND 
                    lbi.id = lbsi.book_image_id AND 
                    lbae.book_message_id = {tgBookDescrMessageId}
    
        """
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        listBookImageIds = res
        
        return listBookImageIds


        
        
    
    
    
    
    
    
    
    
    def get_book_img_rel_django_proj_stat_path_by_alfa_id_blf (self, bookAlfaId):
        """ 
        Получить относительный проектный Джанго путь к картинке книги, начиная от stat в хранилище картинок к книгам по alfaId книги
        """
        
        sql = f"SELECT * FROM {ms.TB_LIB_BOOKS_IMAGES} as lbis, {ms.TB_LIB_BOOK_IMAGES} as lbi WHERE lbis.book_image_id = lbi.id AND lbis.book_alfa_id = {bookAlfaId}"
    
    
        dicRow = self.spps.read_one_row_return_sql_to_dic_mysql_spps(sql)

        # res = self.sps.get_result_from_sql_exec_proc_sps(sql)[0]
        
        # print(f"PR_A477 --> res = {res}")
        
        relImgPath = dicRow['relative_subdir']
        
        imgFileName = dicRow['image_name']
        
        fullFilePath = f"{ms.DJANGO_PROJ_IMAGE_STORAGE}/{relImgPath}/{imgFileName}"
        
        print(f"\n PR_B177 --> fullFilePath = {fullFilePath}\n")
        
        return fullFilePath






    def insert_new_author_to_book_library_db_blf (self, authorFirstname, authorSecondname):
        """ 
        Вставить нового автора в таблицу 'lib_authors'
        """
        
        authorFullName = f"{authorSecondname} {authorFirstname}" # Полное имя автора

        # ПРЕОБРАЗОВАТЬ переменнуюдля стрингового поля в sql-запросе для того вставки f-стринг величины  без дополнительных кавычек и 
        # оперировать с NULL
        authorFirstname = self.sps.insert_null_transformation_sps(authorFirstname, stripVals = ' ')
        
        authorSecondname = self.sps.insert_null_transformation_sps(authorSecondname, stripVals = ' ')
        
        authorFullName = self.sps.insert_null_transformation_sps(authorFullName, stripVals = ' ')
        
            
        
        sql = f"""INSERT INTO {ms.TB_LIB_AUTHORS} (author_first_name, author_second_name, author_full_name) 
                    VALUES ({authorFirstname},{authorSecondname},{authorFullName})
                """
                
                
                
        print(f"PR_B203 --> sql = {sql}")
        
        # Внести данные по автору в таблицу 'lib_authors'
        # TODO: сделать try в самом методе self.sps.execute_sql_SPS()
        try:
            self.sps.execute_sql_SPS(sql)
            print(f"PR_A243 --> SYS LOG: Автор {authorFullName} внесен в таблицу автоматически")
            
            
            # Получить Id последней внесенной записи в табл 'lib_authors', которая будет соответствовать автору обрабатываемой книги. for mysql
            newAuthorId = self.sps.get_last_inserted_id_in_db_mysql_sps ()
            
            print(f"PR_A424 --> SYS LOG: newAuthorId = {newAuthorId}")
                
        except Exception as err:
            print(f"PR_A241 --> SYS LOG: В результате !!! ОШИБКИ !!! автор не внесен в таблицу 'lib_authors' по запросу : \n{sql}")
            
            print(f"PR_A425 --> SYS LOG: Exception -> {err}")
            
            newAuthorId = -1
            
            # TODO: Ввести систему логов в текстовые файлы. Их форматы
            # Внести в проектный лог, что по этой книге и этому файлу не внесен автор. в дальнейшем, чтобы эти логи показывали, где надо вмешаться на уровне оператора библиотеки
            
        # # Получить Id последней внесенной записи в табл 'lib_authors', которая будет соответствовать автору обрабатываемой книги. for sqlite
        # authorId = self.sps.get_last_rowid_from_tb_sps (ms.TB_LIB_AUTHORS)

        return newAuthorId
    
        
        
        
        
        
        
    def insert_new_narrator_to_book_library_db_blf (self, narratorFirstname, narratorSecondname):
        """ 
        Вставить нового  диктора в таблицу 'lib_narrators'
        """
        
        print(f"PR_B204 --> START: insert_new_narrator_to_book_library_db_blf()")

        
        narratorFullName = f"{narratorSecondname} {narratorFirstname}" # Полное имя диктора
        
        # ПРЕОБРАЗОВАТЬ переменнуюдля стрингового поля в sql-запросе для того вставки f-стринг величины  без дополнительных кавычек и 
        # оперировать с NULL
        narratorFirstname = self.sps.insert_null_transformation_sps(narratorFirstname, stripVals = ' ')
        
        narratorSecondname = self.sps.insert_null_transformation_sps(narratorSecondname, stripVals = ' ')
        
        narratorFullName = self.sps.insert_null_transformation_sps(narratorFullName, stripVals = ' ')
        
        
        print(f"PR_B204 --> POINT A")
        
        
        
        sql = f"""INSERT INTO {ms.TB_LIB_NARRATORS} (narrator_first_name, narrator_second_name, narrator_full_name) 
                    VALUES ({narratorFirstname},{narratorSecondname}, {narratorFullName})
                """
        # Внести данные по диктора в таблицу 'lib_narrators'
        try:
            self.sps.execute_sql_SPS(sql)
            print(f"PR_A243 --> SYS LOG: Диктор {narratorFullName} внесен в таблицу автоматически")
            
            
            # Получить Id последней внесенной записи в табл 'lib_narrators', которая будет соответствовать диктору обрабатываемой книги. for mysql
            newNarratorId = self.sps.get_last_inserted_id_in_db_mysql_sps ()
            
            print(f"PR_A424 --> SYS LOG: newNarratorId = {newNarratorId}")
                
        except Exception as err:
            print(f"PR_A241 --> SYS LOG: В результате !!! ОШИБКИ !!! диктор не внесен в таблицу 'lib_narrators' по запросу : \n{sql}")
            
            print(f"PR_A425 --> SYS LOG: Exception -> {err}")
            
            newNarratorId = -1
            
            # TODO: Ввести систему логов в текстовые файлы. Их форматы
            # Внести в проектный лог, что по этой книге и этому файлу не внесен автор. в дальнейшем, чтобы эти логи показывали, где надо вмешаться на уровне оператора библиотеки
            
        # # Получить Id последней внесенной записи в табл 'lib_authors', которая будет соответствовать автору обрабатываемой книги. for sqlite
        # authorId = self.sps.get_last_rowid_from_tb_sps (ms.TB_LIB_AUTHORS)

        return newNarratorId
        
        
        
        
        
        
        
        
        
    def create_new_category_in_tb_lib_categories_blf (self, category):
        """ 
        Создать новую категорию 'lib_categories'
        """

        
        sql = f"""INSERT INTO {ms.TB_LIB_CATEGORIES} (category) 
                    VALUES ('{category}')
                """

        try:
            self.sps.execute_sql_SPS(sql)
            print(f"PR_A679 --> SYS LOG: создана новая категория в таблице 'lib_categories'")
            
            
            # Получить Id последней внесенной записи в табл 'lib_authors', которая будет соответствовать автору обрабатываемой книги. for mysql
            newCategoryId = self.sps.get_last_inserted_id_in_db_mysql_sps ()
            
            print(f"PR_A680 --> SYS LOG: newCategoryId = {newCategoryId}")
                
        except Exception as err:
            print(f"PR_A681 --> SYS LOG: В результате !!! ОШИБКИ !!! новая категория  {category} не создана \n{sql}")
            
            print(f"PR_A682 --> SYS LOG: Exception -> {err}")
            
            newCategoryId = -1


        return newCategoryId
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    def update_author_data_in_tb_lib_authors_by_key (self, **fieldsData):
        """ 
        Обновить данные по автору книги в таблице lib_authors по ключу id автора
        """
        
        # INI
        authorId = fieldsData['authorId']
        authorFirstName = fieldsData['authorFirstName']
        authorSecondName = fieldsData['authorSecondName']
        authorFullName = fieldsData['authorFullName']
        
        sql = f"""
            UPDATE {ms.TB_LIB_AUTHORS}
            SET author_first_name = '{authorFirstName}', author_second_name = '{authorSecondName}', author_full_name = '{authorFullName}'
            WHERE id = {authorId};
        """
        
        # print(f"PR_A501 --> sql = {sql}")
        
        # EXECUTE_UPDATE
        try:
            self.sps.execute_sql_SPS(sql)
            print(f"PR_A504 --> SYS LOG: изменения в данных автора с id = {authorId} внесены в таблицу")
                
        except Exception as err:
            print(f"PR_A506 --> SYS LOG: В результате !!! ОШИБКИ !!!  изменения в данных автора с id = {authorId} не выполнены : \n{sql}")
            
            print(f"PR_A507 --> SYS LOG: Exception -> {err}")
        
        
        
        
        
    def update_narrator_data_in_tb_lib_authors_by_key (self, **fieldsData):
        """ 
        Обновить данные по автору книги в таблице lib_narrator по ключу id автора
        """
        
        # INI
        narratorId = fieldsData['narratorId']
        narratorFirstName = fieldsData['narratorFirstName']
        narratorSecondName = fieldsData['narratorSecondName']
        narratorFullName = fieldsData['narratorFullName']
        
        sql = f"""
            UPDATE {ms.TB_LIB_NARRATORS}
            SET narrator_first_name = '{narratorFirstName}', narrator_second_name = '{narratorSecondName}', narrator_full_name = '{narratorFullName}'
            WHERE id = {narratorId};
        """
        
        # print(f"PR_A501 --> sql = {sql}")
        
        # EXECUTE_UPDATE
        try:
            self.sps.execute_sql_SPS(sql)
            print(f"PR_A749 --> SYS LOG: изменения в данных диктора с id = {narratorId} внесены в таблицу")
                
        except Exception as err:
            print(f"PR_A750 --> SYS LOG: В результате !!! ОШИБКИ !!!  изменения в данных диктора с id = {narratorId} не выполнены : \n{sql}")
            
            print(f"PR_A751 --> SYS LOG: Exception -> {err}")
        
        
        
        
        
        
        
        
    def update_book_status_data_in_tb_lib_book_statuses_by_key (self, **fieldsData):
        """ 
        Обновить данные по одному статусу книги в таблице lib_book_statuses по ключу id статуса
        """
        
        # INI
        bookStatusId = fieldsData['bookStatusId']
        bookStatus = fieldsData['bookStatus']
        
        sql = f"""
            UPDATE {ms.TB_LIB_BOOK_STATUSES}
            SET book_status = '{bookStatus}' 
            WHERE id = {bookStatusId};
        """
        
        # print(f"PR_A501 --> sql = {sql}")
        
        # EXECUTE_UPDATE
        try:
            self.sps.execute_sql_SPS(sql)
            print(f"PR_A534 --> SYS LOG: изменения в данных с ключем id = {bookStatusId} внесены в таблицу")
                
        except Exception as err:
            print(f"PR_A535 --> SYS LOG: В результате !!! ОШИБКИ !!!  изменения в данных с ключем id = {bookStatusId} не выполнены : \n{sql}")
            
            print(f"PR_A536 --> SYS LOG: Exception -> {err}")
        
        
        
        
        
        
    def update_book_category_data_in_tb_lib_categories_by_key (self, **fieldsData):
        """ 
        Обновить данные по одной категории книги в таблице lib_book_statuses по ключу id статуса
        """
        
        # INI
        bookCategoryId = fieldsData['bookCategoryId']
        bookCategory = fieldsData['bookCategory']
        
        sql = f"""
            UPDATE {ms.TB_LIB_CATEGORIES}
            SET category = '{bookCategory}' 
            WHERE id = {bookCategoryId};
        """
        
        # print(f"PR_A501 --> sql = {sql}")
        
        # EXECUTE_UPDATE
        try:
            self.sps.execute_sql_SPS(sql)
            print(f"PR_A652 --> SYS LOG: изменения в данных с ключем id = {bookCategoryId} внесены в таблицу")
                
        except Exception as err:
            print(f"PR_A653 --> SYS LOG: В результате !!! ОШИБКИ !!!  изменения в данных с ключем id = {bookCategoryId} не выполнены : \n{sql}")
            
            print(f"PR_A654 --> SYS LOG: Exception -> {err}")
        
        

        
        
        
        
    def transfer_prev_category_to_categories_vocabulary_blf(self, **fieldsData):
        """ 
        Перенести редактируемое старое название категории в словарь lib_book_categories_vocabularies, в котором хранятся возможные дополнительные названия 
        категории (некоторые из них переносятся туда автоматически в ходе редактирования названий из парсинга новых книг, а некоторые могут вносится сознательно 
        в ручном режиме)
        categId - id редактируемой категории в таблице lib_categories
        """
        
        print(f"PR_A686 --> START: transfer_prev_category_to_categories_vocabulary_blf()")
        
        # INI
        editedBookCategoryId = fieldsData['bookCategoryId']
        newBookCategoryBeforeSave = fieldsData['bookCategory']
        
        # Получить существующее название категории из БД, соотвтетсвующее редактируемой категории с id = editedBookCategoryId, до сохранения нового варианта
        
        categNamePrev = self.get_category_name_by_id_blf(editedBookCategoryId).strip(' ')
        
        print(f"PR_A688 --> categName = {categNamePrev}")
        
        # проверить. есть ли в таблице переводов уже запись с названием categNamePrev. Если есть, то выдать сообщение об этом . Если нет, то выполнить вставку
        # новой транскрипции по категории
        
        # Если не существует подобного термина категории, то делаем вставку
        if not self.spps.if_value_exists_in_tb_given_column_auto_sql_df_spps (ms.TB_LIB_BOOK_CATEGORIES_VOCABILARY, 'categ_translate', categNamePrev):
        
            # Перенести (вставить) в табл lib_book_categories_vocabulary предыдущее название категории с categ_id = editedBookCategoryId
            
            sql = f"INSERT INTO {ms.TB_LIB_BOOK_CATEGORIES_VOCABILARY} (categ_id, categ_translate) VALUES ({editedBookCategoryId}, '{categNamePrev}')"
            
            try: 
                self.sps.execute_sql_SPS(sql)
                print(f"PR_A689 --> SYS LOG: в таблицу lib_book_categories_vocabulary внесена предыдущая транскипция категории {categNamePrev} по категории с id = {editedBookCategoryId}")
                
            except Exception as err:
                print(f"PR_A690 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
                print(f"PR_A691 --> SYS LOG: ERRORR !!! {err}")
                
                
        
        # B. Провверить, была ли в талице транскрипций lib_book_categories_vocabulary новое сохраненное в табл lib_categories  название newBookCategoryBeforeSave
        # Если такое название найдено. то удалить его (это обрабатывает тот случай. если по тем или иным причинам новое название редактируемой категории 
        # создается равным уже существующей транскрипции в таблице переаодов)
        
        # Если существует. то удалить ее
        if self.spps.if_value_exists_in_tb_given_column_auto_sql_df_spps (ms.TB_LIB_BOOK_CATEGORIES_VOCABILARY, 'categ_translate', newBookCategoryBeforeSave):
            
            sql =f"DELETE FROM {ms.TB_LIB_BOOK_CATEGORIES_VOCABILARY} WHERE categ_translate = '{newBookCategoryBeforeSave}'"
            
            
            try: 
                self.sps.execute_sql_SPS(sql)
                print(f"PR_A693 --> SYS LOG: в таблице lib_book_categories_vocabulary удалена запись транскрипции категории {newBookCategoryBeforeSave}, которая после изменений главной категории стала дублирующей по категории с id = {editedBookCategoryId}")
                
            except Exception as err:
                print(f"PR_A694 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
                print(f"PR_A695 --> SYS LOG: ERRORR !!! {err}")
        
        
        
        

        # Если существует термин в словаре
        else:
            
            print(f"PR_A692 --> SYS LOG: в таблице lib_book_categories_vocabulary уже есть транскипция категории {categNamePrev}")


        
        
        print(f"PR_A687 --> END: transfer_prev_category_to_categories_vocabulary_blf()")
        
        
        
        
    def assign_the_status_to_the_book_blf (self, bookId, bookStatus):
        """ 
        Присвоить заданный статус bookStatus для книги c id = bookId
        """
        print(f"PR_A541 --> START: assign_the_status_to_the_book_blf()")

        # A. Проверить наличие заданного на удаление статуса у книги в табл lib_books_statuses
        if self.if_the_status_assigned_for_the_book (bookId, bookStatus): 
            
            print(f"PR_A583 --> SYS LOG: Данной книги с id = {bookId} уже присвоен статус с id = {bookStatus}")
            
        else:

            dicInsertData = {
                'book_alfa_id' : bookId,
                'book_status_id' : bookStatus
            }
            
            try:
                self.sps.insert_record_to_tb_with_many_to_many_relation(ms.TB_LIB_BOOKS_STATUSES, dicInsertData)
            
                print(f"PR_A542 -->  SYS DB LOG: присвоен новый статус {bookStatus} для книги с id = {bookId}")
                
            except Exception as err:
                
                print(f"PR_A584 --> SYS LOG: При выполнении запроса произошла ошибка")
                print(f"PR_A585 --> SYS LOG: ERRORR !!! {err}")

            print(f"PR_A543 --> END: assign_the_status_to_the_book_blf()")







    def assign_the_category_to_the_book_blf (self, bookId, bookCategoryId):
        """ 
        Присвоить заданный категорий bookCategory для книги c id = bookId
        """
        print(f"PR_A641 --> START: assign_the_category_to_the_book_blf()")

        # A. Проверить наличие заданного на удаление категория у книги в табл lib_books_categories
        if self.if_the_category_assigned_for_the_book (bookId, bookCategoryId): 
            
            print(f"PR_A642 --> SYS LOG: Данной книги с id = {bookId} уже присвоена категория с id = {bookCategoryId}")
            
        else:

            dicInsertData = {
                'book_alfa_id' : bookId,
                'category_id' : bookCategoryId
            }
            
            try:
                self.sps.insert_record_to_tb_with_many_to_many_relation(ms.TB_LIB_BOOKS_CATEGORIES, dicInsertData)
            
                print(f"PR_A542 -->  SYS DB LOG: присвоена новая категория {bookCategoryId} для книги с id = {bookId}")
                
            except Exception as err:
                
                print(f"PR_A643 --> SYS LOG: При выполнении запроса произошла ошибка")
                print(f"PR_A644 --> SYS LOG: ERRORR !!! {err}")

            print(f"PR_A645 --> END: assign_the_category_to_the_book_blf()")











    def withdraw_given_status_from_the_book (self, bookId, bookStatus):
        """ 
        Удалить заданный статус bookStatus у книги c id = alfaBookId 
        """
        print(f"PR_A575 --> START: withdraw_given_status_from_the_book()")


        # A. Проверить наличие заданного на удаление статуса у книги в табл lib_books_statuses
        if self.if_the_status_assigned_for_the_book (bookId, bookStatus): 
            
            # B. Если такой статус обнаружен. то удалить его 
            sql = f"DELETE FROM {ms.TB_LIB_BOOKS_STATUSES} WHERE book_alfa_id = {bookId} AND book_status_id = {bookStatus}"
            
            try: 
                self.sps.execute_sql_SPS(sql)
                print(f"PR_A579 --> SYS LOG: У книги с id = {bookId} удален статус c id =  {bookStatus}")
                
            except Exception as err:
                print(f"PR_A580 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
                print(f"PR_A581 --> SYS LOG: ERRORR !!! {err}")
                
        else:
            print(f"PR_A578 --> SYS LOG: У данной книги с id = {bookId} не обнаружен статус с id = {bookStatus}")

        print(f"PR_A576 --> END: withdraw_given_status_from_the_book()")




    def if_the_status_assigned_for_the_book (self, bookId, bookStatus):
        """ 
        Проверить, присвоен ли заданный статус заданной книге
        """
        
        sql = f"SELECT * FROM {ms.TB_LIB_BOOKS_STATUSES} WHERE book_alfa_id = {bookId} AND book_status_id = {bookStatus}"
        
        return self.sps.if_select_result_exists_sps(sql)
        
        
        

    def if_the_category_assigned_for_the_book (self, bookId, bookStatus):
        """ 
        Проверить, присвоен ли заданный категорий заданной книге
        """
        
        sql = f"SELECT * FROM {ms.TB_LIB_BOOKS_CATEGORIES} WHERE book_alfa_id = {bookId} AND category_id = {bookStatus}"
        
        return self.sps.if_select_result_exists_sps(sql)
        
        
        
        
        
        
        
        
    def assign_the_status_to_list_of_books_blf (self, statusId, listOfBooks):
        """ 
        Присвоить статус всем книгам в списке
        """
        
        for bookId in listOfBooks:
            
            self.assign_the_status_to_the_book_blf(bookId, statusId)
            
            
        
        
        
    def withdraw_the_status_from_list_of_books_blf (self, statusId, listOfBooks):
        """ 
        Удалить статус у книг в списке
        """
        
        for bookId in listOfBooks:
            
            self.withdraw_given_status_from_the_book(bookId, statusId)
            
        
        
        
        
        
        
        


    def clear_all_statuses_of_book_in_lib_books_statuses_blf (self, bookAlfaId):
        """ 
        Удалить все статусы, принадлежащие bookAlfaId в таблице lib_books_statuses
        """

        sql = f"DELETE FROM {ms.TB_LIB_BOOKS_STATUSES} WHERE book_alfa_id = {bookAlfaId}"
        
        try:
            print(f"PR_A547 --> Выполнение запроса DELETE")
            self.sps.execute_sql_SPS(sql)
            
            print(f"PR_A544 --> Из таблицы lib_books_statuses удалены все статусы. принадлежавшие книге с alfaId = {bookAlfaId}")
        
        except Exception as err:
            
            print(f"PR_A545 --> Произошла ошибка. Запрос не выполнен: \n{sql}")
            print(f"PR_A546 --> ERROR: {err}")








    def clear_all_categories_of_book_in_lib_books_categories_blf (self, bookAlfaId):
        """ 
        Удалить все категории, принадлежащие bookAlfaId в таблице lib_books_categories
        """

        sql = f"DELETE FROM {ms.TB_LIB_BOOKS_CATEGORIES} WHERE book_alfa_id = {bookAlfaId}"
        
        try:
            print(f"PR_A637 --> Выполнение запроса DELETE")
            self.sps.execute_sql_SPS(sql)
            
            print(f"PR_A638 --> Из таблицы lib_books_categories удалены все статусы. принадлежавшие книге с alfaId = {bookAlfaId}")
        
        except Exception as err:
            
            print(f"PR_A639 --> Произошла ошибка. Запрос не выполнен: \n{sql}")
            print(f"PR_A640 --> ERROR: {err}")










        
        
        

    def assign_chosen_statuses_to_book_blf (self, bookAlfaId, listBookStatusesIds):
        """ 
        Присвоить выбранные статусы  из списка статусов с checkboxes для книги, id которых находятся в списке  listBookStatusesIds, в таблицу  lib_books_statuses, предварительно удалив все присвоенные статусы 
        для alfaBookId , существовавшие ранее
        """
        
        # Удалить все статусы , принадлежавшие книге 
        self.clear_all_statuses_of_book_in_lib_books_statuses_blf (bookAlfaId)
        
        # Внести в таблицу lib_books_statuses новые записи со статусами, id которых находятся в списке  listBookStatusesIds, для книги bookAlfaId
        for statusId in listBookStatusesIds:
            self.assign_the_status_to_the_book_blf(bookAlfaId, statusId)
            
        print(f"PR_A548 --> SYS LOG: В таблице lib_books_statuses сначала удалены все записи по alfaid = {bookAlfaId}, а зптем книге присвоены новые статусы сid статусов из списка {listBookStatusesIds}")
        






    def assign_chosen_categories_to_book_blf (self, bookAlfaId, listBookCategoriesIds):
        """ 
        Присвоить выбранные категории  из списка категорий с checkboxes для книги, id которых находятся в списке  listBookCategoriesIds, в таблицу  lib_books_categories, предварительно удалив все присвоенные категории 
        для alfaBookId , существовавшие ранее
        """
        
        # Удалить все категории , принадлежавшие книге 
        self.clear_all_categories_of_book_in_lib_books_categories_blf (bookAlfaId)
        
        # Внести в таблицу lib_books_statuses новые записи со статусами, id которых находятся в списке  listBookStatusesIds, для книги bookAlfaId
        for categoryId in listBookCategoriesIds:
            self.assign_the_category_to_the_book_blf(bookAlfaId, categoryId) 
            
        print(f"PR_A548 --> SYS LOG: В таблице lib_books_statuses сначала удалены все записи по alfaid = {bookAlfaId}, а зптем книге присвоены новые статусы сid статусов из списка {listBookCategoriesIds}")
        




    def get_df_all_alfa_books_with_full_data_blf (self):
        """ 
        Получить фрейм со всеми книгами библиотеки с набором данных по ним из таблиц lib_books_alfa, lib_books_alfa_ext
        """

        sql = f"SElECT * FROM {ms.TB_LIB_BOOKS_ALFA}, {ms.TB_LIB_BOOKS_ALFA_EXT} WHERE {ms.TB_LIB_BOOKS_ALFA}.id = {ms.TB_LIB_BOOKS_ALFA_EXT}.books_alfa_id"

        dfAllBooks= self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        return dfAllBooks



    def get_df_alfa_books_with_full_data_filtered_by_list_alfa_ids_blf (self, listAlfaIds):
        """ 
        Получить фрейм со всеми книгами библиотеки с набором данных по ним из таблиц lib_books_alfa, lib_books_alfa_ext, отфильтрованными по заданному списку alfa_ids в listAlfaIds
        Прим: Использовать эту конструкцию, в частности, для фильтрации по таблицам МКМ - многие-ко-многим
        """
        
        print(f"PR_A567 --> listAlfaIds = {listAlfaIds}")
        
        if len(listAlfaIds) == 1:
            tupleAlfaIds = f"({listAlfaIds[0]})"
        else:
            tupleAlfaIds = tuple(listAlfaIds)
        
        print(f"PR_A564 --> tupleAlfaIds = {tupleAlfaIds}")

        sql = f"""
                SElECT * FROM {ms.TB_LIB_BOOKS_ALFA}, {ms.TB_LIB_BOOKS_ALFA_EXT} 
                WHERE 
                    {ms.TB_LIB_BOOKS_ALFA}.id = {ms.TB_LIB_BOOKS_ALFA_EXT}.books_alfa_id 
                AND 
                    {ms.TB_LIB_BOOKS_ALFA_EXT}.books_alfa_id IN {tupleAlfaIds}
                """

        dfBooksFiltered = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        return dfBooksFiltered




    def get_lib_book_full_data_by_alfa_id_as_dic_blf (self, alfaBookId):
        """ 
        Получить полные данные по книге из обьединенных таблиц lib_books_alfa и lib_books_alfa_ext в виде словаря
        dicBookData = 
        {
            'id': 5, 
            'liter_group_z': '0000000005', 
            'liter_group_y': '000', 
            'liter_group_x': '000', 
            'final_ilbn': '000-000-0000000005', 
            'date_reg_calend': '05-03-2024 15:42:04', 
            'date_reg_unix': 1709650000.0, 
            'id_1': 5, 
            'books_alfa_id': 5, 
            'book_title': 'Звездная месть', 
            'book_description': '\r\n\r\n ХХV век. Мощь земной цивилизации безгранична. Ее космический флот может уничтожить любую нечеловеческую расу в отдельности и все их вместе взятые. Однако, в своем могуществе Земля не замечает нависшей над ней чудовищной угрозы Вторжения Извне, с которой человечеству еще никогда не приходилось сталкиваться. Надвигающийся апокалипсис может предотвратить космодесантник-смертник, младенцем найденный в анабиозной капсуле на краю вселенной...\r\n', 
            'book_message_id': 4390, 
            'book_orig_source_id': 1, 
            'date_issue_calend': 'NULL', 
            'date_issue_unix': None, 
            'language_id': 1, 
            'serial_id': None, 
            'language_relation_id': None}
            
        """


        sql = f"""
                SElECT * FROM {ms.TB_LIB_BOOKS_ALFA} as lba, {ms.TB_LIB_BOOKS_ALFA_EXT} as lbae
                WHERE 
                    lba.id = lbae.books_alfa_id 
                AND 
                    lbae.books_alfa_id = {alfaBookId}
                """
                
        dicBookData = self.spps.read_one_row_return_sql_to_dic_mysql_spps(sql)
        
        return dicBookData
        
        





    def filter_input_books_source_with_given_status_blf (self, inpSrcBooksAlfaIds : list|tuple, filterStatusId) -> list:
        """ 
        Отфильтровать из входного массива книг inpSrcBooksAlfaIds те книги, которые обладают заданным статусом filterStatusId
        ПРИМ: На данынй моммент inpSrcBooksAlfaIds должен быть списком alfaIds книг [bookAlfaId1, ... , bookAlfaIdN] или кортеж 
        RET: Список listBooksAlfaIdsFiltered
        """
        
        # Если в списке всего один элемент, то он не переводится в кортеж, а трансформируется в принтовую структуру: '(id)', 
        # так как тпала из одного элемента не существует без запятой в конце, которая приводит к SQL-ошибке
        if len(inpSrcBooksAlfaIds) == 1:
            tupleAlfaIds = f"({inpSrcBooksAlfaIds[0]})" # трансформируется в принтовую структуру: '(id)' без запятой в конце
        else:
            tupleAlfaIds = tuple(inpSrcBooksAlfaIds)
        
        sql = f"SELECT book_alfa_id FROM {ms.TB_LIB_BOOKS_STATUSES}  WHERE book_status_id = {filterStatusId} AND book_alfa_id IN {tupleAlfaIds}"
        
        print(f"PR_A573 --> sql = {sql}")

        listBooksAlfaIdsFiltered = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        # проверка на пустоту
        if isinstance(listBooksAlfaIdsFiltered, int):
            ret = []
        else:
            ret = listBooksAlfaIdsFiltered
        
        return ret








    def get_tg_chat_nick_if_book_was_downloaded_from_tg_channel_blf (self, bookAlfaId):
        """ 
        Получить данные по источнику книги из табл lib_orig_sources, для тех книг, источником которых служили телеграм-чаты (los.orig_source_type_id = 1) 
        """
        
        sql = f"""
                SELECT tg_channel_nick FROM {ms.TB_LIB_BOOKS_ALFA_EXT} as lbae,{ms.TB_LIB_ORIG_SOURCES} as los 
                WHERE 
                lbae.books_alfa_id = {bookAlfaId} 
                AND lbae.book_orig_source_id = los.id 
                AND los.orig_source_type_id = 1
                """
                
        tgChNick = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        
        
        return tgChNick






    def obtain_book_complect_full_data_dict_to_tg_public_blf (self, listBookAlfaIds, fgPrint = False):
        """ 
        Составить общий конечный словарь публикаций для комплектов книг из списка listBookAlfaIds с полными данными для публикации книг на ТГ-канале 
        listBookAlfaIds - список alfaids книг
        ПРИМ: Развивающийся словарь (словарь, где данные и структура модифицируются постепенно для улучшения эффективности [к примеру на данный момент 
        тут много избыточной и ненужной информации для публикации. Надо прочистить])
        
        На данный момент имеет формат такого плана:
        
                {
                    'bookAuthorsFullNames': ['Батыршин Борис'],
                    'bookData': {
                        'book_description': '\n\n\nМинистерство обороны Российской Федерации проводит масштабный эксперимент по изменению прошлого. В 1854 год на Крымскую войну должен отправиться батальон морпехов на
                                            большом десантном корабле.\nНо что если что-то пойдет не так и в воронку времени угодят попутчики – гидрокрейсер «Алмаз» и миноносец «Заветный» из 1916 года?
                                            ...(3 hidden lines)',
                        'book_message_id': 4378,
                        'book_orig_source_id': 1,
                        'book_title': 'Крымская война',
                        'books_alfa_id': 1,
                        'date_issue_calend': 'NULL',
                        'date_issue_unix': None,
                        'date_reg_calend': '27-02-2024 09:10:31',
                        'date_reg_unix': 1709030000.0,
                        'final_ilbn': '000-000-0000000001',
                        'id': 1,
                        'id_1': 1,
                        'language_id': 1,
                        'language_relation_id': None,
                        'liter_group_x': '000',
                        'liter_group_y': '000',
                        'liter_group_z': '0000000001',
                        'serial_id': None,
                    },
                    'bookImages': ['ch1_m4378_gr1_book_descr_photo.jpg'],
                    'bookVolumes': ['1. КВ. Попутчики_ch_1_msg4379_gr1_audio_volume.mp3', '2. КВ. Соратники_ch_1_msg4380_gr1_audio_volume.mp3', '3. КВ. Соотечественники_ch_1_msg4381_gr1_audio_volume.mp3'],
                    
                    'bookCategories' : [...],
                    
                    
                }
        
        """

        dicFinalBooksDataPublication : dict = {}

        # Цикл по alfaIds книг, разрешенных к публикации
        for bookAlfaId in listBookAlfaIds:
            pass
        
            # Словарь с данными по книге с текущим по циклу alfaId
            dicBookData = self.get_alfa_book_data_by_alfa_id(bookAlfaId)
            
            # Получить список картинок, соотвтетсвующих описанию книги
            
            dicAlfaBookImagesNames = self.get_book_images_names_dic_in_lib_by_alfa_id_blf(bookAlfaId)
            

            
            
            print(f"PR_B208 --> dicAlfaBookImagesNames = {dicAlfaBookImagesNames}")
            
            listBookImages = list(dicAlfaBookImagesNames.values())
            
            # Получить список авторов книги
            listBookAuthors = self.get_authors_of_book_by_alfa_id(bookAlfaId)
            
            if not isinstance(listBookAuthors, int):
                bookAuthorsFullNames = [x[-1] for x in listBookAuthors]
            else:
                bookAuthorsFullNames = None
            
            # Получить список категорий книги
            listBookCategories = self.get_book_categories_by_alfa_id (bookAlfaId)
            
            print(f"PR_B470 --> bookAlfaId = {bookAlfaId}")
            print(f"PR_B469 --> listBookCategories = {listBookCategories}")
            
            if not isinstance(listBookCategories, int):
            
                bookCategories = [x[-1] for x in listBookCategories]
            else:
                bookCategories = []
            
            # Получить словарь аудио-томов книги, с названием файла, отсортированных по индексу выхода томов
            tupleKeys = tuple([bookAlfaId])
            bookVolumes = self.get_lib_alfa_books_volumes_dic_sliced_with_keys_list(tupleKeys)
            bookVolumes = bookVolumes[bookAlfaId]
        
        
            dicFinalBooksDataPublication[bookAlfaId] = {
                'bookData' : dicBookData,
                'bookImages' : listBookImages,
                'bookAuthorsFullNames' : bookAuthorsFullNames, 
                'bookVolumes' : bookVolumes,
                'bookCategories' : bookCategories,
            }
            
        if fgPrint:
            print(f'PR_A614 --> dicFinalBooksDataPublication:')
            # Beeprint friendly распечатка dicFinalBooksDataPublication
            pp(dicFinalBooksDataPublication)
                
        
        return dicFinalBooksDataPublication








    @staticmethod
    def find_img_full_path_by_name_in_lib_img_storage_recursive_blf (fileImgName):
        """ 
        BookLibraryFuncs
        Найти файл-картинку рекурсивно в проектном хранилище картиинок по ее названию. Вернуть список, в котором возможны три варианта найденной информации:
        - Пустой список - значит в директории не обнаружен
        - Список с одним элементом в виде полного пути к файлу - значит поиск закончен успешно и в Хранилище найден один файл с заданным уникальным названием
        - Список с несколькими элементами в виде путей к файлам - значит нарушен принцип целостноости Хранилища и в нем находятся несколько файлов 
        с одинаковыми названиями
        """
        
        
        listFiles = FilesManager.find_file_in_dir_by_name_recursively(ms.LIB_BOOK_IMAGE_STORAGE, fileImgName)
        
        return listFiles




    def get_book_src_msg_id_if_src_was_telegram_channel_blf (self, bookAlfaId):
        """ 
        Получить id сообщения из ТГ - канала источника, которое является оригинальным источником описания книги, если источником книги 
        являлся ТГ-канал
        ПРИМ: Если нужна будет оптимизауия по скорости при большом обьеме данных, то этот метод может быть оптимизирован {TO_BE_OPTOMIZED_BY_SPEED_}
        """
        
        print(f"PR_A738 --> START: get_book_src_msg_id_if_src_was_telegram_channel_blf()")


        dicBookData = self.get_alfa_book_data_by_alfa_id(bookAlfaId)
        
        print(f"PR_A737 --> dicBookData = \n{dicBookData}")
        
        """ 
        dicBookData = 
        {
            'id': 5, 
            'liter_group_z': '0000000005', 
            'liter_group_y': '000', 
            'liter_group_x': '000', 
            'final_ilbn': '000-000-0000000005', 
            'date_reg_calend': '05-03-2024 15:42:04', 
            'date_reg_unix': 1709650000.0, 
            'id_1': 5, 
            'books_alfa_id': 5, 
            'book_title': 'Звездная месть', 
            'book_description': '\r\n\r\n ХХV век. Мощь земной цивилизации безгранична. Ее космический флот может уничтожить любую нечеловеческую расу в отдельности и все их вместе взятые. Однако, в своем могуществе Земля не замечает нависшей над ней чудовищной угрозы Вторжения Извне, с которой человечеству еще никогда не приходилось сталкиваться. Надвигающийся апокалипсис может предотвратить космодесантник-смертник, младенцем найденный в анабиозной капсуле на краю вселенной...\r\n', 
            'book_message_id': 4390, 
            'book_orig_source_id': 1, 
            'date_issue_calend': 'NULL', 
            'date_issue_unix': None, 
            'language_id': 1, 
            'serial_id': None, 
            'language_relation_id': None}

        """
        
        # Проверяем есть ли в ключе (или в поле) book_message_id какое-то значение (что является подтверждением, что источником книги изначально 
        # являлся ТГ-канал)
        
        
        if self.is_book_source_from_telegram_channel(bookAlfaId):
            
            dicBookData = self.get_alfa_book_data_by_alfa_id(bookAlfaId)
            
            
            
            bookTgMssgId = dicBookData['book_message_id']
            
        else: 
            
            bookTgMssgId = -1
            
            
        print(f"PR_A739 --> END: get_book_src_msg_id_if_src_was_telegram_channel_blf()")
            
        return bookTgMssgId

        



    def is_book_source_from_telegram_channel(self, bookAlfaId):
        """ 
        Является ли оригинальный источник книг Телеграм - каналом (а именно, имется ли в таблице lib_books_alfa_ext в поле book_message_id какое-то значение. Если 
        имеется, то значит источником книги явилось сообщение телеграм-канала)
        ПРИМ: прорабатывается
        """
        
        dicBookData = self.get_alfa_book_data_by_alfa_id(bookAlfaId)
        
        print(f"PR_A740 --> dicBookData = \n{dicBookData}")
        
        # Проверяем есть ли в ключе (или в поле) book_message_id какое-то значение (что является подтверждением, что источником книги изначально 
        # являлся ТГ-канал)
        
        tgMssaId = dicBookData['book_message_id']
        
        print(f"PR_A741 --> tgMssaId = {tgMssaId}")
        
        
        
        if tgMssaId and tgMssaId != -1:
            
            print(f"PR_A742 --> is_book_source_from_telegram_channel = True")
            
            return True
        else:
            print(f"PR_A743 --> is_book_source_from_telegram_channel = False")
            return False
        
        
        
        
        
        
    # def delete_pseudo_book_by_alfa_id_blf (self, bookAlfaId):
    #     """ 
    #     Удалить зарегестрированную псевдо-книгу из таблиц 'lib_books_alfa' и 'lib_books_alfa_ext'
    #     """
        
    #     sql = f"DELETE FROM {ms.TB_LIB_BOOKS_ALFA_EXT} WHERE books_alfa_id = {bookAlfaId}"
        
    #     print(f"PR_A793 --> sql = {sql}")
        
    #     try: 
    #         self.sps.execute_sql_SPS(sql)
    #         print(f"PR_A787 --> SYS LOG: из таблицы 'lib_books_alfa_ext' удалена запись с books_alfa_id = {bookAlfaId}")
            
    #     except Exception as err:
    #         print(f"PR_A788 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
    #         print(f"PR_A789 --> SYS LOG: ERRORR !!! {err}")
    
    
    #     sql = f"DELETE FROM {ms.TB_LIB_BOOKS_ALFA} WHERE id = {bookAlfaId}"
        
        
        
    #     try: 
    #         self.sps.execute_sql_SPS(sql)
    #         print(f"PR_A790 --> SYS LOG: из таблицы 'lib_books_alfa' удалена запись с id = {bookAlfaId}")
            
    #     except Exception as err:
    #         print(f"PR_A791 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
    #         print(f"PR_A792 --> SYS LOG: ERRORR !!! {err}")
    
    
    
    def delete_book_from_lib_by_alfa_id_blf (self, bookAlfaId):
        """ 
        Удалить зарегестрированную книгу (или любой обьектюЮ типа псевдо-книги) из таблиц 'lib_books_alfa' и 'lib_books_alfa_ext'
        ПРИМ: из табл 'lib_books_alfa_ext' запись удаляется в следствии связи FOREIGN KEY ... CASCADE при удалении записи из главной табл 'lib_books_alfa'
        """
        
        # sql = f"DELETE FROM {ms.TB_LIB_BOOKS_ALFA_EXT} WHERE books_alfa_id = {bookAlfaId}"
        
        # print(f"PR_A793 --> sql = {sql}")
        
        # try: 
        #     self.sps.execute_sql_SPS(sql)
        #     print(f"PR_A787 --> SYS LOG: из таблицы 'lib_books_alfa_ext' удалена запись с books_alfa_id = {bookAlfaId}")
            
        # except Exception as err:
        #     print(f"PR_A788 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
        #     print(f"PR_A789 --> SYS LOG: ERRORR !!! {err}")
    
    
        sql = f"DELETE FROM {ms.TB_LIB_BOOKS_ALFA} WHERE id = {bookAlfaId}"
        
        
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_A790 --> SYS LOG: из таблицы 'lib_books_alfa' удалена запись с id = {bookAlfaId}")
            
        except Exception as err:
            print(f"PR_A791 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_A792 --> SYS LOG: ERRORR !!! {err}")
    
    
    
    
    
        
        
        
    def get_del_obj_type_id_by_name (self, delTypeName):
        """ 
        Получить id типа удаляемого обьекта из табл lib_obj_removed_types
        """
        
        sql = f"SELECT id FROM {ms.TB_LIB_OBJ_REMOVED_TYPES} WHERE del_obj_type = '{delTypeName}'"
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return res[0]
        
        
        
        
        
        

    def delete_lib_registered_book_complect_or_pseudo_book_blf(self, bookAlfaId):
        """ 
        Удаленить зарегестрировнный книжный комплект или псевдо-книгу
        """
        
        
        print(f"PR_A776 --> START: delete_lib_registered_book_complect_or_pseudo_book_blf()")
        
        # A.  Проверить имеет ли альфа-книга с id = bookAlfaId  том
        
        # INI
        sourceId = self.get_book_source_id_by_alfa_id_blf (bookAlfaId)
        
        # Если имеет, значит поступила команда на удаление зарегестрированного книжного комплекта (включая все его тома, связи, а так же . при необходимости
        # - удалить книжный комплект из ТГ-канала или другого реплзитория, который задан !!!)
        # TODO: Перевести все реализации функционалов тут в отдельные методы !!!
        
        if self.isBookHasAudioVolumes(bookAlfaId):
            
            print(f"PR_A781 --> SYS LOG: Книга с id = {bookAlfaId} имеет аудио-тома и является книжным комплектом")
            
            # D. Сначала удалить все записи в третичных и вторичных таблицах, имеющих связи с книжным комплектом (Удаляем по типу снизу вверх)
            # начинаем с вторичных и третичных таблиц , связанных с томами книги 
            
            # a/ Альтернативно - удалить запись из внешнего репозитория [при наличии флага на удаление выгруженного прообраза книги в каком-либо внешнем репозитории
            # Пока считаем что флаг выставлен на НЕ удалять книгу и тома на внешних репозиториях]
            
            # b/ Табл lib_audio_volumes_reposit_registration. Пока оставляем тоже нетронутой по возможности. В ней сохраняются записи, которые сохраняют в себе 
            # информацию о брошенках, то есть о тех  томах, которые удалены из регистрации в библиотеке, но их образы продолжают оставаться выгруженными 
            # на каких-либо внешних репозиториях
            
            # c/ Сохраняем messageId томов и альфа книги в архивной таблице удалений с маркером 'BOOK_AUDIO_VOLUME_DEL' И 'BOOK_ALFA_DEL'
            
            # Получить список  ids сообщений, скачанных с ТГ-канала, соотвтетсвующих аудио-томам книги с заданным bookAlfaId
            listBVolumesMssgsIds = self.get_lib_book_volumes_tg_messages_ids_blf(bookAlfaId)
            
            print(f"PR_A801 --> listBVolumesMssgsIds = {listBVolumesMssgsIds}")
            
            
            # записать все messageIds из списка listBVolumesMssgsIds удаляемых томов книги в таблицу архивации удалений lib_objects_removed с маркером 'BOOK_AUDIO_TOM_DEL'
            for messageId in listBVolumesMssgsIds:
                # Вставить (INSERT) в табл lib_objects_removed
                self.insert_message_id_to_tb_lib_object_removed_with_obj_type_marker_blf (sourceId, messageId, "BOOK_AUDIO_VOLUME_DEL")
                
            
            # d/ после фиксации в таблице удалений, удаляем альфа-книгу, которая по цепочке удалит все записи, которые соотвтетсвуют FOREIGN KEY с ON DELETE CASCADE
            # ПРИМ: TODO: разобраться почему. После проверок одна лишь таблица lib_books_categories почему то не удаляет автоматом записи по связи cascade ??? (возможно придется делать это програмно)
            
            
            # вставить messageId альфа-книги в табл lib_objects_removed с меткой 'BOOK_ALFA_DEL'
            bookMessagId = self.get_book_message_id_by_alfa_id_blf (bookAlfaId)
            
            self.insert_message_id_to_tb_lib_object_removed_with_obj_type_marker_blf (sourceId, bookMessagId, "BOOK_ALFA_DEL")
            
            
            # Удалить альфа-книгу (а в ходе ее удаления кдаляются все записи по связям FOREIGN KEY ... CASCADE)
            self.delete_book_from_lib_by_alfa_id_blf(bookAlfaId)
            
            
            # e/ удалить все записи из табл lib_books_categories, соотвтетсвующих bookAlfaId (так как эта таблица глючит в смысле удаления записей по связям cascade)
            # ПРИМ: вроде нормально удаляет по CASCADE

        
        # Если нет томов, то команда - удалить псевдо-книгу (что намного более простая операция). И занести в архив удалений (только, если это псевдо-книга? нет. во всех случаях
        # все множество регестрируемых messageId в библиотеке может делиться на два подмножества: либо это подмножество зарегестрированных, либо - в удаленных архивах)
        # то есть , если по каким-то причинам удаляется не псевдо, а реальный книжный пакет - он тоже со всеми суб-томами попадает в архивы удаленны хсообщений в табл
        # lib_objects_removed
        
        else: 
            
            print(f"PR_A782 --> SYS LOG: Книга с id = {bookAlfaId} НЕ имеет аудио-томов и является, скорее всего, псевдо-книгой")
            
            #  Получить messageId псевдо-книги 
            
            # INI
            bookMessagId = self.get_book_message_id_by_alfa_id_blf (bookAlfaId)
                
            print(f"PR_A783 --> bookMessagId = {bookMessagId}")
            
            # B. Сохранить bookMessagId в таблицу lib_objects_removed с пометкой 'PSEUDO_BOOK_DEL'
            
            self.insert_message_id_to_tb_lib_object_removed_with_obj_type_marker_blf (sourceId, bookMessagId, "PSEUDO_BOOK_DEL")
        
            # C. Удалить псевдо-книгу с текущим alfaId 
            
            self.delete_book_from_lib_by_alfa_id_blf(bookAlfaId)

        
        print(f"PR_A777 --> END: delete_lib_registered_book_complect_or_pseudo_book_blf()")
        
        
        
        
        
    def insert_message_id_to_tb_lib_object_removed_with_obj_type_marker_blf (self, sourceId, objMessageId, delTypeName):
        """ 
        Вставить ТГ messageId удаляемого (удаленного) обьекта библиотеки в архивную таблицу удаленных обьбектов lib_object_removed с фиксацией типа удаленного 
        обьекта, присваиваемого из вариантов таблицы lib_obj_removed_types
        """
        
        # текущее время в разных форматах
        currCalendDateFormat1, currCalendDateFormat2, currCalendDateUnix = FG.get_current_time_format_1_and_2_and_universal_unix() 
        
        
        
        # получить ID для типа уудаленного обьекта delTypeName в табл lib_obj_removed_types
        delTypeId = self.get_del_obj_type_id_by_name(delTypeName)
        
        
        
        sql = f"""
                INSERT INTO {ms.TB_LIB_OBJECTS_REMOVED} 
                (source_id, tg_message_id, del_obj_type_id, cal_date_del, unix_date_del) 
                VALUES 
                ({sourceId}, {objMessageId}, {delTypeId}, '{currCalendDateFormat2}', {currCalendDateUnix})
        """
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_A784 --> SYS LOG: в таблицу архивных удалений 'lib_objects_removed' внесен messageId = {objMessageId} от источника sourceId = {sourceId} с маркером 'PSEUDO_BOOK_DEL'")
            
        except Exception as err:
            print(f"PR_A785 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_A786 --> SYS LOG: ERRORR !!! {err}")

    
    
    
    @staticmethod
    def check_if_vocabulary_volume_replace_keys_exists_in_to_load_document_full_path_blf (fullDocumentBeDownloadedPath, dicReplaceVocabulary):
        """ 
        Проверить, есть ли в названии документа, который сейчас будет скачен с сообщения из ТГ-канала, фрагмент, определяемый в ключах словаря замещений
        VOCABULARY_AWAIT_VOLUME_REPLACE. Этот словарь предназначен для определения пустых файлов, заглушек, которые заведены для того. что бы потом в них
        вставить реальные аудио-тома книги. Поскольку эти заглушки mp3 - индивидуальны, по ним можно определить собственность оригинала. ПОэтому мы их
        изменяем и вместо них подгружаем наши mp3 заглушки
        """
        
        print(f"PR_A858 -->  START: check_if_vocabulary_volume_replace_keys_exists_in_to_load_document_full_path_blf()")
        
        
        print(f"PR_A860 --> fullDocumentBeDownloadedPath = {fullDocumentBeDownloadedPath}")
        
        # Цикл по ключам-искомым-маркерам в словаре dicReplaceVocabulary
        
        for key, val in dicReplaceVocabulary.items():
            
            # Если имкомый фрагмент из словаря замещений для аудио-томов присутствует, то этот документ не должен скачиваться, 
            # а должен быть подменен нашим системным файло Ожидающей книги 
            if key in fullDocumentBeDownloadedPath:
            
                print(f"PR_A861 --> Искомый фрагмент в полном пути загружающегосся документа найден")
                
                # return True
                
                return key
                

                
        print(f"PR_A862 --> Искомый фрагмент в полном пути загружающегося документа НЕ НАЙДЕН")
        
        # return False

        return None
        
        
        



    def obtain_lists_of_lib_categories_and_categ_translations_in_vocabulary_blf(self):
        """ 
        Получить списки существующих категорий и переводов категорий в переводчике категорий из таблиц 'lib_categories' и 'lib_book_categories_vocabulary'
        """
        
        print(f"PR_A919 --> START: obtain_lists_of_lib_categories_and_categ_translations_in_vocabulary_blf()")
        
        sql = f'SELECT category FROM {ms.TB_LIB_CATEGORIES}'
        
        print(f"PR_A922 --> sql = {sql}")
        
        dfExistsCategories = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        print(f"PR_A921 --> dfExistsCategories = \n{dfExistsCategories}")
        
        if not isinstance(dfExistsCategories, int):
            listExistsCategories = PandasManager.convert_df_col_to_list_pm_static(dfExistsCategories,'category')
        else:
            listExistsCategories = []
        
        print(f"PR_A915 --> listExistsCategories = {listExistsCategories}")
        
        
        sql = f'SELECT categ_translate FROM {ms.TB_LIB_BOOK_CATEGORIES_VOCABILARY}'
        dfExistsCategoriesVocabulary = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        if not isinstance(dfExistsCategoriesVocabulary, int):
            listExistsCategoriesVocabulary = PandasManager.convert_df_col_to_list_pm_static(dfExistsCategoriesVocabulary,'categ_translate')
        else:
            listExistsCategoriesVocabulary = []

        print(f"PR_A918 --> listExistsCategoriesVocabulary = {listExistsCategoriesVocabulary}")


        print(f"PR_A920 --> END: obtain_lists_of_lib_categories_and_categ_translations_in_vocabulary_blf()")
        
        # Очистка
        listExistsCategories = [x.strip(' ') for x in listExistsCategories ]
        
        listExistsCategoriesVocabulary = [x.strip(' ') for x in listExistsCategoriesVocabulary ]



        return listExistsCategories, listExistsCategoriesVocabulary





    def register_repository_loaded_book_descr_message_data_blf(self, retData, **kwargs):
        """ 
        Зарегестрировать данные о сообщении с описанием книги, выгруженного в свой ТГ канал (репозиторий)
        inx - порядковый индекс в общем ответе при регистрации группы (если одна картинка, то будет список из одного ответа)
        """

        print(f"PR_A928 --> START: register_repository_loaded_book_descr_message_data_blf()")

        # INI
        
        # # Табличный id текущей картинки в табл 'lib_book_images'
        imageLibTbid = kwargs['imageLibTbid']

        
        bookAlfaId = kwargs['libBookData']['bookAlfaId']
        repositoryId = kwargs['libBookData']['repositoryId']
        
        if not kwargs['libBookData']['bookContinuePart']:
            bookContinuePart = 'NULL'
        
        if not kwargs['libBookData']['bookSerialsPart']:
            bookSerialsPart = 'NULL'
        
        # Тип сообщения (полученный из альфа-книги описания, из библиотеки lib)
        messageTypeId = kwargs['libBookData']['messageTypeId']
        
        # Название файла из описания альфа-книги, который соответствует картиинки этого сообщения (для визиуальности данных в таблице навскидку)
        fileImgName = kwargs['libBookData']['fileImgName'] 
        
        # Возвращаемые данные, возвращаемые после загрузки сообщения в канал
        # https://docs.pyrogram.org/api/types/Message#pyrogram.types.Message [attributes of return data !!]
        # retMssgLoadData = kwargs['retMssgLoadData']
        # id загруженного осообщения в текуещем канале
        messageId = retData.id
        
        print(f"PR_A937 --> messageId = {messageId}")
        
        # Ссылка текущего ТГ канала
        linkOfRepository = self.get_tb_repositories_given_row_full_data_as_dic_blf(repositoryId)['reposit_link']
        # Ссылка на сообщение в текущем ТГ канале
        linkOfMssgInReposit = linkOfRepository + '/' + str(messageId)
        
        # id файла в ТГ-канале (string)
        fileId = retData.photo.file_id
        
        # unique file_id (string)
        fileUniqueId = retData.photo.file_unique_id
        
        # file_size
        fileSize = retData.photo.file_size
        
        # Время регистрации
        dtStringFormat1, dtStringFormat2, universUnix = FG.get_current_time_format_1_and_2_and_universal_unix()
        calDateRegistration = dtStringFormat2
        unixDateRegistration = universUnix
        
        
        print(f"PR_A930 --> fileSize = {fileSize}")
        
        # # bookDescrImgName = self.get_book_descr_image_name_for_photo_mssg_type_by_alfa_id(bookAlfaId)
        # print(f"PR_A936 --> ")
        # print(retMssgLoadData.photo)
        

        
        # Текущая таблица для регистрации загрузки сообщений в заданный ТГ-канал, определяемый в табл 'lib_repositories' by repositoryId
        tbRepositRegistrCurrent = ms.TB_LIB_REPOSIT_BOOKS_REGISTR_ + str(repositoryId)
        
        sql = f"""
                INSERT INTO {tbRepositRegistrCurrent} 
                (
                    book_alfa_id,
                    repository_id,
                    link_in_repository,
                    reposit_own_message_id,
                    file_name,
                    file_id,
                    file_unique_id,
                    file_size,
                    message_type_id,
                    cal_date_registration,
                    unix_date_registration,
                    book_continue_part,
                    book_serials_part,
                    lib_image_id
                )
                    
                VALUES 
                (
                    {bookAlfaId},
                    {repositoryId},
                    '{linkOfMssgInReposit}',
                    {messageId},
                    '{fileImgName}',
                    '{fileId}',
                    '{fileUniqueId}',
                    {fileSize},
                    {messageTypeId},
                    '{calDateRegistration}',
                    {unixDateRegistration},
                    {bookContinuePart},
                    {bookSerialsPart},
                    {imageLibTbid}  
                )
        """
        

        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_A940 --> SYS LOG: Зарегестрирована загрузка сообщения типа - ОПИСАНИЕ КНИГИ с alfaId = {bookAlfaId} в таблице '{tbRepositRegistrCurrent}'")
            
        except Exception as err:
            print(f"PR_A938 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_A939 --> SYS LOG: ERRORR !!! {err}")

        # # автоинкрементное id последней вставки
        # lastId = self.sps.get_last_inserted_id_in_db_mysql_sps()


        print(f"PR_A929 --> END: register_repository_loaded_book_descr_message_data_blf()")
        



    def register_repository_loaded_book_media_group_audio_volume_message_data_blf(self, **kwargs):
        """ 
        Зарегестрировать данные о сообщении в виде медиа-группы с аудио-томами книги, выгруженной в свой заданный ТГ канал (репозиторий)
        """

        print(f"PR_A945 --> START: register_repository_loaded_book_media_group_audio_volume_message_data_blf()")

        # INI
        
        # tbReposBookRegId = kwargs['libBookVolumeData']['tbReposBookRegId']
        repositoryId = kwargs['libBookVolumeData']['repositoryId']
        messageTypeId = kwargs['libBookVolumeData']['messageTypeId']
        bookAlfaId = kwargs['libBookVolumeData']['bookAlfaId']
        dicAlfaBookVolumes = kwargs['libBookVolumeData']['dicAlfaBookVolumes'] # словарь с названиями файлов аудио-томов текущей книги с заданным bookAlfaId
        
        # ids аудио-томов из табл 'lib_book_audio_volumes', в порядке. соотвтетсвующем циклу по возвратным данным загруженой медиа-группы
        libAudioVolumesIds = list(dicAlfaBookVolumes.keys()) 
        
        dicBookVolumesTitles = kwargs['libBookVolumeData']['dicBookVolumesTitles'] # словарь с заголовками к аудио-томам (Caption) заданной книги

        # Возвращаемые данные, возвращаемые после загрузки сообщения в канал
        # https://docs.pyrogram.org/api/types/Message#pyrogram.types.Message [attributes of return data !!]
        listRetMssgLoadData = kwargs['listRetMssgLoadData']

        # Время регистрации
        dtStringFormat1, dtStringFormat2, universUnix = FG.get_current_time_format_1_and_2_and_universal_unix()
        calDateRegistration = dtStringFormat2
        unixDateRegistration = universUnix

        # Цикл по списку возвратных данных от загруженных аудио-томов книги при отсылке медиа-группы
        
        for i, retLoadedMessageData in enumerate(listRetMssgLoadData):
        
            # print(f"PR_A947 --> retLoadedMessageData.id = {retLoadedMessageData.id}")
            
            # Соотвтетсвующее id аудио-тома из таблицы 'lib_book_audio_volumes'
            avLibId = libAudioVolumesIds[i] 
            # Соотвтетсвующее название аудио-тома из таблицы 'lib_book_audio_volumes'
            audioVolumeName = dicAlfaBookVolumes[avLibId]
            
            print(f"PR_A948 --> SYS LOG: Цикл i = {i}")
            print(f"PR_A949 --> SYS LOG: Регистрация возвратнх данных после загрузки в ТГ для аудио-тома '{audioVolumeName}' для книги с bookAlfaId = {bookAlfaId}")
            
            # INI
            # Текущая таблица регистрации загрузок сообщений медиа-группы аудио-томов книги. в зависимости от репозитория (ТГ канала) меняется индекс в названии
            # таблицы, так как у каждого ТГ канала свои таблицы регистрации, отдличающиеся индексом в конце названия базы таблицы. индекс = id репозитория в таблице
            # 'lib_repositories'
            tbRepositRegVolumeCurrent = f"{ms.TB_LIB_REPOSIT_AUDIO_VOLUMES_REGISTR_}{repositoryId}"    
            
            
            # id загруженного осообщения в текуещем канале
            messageId = retLoadedMessageData.id
            
            print(f"PR_A950 --> messageId = {messageId}")
            
            
            # id файла в ТГ-канале (string)
            fileId = retLoadedMessageData.audio.file_id
            
            # unique file_id (string)
            fileUniqueId = retLoadedMessageData.audio.file_unique_id
            
            # file_size
            fileSize = retLoadedMessageData.audio.file_size
            
            # Ссылка текущего ТГ канала
            linkOfRepository = self.get_tb_repositories_given_row_full_data_as_dic_blf(repositoryId)['reposit_link']
            # Ссылка на сообщение данного аудио-тома в текущем ТГ канале
            linkOfMssgInReposit = linkOfRepository + '/' + str(messageId)
                
            
            

            # A. Внести все необходимые регистрационные данные загруженного текущего по циклу for аудио-тома в таблицу 'lib_reposit_audio_volumes_registr_1'
            
            sql = f"""
                    INSERT INTO {tbRepositRegVolumeCurrent} 
                    (
                        book_alfa_id,
                        lib_audio_volume_id,
                        repository_id,
                        link_in_repository,
                        reposit_own_message_id,
                        file_name,
                        file_id,
                        file_unique_id,
                        file_size,
                        message_type_id,
                        cal_date_registration,
                        unix_date_registration
                    )
                        
                    VALUES 
                    (
                        {bookAlfaId},
                        {avLibId},
                        {repositoryId},
                        '{linkOfMssgInReposit}',
                        {messageId},
                        '{audioVolumeName}',
                        '{fileId}',
                        '{fileUniqueId}',
                        {fileSize},
                        {messageTypeId},
                        '{calDateRegistration}',
                        {unixDateRegistration}
                    )
            """
            

            try: 
                self.sps.execute_sql_SPS(sql)
                print(f"PR_A940 --> SYS LOG: Зарегестрирована загрузка сообщения типа - АУДИО-ТОМ с libVolumeId =  для книги с  alfaId = {bookAlfaId} в таблице '{tbRepositRegVolumeCurrent}'")
                
            except Exception as err:
                print(f"PR_A938 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
                print(f"PR_A939 --> SYS LOG: ERRORR !!! {err}")


            


        print(f"PR_A946 --> END: register_repository_loaded_book_media_group_audio_volume_message_data_blf()")




    def get_tb_repositories_given_row_full_data_as_dic_blf(self, repositoryId):
        """ 
        Получить полные общие данные по одной записи репозитория по id из таблицы 'lib_repositories' = входному repositoryId
        """
        
        print(f"PR_A931 --> START: get_full_repository_one_record_data()")
        
        # PARS
        dicKeyVal = {
            'id' : repositoryId
        }
        
        dicRepositoryRecordData = self.spps.read_table_given_row_full_data_as_dic_spps (ms.TB_LIB_REPOSITORIES, dicKeyVal)
        
        print(f"PR_A932 --> END: get_full_repository_one_record_data()")

        return dicRepositoryRecordData
    
    
    
    
    
    # def get_sll_tg_type_repositories_ids (self):
    #     """ 
    #     Получить все ids репозиториев из табл 'lib_repositories', которые представляют ТГ-каналы по типу в поле 'repository_type_id'
    #     """
    
    

    
    
    
    
    def obtain_lib_books_and_volumes_given_source_messages_ids_done_blf (self, origSourceId):
        """ 
        Получить общий список ids сообщений, обоих типов Photo и Audio, которые уже выполнили свою роль и на базе их были образованы и зарегестрированы
        книги и их томы в библиотеке LABBA или Lib. Эти сообщения с заданного канала уже не надо скачивать при следующих обращениях на скачивание 
        аудио-книг с заданного ТГ канала. Это первичный и основной механизм отсечения сообщений, которые уже не нужны и выполнили свою роль.
        Дополнительный механизм отсечения - это удаленные , по тем или иным причинам, сущности на базе сообщений в модулях lib
        Еще один механизм отсечения - это отсечение уже скчанных и находящихся сообщений в таблицах tg_proceeded. И четвертый, по умолчанию отсекаются 
        сообщения, типы которых не Photo и Audio (на данный момент. В будущем этот ряд может быть увеличен)
        
        origSourceId - источник сообщений, по которому нужно получить спискок ids реализованных сообщений (в будущем это могут быть не только ТГ-каналы)
        (Тогда под message_id может пониматься любой обьект-сущность в исходном источнике, который несет в себе все данные для создания пудио-книги)
        origSourceId определяется в таблице исходных источников в табл 'lib_orig_sources'
        
        """
        
        print(f"PR_B014 --> START: obtain_lib_books_and_volumes_given_source_messages_ids_done_blf()")

        # 1. Получить список реализованных исходных сообщений с заданного канала по Alpha-книгам изтабл 'lib_books_alfa_ext'
        sql = f"SELECT book_message_id FROM {ms.TB_LIB_BOOKS_ALFA_EXT} WHERE book_orig_source_id = {origSourceId}"
        
        listLibBooksDoneMessagesIds = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if isinstance(listLibBooksDoneMessagesIds, int):
            listLibBooksDoneMessagesIds = []
    
    
        # 2. Получить список реализованных исходных сообщений с заданного канала по аудио-томам книг из табл 'lib_book_audio_volumes'
        sql = f"SELECT volume_message_id FROM {ms.TB_LIB_BOOK_AUDIO_VOLUMES} WHERE source_id = {origSourceId}"
        
        listLibBooksvolumesDoneMessagesIds = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if isinstance(listLibBooksvolumesDoneMessagesIds, int):
            listLibBooksvolumesDoneMessagesIds = []
        
        
        
        
        
        
        
        
        
        
        listLibMessagesIdsDone = listLibBooksDoneMessagesIds + listLibBooksvolumesDoneMessagesIds
        
        print(f"PR_B015 --> END: obtain_lib_books_and_volumes_given_source_messages_ids_done_blf()")
        
        return listLibMessagesIdsDone
        
    
    
    
    
    
    def get_orig_source_tbid_by_tg_channel_id_blf(self, tgChannelId):
        """ 
        Получить табличное id записи в таблице 'lib_orig_sources' по id ТГ-канала
        """
    
        sql = f"SELECT id FROM {ms.TB_LIB_ORIG_SOURCES} WHERE tg_channel_id = {tgChannelId}" 
        
        tbId = self.sps.get_result_from_sql_exec_proc_sps(sql)
    
    
        return tbId[0]
    
    
    
    
    
    def get_all_books_orig_sources_ids_blf (self):
        """ 
        Получить  ids всех исходных источников книг для библиотеки
        RET: list of sources ids
        """
        
        sql = f"SELECT id FROM {ms.TB_LIB_ORIG_SOURCES}"
        
        listOrigSourcesIds = self.sps.get_result_from_sql_exec_proc_sps(sql)
    
        return listOrigSourcesIds
    
    
    
    
    def get_df_all_books_orig_sources_ids_blf (self):
        """ 
        Получить  фрейм всех исходных источников книг для библиотеки
        RET: df of all sources 
        """
        
        sql = f"SELECT * FROM {ms.TB_LIB_ORIG_SOURCES}"
        
        dfOrigSources = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
    
        return dfOrigSources
    
    
    
    
    
    def get_df_all_lib_repositories_data_blf (self):
        """ 
        Получить  ids всех репозиториев библиотеки
        RET: list of  repositories tbids
        """
        
        sql = f"SELECT * FROM {ms.TB_LIB_REPOSITORIES}"
        
        dfOrigSourcesIds = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
    
        return dfOrigSourcesIds
    
    
    
    
    
    
    
    
    
    
    def get_book_complects_description_photo_message_ids_by_orig_source_id_blf(self, origSourceId):
        """ 
        Получить messageIds  описаний книг (типа Photo) из таблицы 'tg_book_complects_ch_01' в разрезе id заданного оригинального источника 
        """
    
        sql = f"SELECT book_msg_id FROM {ms.TB_TG_BOOK_COMPLECTS_CH_01} WHERE channel_id_ref = {origSourceId}"
        
        bookComplectsDescrMessagesIds = self.sps.get_result_from_sql_exec_proc_sps(sql)
    
        return bookComplectsDescrMessagesIds
    
    
    
    
    def get_book_complects_volumes_messages_ids_by_orig_source_id_blf(self, origSourceId):
        """ 
        Получить ids сообщений типа Аудио-томов из таблицы tg_book_complect_volumes_ch_01 от заданного источника origSourceId
        """
    
        sql = f"SELECT volume_msg_id FROM {ms.TB_TG_BOOK_COMPLECT_VOLUMES_CH_01} WHERE channel_id_ref = {origSourceId}"
        
        volumesInBookComplectsMessagesIds = self.sps.get_result_from_sql_exec_proc_sps(sql)
    
        return volumesInBookComplectsMessagesIds
    
    
    
    
    def get_total_messages_ids_of_entities_in_book_comlects_by_orig_source_id_blf(self, origSourceId):
        """ 
        Получить все messagesIds всех типов сущностей, базирующихся на сообщениях из оргинального источника в ТГ
        То есть все messagesIds, сформированных и существующих в таблицах tg_book_complects_ch_01 и tg_book_complect_volumes_ch_01
        """
        
        print(f"PR_B006 --> START: get_total_messages_ids_of_entities_in_book_comlects_by_orig_source_id_blf()")
    
    
        bookComplectsDescrMessagesIds = self.get_book_complects_description_photo_message_ids_by_orig_source_id_blf(origSourceId)
        
        # Если нет результата
        if isinstance(bookComplectsDescrMessagesIds, int):
            bookComplectsDescrMessagesIds = []
        
        
        print(f"PR_B008 --> bookComplectsDescrMessagesIds = {bookComplectsDescrMessagesIds}")
        
        volumesInBookComplectsMessagesIds = self.get_book_complects_volumes_messages_ids_by_orig_source_id_blf(origSourceId)
        
        
        # Если нет результата
        if isinstance(volumesInBookComplectsMessagesIds, int):
            volumesInBookComplectsMessagesIds = []

        print(f"PR_B009 --> volumesInBookComplectsMessagesIds = {volumesInBookComplectsMessagesIds}")
        
        
        totalBookComplectsMessagesIdBySource = bookComplectsDescrMessagesIds + volumesInBookComplectsMessagesIds
        
        
        print(f"PR_B010 --> totalBookComplectsMessagesIdBySource = {totalBookComplectsMessagesIdBySource}")
        

        print(f"PR_B007 --> END: get_total_messages_ids_of_entities_in_book_comlects_by_orig_source_id_blf()")
        
        return totalBookComplectsMessagesIdBySource
    
    
    
    def delete_book_complect_from_db_blf(self, sourceId, bookComplectDescrMessageId):
        """ 
        Удалить книжный комплект из таблиц tg_book_complects_ch_01 и tg_book_complect_volumes_ch_01 по его id источника и id сообщения с 
        родительским описанием книги bookComplectDescrMessageId
        
        """
        
        print(f"PR_A985 --> START: delete_book_complect_from_db_blf()")

        
        # Получить tbid описания книги в книжном комплекте в таблице tg_book_complects_ch_01 по id источника и id исходного сообщения в ТГ источнике
        
        bookComplectDescrTbId = self.get_tbid_of_book_complect_description_entity_by_source_id_and_descr_messgae_id_blf(sourceId, bookComplectDescrMessageId)

        # Удаление аудио-томов книжного комплекта
        
        sql = f"DELETE FROM {ms.TB_TG_BOOK_COMPLECT_VOLUMES_CH_01} WHERE book_complect_id_ref = {bookComplectDescrTbId}"
        
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_A982 --> SYS LOG: удалены аудио-тома книжного комплекта с табличным id = {bookComplectDescrTbId} с id источника = {sourceId}")
            
        except Exception as err:
            print(f"PR_A983 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_A984 --> SYS LOG: ERRORR !!! {err}")


        # удаление записи с описанием книги в книжном комплекте 
        
        sql = f"DELETE FROM {ms.TB_TG_BOOK_COMPLECTS_CH_01} WHERE channel_id_ref = {sourceId} AND book_msg_id = {bookComplectDescrMessageId}"
        
        print(f"PR_A990 --> sql = {sql}")
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_A987 --> SYS LOG: Удалена запись из табл tg_book_complects_ch_01 с id источника = {sourceId} и book_msg_id = {bookComplectDescrMessageId}")
            
        except Exception as err:
            print(f"PR_A988 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_A989 --> SYS LOG: ERRORR !!! {err}")


        print(f"PR_A986 --> END: delete_book_complect_from_db_blf()")

    
    
    
    

    def get_tbid_of_book_complect_description_entity_by_source_id_and_descr_messgae_id_blf (self, sourceId, bookComplectDescrMessageId):
        """
        Получить табличный id записи, которая является описанием книги в книжном комплекте в табл tg_book_complects_ch_01
        bookComplectDescrMessageId - id сообщения описания книги (главного) в книжном комплекте
        sourcrId - исходный источник сообщения
        """



        sql = f"SELECT id FROM {ms.TB_TG_BOOK_COMPLECTS_CH_01} WHERE channel_id_ref = {sourceId} AND book_msg_id = {bookComplectDescrMessageId}"
        
        
        bookComplectDescrTbId = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        
        return bookComplectDescrTbId[0]
    
    
    
    
    
    
    def get_reject_messages_ids_list_for_first_level_blf (self, origSourceId):
        """ 
        Список ОТСЕЧЕНИЯ messagesids НА ПЕРВОМ УРОВНЕ
        Получить общий список messagesIds всех типов, которые уже находятся в сформированных книжных комплектах  +
        + зарегестрированных в библиотеке
        Считывает существующие ids сообщений в друх верхних уровнях: книжных комплектов и книг в библиотеке, вклюячая все типы сообщений,
        участвовавших в создании сущностей каждого уровня
        
        currentSourceId - текущий источник, по которому производится скачивание книго-образующих сообщений
        
        TODO: Потом добавить сюда сообщения из мусорки (удаленных сообщений) и возможно из сообщений в tg_auxilary_messages_proceeded (продумать)
        
        """
        
        print(f"PR_B003 --> START: get_reject_messages_ids_list_for_first_level_blf()")
        
        print(f"PR_B005 --> origSourceId = {origSourceId}")
        
        # 1. Список уже существующих messagesIds всех типлв в книжных комплектах
        totalBookComplectsMessagesIdBySource = self.get_total_messages_ids_of_entities_in_book_comlects_by_orig_source_id_blf(origSourceId)
        
        if isinstance(totalBookComplectsMessagesIdBySource, int):
            totalBookComplectsMessagesIdBySource = []
        
        print(f"PR_B012 --> totalBookComplectsMessagesIdBySource = {totalBookComplectsMessagesIdBySource}")
        
        # 2. Список уже зарегестриованных messagesIds всех типов в библиотеке LABBA
        listLibMessagesIdsDone = self.obtain_lib_books_and_volumes_given_source_messages_ids_done_blf(origSourceId)
        
        if isinstance(listLibMessagesIdsDone, int):
            listLibMessagesIdsDone = []
        
        
        # 3. Списки успешно загруженных сообщений в таблице tg_messages_proceeded
        # PARS
        listGivenStatuses = [1, 4, 7] # Правильные статусы загрузки
        listGivenTypes = [1,2] # Типы - описание с картинкой и аудио-том
        
        listTgMessagesSuccsess = self.tlf.get_tg_procceded_messages_ids_with_given_statuses_types_source_id_tlf (origSourceId, listGivenStatuses, listGivenTypes)
        
        if isinstance(listTgMessagesSuccsess, int):
            listTgMessagesSuccsess = []
            
            
            
        
        # 4. Из таблицы tg_auxilary_messages_proceeded !!! 
        
        
        
        # 5. из урны !!!
        
        
        print(f"PR_B016 --> listTgMessagesSuccsess = {listTgMessagesSuccsess}")
        
        # Общий список существующих и зарегестрированных ids сообщений в верхних двух уровнях: книжные комплекты и в библиотеке зарегестрированных книг
        totalRejectMessagesIdsOfFirstLevel = totalBookComplectsMessagesIdBySource + listLibMessagesIdsDone + listTgMessagesSuccsess
        
        
        print(f"PR_B004 --> END: get_reject_messages_ids_list_for_first_level_blf()")

        
        return totalRejectMessagesIdsOfFirstLevel
        
    
    
    
    
    
    
    def get_reject_messages_ids_list_for_second_level_blf (self, origSourceId):
        """ 
        Список ОТСЕЧЕНИЯ messagesids НА ВТОРОМ УРОВНЕ
        Получить общий список messagesIds всех типов, которые уже находятся в сформированных книжных комплектах  +
        + зарегестрированных в библиотеке
        Считывает существующие ids сообщений в друх верхних уровнях: книжных комплектов и книг в библиотеке, вклюячая все типы сообщений,
        участвовавших в создании сущностей каждого уровня
        
        currentSourceId - текущий источник, по которому производится скачивание книго-образующих сообщений
        
        TODO: Потом добавить сюда сообщения из мусорки (удаленных сообщений) и возможно из сообщений в tg_auxilary_messages_proceeded (продумать)
        
        """
        
        print(f"PR_B036 --> START: get_reject_messages_ids_list_for_first_level_blf()")
        
        print(f"PR_B037 --> origSourceId = {origSourceId}")
        
        # 1. Список уже существующих messagesIds всех типлв в книжных комплектах
        totalBookComplectsMessagesIdBySource = self.get_total_messages_ids_of_entities_in_book_comlects_by_orig_source_id_blf(origSourceId)
        
        if isinstance(totalBookComplectsMessagesIdBySource, int):
            totalBookComplectsMessagesIdBySource = []
        
        print(f"PR_B038 --> totalBookComplectsMessagesIdBySource = {totalBookComplectsMessagesIdBySource}")
        
        # 2. Список уже зарегестриованных messagesIds всех типов в библиотеке LABBA
        listLibMessagesIdsDone = self.obtain_lib_books_and_volumes_given_source_messages_ids_done_blf(origSourceId)
        
        if isinstance(listLibMessagesIdsDone, int):
            listLibMessagesIdsDone = []
        
        
            
        
        # 4. Из таблицы tg_auxilary_messages_proceeded !!! 
        
        
        
        # 5. из урны !!!
        
        
        print(f"PR_B039 --> listTgMessagesSuccsess = {listLibMessagesIdsDone}")
        
        # Общий список существующих и зарегестрированных ids сообщений в верхних двух уровнях: книжные комплекты и в библиотеке зарегестрированных книг
        totalRejectMessagesIdsOfFirstLevel = totalBookComplectsMessagesIdBySource + listLibMessagesIdsDone
        
        print(f"PR_B040 --> END: get_reject_messages_ids_list_for_first_level_blf()")

        
        return totalRejectMessagesIdsOfFirstLevel
        
    
    
    
    
    
    
    
    
    def get_reject_messages_ids_list_for_third_level_blf (self, origSourceId):
        """ 
        Список ОТСЕЧЕНИЯ messagesids НА ТРЕТЬЕМ УРОВНЕ
        Получить общий список messagesIds всех типов, зарегестрированных в библиотеке
        
        Считывает существующие ids сообщений в друх верхних уровнях: книжных комплектов и книг в библиотеке, вклюячая все типы сообщений,
        участвовавших в создании сущностей каждого уровня
        
        currentSourceId - текущий источник, по которому производится скачивание книго-образующих сообщений
        
        TODO: Потом добавить сюда сообщения из мусорки (удаленных сообщений) и возможно из сообщений в tg_auxilary_messages_proceeded (продумать)
        
        """
        
        print(f"PR_B027 --> START: get_reject_messages_ids_list_for_first_level_blf()")

        # 2. Список уже зарегестриованных messagesIds всех типов в библиотеке LABBA
        listLibMessagesIdsDone = self.obtain_lib_books_and_volumes_given_source_messages_ids_done_blf(origSourceId)
        
        if isinstance(listLibMessagesIdsDone, int):
            listLibMessagesIdsDone = []


        print(f"PR_B028 --> listLibMessagesIdsDone = {listLibMessagesIdsDone}")
        

        # 3. Отсечение для регистрации тех книг, в которых находятс книги или аудио-тома с напрвильным статусом, свидетельствующим о том, Что сообщение было
        # скачано либо не до конца, либо с ошибко, либо еще что другое
        # Список книг и аудио-томов, которые были скачаны неправильно (с ошибкой или недогруз, пр)
        # wrongStatuses = [2, 3, 5, 6, 8]
        wrongStatuses = [2, 5]
        
        bookDescrMessageType = 1
        
        listWrongBookDescrMessagesIds = self.obtain_book_descr_ids_with_given_statuses_in_tg_procceeded_blf ( origSourceId, bookDescrMessageType, wrongStatuses)
        
        if isinstance(listWrongBookDescrMessagesIds, int):
            listWrongBookDescrMessagesIds = []
        

        print(f"PR_B049 --> PR_B048 -->  listWrongBookDescrMessagesIds = {listWrongBookDescrMessagesIds}")

        # 3b. Получить все ids описаний книг в книжных комплектах в табл 'tg_book_complects_ch_01', у которых в каком-либо аудио-томах присутствует
        # том с неправильным статустом в таблице 'tg_messages_proceeded' из подмножества wrongStatuses = [2, 3, 5, 6, 8]
        listBookDescrIdsWhereEvenOneVolumeFasWrongStatus = self.obtain_all_book_complects_descr_ids_where_volumes_statuses_in_given_list_by_source_id_blf (origSourceId, wrongStatuses)

        if isinstance(listBookDescrIdsWhereEvenOneVolumeFasWrongStatus, int):
            listBookDescrIdsWhereEvenOneVolumeFasWrongStatus = []

        print(f"PR_B050 --> listBookDescrIdsWhereEvenOneVolumeFasWrongStatus = {listBookDescrIdsWhereEvenOneVolumeFasWrongStatus}")
        
        # # Общий список существующих и зарегестрированных ids сообщений в верхних двух уровнях: книжные комплекты и в библиотеке зарегестрированных книг
        # totalRejectMessagesIdsForThirdLevel = listLibMessagesIdsDone + listWrongBookDescrMessagesIds + listBookDescrIdsWhereEvenOneVolumeFasWrongStatus
        
        
        print(f"PR_B029 --> END: get_reject_messages_ids_list_for_first_level_blf()")

        
        return listLibMessagesIdsDone, listWrongBookDescrMessagesIds, listBookDescrIdsWhereEvenOneVolumeFasWrongStatus
        
    
    
    
    
    
    
    
    
    
    def get_remove_messages_ids_list_for_first_and_second_level_blf (self, origSourceId):
        """ 
        OBSOLETED: Использовать remove_all_registered_messages_from_tg_procceeded_blf()
        Список ОЧИСТКИ  messagesIds НА ПЕРВОМ УРОВНЕ
        Получить общий список messagesIds всех типов, которые уже находятся в сформированных книжных комплектах  +
        + зарегестрированных в библиотеке
        Считывает существующие ids сообщений в друх верхних уровнях: книжных комплектов и книг в библиотеке, вклюячая все типы сообщений,
        участвовавших в создании сущностей каждого уровня
        
        currentSourceId - текущий источник, по которому производится скачивание книго-образующих сообщений
        
        TODO: Потом добавить сюда сообщения из мусорки (удаленных сообщений) и возможно из сообщений в tg_auxilary_messages_proceeded (продумать)
        
        """
        
        print(f"PR_B018 --> START: get_reject_messages_ids_list_for_first_level_blf()")
        
        print(f"PR_B017 --> origSourceId = {origSourceId}")
        
        
        # !!! Нельзя удалять сообщения в tg_procceeded на базе реализованных комплектов, так как при регистрации система берет данные из ьаблиц tg_proceeded
        # # 1. Список уже существующих messagesIds всех типлв в книжных комплектах
        # totalBookComplectsMessagesIdBySource = self.get_total_messages_ids_of_entities_in_book_comlects_by_orig_source_id_blf(origSourceId)
        
        # if isinstance(totalBookComplectsMessagesIdBySource, int):
        #     totalBookComplectsMessagesIdBySource = []
        
        # print(f"PR_B020 --> totalBookComplectsMessagesIdBySource = {totalBookComplectsMessagesIdBySource}")
        
        
        # 2. Список уже зарегестриованных messagesIds всех типов в библиотеке LABBA
        listLibMessagesIdsDone = self.obtain_lib_books_and_volumes_given_source_messages_ids_done_blf(origSourceId)
        
        if isinstance(listLibMessagesIdsDone, int):
            listLibMessagesIdsDone = []
        
        
        
        # # 4. Из таблицы tg_auxilary_messages_proceeded
        
        
        # # 5. из урны
        
        
        # print(f"PR_B016 --> listTgMessagesSuccsess = {listTgMessagesSuccsess}")
        
        # Общий список существующих и зарегестрированных ids сообщений в верхних двух уровнях: книжные комплекты и в библиотеке зарегестрированных книг
        totalRemoveMessagesIdsOfFirstLevel = listLibMessagesIdsDone
        
        
        print(f"PR_B019 --> END: get_reject_messages_ids_list_for_first_level_blf()")

        
        return totalRemoveMessagesIdsOfFirstLevel
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    def clear_table_from_given_messages_ids_by_source_id_blf (self, tb, origSourceId, listCRemoveMessagesIds, listKeysNames):
        """ 
        Очистить таблицу от сообщений в заданном списке по ключу: origSourceId + tgMessagesId
        listCRemoveMessagesIds - список сообщений, Которые надо удалить в купе с ключем по источнику origSourceId из таблицы
        listKeysNames - список названий ключевых полей в последовательности [origSourceId, tgMessageId]
        origSourceId - текущий источник сообщений
        
        """
        
        print(f"START: clear_table_from_given_messages_ids_by_source_id_blf()")
        
        # INI
        fieldForOrigSource = listKeysNames[0]
        fieldNameForMessageId = listKeysNames[1]
        
        listCRemoveMessagesIdsSql = f"{listCRemoveMessagesIds}".replace('[','').replace(']','')
    
        sql = f"DELETE FROM {tb} WHERE {fieldForOrigSource} = {origSourceId} AND {fieldNameForMessageId} IN ({listCRemoveMessagesIdsSql})"
    

    
        print(f"PR_A992 --> sql = {sql}")
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_A993 --> SYS LOG: В таблице {tb} удалены записи по ключам {fieldForOrigSource} = {origSourceId} и {fieldNameForMessageId} находящимся в множестве {listCRemoveMessagesIds}")
            
        except Exception as err:
            print(f"PR_A994 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_A995 --> SYS LOG: ERRORR !!! {err}")


        print(f"START: clear_table_from_given_messages_ids_by_source_id_blf()")

    
    
    
    def reject_proccessing_if_in_reject_messages_ids_list_blf (self, messageId, listRejectMessagesIdsBySource, flagLoadImgAnyway = False):
        """ 
        Отсечь от дальнейшей обработки то сообщение, которое подпадает под множество listRejectMessagesIds и имеет источник = origSourceId
        messageId - текущее messageId от источника с id = origSourceId
        listRejectMessagesIdsBySource - список messagesIds, попадая в подмножество которых текущее сообщение messageId должно быть 
        отсечено от дальнейшей обработки. Список подготовлен в разрезе sourceId текущего сообщения messageId
        
        
        RET: True or False (отсечь или пропустить)
        """
        
        if (
            
            # 1. ОТСЕЧЕНИЕ НА УРОВНЕ ПЕРВИНОГО СКАЧИВАНИЯ СООБЩЕНИЙ И АНАЛИЗА УЖЕ СУЩЕСТВУЮЩИХ СООБЩЕНИЙ В таблицах tg_proceeded_...
            messageId in listRejectMessagesIdsBySource
            and not flagLoadImgAnyway # Флаг скачивания картинок, несмотря на то, что система обнаруживает, что сообщение с картинкой и описанием уже было обработано
            ): # списки ID считанных в БД простых и декларративных сообщений
            
            print(f"PR_A997 --> SYS LOG: Сообщение с id = {messageId} подпадает под отсечение, так как входит в общий список отсечения \n{listRejectMessagesIdsBySource}")
            
            ret = True
            
        # Если  messageId не входит в список  listGeneralMessageRejection и флаг  flagLoadImgAnyway = True (то есть флаг говорит, что не важно все, 
        # пропустить messageId на дальнейшую обработку)
        else:
            
            print(f"PR_A998 --> SYS LOG: Сообщение с id = {messageId} НЕ подпадает под отсечение, так как НЕ входит в общий список отсечения \n{listRejectMessagesIdsBySource} и флаг flagLoadImgAnyway = {flagLoadImgAnyway} не принуждает пропустить сообщение для дальнейшей обработки")

            
            ret = False


        return ret
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def obtain_all_book_complects_descr_ids_where_volumes_statuses_in_given_list_by_source_id_blf (self, origSourceId, listVolumesStatuses, inOperand = 'IN')->list:
        """ 
        Получить все ids описаний книг в книжных комплектах в табл 'tg_book_complects_ch_01', тома статусы которых в таблице 'tg_messages_proceeded' 
        входят или не входят в множество по списку listVolumesStatuses  
        
        inOperand - операнд в sql - запросе, который можно инвертировать. Возможные значения: 'IN' и 'NOT IN'. По усолчанию: 'IN'
        origSourceId - id текущего источника ТГ канала
        """
        
        print(f"PR_B041 --> START: obtain_all_book_complects_with_wrong_statuses_volume_by_source_id_blf()")
        

        # перевод целочисленных элементов списка статусов в стриноговые элементы
        listVolumesStatuses = [str(x) for x in listVolumesStatuses]
        # Создание sql-формата для списка
        listVolumesStatusesSql = ",".join(listVolumesStatuses)
        
        sql = f"""
                    SELECT tgc.book_msg_id FROM 
                        {ms.TB_TG_BOOK_COMPLECT_VOLUMES_CH_01} as tgcv
                        LEFT JOIN {ms.TB_TG_BOOK_COMPLECTS_CH_01} as tgc
                            ON tgcv.book_complect_id_ref = tgc.id
                        LEFT JOIN {ms.TB_MSSGS_PROCEEDED_} as mp
                            ON tgcv.volume_msg_id = mp.message_own_id 
                        WHERE 
                            tgcv.channel_id_ref = {origSourceId}   AND 
                            mp.message_proc_status_ref_id {inOperand} ({listVolumesStatusesSql})
                        GROUP BY tgc.book_msg_id
        """
        
        print(f"PR_B044 --> sql = {sql}")
        
        
        listBookDescrIds = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
            
        print(f"PR_B042 --> END: obtain_all_book_complects_with_wrong_statuses_volume_by_source_id_blf()")
        
        return listBookDescrIds

    
    
    
    
    def obtain_book_descr_ids_with_given_statuses_in_tg_procceeded_blf (self, origSourceId, bookDescrMessageType, listBookDescrStatuses, inOperand = 'IN'):
        """ 
        Поулчить ids описаний книг в тпблице 'tg_messages_proceeded' , которы подпадают или не подпадают в подмножество списка заданных статусов
        listBookDexzcrStatuses - задаваемое подмножество статусов в виде списка
        inOperand - операнд в sql - запросе, который можно инвертировать. Возможные значения: 'IN' и 'NOT IN'. По усолчанию: 'IN'
        origSourceId - id текущего источника ТГ канала
        bookDescrMessageType -  тип для сообщения с описанием книги из табл 'tg_message_types'
        """
    
        print(f"PR_B045 --> START: obtain_book_descr_ids_with_given_statuses_in_tg_procceeded_blf()")
        
        # # INI
        # # id типа сообщения, который определяет описание книги с названием 'TEXT_WITH_IMAGE_MSSG_' в табл 'tg_message_types'
        # bookDescrMessageType = 1


        # перевод целочисленных элементов списка статусов в стриноговые элементы
        listBookDescrStatuses = [str(x) for x in listBookDescrStatuses]
        # Создание sql-формата для списка
        listlistBookDescrStatusesSql = ",".join(listBookDescrStatuses)


        sql = f""" 
                    SELECT message_own_id FROM {ms.TB_MSSGS_PROCEEDED_} 
                    WHERE 
                    channels_ref_id = {origSourceId} AND 
                    message_type_ref_id = {bookDescrMessageType} AND 
                    message_proc_status_ref_id {inOperand} ({listlistBookDescrStatusesSql})
        """
    
    
        print(f"PR_B047 --> sql = {sql}")
        
        
        listBookDescrIds = self.sps.get_result_from_sql_exec_proc_sps(sql)


    
        print(f"PR_B046 --> END: obtain_book_descr_ids_with_given_statuses_in_tg_procceeded_blf()")

    
        return listBookDescrIds
    
    
    
    
    
    
    
    
    def remove_prime_tg_messages_material_and_book_complects_after_book_registration_in_toto_blf (self):
        """ 
        Удалить весь в целом первичный материал в виде сообщений -книгах и сообщений-аудио томов из tg_tables, а так же книжные комплекты, которые выполнили свою роль и
        книга с томами полноценно создана и зарегестрирована в библиотек LIB, сварвынив все зарегестрированные message_ids в таблиах 
        Использует подход сообщений-обьектов. Удаляет так же все зарегестрированные групповые картинки-сообщения
        """

        print(f"PR_B070 --> START: remove_prime_tg_messages_material_after_book_registration_in_toto_blf()")

        # A. Удалить все сообщения из табл 'tg_messages_proceeded' и 'tg_message_proceeded_ext', коотрые явились образующими для всех зарегестрированных 
        # книг и аудио-томов в списке listTotalRegisteredIdsOfBooksAndVolumes
        # 
        
        self.remove_all_registered_messages_from_tg_procceeded_blf()
            
        print(f"PR_B070 --> POINT A")
            
            
        
        # B. Удалить все книжные комплекты зарегестрированных в библиотеке  LIB книжных сущностей (книг и томов), которые уже отыграли свою роль и больше 
        # не нужны
        self.remove_book_complects_for_lib_reistered_books_blf()
        
        
        print(f"PR_B071 --> END: remove_prime_tg_messages_material_after_book_registration_in_toto_blf()")

            


    def remove_book_complects_for_all_registered_books_and_volumes_blf (self):
        """ 
        OBSOLETED:  Некорректное удаление по неполному составному ключу: remove_book_complects_for_all_registered_books_and_volumes_mssg_objs_based_blf()
        Удалить все книжные комплекты для зарегестрированных книг. Они выполнили свою задачу и больше не нужны
        """
        
        # Список всех ids сообщений всех зарегестрированных в библиотеке  LIB сущностей (книги, тома) 
        listTotalRegisteredIdsOfBooksAndVolumes = self.get_total_registered_messages_ids_of_books_and_volumes()

        
        listTotalRegisteredIdsOfBooksAndVolumes = [str(x) for x in listTotalRegisteredIdsOfBooksAndVolumes]
        
        listTotalRegisteredIdsOfBooksAndVolumesSql = ",".join(listTotalRegisteredIdsOfBooksAndVolumes)
        
        
        
        # сначала подчиненная таблица
        sql = f"DELETE FROM {ms.TB_TG_BOOK_COMPLECT_VOLUMES_CH_01} WHERE volume_msg_id IN ({listTotalRegisteredIdsOfBooksAndVolumesSql})"


        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B062 --> SYS LOG: Из табл 'tg_book_complect_volumes_ch_01' удалены все аудио-тома для сообщений зарегестрированных книг")
            
        except Exception as err:
            print(f"PR_B063 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B064 --> SYS LOG: ERRORR !!! {err}")
            
        # Главная таблица
        sql = f"DELETE FROM {ms.TB_TG_BOOK_COMPLECTS_CH_01} WHERE book_msg_id IN ({listTotalRegisteredIdsOfBooksAndVolumesSql})"


        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B065 --> SYS LOG: Из табл 'tg_book_complects_ch_01' удалены все описания книг для сообщений зарегестрированных книг")
            
        except Exception as err:
            print(f"PR_B066 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B067 --> SYS LOG: ERRORR !!! {err}")
            





    def remove_book_complects_for_all_registered_books_and_volumes_mssg_objs_based_blf (self):
        """ 
        OBSOLETED: Use remove_book_complects_for_lib_reistered_books_blf()
        NEW:  29-03-2024
        Удалить все книжные комплекты для зарегестрированных книг. Они выполнили свою задачу и больше не нужны, базируясь 
        на новом подходе с осбектами-сообщениями. содержащих в себе уникальный относитьельный составной ключ пару:
        """
        
        # Список всех ids сообщений всех зарегестрированных в библиотеке  LIB сущностей (книги, тома) 
        listTotalRegisteredIdsOfBooksAndVolumesObjs = self.get_total_registered_books_and_volumes_messages_objects_of_all_sources()
        
        
        print(f"PR_B170 --> listTotalRegisteredBooksAndVolumesMessagesObjs = {listTotalRegisteredIdsOfBooksAndVolumesObjs}")

        # A. Удаление из табл 'tg_message_proceeded_ext' (сначала удаляем из подчиненной табл) по всем источникам последовательно через цикл по источникам
        
        allSourcesIds = self.get_all_books_orig_sources_ids_blf()
        
        for sourceId in allSourcesIds:
        
        
            # Добыть список listMessagesIdsFordeleteBySourceId из списка обьектов listTotalRegisteredBooksAndVolumesMessagesObjs по атрибуту x.messageId
            listMessagesIdsForDeleteBySourceId = [int(x.messageId) for x in listTotalRegisteredIdsOfBooksAndVolumesObjs] 
            
            # Получить sql-вставку для IN
            listTotalRegisteredTbidsForDeleteSql = self.sps.transform_list_valuews_to_sql_string_for_tuple_inside_sps(listMessagesIdsForDeleteBySourceId)
            
        
            
            # сначала подчиненная таблица
            sql = f"DELETE FROM {ms.TB_TG_BOOK_COMPLECT_VOLUMES_CH_01} WHERE volume_msg_id IN ({listTotalRegisteredTbidsForDeleteSql}) AND channel_id_ref = {sourceId}"


            try: 
                self.sps.execute_sql_SPS(sql)
                print(f"PR_B164 --> SYS LOG: Из табл 'tg_book_complect_volumes_ch_01' удалены все аудио-тома для сообщений зарегестрированных книг")
                
            except Exception as err:
                print(f"PR_B165 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
                print(f"PR_B166 --> SYS LOG: ERRORR !!! {err}")
                
            # Главная таблица
            sql = f"DELETE FROM {ms.TB_TG_BOOK_COMPLECTS_CH_01} WHERE book_msg_id IN ({listTotalRegisteredTbidsForDeleteSql}) AND channel_id_ref = {sourceId}"


            try: 
                self.sps.execute_sql_SPS(sql)
                print(f"PR_B167 --> SYS LOG: Из табл 'tg_book_complects_ch_01' удалены все описания книг для сообщений зарегестрированных книг")
                
            except Exception as err:
                print(f"PR_B168 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
                print(f"PR_B169 --> SYS LOG: ERRORR !!! {err}")
                













    def remove_all_tg_messages_in_tbs_procceeded_of_registered_in_lib_books_blf (self):
        """ 
        OBSOLETED:  Некорректное удаление по неполному составному ключу : use remove_all_tg_messages_in_tbs_procceeded_already_registered_in_lib_books_blf()
        Удалить все соообщения из таблиц 'tg_messages_proceeded' и 'tg_message_proceeded_ext' зарегестрированных книг
        Это - первичный материал, который уже выполнил свою книго-образующую задачу
        """

        # Список всех ids сообщений зарегестрированных книг в библиотеке
        listTotalRegisteredIdsOfBooksAndVolumes = self.get_total_registered_messages_ids_of_books_and_volumes()
        
        listTotalRegisteredIdsOfBooksAndVolumes = [str(x) for x in listTotalRegisteredIdsOfBooksAndVolumes]

        listTotalRegisteredIdsOfBooksAndVolumesSql = ",".join(listTotalRegisteredIdsOfBooksAndVolumes)
        
        
        
        

        sql = f"""
                DELETE FROM {ms.TB_MSSGS_PROCEEDED_EXT_} WHERE message_proceeded_ref_id IN 
                ( SELECT id FROM {ms.TB_MSSGS_PROCEEDED_}
                WHERE message_own_id IN ({listTotalRegisteredIdsOfBooksAndVolumesSql}) )
                """
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B059 --> SYS LOG: Из табл 'tg_messages_proceeded_ext' удалены все расширения для сообщений зарегестрированных книг")
            
        except Exception as err:
            print(f"PR_B060 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B061 --> SYS LOG: ERRORR !!! {err}")
            


        # 1. Удалить все сообщения из табл 'tg_messages_proceeded', коотрые явились образующими для всех зарегестрированных книг и аудио-томов 
        # в списке listTotalRegisteredIdsOfBooksAndVolumes
        sql = f"DELETE FROM {ms.TB_MSSGS_PROCEEDED_} WHERE message_own_id IN ({listTotalRegisteredIdsOfBooksAndVolumesSql})"
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B056 --> SYS LOG: Из табл 'tg_messages_proceeded' удалены все сообщения зарегестрированных книг")
            
        except Exception as err:
            print(f"PR_B057 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B058 --> SYS LOG: ERRORR !!! {err}")
            
            




    def remove_all_tg_messages_in_tbs_procceeded_already_registered_in_lib_books_blf (self):
        """ 
        OBSOLETED: Ненужная сложность с обьектами и с циклами. USE: remove_all_registered_messages_from_tg_procceeded_blf()
        NEW:  28-03-2024
        Удалить все соообщения из таблиц 'tg_messages_proceeded' и 'tg_message_proceeded_ext' зарегестрированных книг
        Это - первичный материал, который уже выполнил свою книго-образующую задачу
        """
        
        print(f"PR_B141 --> START: remove_all_tg_messages_in_tbs_procceeded_already_registered_in_lib_books_blf()")

        # Список всех ids сообщений зарегестрированных книг в библиотеке
        listTotalRegisteredBooksAndVolumesMessagesObjs = self.get_total_registered_books_and_volumes_messages_objects_of_all_sources()
        
        # listTotalRegisteredIdsOfBooksAndVolumes = [str(x) for x in listTotalRegisteredIdsOfBooksAndVolumes]

        # listTotalRegisteredIdsOfBooksAndVolumesSql = ",".join(listTotalRegisteredIdsOfBooksAndVolumes)
        print(f"PR_B163 --> listTotalRegisteredBooksAndVolumesMessagesObjs = {listTotalRegisteredBooksAndVolumesMessagesObjs}")

        # A. Удаление из табл 'tg_message_proceeded_ext' (сначала удаляем из подчиненной табл) по всем источникам последовательно через уикл по источникам
        
        allSourcesIds = self.get_all_books_orig_sources_ids_blf()
        
        
        
        for sourceId in allSourcesIds:
            
            
            print(f"PR_B152 --> listTotalRegisteredBooksAndVolumesMessagesObjs = {listTotalRegisteredBooksAndVolumesMessagesObjs}")
            
            # print(f"PR_B153 --> object attr val = {listTotalRegisteredBooksAndVolumesMessagesObjs[4].messageId}")
            
            # Получить список ids всех зарегестрированных сообщений для книг и аудио-томоы. прошедших регистрацию в 
            # фильтре по текущему в цикле id источника и взятых из полного списка книг и томов 
            # сообщений -обьектов из listTotalRegisteredIdsOfBooksAndVolumes
            
            
            
            # Создать список listMessagesIdsFordeleteBySourceId из списка обьектов listTotalRegisteredBooksAndVolumesMessagesObjs
            listMessagesIdsFordeleteBySourceId = [int(x.messageId) for x in listTotalRegisteredBooksAndVolumesMessagesObjs] 

            # listMessagesIdsFordeleteBySourceId = []
            
            # for obj in listTotalRegisteredBooksAndVolumesMessagesObjs:
                
            #     print(f"PR_B155 --> obj.messageId = {obj.messageId}")
                
            #     listMessagesIdsFordeleteBySourceId.append(obj.messageId)
            
            
            
            # Переводим цифры в стринги
            listMessagesIdsFordeleteBySourceId = [str(x) for x in listMessagesIdsFordeleteBySourceId]
            listMessagesIdsFordeleteBySourceIdSql = ",".join(listMessagesIdsFordeleteBySourceId)
            
            
            print(f"PR_B154 --> listMessagesIdsFordeleteBySourceIdSql = {listMessagesIdsFordeleteBySourceIdSql}")
            
            
        

            sql = f"""
                    DELETE FROM {ms.TB_MSSGS_PROCEEDED_EXT_} WHERE message_proceeded_ref_id IN 
                    ( SELECT id FROM {ms.TB_MSSGS_PROCEEDED_}
                    WHERE message_own_id IN ({listMessagesIdsFordeleteBySourceIdSql}) AND channels_ref_id = {sourceId} )
                    """
            
            try: 
                self.sps.execute_sql_SPS(sql)
                print(f"PR_B134 --> SYS LOG: Из табл 'tg_messages_proceeded_ext' удалены все расширения для сообщений зарегестрированных книг")
                
            except Exception as err:
                print(f"PR_B135 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
                print(f"PR_B136 --> SYS LOG: ERRORR !!! {err}")
                


            # B. Удалить все сообщения из табл 'tg_messages_proceeded', коотрые явились образующими для всех зарегестрированных книг и аудио-томов 
            # в списке listTotalRegisteredIdsOfBooksAndVolumes
            sql = f"DELETE FROM {ms.TB_MSSGS_PROCEEDED_} WHERE message_own_id IN ({listMessagesIdsFordeleteBySourceIdSql}) AND channels_ref_id = {sourceId}"
            
            try: 
                self.sps.execute_sql_SPS(sql)
                print(f"PR_B137 --> SYS LOG: Из табл 'tg_messages_proceeded' удалены все сообщения зарегестрированных книг")
                
            except Exception as err:
                print(f"PR_B138 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
                print(f"PR_B139 --> SYS LOG: ERRORR !!! {err}")
                
                
        print(f"PR_B142 --> END: remove_all_tg_messages_in_tbs_procceeded_already_registered_in_lib_books_blf()")






    def remove_all_registered_messages_from_tg_procceeded_blf (self):
        """ 
        NEW:  29-03-2024
        Удалить все соообщения из таблиц 'tg_messages_proceeded' и 'tg_message_proceeded_ext' зарегестрированных книг
        Это - первичный материал, который уже выполнил свою книго-образующую задачу
        """
        
        print(f"PR_B185 --> START: remove_all_registered_messages_from_tg_procceeded_blf()")

        # # Список уже зарегестрированных в LIB сообщений с их идентификатором tbid в главной таблице скачанных сообщений 'tg_messages_proceeded'
        # # ПРИМ: зарегестрированные сообщения из таблиц 1. lib_books_alfa_ext, 2. lib_book_audio_volumes, 3. lib_book_images
        listReisteredMessagesTbids = self.obtain_lib_registered_messages_with_tg_procceeded_tbids_blf(retSwitch = '_TBIDS_')
        
        print(f"PR_B178 --> listReisteredMessagesTbids = {listReisteredMessagesTbids}")
        
        # SQLирование списка
        listReisteredMessagesTbidsSql = self.sps.transform_list_valuews_to_sql_string_for_tuple_inside_sps(listReisteredMessagesTbids)
        
        # Удалить зарегестрированные сообщения из подчиненной табл 'tg_message_proceeded_ext'
        sql = f"DELETE FROM {ms.TB_MSSGS_PROCEEDED_EXT_} WHERE message_proceeded_ref_id IN ({listReisteredMessagesTbidsSql})"
                
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B179 --> SYS LOG: Из табл 'tg_messages_proceeded_ext' удалены все расширения для сообщений зарегестрированных книг")
            
        except Exception as err:
            print(f"PR_B180 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B181 --> SYS LOG: ERRORR !!! {err}")
            


        # B. Удалить все сообщения из табл 'tg_messages_proceeded', коотрые явились образующими для всех зарегестрированных книг и аудио-томов 
        # в списке listTotalRegisteredIdsOfBooksAndVolumes
        sql = f"DELETE FROM {ms.TB_MSSGS_PROCEEDED_} WHERE id IN ({listReisteredMessagesTbidsSql})"
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B182 --> SYS LOG: Из табл 'tg_messages_proceeded' удалены все сообщения зарегестрированных книг")
            
        except Exception as err:
            print(f"PR_B183 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B184 --> SYS LOG: ERRORR !!! {err}")


        print(f"PR_B186 --> END: remove_all_registered_messages_from_tg_procceeded_blf()")





    def obtain_lib_registered_messages_with_tg_procceeded_tbids_blf (self, retSwitch = '_TBIDS_'):
        """ 
        NEW:  29-03-2024
        Список уже зарегестрированных в LIB сообщений с их идентификатором tbid в главной таблице скачанных сообщений 'tg_messages_proceeded'
        ПРИМ: зарегестрированные сообщения из таблиц 1. lib_books_alfa_ext, 2. lib_book_audio_volumes, 3. lib_book_images
        retSwitch - переключатель, который указывает в каком виде возвращать результат. По умолчанию -  '_TBIDS_', и выводится список 
        tbids сообщений из таблицы 'tg_messages_proceeded'. Если задается  '_OBJECTS_' -  то возвращается список обьектов класса LibUniqueMessage
        Если '_FULL_LIST_' - nто возвращается списки в списке всех значений

        """


        # При обьединении результатов идентичные результаты приводятся к одному результату (и нам не нужны множественные одинаковые значения)
        # ПРИМ: названия столбцов определяются первой таблицей
        # ПРИМ: Порядок полей в запросе ВАЖЕН!!! так как потом из них создаются обьекты (то есть интерфейс должен быть соблюден для обьектов 
        # класса LibUniqueMessage в конструкторе)
        sql = f"""
					SELECT book_orig_source_id, book_message_id, mpe.message_proceeded_ref_id FROM {ms.TB_LIB_BOOKS_ALFA_EXT} AS lbae, {ms.TB_MSSGS_PROCEEDED_EXT_} as mpe
					WHERE lbae.serial_id = mpe.channels_ref_id_ext AND lbae.book_message_id = mpe.message_own_id_ext
						UNION 
					SELECT source_id, volume_message_id, mpe.message_proceeded_ref_id FROM {ms.TB_LIB_BOOK_AUDIO_VOLUMES} AS lbav, {ms.TB_MSSGS_PROCEEDED_EXT_} as mpe
					WHERE lbav.source_id = mpe.channels_ref_id_ext AND lbav.volume_message_id = mpe.message_own_id_ext
						UNION
					SELECT orig_source_id, tg_message_id, mpe.message_proceeded_ref_id FROM {ms.TB_LIB_BOOK_IMAGES} as lbi, {ms.TB_MSSGS_PROCEEDED_EXT_} as mpe
					WHERE lbi.orig_source_id = mpe.channels_ref_id_ext AND lbi.tg_message_id = mpe.message_own_id_ext
        """

        # Список уже зарегестрированных в LIB сообщений с их идентификатором tbid в главной таблице скачанных сообщений 'tg_messages_proceeded'
        # ПРИМ: зарегестрированные сообщения из таблиц 1. lib_books_alfa_ext, 2. lib_book_audio_volumes, 3. lib_book_images

        listReisteredMessagesFull = self.sps.get_result_from_sql_exec_proc_sps(sql)



        
        # переключение типа возврата
        for case in Switch(retSwitch):
            if case('_TBIDS_'): 
                if not isinstance(listReisteredMessagesFull, int):
                # Трансформировать в список чисто tbids сообщений
                    listReisteredMessagesTbids = [x[2] for x in listReisteredMessagesFull]
                else:
                    listReisteredMessagesTbids = []
                
                return listReisteredMessagesTbids
                break

            if case('_OBJECTS_'): 
                if not isinstance(listReisteredMessagesFull, int):
                # Трансформировать в список обьектов класса LibUniqueMessage
                    listReisteredMessagesObjs = [LibUniqueMessage(x) for x in listReisteredMessagesFull]
                else:
                    listReisteredMessagesObjs = []
                
                return listReisteredMessagesObjs
                break
            
            # возвращается списки в списке всех значений
            if case('_FULL_LIST_'): 
                if not isinstance(listReisteredMessagesFull, int):
                    return listReisteredMessagesFull
                else:
                    return []
                break

            if case(): # default
                print('Другое число')
                break
        




    def remove_book_complects_for_lib_reistered_books_blf (self):
        """ 
        NEW:  29-03-2024
        Удалить  книжные комплекты  изтаблиц 'tg_book_complects_ch_01' и 'tg_book_complect_volumes_ch_01' зарегестрированных книг
        Это - первичный материал, который уже выполнил свою книго-образующую задачу
        """
        
        print(f"PR_B188 --> START: remove_all_registered_messages_from_tg_procceeded_blf()")

        # # Список уже зарегестрированных в LIB сообщений с их идентификатором tbid в главной таблице скачанных сообщений 'tg_messages_proceeded'
        # # ПРИМ: зарегестрированные сообщения из таблиц 1. lib_books_alfa_ext, 2. lib_book_audio_volumes, 3. lib_book_images
        listRegisteredMessagesTbids = self.obtain_lib_registered_messages_with_tg_book_complects_tbids_blf(retSwitch = '_TBIDS_')
        
        print(f"PR_B189 --> listReisteredMessagesTbids = {listRegisteredMessagesTbids}")
        
        # SQLирование списка
        listRegisteredMessagesTbidsSql = self.sps.transform_list_valuews_to_sql_string_for_tuple_inside_sps(listRegisteredMessagesTbids)
        
        # Удалить зарегестрированные сообщения из подчиненной табл 'tg_message_proceeded_ext'
        sql = f"DELETE FROM {ms.TB_TG_BOOK_COMPLECT_VOLUMES_CH_01} WHERE book_complect_id_ref IN ({listRegisteredMessagesTbidsSql})"
                
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B190 --> SYS LOG: Из табл 'tg_messages_proceeded_ext' удалены все расширения для сообщений зарегестрированных книг")
            
        except Exception as err:
            print(f"PR_B191 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B192 --> SYS LOG: ERRORR !!! {err}")
            


        # B. Удалить все сообщения из табл 'tg_messages_proceeded', коотрые явились образующими для всех зарегестрированных книг и аудио-томов 
        # в списке listTotalRegisteredIdsOfBooksAndVolumes
        sql = f"DELETE FROM {ms.TB_TG_BOOK_COMPLECTS_CH_01} WHERE id IN ({listRegisteredMessagesTbidsSql})"
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B193 --> SYS LOG: Из табл 'tg_messages_proceeded' удалены все сообщения зарегестрированных книг")
            
        except Exception as err:
            print(f"PR_B194 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B195 --> SYS LOG: ERRORR !!! {err}")


        print(f"PR_B196 --> END: remove_all_registered_messages_from_tg_procceeded_blf()")











    def obtain_lib_registered_messages_with_tg_book_complects_tbids_blf (self, retSwitch = '_TBIDS_'):
        """ 
        NEW:  29-03-2024
        Список уже зарегестрированных в LIB сообщений с их идентификатором tbid в главной таблице скачанных сообщений 'tg_book_complects_ch_01'
        ПРИМ: зарегестрированные сообщения из таблиц 1. lib_books_alfa_ext, 2. lib_book_audio_volumes, 3. lib_book_images
        retSwitch - переключатель, который указывает в каком виде возвращать результат. По умолчанию -  '_TBIDS_', и выводится список 
        tbids сообщений из таблицы 'tg_messages_proceeded'. Если задается  '_OBJECTS_' -  то возвращается список обьектов класса LibUniqueMessage
        Если '_FULL_LIST_' - nто возвращается списки в списке всех значений

        """


        # При обьединении результатов идентичные результаты приводятся к одному результату (и нам не нужны множественные одинаковые значения)
        # ПРИМ: названия столбцов определяются первой таблицей
        # ПРИМ: Порядок полей в запросе ВАЖЕН!!! так как потом из них создаются обьекты (то есть интерфейс должен быть соблюден для обьектов 
        # класса LibUniqueMessage в конструкторе)
        sql = f"""
					SELECT book_orig_source_id, book_message_id, tbc.id FROM {ms.TB_LIB_BOOKS_ALFA_EXT} AS lbae, {ms.TB_TG_BOOK_COMPLECTS_CH_01} as tbc
					WHERE lbae.serial_id = tbc.channel_id_ref AND lbae.book_message_id = tbc.book_msg_id
						UNION 
					SELECT source_id, volume_message_id, tbc.id FROM {ms.TB_LIB_BOOK_AUDIO_VOLUMES} AS lbav, {ms.TB_TG_BOOK_COMPLECTS_CH_01} as tbc
					WHERE lbav.source_id = tbc.channel_id_ref AND lbav.volume_message_id = tbc.book_msg_id
						UNION
					SELECT orig_source_id, tg_message_id, tbc.id FROM {ms.TB_LIB_BOOK_IMAGES} as lbi, {ms.TB_TG_BOOK_COMPLECTS_CH_01} as tbc
					WHERE lbi.orig_source_id = tbc.channel_id_ref AND lbi.tg_message_id = tbc.book_msg_id
        """

        # Список уже зарегестрированных в LIB сообщений с их идентификатором tbid в главной таблице скачанных сообщений 'tg_messages_proceeded'
        # ПРИМ: зарегестрированные сообщения из таблиц 1. lib_books_alfa_ext, 2. lib_book_audio_volumes, 3. lib_book_images

        listReisteredMessagesFull = self.sps.get_result_from_sql_exec_proc_sps(sql)



        
        # переключение типа возврата
        for case in Switch(retSwitch):
            if case('_TBIDS_'): 
                
                if not isinstance(listReisteredMessagesFull, int):
                # Трансформировать в список чисто tbids сообщений
                    listReisteredMessagesTbids = [x[2] for x in listReisteredMessagesFull]
                else:
                    listReisteredMessagesTbids = []
                    
                return listReisteredMessagesTbids
                break

            if case('_OBJECTS_'): 
                if not isinstance(listReisteredMessagesFull, int):
                # Трансформировать в список обьектов класса LibUniqueMessage
                    listReisteredMessagesObjs = [LibUniqueMessage(x) for x in listReisteredMessagesFull]
                else:
                    listReisteredMessagesObjs = []
                return listReisteredMessagesObjs
                break
            
            # возвращается списки в списке всех значений
            if case('_FULL_LIST_'): 
                if not isinstance(listReisteredMessagesFull, int):
                    return listReisteredMessagesFull
                else:
                    return []
                break

            if case(): # default
                print('Другое число')
                break
        
















    
    
    def get_total_registered_messages_ids_of_books_and_volumes(self):
        """ 
        OBSOLETED: Use get_total_registered_books_and_volumes_messages_objects()
        Получить список ids всех книго-образующих сообщений , которые выполнили свою роль для всех зарегестрированных в библиотеке LIB сущностей, как книг, так 
        и аудио-томов 
        """
        
        listBookRegisteredMessagesIds = self.get_all_registered_message_ids_of_books_in_lib_blf()
        
        print(f"PR_B068 --> listBookRegisteredMessagesIds = {listBookRegisteredMessagesIds}")
        
        
        
    
        listVolumesRegisteredMessagesIds = self.get_all_registered_message_ids_of_audio_volumes_in_lib_blf()
        
        print(f"PR_B069 --> listVolumesRegisteredMessagesIds = {listVolumesRegisteredMessagesIds}")
        
        
        # Список всех зарегестрированных картинок, включая те ,которые зарегестрированы и я вляются групповыми (альбомными)
        
        listRegisteredImagesMessagesIds = []
        
        
    
        listTotalRegisteredIdsOfBooksAndVolumes = listBookRegisteredMessagesIds + listVolumesRegisteredMessagesIds
        
        return listTotalRegisteredIdsOfBooksAndVolumes
    
    
    
    
    
    def get_total_registered_books_and_volumes_messages_objects_of_all_sources(self):
        """ 
        NEW: 28-03-2024
        Получить список обьектов книго-образующих сообщений , которые выполнили свою роль для всех зарегестрированных в библиотеке LIB сущностей, как книг, так 
        и аудио-томов 
        """
        
        print(f"PR_B143 --> START: get_total_registered_books_and_volumes_messages_objects_of_all_sources()")

        # A. обьекты-сообщения из табл зарегестрированных описаний книг 'lib_books_alfa' + 'lib_books_alfa_ext'
        listAllRegisteredBookMessagesObjsByAllSources = self.get_all_registered_book_messages_objs_in_lib_by_all_sources_existing_blf()
        
        print(f"PR_B068 --> listAllRegisteredBookMessagesObjsByAllSources = {listAllRegisteredBookMessagesObjsByAllSources}")
        # pp(listAllRegisteredBookMessagesObjsByAllSources)
    
        # B. Обьекты - сообщения из табл зарегестрированных аудил-томов 'lib_book_audio_volumes'
        listVolumesRegisteredMessagesObjects = self.get_all_registered_audio_volumes_messages_objects_by_all_sources_existing_blf()
        
        print(f"PR_B069 --> listVolumesRegisteredMessagesIds = {listVolumesRegisteredMessagesObjects}")
        
        
        # C. Обьекты - сообщения из табл зарегестрированных картинок, включая групповые, из табл 'lib_book_images'
        listImagesRegisteredMessagesObjects = self.get_all_registered_image_messages_objects_in_lib_book_images_by_all_sources_blf()
        
        
        
        # Список всех зарегестрированных сообщений-обьектов, включая те ,которые зарегестрированы и я вляются групповыми (альбомными)

        listTotalRegisteredBooksAndVolumesMessagesObjs = listAllRegisteredBookMessagesObjsByAllSources + listVolumesRegisteredMessagesObjects + listImagesRegisteredMessagesObjects
        
        qn = len(listTotalRegisteredBooksAndVolumesMessagesObjs)
        
        print(f"PR_B156 --> listTotalRegisteredBooksAndVolumesMessagesObjs_QN = {qn}")
        
        
        return listTotalRegisteredBooksAndVolumesMessagesObjs
    
    
    
    
    
    
    
    def get_all_registered_message_ids_of_books_in_lib_blf (self):
        """ 
        OBSOLETED:  Некорректное удаление по неполному составному ключу : book_message_id
        Получить ids всех книго-образующих сообщений зарегестрированных в библиотеке описаний книг 
        """
    
        sql = f"SELECT book_message_id FROM {ms.TB_LIB_BOOKS_ALFA_EXT}"
        
        listBookRegisteredMessagesIds = self.sps.get_result_from_sql_exec_proc_sps(sql)
    
    
        return listBookRegisteredMessagesIds
    
    
    
    
    
    
    def get_all_registered_book_messages_objs_in_lib_by_source_id_blf (self, origSourceId):
        """ 
        Получить список всех зарегестрированных обьектов типа LibUniqueMessage всех книго-образующих сообщений зарегестрированных в библиотеке описаний 
        книг по заданному их  origSourceId (id телеграм каналов, из которых взяты эти оразующие сообщения)
        book_message_id и source_id
        """
        
        print(f"PR_B148 --> START: get_all_registered_book_messages_objs_in_lib_by_source_id_blf()")

    
        sql = f"SELECT book_orig_source_id, book_message_id FROM {ms.TB_LIB_BOOKS_ALFA_EXT} WHERE book_orig_source_id = {origSourceId}"
        
        print(f"PR_B150 --> sql = {sql}")
        
        
        listBookRegisteredResultPairs = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        print(f"PR_B149 --> listBookRegisteredResultPairs = {listBookRegisteredResultPairs}")
        
        
        if not isinstance(listBookRegisteredResultPairs, int):
            listRegisteredBookMessagesObjs = [LibUniqueMessage(listParamsPair = x) for x in listBookRegisteredResultPairs]
        else:
            listRegisteredBookMessagesObjs = []
    
        return listRegisteredBookMessagesObjs
    
    
    
    
    
    def get_all_registered_book_messages_objs_in_lib_by_all_sources_existing_blf (self):
        """ 
        Получить все обьекты сообщений образующих книги по всем существующим источникам в тбалице 'lib_orig_sources' 
        """
        
        print(f"PR_B144 --> START: get_all_registered_book_messages_objs_in_lib_by_all_sources_existing_blf()")

        
        listAllRegisteredBookMessagesObjsByAllSources = []
    
    
        # Список ids всех оригинальных источников из табл lib_orig_sources
        allSourcesIds = self.get_all_books_orig_sources_ids_blf()
        
        print(f"PR_B146 --> allSourcesIds = {allSourcesIds}")
        
        # Цикл по оригинальным источникам сообщений (ТГ-каналов считай)
        
        for sourceId in allSourcesIds:
            
            print(f"PR_B144 --> POINT E")
        
            # Суммируем списки обьектов-сообщений по всем существующим источникам
            listAllRegisteredBookMessagesObjsByAllSources += self.get_all_registered_book_messages_objs_in_lib_by_source_id_blf(sourceId)
            
            
            
        return listAllRegisteredBookMessagesObjsByAllSources 
            
    
    
    
    
    
    def get_all_registered_alfa_ids_of_books_in_lib_blf (self):
        """ 
        Получить табличные alfaIds всех книго-образующих сообщений зарегестрированных в библиотеке описаний книг в табл 'lib_books_alfa'
        """
    
        sql = f"SELECT id FROM {ms.TB_LIB_BOOKS_ALFA}"
        
        listBookRegisteredAlfaIds = self.sps.get_result_from_sql_exec_proc_sps(sql)
    
    
        
    
        return listBookRegisteredAlfaIds
    
    
    
    
    
    
    
    def get_all_registered_message_ids_of_audio_volumes_in_lib_blf (self):
        """ 
        OBSOLLETED: неполный уникальный ключ для сообщений . Use: get_all_registered_audio_volumes_messages_objects_by_given_source_id_blf()
        Получить ids всех книго-образующих сообщений зарегестрированных в библиотеке аудио-томов книг
        """
    
    
        sql = f"SELECT volume_message_id FROM {ms.TB_LIB_BOOK_AUDIO_VOLUMES}"
        
        listVolumesRegisteredMessagesIds = self.sps.get_result_from_sql_exec_proc_sps(sql)
    
    
        return listVolumesRegisteredMessagesIds
    
    
    
    
    
    
    def get_all_registered_audio_volumes_messages_objects_by_given_source_id_blf (self, origSourceId):
        """ 
        NEW: 28-03-2024
        Получить список обьектов всех книго-образующих сообщений зарегестрированных в библиотеке аудио-томов книг,
        в разрезе заданного orig_source_id
        """
    
    
        sql = f"SELECT source_id, volume_message_id FROM {ms.TB_LIB_BOOK_AUDIO_VOLUMES} WHERE source_id = {origSourceId}"
        
        listVolumesRegisteredMessagesResPairs = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if not isinstance(listVolumesRegisteredMessagesResPairs, int):
        
            listVolumesRegisteredMessagesObjectsBySource = [LibUniqueMessage(listParamsPair = x) for x in listVolumesRegisteredMessagesResPairs]
    
        else:
            listVolumesRegisteredMessagesObjectsBySource = []
    
    
    
        return listVolumesRegisteredMessagesObjectsBySource
    
    
    
    
    
    
    def get_all_registered_image_messages_objects_in_lib_book_images_by_given_source_id_blf (self, origSourceId):
        """ 
        NEW: 28-03-2024
        Получить список обьектов всех книго-образующих сообщений зарегестрированных в библиотеке картинок для книг,
        в разрезе заданного orig_source_id
        """
    
    
        sql = f"SELECT orig_source_id, tg_message_id FROM {ms.TB_LIB_BOOK_IMAGES} WHERE orig_source_id = {origSourceId}"
        
        listImagesRegisteredMessagesResPairs = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if not isinstance(listImagesRegisteredMessagesResPairs, int):
        
            listimagesRegisteredMessagesObjectsBySource = [LibUniqueMessage(listParamsPair = x) for x in listImagesRegisteredMessagesResPairs]
    
        else:
            listimagesRegisteredMessagesObjectsBySource = []
    
    
    
        return listimagesRegisteredMessagesObjectsBySource
    
    
    
    
    
    
    
    
    
    
    
    
    def get_all_registered_audio_volumes_messages_objects_by_all_sources_existing_blf(self):
        """ 
        Получить все обьекты сообщений, образующих аудио-тома книги, по всем существующим источникам
        """
        
        print(f"PR_B151 --> START: get_all_registered_audio_volumes_messages_objects_by_all_sources_existing_blf()")

        
        totalListsOfAllRegisteredAudioVolumesMessagesObjectsByAllSources = []
    
        # Все  ids источников
        allSourcesIds = self.get_all_books_orig_sources_ids_blf()
        
        
        
        for sourceId in allSourcesIds:
        
            totalListsOfAllRegisteredAudioVolumesMessagesObjectsByAllSources += self.get_all_registered_audio_volumes_messages_objects_by_given_source_id_blf(sourceId)
            
            print(f"PR_B151 --> POINT G")
            
        return totalListsOfAllRegisteredAudioVolumesMessagesObjectsByAllSources
        
        
    
    
    
    
    # def get_all_registered_image_messages_ids_in_lib_book_images_blf (self):
    #     """ 
    #     Список всех зарегестрированных картинок, включая те ,которые зарегестрированы и я вляются групповыми (альбомными)
    #     """
    
    
    #     sql = f"SELECT volume_message_id FROM {ms.TB_LIB_BOOK_AUDIO_VOLUMES}"
        
    #     listVolumesRegisteredMessagesIds = self.sps.get_result_from_sql_exec_proc_sps(sql)
    
    
    #     return listVolumesRegisteredMessagesIds
    
    
    
    def get_all_registered_image_messages_objects_in_lib_book_images_by_all_sources_blf (self):
        """ 
        Список всех зарегестрированных картинок в виде сообщений-обьектов, включая те ,которые зарегестрированы и я вляются групповыми (альбомными)
        по всем источникам
        """
    
        print(f"PR_B162 --> START: get_all_registered_image_messages_objects_in_lib_book_images_by_all_sources_blf()")

        
        totalListsOfAllRegisteredImagesMessagesObjectsByAllSources = []
    
        # Все  ids источников
        allSourcesIds = self.get_all_books_orig_sources_ids_blf()
        
        
        
        for sourceId in allSourcesIds:
        
            totalListsOfAllRegisteredImagesMessagesObjectsByAllSources += self.get_all_registered_image_messages_objects_in_lib_book_images_by_given_source_id_blf(sourceId)
            
            print(f"PR_B162 --> POINT J")
            
        return totalListsOfAllRegisteredImagesMessagesObjectsByAllSources
    
    
    
    
    
    
    
    def move_downloaded_imagefrom_prime_storage_to_project_lib_dir_blf(self):
        """ 
        ЗАГОТОВКА
        Перенести скаченные картинки к описаниям книг из первичного Хранилища в проектный директорий для скаченных картинок
        """
        
        
        
    
    
    
    
    def get_dic_of_full_book_data_by_alfa_id_blf (self, bookAlfaId):
        """ 
        Получить данные книги в виде словаря по ее alfa_id
        """

        sql = f"""
                SELECT * FROM 
                    {ms.TB_LIB_BOOKS_ALFA} as lba, 
                    {ms.TB_LIB_BOOKS_ALFA_EXT} as lbae 
                WHERE 
                    lbae.books_alfa_id = lba.id AND
                    lba.id = {bookAlfaId}
            """
    
        dicLibBookData = self.spps.read_one_row_return_sql_to_dic_mysql_spps(sql)
        
        
        return dicLibBookData
    
    
    
    

    
    
    
    def get_dic_of_full_book_data_by_message_id_blf (self, bookMessageId):
        """ 
        Получить данные книги в виде словаря по ее  id собразующего ТГ сообщения
        """

        sql = f"""
                SELECT * FROM 
                    {ms.TB_LIB_BOOKS_ALFA} as lba, 
                    {ms.TB_LIB_BOOKS_ALFA_EXT} as lbae 
                WHERE 
                    lbae.books_alfa_id = lba.id AND
                    lbae.book_message_id = {bookMessageId}
            """
    
        dicLibBookData = self.spps.read_one_row_return_sql_to_dic_mysql_spps(sql)
        
        
        return dicLibBookData
    
    
    
    
    
    
    def get_dic_of_full_volume_data_by_alfa_id_blf (self, volumeTbId):
        """ 
        Получить данные аудио-тома книги в виде словаря по его табличному id
        """

        sql = f"""
                SELECT * FROM 
                    {ms.TB_LIB_BOOK_AUDIO_VOLUMES}  
                WHERE 
                    id = {volumeTbId}
            """
    
        dicLibVolumeData = self.spps.read_one_row_return_sql_to_dic_mysql_spps(sql)
        
        
        return dicLibVolumeData
    
    
    
    
    
    def get_dic_of_full_volume_data_by_message_id_blf (self, volumeMessageId):
        """ 
        Получить данные аудио-тома книги в виде словаря по  его  id собразующего ТГ сообщения
        """

        sql = f"""
                SELECT * FROM 
                    {ms.TB_LIB_BOOK_AUDIO_VOLUMES}  
                WHERE 
                    volume_message_id = {volumeMessageId}
            """
    
        dicLibVolumeData = self.spps.read_one_row_return_sql_to_dic_mysql_spps(sql)
        
        
        return dicLibVolumeData
    
    
    
    
    def if_tg_message_belongs_to_message_group_objects_blf (self, bookTbId):
        """ 
        bookTbId - табличный id сообщения
        ПроверитьЮ является ли сообщение с картинкой или документом групповым обьектом сообщения. То есть не является ли сообщение одним из группы картинок или документов,
        формирующих альбом или группу
        Поверка происходит по анализу поля 'messages_grouped_id' в таблице 'tg_message_proceeded_ext'. Если там есть целочисленное значение, то это 
        означает что кртинка или документ принадлежит группе и id этой группы для всех ее членов является как раз это целочисленное значение в поле 'messages_grouped_id'
        """
    
        sql = f"""SELECT messages_grouped_id FROM {ms.TB_MSSGS_PROCEEDED_} as mp, {ms.TB_MSSGS_PROCEEDED_EXT_} as mpe 
                    WHERE mpe.message_proceeded_ref_id = mp.id AND mp.id = {bookTbId}"""
    
    
        dicMessageExtRow = self.spps.read_one_row_return_sql_to_dic_mysql_spps(sql)
        
        if dicMessageExtRow['messages_grouped_id'] > 0:
            return True
        else:
            return False

    
    
    
    
    def get_tg_proceed_tbid_by_message_id_and_source_id_blf(self, sourceId, mesageId):
        """ 
        Получить табличный id сообщения из табл 'tg_messages_proceeded' по сложному ключу: id источника и messageId
        """
    
        sql = f"SELECT id FROM {ms.TB_MSSGS_PROCEEDED_} WHERE channels_ref_id = {sourceId} AND message_own_id = {mesageId}"
        
        print(f"PR_B117 --> sql = {sql}")
        
        
        messageTbID = self.sps.get_result_from_sql_exec_proc_sps(sql)
    
    
        return messageTbID[0]
    
    
    
    def get_tg_message_grouped_id_if_any_by_mssg_tbid_blf (self, bookTbId):
        """ 
        bookTbId - табличный id сообщения
        Получить групповой идентификатор сообщения, если он есть
        """
        
        sql = f"""SELECT messages_grouped_id FROM {ms.TB_MSSGS_PROCEEDED_} as mp, {ms.TB_MSSGS_PROCEEDED_EXT_} as mpe 
                    WHERE mpe.message_proceeded_ref_id = mp.id AND mp.id = {bookTbId}"""
    
    
    
        messageGroupedId = self.sps.get_result_from_sql_exec_proc_sps(sql)
    
    
        return messageGroupedId[0]
    
    
    
    
    

    
    def get_image_id_by_its_name_blf (self, imgName):
        """ 
        Получить id картинки по названию файла, который всегда уникально
        """
    
    
        sql = f"SELECT id FROM {ms.TB_LIB_BOOK_IMAGES} WHERE image_name = '{imgName}'"
        
        imgTbid = self.sps.get_result_from_sql_exec_proc_sps(sql)
    
        return imgTbid[0]
    
    
    
    def get_alfa_ids_from_reposit_book_registr_blf(self, repositId):
        """ 
        Получить все alfa_ids из табл решистрации выгрузки книг на свои каналы
        repositId -  id нашего канала из табл 'lib_repositories'
        """
        
        repBookTable = ms.TB_LIB_REPOSIT_BOOKS_REGISTR_ + str(repositId)
        
        sql = f"SELECT book_alfa_id FROM {repBookTable} GROUP BY book_alfa_id"
    
    
        alfaIds = self.sps.get_result_from_sql_exec_proc_sps(sql)
    
    
        return alfaIds
    
    
    
    
    
    def delete_lib_categories_and_ties_by_list_ids_blf (self, listCategIdsDelete):
        """ 
        Удалить категории из табл lib_categories и все их связи в таблицах 'lib_books_categories' и 'lib_book_categories_vocabulary', 
        ids которых входят в подмноэество списка listCategIdsDelete
        """
        
        print(f"PR_B371 --> START: delete_lib_categories_and_ties_by_list_ids_blf()")
        
        listCategIdsDeleteSQL = self.sps.transform_list_valuews_to_sql_string_for_tuple_inside_sps(listCategIdsDelete)
    
        # A. Удалить связи категорий из табл lib_book_categories_vocabulary, которые находятся в списке  listCategIdsDelete
        sql = f"DELETE FROM {ms.TB_LIB_BOOK_CATEGORIES_VOCABILARY} WHERE categ_id IN ({listCategIdsDeleteSQL})"
        
        # print(f"PR_B361 --> sql = {sql}")
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B362 --> SYS LOG: В таблице 'lib_book_categories_vocabulary' удалены все записи, у которых значение поля 'categ_id' находилось в подмножестве списка [{listCategIdsDelete}]")
            
        except Exception as err:
            print(f"PR_B363 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B364 --> SYS LOG: ERRORR !!! {err}")


        # B.  Удалить связи категорий из табл lib_books_categories, которые находятся в списке  listCategIdsDelete        
        sql = f"DELETE FROM {ms.TB_LIB_BOOKS_CATEGORIES} WHERE category_id IN ({listCategIdsDeleteSQL})"
        
        # print(f"PR_B361 --> sql = {sql}")
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B365 --> SYS LOG: В таблице 'lib_books_categories' удалены все записи, у которых значение поля 'category_id' находилось в подмножестве списка [{listCategIdsDelete}]")
            
        except Exception as err:
            print(f"PR_B366 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B367 --> SYS LOG: ERRORR !!! {err}")
        
    
        # C. Удалить категории из таблицы 'lib_categories' , которые находятся в списке listCategIdsDeleteSQL
        sql = f"DELETE FROM {ms.TB_LIB_CATEGORIES} WHERE id IN ({listCategIdsDeleteSQL})"
        
        # print(f"PR_B361 --> sql = {sql}")
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B368 --> SYS LOG: В таблице 'lib_categories' удалены категории, у которых значение поля 'id' находилось в подмножестве списка [{listCategIdsDelete}]")
            
        except Exception as err:
            print(f"PR_B369 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B370 --> SYS LOG: ERRORR !!! {err}")
    
    
        print(f"PR_B372 --> END: delete_lib_categories_and_ties_by_list_ids_blf()")
    
    
    
    
    
    
    
    def assign_authors_to_given_book_blf (self, bookAlfaId, authorsIds):
        """ 
        Присвоить авторов из списка для заданной книги в таблицу 'lib_books_authors'
        authorsIds - спискок Tbids авторов из табл 'lib_authors'
        """
    
        for authorId in authorsIds:
            
            authorFIO = self.get_author_fio_by_id_blf(authorId)
            
            sql = f"INSERT INTO {ms.TB_LIB_BOOKS_AUTHORS} (book_alfa_id, author_id) VALUES ({bookAlfaId}, {authorId})"
            
            try: 
                self.sps.execute_sql_SPS(sql)
                print(f"PR_B377 --> SYS LOG: Книге с alfaId = {bookAlfaId} присвоен автор с id = {authorId} ({authorFIO})")
                
            except Exception as err:
                print(f"PR_B378 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
                print(f"PR_B379 --> SYS LOG: ERRORR !!! {err}")






    def assign_narrators_to_given_book_blf (self, bookAlfaId, narratorsIds):
        """ 
        Присвоить  lbrnjhjd из списка для заданной книги в таблицу 'lib_books_narrators'
        narratorsIds - спискок Tbids дикторов из табл 'lib_narrators'
        """
    
        for narratorId in narratorsIds:
            
            narratorFIO = self.get_narrator_fio_by_id_blf(narratorId)
            
            sql = f"INSERT INTO {ms.TB_LIB_BOOKS_NARRATORS} (book_alfa_id, narrator_id) VALUES ({bookAlfaId}, {narratorId})"
            
            try: 
                self.sps.execute_sql_SPS(sql)
                print(f"PR_B435 --> SYS LOG: Книге с alfaId = {bookAlfaId} присвоен диктор с id = {narratorId} ({narratorFIO})")
                
            except Exception as err:
                print(f"PR_B436 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
                print(f"PR_B437 --> SYS LOG: ERRORR !!! {err}")







    def assign_repositories_to_given_source_blf (self, origSourceId, repositoriesTbids):
        """ 
        Присвоить  ids из списка repositoriesTbids для заданного источника в таблице 'lib_sources_assigned_repositories'
        narratorsIds - спискок Tbids дикторов из табл 'lib_narrators'
        """
    
        for repositoryId in repositoriesTbids:
            
            repositName = self.get_repositorty_name_by_its_tbid_blf(repositoryId)
            
            sql = f"INSERT INTO {ms.TB_LIB_SOURCES_ASSIGNED_REPOSITORIES} (orig_source_id, repository_id) VALUES ({origSourceId}, {repositoryId})"
            
            try: 
                self.sps.execute_sql_SPS(sql)
                print(f"PR_B460 --> SYS LOG: Источнику с origSourceId = {origSourceId} присвоен репозиторий с id = {repositoryId} ({repositName})")
                
            except Exception as err:
                print(f"PR_B461 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
                print(f"PR_B462 --> SYS LOG: ERRORR !!! {err}")








    def assign_repositories_to_given_lib_book_blf (self, bookAlfaId, repositoriesTbids):
        """ 
        Присвоить  ids из списка repositoriesTbids для заданной книги в таблице 'lib_books_assigned_repositories'
        repositoriesTbids - спискок Tbids репозиториев
        """
    
        for repositoryId in repositoriesTbids:
            
            repositName = self.get_repositorty_name_by_its_tbid_blf(repositoryId)
            
            sql = f"INSERT INTO {ms.TB_LIB_BOOKS_ASSIGNED_REPOSITORIES} (book_alfa_id, repository_id) VALUES ({bookAlfaId}, {repositoryId})"
            
            try: 
                self.sps.execute_sql_SPS(sql)
                print(f"PR_B495 --> SYS LOG: Книге с bookAlfaId = {bookAlfaId} присвоен репозиторий с id = {repositoryId} ({repositName})")
                
            except Exception as err:
                print(f"PR_B496 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
                print(f"PR_B497 --> SYS LOG: ERRORR !!! {err}")














    
    def remove_all_assigned_authors_from_given_book_blf (self, bookAlfaId):
        """ 
        Удалить всех авторов, присвоенных книге из табл 'lib_books_authors'
        """
    
    
        sql = f"DELETE FROM {ms.TB_LIB_BOOKS_AUTHORS} WHERE book_alfa_id = {bookAlfaId}"
    
    

        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B381 --> SYS LOG: Из табл 'lib_books_authors' удалены все связи с авторами для книги с alfaId = {bookAlfaId}")
            
        except Exception as err:
            print(f"PR_B382 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B383 --> SYS LOG: ERRORR !!! {err}")




    def remove_all_assigned_narrators_from_given_book_blf (self, bookAlfaId):
        """ 
        Удалить всех  дикторов, присвоенных книге из табл 'lib_books_narrators'
        """
    
    
        sql = f"DELETE FROM {ms.TB_LIB_BOOKS_NARRATORS} WHERE book_alfa_id = {bookAlfaId}"
    
    

        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B432 --> SYS LOG: Из табл 'lib_books_narrators' удалены все связи с дикторами для книги с alfaId = {bookAlfaId}")
            
        except Exception as err:
            print(f"PR_B433 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B434 --> SYS LOG: ERRORR !!! {err}")







    def remove_all_assigned_repositories_from_given_source_blf (self, origSourceId):
        """ 
        Удалить все  репозитории, присвоенные заданному источнику в табл 'lib_sources_assigned_repositories'
        """
    
    
        sql = f"DELETE FROM {ms.TB_LIB_SOURCES_ASSIGNED_REPOSITORIES} WHERE orig_source_id = {origSourceId}"
    
    

        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B457 --> SYS LOG: Из табл 'lib_sources_assigned_repositories' удалены все связи с репозиториями для источника с origSourceId = {origSourceId}")
            
        except Exception as err:
            print(f"PR_B458 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B459 --> SYS LOG: ERRORR !!! {err}")







    def remove_all_assigned_repositories_from_given_lib_book_blf (self, bookAlfaId):
        """ 
        Удалить все  репозитории, присвоенные заданной книге в табл 'lib_books_assigned_repositories'
        """
    
    
        sql = f"DELETE FROM {ms.TB_LIB_BOOKS_ASSIGNED_REPOSITORIES} WHERE book_alfa_id = {bookAlfaId}"
    
    

        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B492 --> SYS LOG: Из табл 'lib_books_assigned_repositories' удалены все связи с репозиториями для книги с bookAlfaId = {bookAlfaId}")
            
        except Exception as err:
            print(f"PR_B493 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B494 --> SYS LOG: ERRORR !!! {err}")















    
    def remove_authors_ties_and_after_authors_itself_in_lib_blf(self, listAuthorsTbidsDel):
        """ 
        Удалить сначала связи авторов из табл 'lib_books_authors', и затем самих авторов из табл 'lib_authors', тех авторов,
        tbids которых находятся в заданном списке listAothorsTbids
        """
        
        # Флаг, что все связи с авторами в табл 'lib_books_authors', удалены успешно
        flagTiesDeleted = False
        
        # Transform list to IN tuple sql
        tupleAthorsTbidsDelInSql = self.sps.transform_list_valuews_to_sql_string_for_tuple_inside_sps(listAuthorsTbidsDel)
    
        # A. Удалить сначала все связи в табл 'lib_books_authors' (ПРИМ: Это надо делать только после предупреждения, так как это существенное удаление)

        sql = f"DELETE FROM {ms.TB_LIB_BOOKS_AUTHORS} WHERE author_id IN ({tupleAthorsTbidsDelInSql})"
        

        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B396 --> SYS LOG: Из таблицы 'lib_books_authors' удалены все записи авторов, которые связвны с книгами и tbid которых принадлежит списку {listAuthorsTbidsDel} ")
            
            # Флаг, что все связи с авторами в табл 'lib_books_authors', удалены успешно
            flagTiesDeleted = True
            
        except Exception as err:
            print(f"PR_B397 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B398 --> SYS LOG: ERRORR !!! {err}")
    
    
        # B. Удалить авторов из табл 'lib_authors', если предварительно успешно были удалены все связи текущих авторов из таблицы связей 'lib_books_authors'
        # Если предварительно все связи с авторами удалены успешно из табл 'lib_books_authors'
        if flagTiesDeleted:
            
            sql = f"DELETE FROM {ms.TB_LIB_AUTHORS} WHERE id IN ({tupleAthorsTbidsDelInSql})"
    
            try: 
                self.sps.execute_sql_SPS(sql)
                print(f"PR_B399 --> SYS LOG: Из таблицы 'lib_authors' удалены все записи авторов c tbid всписке {listAuthorsTbidsDel} ")
                
            except Exception as err:
                print(f"PR_B400 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
                print(f"PR_B401 --> SYS LOG: ERRORR !!! {err}")
        
            
        




    def insert_new_narrator_to_book_library_db_blf (self, narratorFirstName, narratorSecondName):
        """ 
        Вставить нового диктора в таблицу 'lib_narrators'
        """
        
        narratorFullName = f"{narratorSecondName} {narratorFirstName}" # Полное имя  диктора

        # ПРЕОБРАЗОВАТЬ переменнуюдля стрингового поля в sql-запросе для того вставки f-стринг величины  без дополнительных кавычек и 
        # оперировать с NULL
        narratorFirstName = self.sps.insert_null_transformation_sps(narratorFirstName, stripVals = ' ')
        
        narratorSecondName = self.sps.insert_null_transformation_sps(narratorSecondName, stripVals = ' ')
        
        narratorFullName = self.sps.insert_null_transformation_sps(narratorFullName, stripVals = ' ')
        
            
        
        sql = f"""INSERT INTO {ms.TB_LIB_NARRATORS} (narrator_first_name, narrator_second_name, narrator_full_name) 
                    VALUES ({narratorFirstName},{narratorSecondName},{narratorFullName})
                """
                
                
                
        print(f"PR_B408 --> sql = {sql}")
        
        # Внести данные по автору в таблицу 'lib_authors'
        # TODO: сделать try в самом методе self.sps.execute_sql_SPS()
        try:
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B409 --> SYS LOG: Автор {narratorFullName} внесен в таблицу автоматически")
            
            
            # Получить Id последней внесенной записи в табл 'lib_authors', которая будет соответствовать автору обрабатываемой книги. for mysql
            newNarratorId = self.sps.get_last_inserted_id_in_db_mysql_sps ()
            
            print(f"PR_B410 --> SYS LOG: newNarratorId = {newNarratorId}")
                
        except Exception as err:
            print(f"PR_B411 --> SYS LOG: В результате !!! ОШИБКИ !!! автор не внесен в таблицу 'lib_authors' по запросу : \n{sql}")
            
            print(f"PR_B412 --> SYS LOG: Exception -> {err}")
            
            newNarratorId = -1
            
            # TODO: Ввести систему логов в текстовые файлы. Их форматы
            # Внести в проектный лог, что по этой книге и этому файлу не внесен автор. в дальнейшем, чтобы эти логи показывали, где надо вмешаться на уровне оператора библиотеки
            
        # # Получить Id последней внесенной записи в табл 'lib_authors', которая будет соответствовать автору обрабатываемой книги. for sqlite
        # authorId = self.sps.get_last_rowid_from_tb_sps (ms.TB_LIB_AUTHORS)

        return newNarratorId
    





    def update_data_of_edited_lib_narrator_blf (self, narrTbid, narrFirstName, narrSecondName):
        """ 
        Обновить данные по диктору в таблице 'lib_narrators'
        """
        
        print(f"PR_B424 --> START: update_edited_lib_narrator_blf()")
        
        narrFullName = f"{narrSecondName} {narrFirstName}"
        
        sql = f"""
            UPDATE {ms.TB_LIB_NARRATORS} SET 
            narrator_first_name = '{narrFirstName}', 
            narrator_second_name = '{narrSecondName}',
            narrator_full_name = '{narrFullName}' 
            WHERE ID = {narrTbid}
            
        """
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B426 --> SYS LOG: У диктора с id = {narrTbid} обновлены данные: {narrFullName}")
            
        except Exception as err:
            print(f"PR_B427 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B428 --> SYS LOG: ERRORR !!! {err}")


        print(f"PR_B425 --> END: update_edited_lib_narrator_blf()")







    def get_repositorty_name_by_its_tbid_blf(self, repositTbid):
        """ 
        Получить название своего репозитория по его tbid из табл 'lib_repositories'
        """


        sql = f"SELECT repository FROM {ms.TB_LIB_REPOSITORIES} WHERE id = {repositTbid}"
        
        repostName = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return repostName[0]






    def get_repositorty_tg_channel_id_by_its_tbid_blf(self, repositTbid):
        """ 
        Получить ID телеграм-канала по его tbid из табл 'lib_repositories'
        """


        sql = f"SELECT repository_tg_id FROM {ms.TB_LIB_REPOSITORIES} WHERE id = {repositTbid}"
        
        repositTgChId = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return repositTgChId[0]












if __name__ == '__main__':
    pass

    
    
    
    # ПРОРАБОТКА:
    
    
    
    
    
    # # # ПРОРАБОТКА:
    
    # blf = BookLibraryFuncs()
    # # При обьединении результатов идентичные результаты приводятся к одному результату (и нам не нужны множественные одинаковые значения)
    # # ПРИМ: названия столбцов определяются первой таблицей
    # blf.remove_all_registered_messages_from_tg_procceeded_blf()



    
    
    
    
    
    
    # print([ord(char) - 96 for char in input('Write Text: ').lower()])
    
    
    # # ПРОРАБОТКА: read_sql_to_df_pandas_mysql_spps
    
    # spps = SqlitePandasProcessorSpeedup(ms.DB_CONNECTION)
    
    # sql = f"""SELECT * FROM  {ms.TB_LIB_BOOK_STATUSES}"""

    # dfBookStatuses = spps.read_sql_to_df_pandas_mysql_spps (sql) 
    
    # print(f"dfBookStatuses = {dfBookStatuses}")

    
    
    
    
    
    
    
    # # # ПРОРАБОТКА: get_lib_alfa_books_authors_dic_sliced_with_keys_list
    
    
    # blf = BookLibraryFuncs()
    
    # tupleKeys = (1,2,3)
    
    # dicBookAuthors = blf.get_lib_alfa_books_authors_dic_filtered_by_keys_list(tupleKeys)
    
    # print(f"PR_A442 --> dicBookAuthors = {dicBookAuthors}")
    
    
    
    
    