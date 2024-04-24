
import sys
sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')
import settings_bdp_main as ms # общие установки для всех модулей

import noocube.funcs_general as FG




class LogManager ():
    """ 
    Модуль управления логированием 
    """
    
    cdate = FG.get_calend_date_format6()
    # Файл для сохранения логических ошибок в пространстве библиотеки
    LIB_LOGIC_ERROR_LOG_FILE = f"{ms.LOG_DIR}/lib_logic_error_log_{cdate}.txt"
    
    

    def __init__(self, **dicTrough):
        pass





    def log_labba_logic_errors_lm (self, errMessage, persMarker):
        """ 
        Залогировать логическую ошибку в библиотеке LABBA
        persMarker - персональный маркер ошибки, по которому муожно идентифицировать место возникновение сообщений и отсечь, если эта ошибка уже внесена в файл
        {_ERR_LOGIC_001_} - общий маркер обшибке в подмножестве всех ошибок в проекте (формирующегося во времени)
        """

        dtStringFormat1, dtStringFormat2, universUnix = FG.get_current_time_format_1_and_2_and_universal_unix()
    
        # СОХРАНЕНИЕ информации о логичекой обшибке в библиотеке LABBIE (сохраняет как append в файле)
        with open(LogManager.LIB_LOGIC_ERROR_LOG_FILE,"a", encoding= 'utf-8') as f:
            
            f.write(f"\n------------- {dtStringFormat2}\n")
            f.write("{_ERR_LOGIC_001_}\n")
            f.write(errMessage)
            f.write(f"\n##\n")
            
        print(f"PR_B262 --> SYS LOG: Данные об ошибке внесены в лог-файл {LogManager.LIB_LOGIC_ERROR_LOG_FILE}")
    








