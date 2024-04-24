
from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup
from noocube.sqlite_pandas_processor_speedup import SqlitePandasProcessorSpeedup

from noocube.bonds_main_manager_speedup import BondsMainManagerSpeedup

# Динамическое подключение settings_bdp_main в корне проекта
import sys
sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')
import settings_bdp_main as ms # общие установки для всех модулей


class CompInfPageManager ():
    """ 
    Класс для обеспечения информационной страницы компании
    """
    
    
    

    def __init__(self, dicTrough={}):
        self.db_uri = f"sqlite:///{ms.DB_CONNECTION.dataBase}" # Pandas по умолчанию работает через SQLAlchemy и может создавать сама присоединение к БД по формату адреса URI (см. в документации SQLAlchemy)
        self.db_connection = ms.DB_CONNECTION
        self.sps = SqliteProcessorSpeedup(self.db_connection) # Обьект класса SqliteProcessorSpeedup
        self.spps = SqlitePandasProcessorSpeedup(self.db_connection) # Обьект класса SqlitePandasProcessorSpeedup
        self.bmms = BondsMainManagerSpeedup(self.db_connection)
        # self.request = request
        self.dicTrough = dicTrough
    
    
    
    def insert_inn_to_bonds_archive_by_isin_cipm(self, dicThrough):
        """ 
        Вставить ИНН компании в нужные таблицы системы 
        """

    
        print(f"PR_703 --> isin = {dicThrough['isin']}")
        inn = dicThrough['inn']
        isin = dicThrough['isin']
        
        sql = f"UPDATE {ms.TB_BONDS_ARCHIVE} SET inn_ref='{inn}'  WHERE isin='{isin}'"
        print(f"PR_704 --> sql = {sql}")
        
        self.sps.execute_sql_SPS(sql)
        
        
    def get_inn_by_isin_from_bonds_archive_cipm (self, isin):
        """ 
        Получить инн компании по ее ИСИН из архивных таблиц корпоративов bonds_archive
        """
        
        sql = f"SELECT inn_ref FROM {ms.TB_BONDS_ARCHIVE} WHERE isin='{isin}'"
        
        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        if not isinstance(res, int):
            ret = res[0]
        else:
            ret = -1
        
        return ret
        
        
    
    
    
    def get_bond_nick_name_by_isin (self, isin):
        """ 
        Получить ник-нейм облигации по ее ИСИН
        """
    
        sql = f"SELECT bond_name FROM {ms.TB_BONDS_ARCHIVE} WHERE isin='{isin}'"

        res = self.sps.get_result_from_sql_exec_proc_sps(sql)
        
        
        if not isinstance(res, int):
            ret = res[0]
        else:
            ret = -1
        
        
        return ret
    

if __name__ == '__main__':
    pass



    
    