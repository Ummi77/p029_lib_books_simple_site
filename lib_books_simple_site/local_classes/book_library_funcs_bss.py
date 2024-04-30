

import sys
sys.path.append('/home/ak/projects/P029_book_lib_site_simple_tg_django/book_lib_site_simple_tg_django')
import lib_books_simple_site.settings_bdp_main as ms # общие установки для всех модулей

from noocube.pandas_manager import PandasManager
from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup
from noocube.sqlite_pandas_processor_speedup import SqlitePandasProcessorSpeedup
from beeprint import pp

import pandas as pd

# from noocube.files_manager import FilesManager
# import noocube.funcs_general as FG
# from lib_books_simple_site.local_classes.tg_local_funcs import TgLocalFuncs
# from lib_books_simple_site.local_classes.stractures import LibUniqueMessage

# from noocube.switch import Switch

# from noocube.funcs_general_class import FunctionsGeneralClass



# Глобальные обьекты для этого модуля



class BookLibraryFuncsBss ():
    """ 
    Методы для библиотеки книг для VPS book site simple
    """
    
    
    def __init__(self): 

        self.sps = SqliteProcessorSpeedup(ms.DB_CONNECTION) # Обьект класса SqliteProcessorSpeedup
        self.spps = SqlitePandasProcessorSpeedup(ms.DB_CONNECTION) # Обьект класса SqlitePandasProcessorSpeedup
        # self.tlf = TgLocalFuncs()
        self.pd = PandasManager()
    




    def api_insert_categories_from_dic_tb_data_bss (self, dicTbCategories):
        """
        Заполнить очищенную от всех данных таблицу lib_categories  проекцией данных из этой же таблицы из проекта 021  
        
        """
        
        # Получить фрейм
        dfTbCategories = self.pd.read_data_from_dict_to_two_columns_frame_pm_static(dicTbCategories, ['id', 'category'])
        
        print(f"PR_NC_224 --> dfTbCategories = \n{dfTbCategories}")
        
        
        try: 
            
            # вставить фрейм в таблицу
            self.spps.insert_df_to_tb_no_key_check_simple_pandas_spps(dfTbCategories, ms.TB_LIB_CATEGORIES)

            print(f"PR_B513 --> SYS LOG: в очищенную таблицу 'lib_categories' перенесены значения из этой же табл из проекта PRJ021")
            
        except Exception as err:
            print(f"PR_B514 --> SYS LOG: При выполнении запроса произошла ошибка:")
            print(f"PR_B515 --> SYS LOG: ERRORR !!! {err}")




    def api_insert_languages_from_dic_tb_data_bss (self, dicTbLanguages):
        """
        Заполнить очищенную от всех данных таблицу lib_languages  проекцией данных из этой же таблицы из проекта 021  
        
        """
        
        # Получить фрейм
        dfTbLanguages = self.pd.read_data_from_dict_to_two_columns_frame_pm_static(dicTbLanguages, ['id', 'language'])
        
        print(f"PR_B526 --> dfTbCategories = \n{dfTbLanguages}")
        
        
        try: 
            
            # вставить фрейм в таблицу
            self.spps.insert_df_to_tb_no_key_check_simple_pandas_spps(dfTbLanguages, ms.TB_LIB_LANGUAGES)

            print(f"PR_B527 --> SYS LOG: в очищенную таблицу 'lib_languages' перенесены значения из этой же табл из проекта PRJ021")
            
        except Exception as err:
            print(f"PR_B528 --> SYS LOG: При выполнении запроса произошла ошибка:")
            print(f"PR_B529 --> SYS LOG: ERRORR !!! {err}")









    def api_insert_persons_from_dic_tb_data_bss (self, tbName, dicTbPersons, dicTbPersonsFields):
        """
        Заполнить очищенную от всех данных таблицу lib_authors или lib_narrators  проекцией данных из этих же таблиц из проекта 021  
        dicTbPersons - словарь со значениями полей 
        dicTbPersonsFields - названия полей в таблице по стандартному интерфейсу названий для Persons сущностей: firstName, secondName, fullName
        
        """
        
        # INI
        
        firstName = dicTbPersonsFields['firstName']
        secondName = dicTbPersonsFields['secondName']
        fullName = dicTbPersonsFields['fullName']
        
        # A. Создать пустой фрейм с заданынми названиями колонок
        
        # Названия колонок для создания путого фрейма
        columnsNames =  ['id', firstName,secondName,fullName]

        dfPersons = PandasManager.create_empty_frame_with_given_columns_names_pm_static (columnsNames)
        
        
        # B. Создать цикл по данным таблицы в словаре dicTbPersons
        for key, val in dicTbPersons.items():
        
            # INI
            # Текущий по циклу словарь с данынми по текущей Персоне
            dicPersonData = val
            id = key
            
            firstName = dicPersonData['firstName']
            secondName = dicPersonData['secondName']
            fullName = dicPersonData['fullName']
            
            
            # C. Добавить в фрейм dfPersons ряд с данными : id, firstName,secondName,fullName
                # ~ https://www.geeksforgeeks.org/how-to-add-one-row-in-an-existing-pandas-dataframe/
            dfPersons.loc[len(dfPersons.index)] = [id, firstName, secondName, fullName] 
                
            
        # print(f"PR_B522 --> dfPersons = \n{dfPersons}")
        
        
        try: 
            
            # ВСТВИТЬ фрейм в таблицу
            self.spps.insert_df_to_tb_no_key_check_simple_pandas_spps(dfPersons, tbName)
            
            print(f"PR_B523 --> SYS LOG: в очищенную таблицу '{tbName}' перенесены значения из этой же табл из проекта PRJ029")
            
        except Exception as err:
            print(f"PR_B524 --> SYS LOG: При выполнении запроса произошла ошибка:")
            print(f"PR_B525 --> SYS LOG: ERRORR !!! {err}")










if __name__ == '__main__':
    pass

    
    
    
    # ПРОРАБОТКА:
    
    
    
    
    
