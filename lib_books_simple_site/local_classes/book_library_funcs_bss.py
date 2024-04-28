

import sys
sys.path.append('/home/ak/projects/P029_book_lib_site_simple_tg_django/book_lib_site_simple_tg_django')
import lib_books_simple_site.settings_bdp_main as ms # общие установки для всех модулей

from noocube.pandas_manager import PandasManager
from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup
from noocube.sqlite_pandas_processor_speedup import SqlitePandasProcessorSpeedup
from beeprint import pp
from noocube.files_manager import FilesManager
import noocube.funcs_general as FG
from lib_books_simple_site.local_classes.tg_local_funcs import TgLocalFuncs
from lib_books_simple_site.local_classes.stractures import LibUniqueMessage

from noocube.switch import Switch

# from noocube.funcs_general_class import FunctionsGeneralClass



# Глобальные обьекты для этого модуля



class BookLibraryFuncsBss ():
    """ 
    Методы для библиотеки книг для VPS book site simple
    """
    
    
    def __init__(self): 

        self.sps = SqliteProcessorSpeedup(ms.DB_CONNECTION) # Обьект класса SqliteProcessorSpeedup
        self.spps = SqlitePandasProcessorSpeedup(ms.DB_CONNECTION) # Обьект класса SqlitePandasProcessorSpeedup
        self.tlf = TgLocalFuncs()
        self.pd = PandasManager()
    




    def api_insert_categories_from_dic_tb_data_bss (self, dicTbCategories):
        """Заполнить очищенную от всех данных таблицу lib_categories  проекцией данных из этой же таблицы из проекта 021  """
        
        # Получить фрейм
        dfTbCategories = self.pd.read_data_from_dict_to_two_columns_frame_pm_static(dicTbCategories, ['id', 'category'])
        
        print(f"PR_NC_224 --> dfTbCategories = \n{dfTbCategories}")
        
        
        try: 
            
            # вставить фрейм в таблицу
            self.spps.insert_df_to_tb_no_key_check_simple_pandas_spps(dfTbCategories, ms.TB_LIB_CATEGORIES)
            # self.spps.insert_df_to_tb_pandas_spps(dfTbCategories, ms.TB_LIB_CATEGORIES, ['*'], 'id', db='mysql')
            # self.spps.insert_df_to_tb_no_key_check_pandas_spps(dfTbCategories, ms.TB_LIB_CATEGORIES)
            
            
            print(f"PR_B513 --> SYS LOG: в очищенную таблицу 'lib_categories' перенесены значения из этой же табл из проекта PRJ029")
            
        except Exception as err:
            print(f"PR_B514 --> SYS LOG: При выполнении запроса произошла ошибка:")
            print(f"PR_B515 --> SYS LOG: ERRORR !!! {err}")






if __name__ == '__main__':
    pass

    
    
    
    # ПРОРАБОТКА:
    
    
    
    
    
