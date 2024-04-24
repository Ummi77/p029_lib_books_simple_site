
import sys
sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')
import settings_bdp_main as ms # общие установки для всех модулей

from noocube.pandas_manager import PandasManager
from noocube.sqlite_pandas_processor_speedup import SqlitePandasProcessorSpeedup


class LibBookVolume ():
    """ 
    Обьект Book Volume. СТруктура для хранения в себе нескольких значений полей из таблицы или фрейма. 
    В частности, для создания прообраза словаря, но не с единственным значением по ключу, а с множественными, в виде значений, например, 
    полей таблицы по ключу. И в частности для передачи для темплейта Джанго в JJ одним обьектом, а не мноеством словарей или переменных
    """
    table = 'lib_book_audio_volumes'
    keyField = 'id'
    field1 = 'volume_file_name'
    field2 = 'volume_title'
    
    def __init__(self): 

        pass
        
        
        
    

class LibBookVolumeHeroMySql ():
    """ 
    Обьект Book Volume с супер-способностями и связью с соотвтетсвующей таблице в БД, который ожет выполнять операции INSERT, UPDATE. И это только на данный момент)
    TODO: И похоже, что такие классы нужно создать для всех таблиц. И даже, возможно создать автогенератор подобных структур на основе таблиц в Бд
    differenciateor -  для дифференцированной реализации конструктора , испоьзуя swithch() [Реализовать во времени]
    Если в параметрах конструктора задан именной key, то этот ключ имеет приоретет над атрибутом класса (а точнее, его надо туда переприсвоить !!! [Позже реализовать])
    """
    table = ms.TB_LIB_BOOK_AUDIO_VOLUMES 
    keyField = 'id'
    
    def __init__(self,dicFieldsVals,  key = '', differenciateor = ''): 

        self.dicFieldsVals = dicFieldsVals
        self.spps = SqlitePandasProcessorSpeedup(ms.DB_CONNECTION)

        
    def updateRecord(self):
        """ 
        Обновить запись на основе данных в обьекте класса 
        """
        
        # Считать словарь с полями в фрейм
        df = PandasManager.read_df_from_dictionary_static(self.dicFieldsVals)
        
        # Выполнить UPDATE записи с заданнымключем в заданной таблице, обновить данными , находящимися в словаре dicFieldsVals
        self.spps.insert_or_update_df_to_tb_by_given_simple_key_spps(df, self.table, self.keyField)
        
        
        
        
        

class LibUniqueMessage ():
    """ 
    Структура для создания обьекта сообщения , однозначно определеямеого в системе через составной ключ:
    messgOrigSourceId и messageTgId 
    """

    
    def __init__(self, messgOrigSourceId = None, messageId = None, procceedTbid = None ,listParams = None): 

        pass
        
        # Если задан список значений (порядок в списке важен!!!)
        if listParams:

            # Анализ кол-ва элементов в списке (Если один элемент, то значит обьект строится по procceedTbid ['tg_messages_proceeded'])
            
            # Обьект однозначно задается procceedTbid ['tg_messages_proceeded']
            if len(listParams) == 1:
                self.procceedTbid = procceedTbid
            
            # Обьект однозначно задается messgOrigSourceId и messageId из списка
            elif len(listParams) == 2:
                self.messgOrigSourceId = listParams[0]
                self.messageId = listParams[1]
            
            # Обьект задается в наиболее полной форме messgOrigSourceId и messageId и procceedTbid ['tg_messages_proceeded'] из списка
            elif len(listParams) == 3:
                self.messgOrigSourceId = listParams[0]
                self.messageId = listParams[1]
                self.procceedTbid = listParams[2]
        
        
        # Если обьект задается не списком , просто через отдельные параметры в конструкторе
        
        # Обьект однозначно задается параметрами messgOrigSourceId и messageId  в конструкторе 
        elif messgOrigSourceId and messageId and not procceedTbid:
        
            self.messgOrigSourceId = messgOrigSourceId
            self.messageId = messageId
            
        # Обьект однозначно задается параметрами messgOrigSourceId и messageId и  procceedTbid в конструкторе     
        elif messgOrigSourceId and messageId and procceedTbid:
            
                self.messgOrigSourceId = messgOrigSourceId
                self.messageId = messageId
                self.procceedTbid = procceedTbid
            
        # Обьект однозначно задается одним параметром procceedTbid в конструкторе 
        elif not messgOrigSourceId and not messageId and procceedTbid:
            self.procceedTbid = procceedTbid
        






























