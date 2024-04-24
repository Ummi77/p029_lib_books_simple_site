# Динамическое подключение settings_bdp_main в корне проекта
import sys
sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')
import settings_bdp_main as ms # общие установки для всех модулей

from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup
from noocube.sqlite_pandas_processor_speedup import SqlitePandasProcessorSpeedup
# # # from noocube.django_view_manager import DjangoViewManager
# from noocube.bonds_main_manager_speedup import BondsMainManagerSpeedup
# from noocube.funcs_general_class import FunctionsGeneralClass

from noocube.pandas_manager import PandasManager

from noocube.files_manager import FilesManager


from noocube.funcs_general_class import FunctionsGeneralClass


class TgLocalFuncs ():
    """ 
    Модуль отвечающий за работу с локальными методами в связи с Телеграм-таблицами
    """



    def __init__(self, **dicTrough):
        self.db_uri = f"sqlite:///{ms.DB_CONNECTION.dataBase}" # Pandas по умолчанию работает через SQLAlchemy и может создавать сама присоединение к БД по формату адреса URI (см. в документации SQLAlchemy)
        self.db_connection = ms.DB_CONNECTION
        self.sps = SqliteProcessorSpeedup(self.db_connection) # Обьект класса SqliteProcessorSpeedup
        self.spps = SqlitePandasProcessorSpeedup(self.db_connection) # Обьект класса SqlitePandasProcessorSpeedup
        # self.bmms = BondsMainManagerSpeedup(self.db_connection)
        # self.request = request
        self.dicTrough = dicTrough
        







# #######################   I.  ПРОСТЕЙШИЕ МЕТОДЫ  ===============================


    def get_dic_book_data_by_chat_message_id_tlf (self, chatMssgId):
        """  
        OBSOLETED: chatMssgId - не является уникальным. Ниже методы - с уникальным составным ключем либо по tbid 
        Получить данные по книге из таблиц с ТГ сообщениями
        """
        
        print(f"PR_A273 --> START: get_dic_book_data_by_chat_message_id_tlf()")

        sql = f"SELECT *  FROM {ms.TB_MSSGS_PROCEEDED_} as mp, {ms.TB_MSSGS_PROCEEDED_EXT_} as mpe WHERE mp.id = mpe.message_proceeded_ref_id"


        # # Для SQLite
        # df = self.spps.read_sql_to_df_pandas_SPPS(sql)
        
        # Для MySQL
        df = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(df, True, marker='PR_A224 --> ')
        
        keyVal = {
            'key' : 'message_own_id',
            'val' : chatMssgId
        }
        
        # Конвертировать один ряд фрейма , взятый по значению в поле-ключе, в словрь
        dicBookData = PandasManager.read_df_row_to_dic_by_key_val_stat_pm (df, keyVal)
        
        print(f"PR_A223 --> dic = {dicBookData}")
        
        print(f"PR_A274 --> END: get_dic_book_data_by_chat_message_id_tlf()")

        
        return dicBookData
        
        
        
        

    def get_dic_tg_book_data_by_tbid_tlf (self, messageTbid):
        """  
        Получить данные по книге из таблиц с ТГ сообщениями
        """
        
        print(f"PR_B119 --> START: get_dic_tg_book_data_by_tbid_tlf()")

        sql = f"""
        SELECT *  FROM {ms.TB_MSSGS_PROCEEDED_} as mp, {ms.TB_MSSGS_PROCEEDED_EXT_} as mpe 
        WHERE mp.id = mpe.message_proceeded_ref_id AND mp.id = {messageTbid}"""


        # Конвертировать один ряд фрейма , взятый по значению в поле-ключе, в словрь
        dicTgBookData = self.spps.read_one_row_return_sql_to_dic_mysql_spps(sql)
        
        # print(f"PR_B120 --> dic = {dicTgBookData}")
        
        print(f"PR_B121 --> END: get_dic_tg_book_data_by_tbid_tlf()")

        
        return dicTgBookData
        
        
        
        
        
        
    def get_book_title_by_tg_message_id (self, chatMssgId):
        """ 
        Найти название книги по ID сообщения в ТГ канале
        """
        
        
        
        dicBookData = self.get_dic_book_data_by_chat_message_id_tlf(chatMssgId)
        
        
        
        bookTitle = dicBookData['message_document_name']  
        
        return bookTitle
        
        
        
        
        
        
    def get_tg_message_status_by_name_tlf (self, statusName):
        """ 
        Получить id статуса скаченных ТГ-сообщений по имени
        """
        
        
        sql = f"SELECT id FROM {ms.TB_TG_MESSAGE_PROC_STATUS} WHERE message_proc_status = '{statusName}'"
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return res[0]
    
    
    
    
    
    def get_tg_messsage_id_by_its_tbid_tlf (self, messageTbid):
        """ 
        Получить tg_message_id сообщения по его табличному id
        """
    
        sql = f"SELECT message_own_id FROM {ms.TB_MSSGS_PROCEEDED_} WHERE id = {messageTbid}"
        
        tgMessageId = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        
        return tgMessageId[0]
    
    
    
    
    def get_messsage_orig_source_id_by_its_tbid_tlf (self, messageTbid):
        """ 
        Получить origSourceId сообщения по его табличному id
        """
    
        sql = f"SELECT channels_ref_id FROM {ms.TB_MSSGS_PROCEEDED_} WHERE id = {messageTbid}"
        
        tgOrigSourceId = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        
        return tgOrigSourceId[0]
    
    
    
        


# #######################  END I. ПРОСТЕЙШИЕ МЕТОДЫ   ===============================



    def obtain_photo_and_docs_messages_downloaded_with_mistakes_tlf (self, excludeFragmentInName = 'ждем следующий том'):
        """ 
        Получить сообщения типа photo или documents из таблицы 'tg_messages_proceeded', статус которых = 'IMAGE_DOWNLOADING_ERROR_'  или
        'DOCUMENT_DOWNLOADING_ERROR_' в виде списка tg_messages_ids этих сообщений
        ПРИМ: не включать статус ошибки для сообщений-пустышек, которые содержат в себе фрагмент 'ждем следующий том' в поле 'message_document_name'
        excludeFragmentInName - стринговый фрагмент-маркер, при нахождении которого в названии документа или фото дае при условии статуса ошибки у этой записи,
        мы его игнорируем (это в частности необходимо, что бы игнорировать аудио-тома пустышки, не скачанные из ТГ канала, а добавленные программой. И соотвтетсвенно
        они не имеют статуса сачанного сообщения и без этого игнора будут попадать в список ошибочных сообщений)
        """
        
        
        
        imgErrorStatusId = self.get_tg_message_status_by_name_tlf('IMAGE_DOWNLOADING_ERROR_')
        docErrorStatusId =  self.get_tg_message_status_by_name_tlf('DOCUMENT_DOWNLOADING_ERROR_')
        
        sql = f"""
            SELECT message_own_id, message_document_name, message_img_loded_path FROM {ms.TB_MSSGS_PROCEEDED_} as mp, 
            {ms.TB_MSSGS_PROCEEDED_EXT_} as mpe,
            {ms.TB_TG_MESSAGE_TYPE} as mt,
            {ms.TB_TG_MESSAGE_PROC_STATUS} as mps
            
            WHERE 
            mp.id = mpe.message_proceeded_ref_id AND 
            mp.message_type_ref_id = mt.id AND 
            mp.message_proc_status_ref_id = mps.id AND 
            (mp.message_proc_status_ref_id = {imgErrorStatusId} OR mp.message_proc_status_ref_id = {docErrorStatusId}) 
            """
            

        dfMessages = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        # Отфильтровываем аудио-пустышки исключив те, в нащзвании которых присутствует маркер пустышки excludeFragmentInName
        # ~ https://stackoverflow.com/questions/17097643/search-for-does-not-contain-on-a-dataframe-in-pandas
        
        dfMessages = dfMessages[~dfMessages["message_document_name"].str.contains(excludeFragmentInName, na=False)]
        
        print(f"PR_A881--> dfMessages = \n{dfMessages}")
        
        listMessagesWithMistake = PandasManager.convert_df_col_to_list_pm_static(dfMessages, 'message_own_id')

        return listMessagesWithMistake







    def get_tg_procceded_messages_tbids_with_given_statuses_tlf (self, listGivenStatuses : list):
        """ 
        Получить табличные ids (tbids)  с заданными в списке listGivenStatuses статусами
        """

        givenStatusesSql = f"{listGivenStatuses}".replace('[','').replace(']','')
        
        sql = f"""
            SELECT id FROM {ms.TB_MSSGS_PROCEEDED_} 
            WHERE 
            message_proc_status_ref_id in ({givenStatusesSql})
            """
            

        listTbids = self.sps.get_result_from_sql_exec_proc_sps(sql)

        return listTbids







    def get_tg_procceded_messages_ids_with_given_statuses_types_source_id_tlf (self, sourceId, listGivenStatuses, listGivenTypes):
        """ 
        Получить табличные ids (tbids)  с заданными в списке listGivenStatuses статусами и заданными типами в listTypes и в разрезе заданного источника 
        sourceId -  id источника
        """

        givenStatusesSql = f"{listGivenStatuses}".replace('[','').replace(']','')
        
        listGivenTypesSql = f"{listGivenTypes}".replace('[','').replace(']','')
        
        sql = f"""
            SELECT message_own_id FROM {ms.TB_MSSGS_PROCEEDED_} 
            WHERE 
            message_proc_status_ref_id IN ({givenStatusesSql}) AND 
            message_type_ref_id IN  ({listGivenTypesSql}) AND 
            channels_ref_id = {sourceId}
            """
            

        listMessagesIds = self.sps.get_result_from_sql_exec_proc_sps(sql)

        return listMessagesIds












    def get_message_type_id_by_tg_msg_id (self, tgMessageId):
        """ 
        Получить id типа сообщения по его id в ТГ
        """
        
        sql = f"""SELECT tmt.id FROM {ms.TB_MSSGS_PROCEEDED_} as mp, {ms.TB_TG_MESSAGE_TYPE} as tmt 
                WHERE
                mp.message_type_ref_id = tmps.id AND 
                mp.message_own_id = {tgMessageId}
        """
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return res[0]



    def get_message_type_name_by_tg_msg_id (self, tgMessageId):
        """ 
        Получить  название типа сообщения по его id в ТГ
        """
        
        sql = f"""SELECT message_type FROM {ms.TB_MSSGS_PROCEEDED_} as mp, {ms.TB_TG_MESSAGE_TYPE} as tmt 
                WHERE
                mp.message_type_ref_id = tmt.id AND 
                mp.message_own_id = {tgMessageId}
        """
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return res[0]





    def get_tg_mssg_type_id_by_name_tlf (self, mssgTypeName):
        """ 
        Получить id типа сообщения в Телеграме по его названию
        """
        
        sql = f"SELECT id FROM {ms.TB_TG_MESSAGE_TYPE} WHERE message_type = '{mssgTypeName}'"
        
        mssgTypeId = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return mssgTypeId[0]
        
        




    def delete_from_tg_messages_procceded_by_message_id_tlf (self, messageId):
        """ 
        Удалить запись из таблицы 'tg_messages_proceeded' по ключу 'message_own_id'
        """

        sql = f"DELETE FROM {ms.TB_MSSGS_PROCEEDED_} WHERE message_own_id = {messageId}"
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_A965 --> SYS LOG: Из таблицы 'tg_messages_proceeded' удалена запись с message_own_id = {messageId}")
            
        except Exception as err:
            print(f"PR_A966 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_A967 --> SYS LOG: ERRORR !!! {err}")





    def delete_from_tg_messages_procceded_by_tbid_tlf (self, tbId):
        """ 
        Удалить запись из таблицы 'tg_messages_proceeded' по ключу 'id' (табличный id записи)
        """

        sql = f"DELETE FROM {ms.TB_MSSGS_PROCEEDED_} WHERE id = {tbId}"
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B033 --> SYS LOG: Из таблицы 'tg_messages_proceeded' удалена запись с табличным id = {tbId}")
            
        except Exception as err:
            print(f"PR_B034 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B035 --> SYS LOG: ERRORR !!! {err}")






    def obtain_all_messages_ids_with_given_grouped_id_tlf (self, mssgGroupedId):
        """ 
        Получить все сообщения , относящимся к заданной группе с идентификатором mssgGroupedId
        """

        sql = f"""SELECT mp.id FROM {ms.TB_MSSGS_PROCEEDED_} as mp, {ms.TB_MSSGS_PROCEEDED_EXT_} as mpe 
                    WHERE mpe.message_proceeded_ref_id = mp.id AND mpe.messages_grouped_id = {mssgGroupedId}"""
    
    
        messagesTbIdsOfGivenGroup = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return messagesTbIdsOfGivenGroup
    
    


    def get_grpoup_id_by_message_tbid_tlf (self, messageTbid):
        """ 
        Получить групповой идентификатор сообщения по его tbid в табл 'tg_messages_proceeded'
        Если messageGroupId будет = -1, это означает, что у сообщения нет никакой группы
        Группа отстуствует у картинок, если она одна. И у томов. если том один
        """
        
        sql = f"""SELECT mpe.messages_grouped_id FROM {ms.TB_MSSGS_PROCEEDED_} as mp, {ms.TB_MSSGS_PROCEEDED_EXT_} as mpe 
                    WHERE mpe.message_proceeded_ref_id = mp.id AND mp.id = {messageTbid}"""
    
    
        messageGroupId = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if isinstance(messageGroupId, int):
            return messageGroupId
        else:
            return messageGroupId[0]





    def find_grouped_photo_message_book_description_tlf(self, groupedId):
        """ 
        groupedId - иденификатор группы
        Найти в групповом наборе photo-сообщений (в альбоме), в котором хранится опиание книги
        ПРИМ: На данный момент считаем, что такое описание и все его части хранятся привязаны только к одному из photo-сообщений группы
        Если встретятся случая распределенных описаний по разным членам группы, тогда нужно будет перерабатывать алгоритм
        """
        
        
        messagesTbIdsOfGivenGroup = self.obtain_all_messages_ids_with_given_grouped_id_tlf (groupedId)
        
        mssgsTbidsSql = self.sps.transform_list_valuews_to_sql_string_for_tuple_inside_sps(messagesTbIdsOfGivenGroup)
        
        # Цикл для перебора всех photo-сообщений группы для нахождение основного с описанием книги
        

        
        sql = f"""
                SELECT message_proceeded_ref_id FROM {ms.TB_MSSGS_PROCEEDED_EXT_} WHERE message_proceeded_ref_id IN ({mssgsTbidsSql}) AND message_text is not NULL AND CHAR_LENGTH(message_text) > 10
        """
        
        print(f"PR_B158 --> sql = {sql}")
    
        mainBookPhotoMssgTbid = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if not isinstance(mainBookPhotoMssgTbid, int):
            mainBookPhotoMssgTbid = mainBookPhotoMssgTbid[0]


        return mainBookPhotoMssgTbid






    def get_all_tbids_from_tg_messages_proceeded_tlf (self):
        """ 
        Получить все табличные ids из табл tg_messages_proceeded
        """
        
        sql = f"SELECT id FROM {ms.TB_MSSGS_PROCEEDED_}"
        
        messagesTbids = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        return messagesTbids
        



    def obtain_df_tb_proceeded_types_sequences_by_tg_source_id_tlf(self, tgSourceId):
        """ 
        Получить фрейм из двух полей: tbids сообщений из табл 'tg_messages_proceeded'  и 
        последовательность типов сообщений по колонке 'message_type_ref_id' в разрезе ТГ источника
        то есть, последовательная цепочка типов 1 и 2, которы еопределяют книга - аудио том, отфильтрованных по одному
        заданному ТГ источнику tgSourceId
        """

        sql = f"""
                    SELECT id, message_type_ref_id, message_own_id FROM 
                    {ms.TB_MSSGS_PROCEEDED_}
                        WHERE 
                            channels_ref_id = {tgSourceId}
        """
            
            
        dfProcceededTypeSequences = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        return dfProcceededTypeSequences
    
    
    





    def get_df_full_data_tbs_procceeded_tlf (self):
        """ 
        Получить фрейм с полными данными из таблиц 'tg_messages_proceeded' и 'tg_messages_proceeded_ext'
        """
        

        sql = f"""
        SELECT *  FROM {ms.TB_MSSGS_PROCEEDED_} as mp, {ms.TB_MSSGS_PROCEEDED_EXT_} as mpe 
        WHERE mp.id = mpe.message_proceeded_ref_id"""



        dfFullProcceeded = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        return dfFullProcceeded




    def get_df_full_dta_tbs_procceeded_by_source_id_tlf (self, soourceId):
        """ 
        Получить фрейм с полными данными из таблиц 'tg_messages_proceeded' и 'tg_messages_proceeded_ext' в разрезе заданного источника
        """
        

        sql = f"""
        SELECT *  FROM {ms.TB_MSSGS_PROCEEDED_} as mp, {ms.TB_MSSGS_PROCEEDED_EXT_} as mpe 
        WHERE mp.id = mpe.message_proceeded_ref_id AND mp.channels_ref_id = {soourceId}"""



        dfFullProcceeded = self.spps.read_sql_to_df_pandas_mysql_spps(sql)
        
        return dfFullProcceeded







    def delete_messages_from_tbs_procceeded_based_on_tbids_list_tlf (self, mssgTbidsList):
        """ 
        Удалить сообщения из таблиц 'tg_messages_proceeded' и 'tg_message_proceeded_ext' на основе списка tbids сообщений
        """
        
        print(f"PR_B310 --> START: delete_messages_from_tbs_procceeded_based_on_tbids_list_tlf()")
    
        inSqlList = self.sps.transform_list_valuews_to_sql_string_for_tuple_inside_sps(mssgTbidsList)
        
        sql = f"DELETE FROM {ms.TB_MSSGS_PROCEEDED_EXT_} WHERE message_proceeded_ref_id IN ({inSqlList})"
        
        print(f"PR_B315 --> sql = {sql}")
        
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B304 --> SYS LOG: Из таблицы 'tg_message_proceeded_ext' были удалены сообщения с message_proceeded_ref_id входящим в множество {mssgTbidsList}")
            
        except Exception as err:
            print(f"PR_B305 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B306 --> SYS LOG: ERRORR !!! {err}")


        sql = f"DELETE FROM {ms.TB_MSSGS_PROCEEDED_} WHERE id IN ({inSqlList})"
        
        
        try: 
            self.sps.execute_sql_SPS(sql)
            print(f"PR_B307 --> SYS LOG: Из таблицы 'tg_message_proceeded' были удалены сообщения с id входящим в множество {mssgTbidsList}")
            
        except Exception as err:
            print(f"PR_B308 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
            print(f"PR_B309 --> SYS LOG: ERRORR !!! {err}")

        print(f"PR_B311 --> END: delete_messages_from_tbs_procceeded_based_on_tbids_list_tlf()")







    def transfer_downloaded_images_from_prime_storage_to_project_dir_tlf ():
        """ 
        Перенос загруженных картинок из первичного директория в проектный директорий. предназначенный для скаченных картинок из тг канала
        """
        
        print(f"PR_B312 --> START: transfer_downloaded_images_from_prime_storage_to_project_dir_tlf()")

        # Проектный директорий для загруженных с ТГ картинок
        insideProjDir = ms.LIB_BOOK_IMAGE_STORAGE_FOR_DOWNLOADED_IMAGES
        
        # Первичное Хранилище
        outsideProjDir = ms.TG_DOWNLOAD_PRIME_STORAGE
        
        fileSizeLimit = 500 # байт
        
        # Фильтруем по расширению (пока можно фильтровать только по одному расширению. Поэтому , если надо несколько расширений, то создаем списки и конкатинируем их)
        filterFileExt = 'jpg' 
        
        copiedFilesList = FilesManager.copy_files_of_given_ext_from_src_to_dest_dir_with_exist_and_size_checking (outsideProjDir, insideProjDir, filterFileExt, fileSizeLimit )
        
        print(f"PR_A170 --> copiedFilesList = {copiedFilesList}")
        

        print(f"PR_B313 --> END: transfer_downloaded_images_from_prime_storage_to_project_dir_tlf()")






    def transfer_logic_error_messages_to_errors_tables_by_tbids_tlf (self, listTbids):
        """ 
        Перенести сообщения, распознанные системой как ошибочные по логике, из таблиц 'tg_messages_proceeded' и 'tg_messages_proceeded_ext' в таблицы 
        'tg_messages_proceeded_err' и 'tg_messages_proceeded_err_ext'
        listTbids - список tbids сообщений, которыфе надо перенести
        """

        print(f"PR_B335 --> START: transfer_logic_error_messages_to_errors_tables_by_tbids_tlf()")

        # ini
        
        # Флаги успешности выполнения запростов на вставку 
        flagInsert1 = False
        flagInsert2 = False


        # # Цикл по  tbidsForTransferToAuxilarList
        
        print(f"PR_B337 --> Цикл переносов по списку : {listTbids}")
        
        for inx, msgeTbid in enumerate(listTbids):
            
            print(f"PR_B338 --> Индекс цикла: {inx}. mssgTbId = {msgeTbid}")

            sql = f"""
                        INSERT INTO {ms.TB_TG_PROCCEEDED_ERR} 
                        (
                            channels_ref_id,
                            message_own_id,
                            message_type_ref_id,
                            message_proc_status_ref_id,
                            date_reg_calend,
                            date_reg_unix,
                            date_executed_calend,
                            date_executed_unix,
                            tg_sample_id
                        )
                        SELECT 
                            channels_ref_id,
                            message_own_id,
                            message_type_ref_id,
                            message_proc_status_ref_id,
                            date_reg_calend,
                            date_reg_unix,
                            date_executed_calend,
                            date_executed_unix,
                            tg_sample_id
                        FROM {ms.TB_MSSGS_PROCEEDED_} 
                        WHERE id = {msgeTbid}
            """
        
            print(f"PR_B279-->  sql = {sql}")
            
            try: 
                self.sps.execute_sql_SPS(sql)
                print(f"PR_B280 --> SYS LOG: из табл 'tg_messages_proceeded' в табл 'tg_messages_proceeded_err' перенесена запись с tbid = {msgeTbid}")
                
                # автоинкрементное id последней вставки
                lastId = self.sps.get_last_inserted_id_in_db_mysql_sps()
                
                flagInsert1 = True
                
                
            except Exception as err:
                print(f"PR_B281 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
                print(f"PR_B282 --> SYS LOG: ERRORR !!! {err}")


        
        # #     # Получить текст сообщения из 'tg_message_proceeded_ext'
            
        #     sql = f"SELECT message_text FROM {ms.TB_MSSGS_PROCEEDED_EXT_} WHERE message_proceeded_ref_id = {msgeTbid}"
            
        #     mssgText = self.sps.get_result_from_sql_exec_proc_sps(sql)
            
        #     print(f"PR_B283--> mssgText = {mssgText}")
        
        
            # 2. Копируем (создаем) записи из главной табл 'tg_message_proceeded_ext' в главную табл 'tg_auxilary_messages_proceeded_ext'
            
            
            sql2 = f"""
                        INSERT INTO {ms.TB_TG_PROCCEEDED_ERR_EXT} 
                        (
                            message_proceeded_ref_id,
                            channels_ref_id_ext,
                            message_own_id_ext,
                            message_text,
                            message_img_loded_path,
                            message_img_name,
                            message_document_loded_path,
                            message_document_name,
                            message_document_size,
                            messages_grouped_id
                        )
                        SELECT 
                            {lastId} AS message_proceeded_ref_id,
                            channels_ref_id_ext,
                            message_own_id_ext,
                            message_text,
                            message_img_loded_path,
                            message_img_name,
                            message_document_loded_path,
                            message_document_name,
                            message_document_size,
                            messages_grouped_id
                        FROM {ms.TB_MSSGS_PROCEEDED_EXT_} 
                        WHERE message_proceeded_ref_id = {msgeTbid}
            """
            
            print(f"PR_B279-->  sql = {sql2}")
            
            try: 
                self.sps.execute_sql_SPS(sql2)
                print(f"PR_B325 --> SYS LOG: из табл 'tg_message_proceeded_ext' в табл 'tg_message_proceeded_err_ext' перенесена запись с tbid = {msgeTbid}")
                
                flagInsert2 = True
                
            except Exception as err:
                print(f"PR_B326 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql2}")
                print(f"PR_B327 --> SYS LOG: ERRORR !!! {err}")


            if flagInsert1 and flagInsert2:
            
                # 3. Удалить записи в зависимой табл 'tg_message_proceeded_ext'
                
                sql = f"DELETE FROM {ms.TB_MSSGS_PROCEEDED_EXT_} WHERE message_proceeded_ref_id = {msgeTbid}"
                
                try: 
                    self.sps.execute_sql_SPS(sql)
                    print(f"PR_B328 --> SYS LOG: из табл 'tg_message_proceeded_ext' удалена запись . где message_proceeded_ref_id = {msgeTbid}")
                    
                    flagInsert2 = True
                    
                except Exception as err:
                    print(f"PR_B329 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
                    print(f"PR_B330 --> SYS LOG: ERRORR !!! {err}")
                
                
                # 4. Удалить записи из главной табл 'tg_messages_proceeded'
                    
                sql = f"DELETE FROM {ms.TB_MSSGS_PROCEEDED_} WHERE id = {msgeTbid}"
                
                try: 
                    self.sps.execute_sql_SPS(sql)
                    print(f"PR_B331 --> SYS LOG: из табл 'tg_message_proceeded' удалена запись . где id = {msgeTbid}")
                    
                    flagInsert2 = True
                    
                except Exception as err:
                    print(f"PR_B332 --> SYS LOG: При выполнении запроса произошла ошибка: \n{sql}")
                    print(f"PR_B333 --> SYS LOG: ERRORR !!! {err}")
                

        print(f"PR_B336 --> START: transfer_logic_error_messages_to_errors_tables_by_tbids_tlf()")



    def trucate_tbs_tg_procceeded_err(self):
        """ 
        Очистить и обнулить счетчик в таблицах 'tg_messages_proceeded_err' и 'tg_message_proceeded_err_ext'
        """
        
        try: 
            self.sps.truncate_table_mysql_sps(ms.TB_TG_PROCCEEDED_ERR_EXT)
            print(f"PR_B319 --> SYS LOG: Удалены записи и обнулена таблица 'tg_message_proceeded_err_ext'")
            
        except Exception as err:
            print(f"PR_B320 --> SYS LOG: При выполнении запроса произошла ошибка иа таблица 'tg_message_proceeded_err_ext' не очищена от записей!!!")
            print(f"PR_B321 --> SYS LOG: ERRORR !!! {err}")
            
            


        try: 
            self.sps.truncate_table_mysql_sps(ms.TB_TG_PROCCEEDED_ERR)
            print(f"PR_B322 --> SYS LOG: Удалены записи и обнулена таблица 'tg_messages_proceeded_err'")
            
        except Exception as err:
            print(f"PR_B323 --> SYS LOG: При выполнении запроса произошла ошибка иа таблица 'tg_messages_proceeded_err' не очищена от записей!!!")
            print(f"PR_B324 --> SYS LOG: ERRORR !!! {err}")
            
            
















if __name__ == '__main__':
    pass


    # # # ПРОРАБОТКА: 

































        
        
        
        
        
        
        
        