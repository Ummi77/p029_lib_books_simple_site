


from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup
from noocube.sqlite_pandas_processor_speedup import SqlitePandasProcessorSpeedup
# # from noocube.django_view_manager import DjangoViewManager
from noocube.bonds_main_manager_speedup import BondsMainManagerSpeedup



# from noocube.request_manager_jango import RequestManagerJango
# from noocube.pandas_manager import PandasManager
# from noocube.sql_syntaxer import SQLSyntaxer
# from noocube.json_manager import JsonManager
# # import pandas as pd
# import noocube.funcs_general  as FG

from noocube.funcs_general_class import FunctionsGeneralClass


# import uno
# from com.sun.star.beans import PropertyValue

# Динамическое подключение settings_bdp_main в корне проекта
import sys
sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')
import settings_bdp_main as ms # общие установки для всех модулей



class LocalFunctionsDatabase ():
    """ 
    Методы проекта, связанные с облигациями и, в частности, с БД 'bonds'
    dicTrhough - сквозной словарь данных (аналог **kwargs)
    """


    def __init__(self, **dicTrough):
        self.db_uri = f"sqlite:///{ms.DB_CONNECTION.dataBase}" # Pandas по умолчанию работает через SQLAlchemy и может создавать сама присоединение к БД по формату адреса URI (см. в документации SQLAlchemy)
        self.db_connection = ms.DB_CONNECTION
        self.sps = SqliteProcessorSpeedup(self.db_connection) # Обьект класса SqliteProcessorSpeedup
        self.spps = SqlitePandasProcessorSpeedup(self.db_connection) # Обьект класса SqlitePandasProcessorSpeedup
        self.bmms = BondsMainManagerSpeedup(self.db_connection)
        # self.request = request
        self.dicTrough = dicTrough
        





    # ############ I. Операции с БД  ==============================================================


        
        
        
        
    def clear_messages_tebles_in_db_lfdb (self):
        """ 
        LocalFunctionsDatabase
        Очистить таблицы tg_messages_proceeded, tg_message_proceeded_ext, tg_auxilary_messages_proceeded и tg_auxilary_messages_proceeded_ext в БД

        """

        try:
            self.sps.truncate_table_mysql_sps(ms.TB_MSSGS_PROCEEDED_)
            self.sps.truncate_table_mysql_sps(ms.TB_MSSGS_PROCEEDED_EXT_)
            self.sps.truncate_table_mysql_sps(ms.TB_AUXILARY_MSSGS_PROCEEDED_)
            self.sps.truncate_table_mysql_sps(ms.TB_AUXILARY_MSSGS_PROCEEDED_EXT_)
            
            self.sps.truncate_table_mysql_sps(ms.TB_TG_BOOK_COMPLECTS_CH_01)
            self.sps.truncate_table_mysql_sps(ms.TB_TG_BOOK_COMPLECT_VOLUMES_CH_01)
            
            
            
            print(f"PR_A217 --> SYS LOG: Очищены таблицы tg_messages_proceeded, tg_message_proceeded_ext, tg_auxilary_messages_proceeded и tg_auxilary_messages_proceeded_ext в БД")
            
        except: 
            
            print(f"PR_A218 --> SYS LOG: Произошла какя-то ошибка при очищении таблиц сообщений в БД")
        
        
        
        
        
        
        
        





    ############ END I. Операции с БД  ==========















if __name__ == '__main__':
    pass


    # # # ПРОРАБОТКА: метода create_row_in_tb_lib_book_serial_ilbn_to_issue_book_serial_number ()
    
    # # # help(ms)
    
    # lfdb = LocalFunctionsDatabase()
    
    
    # lfdb.issue_new_book_serial_number_ilbn_lfdb()
    
    
    
    
    
    
    
    
    
    
    















