
### Standart Import Block
import sys
sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')
import settings_bdp_main as ms # общие установки для всех модулей

from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup
from noocube.sqlite_pandas_processor_speedup import SqlitePandasProcessorSpeedup
from noocube.funcs_general_class import FunctionsGeneralClass
from noocube.pandas_manager import PandasManager
import noocube.funcs_general as FG
### END Standart Import Block




class BookEditManager():
    """ 
    Модуль отвечающий за предварительное редактирование данных по книгам, томам и пр. перед тем, как перевести их в конечную библиотеку, которая выгружается на 
    внешние публичные рессурсы
    """
    



    def __init__(self, **dicTrough):
        self.db_uri = f"sqlite:///{ms.DB_CONNECTION.dataBase}" # Pandas по умолчанию работает через SQLAlchemy и может создавать сама присоединение к БД по формату адреса URI (см. в документации SQLAlchemy)
        self.db_connection = ms.DB_CONNECTION
        self.sps = SqliteProcessorSpeedup(self.db_connection) # Обьект класса SqliteProcessorSpeedup
        self.spps = SqlitePandasProcessorSpeedup(self.db_connection) # Обьект класса SqlitePandasProcessorSpeedup
        # self.request = request
        self.dicTrough = dicTrough
        










































if __name__ == '__main__':
    pass


















