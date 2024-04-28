
from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup
from noocube.files_manager import FilesManager

# Динамическое подключение settings_bdp_main в корне проекта
import sys
sys.path.append('/home/ak/projects/P029_book_lib_site_simple_tg_django/book_lib_site_simple_tg_django')

import lib_books_simple_site.settings_bdp_main as ms # общие установки для всех модулей

from noocube.funcs_general_class import FunctionsGeneralClass

# from lib_books_simple_site.local_classes.local_funcs import LocalFunctions

from lib_books_simple_site.local_classes.local_funcs import LocalFunctions

from noocube.text_formater import TextFormater



class ProgrammingHelpers():
    """
    Разгные вспомогательные функции
    """

    @staticmethod
    def make_mem(string_sample):
        """ 
        ProgrammingHelpers
        Создает мем из строки 
        """
        
        
        mem = string_sample.strip().replace(' ','_').upper() + '_'\
            
        return mem
    
    

    @staticmethod
    def get_tg_message_id_from_downlodaed_photo_name (downlodedPhotoName):
        """ 
        Считать из названия скаченной картинки книги id ТГ сообщения, с которого скачана это изображение
        """
        
        
        
        
        
        
    @staticmethod
    def devide_db_dump_by_given_marker_static (textSourceFile, srchMarker, targetFile, breakLine = '\n', linetimes = 1, before = True, textReplaceDic = []):
        """ 
        РАзделить тектовый файл после-перед найденными маркерами определеннымми линиями-разделителями
        """

        FilesManager.devide_text_in_file_by_given_marker_and_save_to_another_file_static (textSourceFile, srchMarker, targetFile, breakLine = breakLine, linetimes = linetimes, before = True, textReplaceDic = textReplaceDic)
        








    # @staticmethod
    # def clear_proceeded_messages_from_system_021 ():
    #     """ 
    #     ProgrammingHelpers
    #     Очистить таблицы с корнями ...messages_proceeded... БД системы 021
    #     Иными словами очистить проанализированные сообщения (это нужно на этапе разработки)
    #     """
        
    #     sps = SqliteProcessorSpeedup(ms.DB_CONNECTION)
        
        
    #     sps.clear_table_sps(ms.TB_MSSGS_PROCEEDED_)
        
    #     sps.clear_table_sps(ms.TB_MSSGS_PROCEEDED_EXT_)
        
    #     sps.clear_table_sps(ms.TB_AUXILARY_MSSGS_PROCEEDED_)
        
    #     sps.clear_table_sps(ms.TB_AUXILARY_MSSGS_PROCEEDED_EXT_)



    # @staticmethod
    # def copy_img_files_from_src_to_dest_dir (outsideProjDir, insideProjDir, filterFileExt, fileSizeLimit ):
    #     """ 
    #     ProgrammingHelpers
    #     [29-01-2024]
    #     Скопировать файлы с заданным расширением из локальной директории скачивания аудио-книг во внутреннй диреткорий проекта для дальнейшего использования 
    #     при выводе в таблицах сайта.
    #     Нулевые файлы отсеиваются от копирования
    #     """
        
    #     copiedFilesList = FilesManager.copy_files_of_given_ext_from_src_to_dest_dir_with_exist_and_size_checking (outsideProjDir, insideProjDir, filterFileExt, fileSizeLimit )
        
    #     return copiedFilesList
    
    
    # @staticmethod
    # def get_delta_detween_max_and_min_ids_in_registration_messages_tabeles_simple():
    #     """ 
    #     ProgrammingHelpers
    #     Получение ориентировочного значения кол-ва загруженных и зарегестрированных в БД сообщений в каналена данный момент 
    #     (естественно они не включают новые появившиеся сообщения в канале)
        
    #     Получить разницу между максимальными и минимальными значениями собственных ID сообщений, зарегестрированных в таблицах 'tg_messages_proceeded' 
    #     и 'tg_auxilary_messages_proceeded' , чтобы получить ориентировочное значение успешно обработанных значений сообщений в канале с конца, определяемых
    #     во View analyze_and_download_messages_from_ch_id_01() лимитом сообщений для обработки , начиная с конца и вверх по каналу
    #     Это значение не абсолютно, так как оно отображает зафиксированное значение сообщений из канала на тото момент, когда была запущена
    #     функция скачивания и обработки сообщений. С той поры в канале согут прибавится новые сообщений. Но примерное значение обработанных сообщений 
    #     в предыдущих сессиях может быть понятно ля того, что бы ориентировочно задавать следующий лимит в view analyze_and_download_messages_from_ch_id_01()
        
    #     ПРМИ: simple - означает то, что разницу в макисмльных и минимальных значениях ID сообщений вычисляется макимально просто, без анализа статуса сообщений,
    #     который может выражать ошибочность скачивания сообщений. !!!
    #     """
        
    #     sps = SqliteProcessorSpeedup(ms.DB_CONNECTION)
        
    #     # A. Сначала скачиваем все message_own_id из табл 'tg_messages_proceeded', находим минмальный и максимальный ID в данной таблице
    #     sql = f"SELECT message_own_id FROM {ms.TB_MSSGS_PROCEEDED_}"
        
    #     resMainIdList = sps.get_result_from_sql_exec_proc_sps(sql) # Список числовых ID сообщений из таблицы 'tg_messages_proceeded'
        
    #     # B. Получить все message_own_id из табл 'tg_auxilary_messages_proceeded', находим минмальный и максимальный ID в данной таблице
    #     sql = f"SELECT message_own_id FROM {ms.TB_AUXILARY_MSSGS_PROCEEDED_}"
        
    #     resAuxilaryIdList = sps.get_result_from_sql_exec_proc_sps(sql) # Список числовых ID сообщений из таблицы 'tg_auxilary_messages_proceeded'
        
    #     totalList = [resMainIdList, resAuxilaryIdList] # Составляем список списков числовых ID из разных таблиц
        
    #     # C. Получить минимум - максимум из списка списков числовых ID из разных таблиц
    #     minMaxList = FunctionsGeneralClass.get_min_max_from_list_of_int_lists(totalList)
        
    #     # Получаем разницу дельта из максимального и минимального значений ID сообщений из всех списков из всех таблиц
    #     resMaxMinIdsDelta = minMaxList[1] - minMaxList[0]
        
    #     return minMaxList, resMaxMinIdsDelta





if __name__ == '__main__':
    pass



    # ПРОРАБОТКА: Разделение текста линиями , перед найденными маркерами 
    
    srchMarker = 'CREATE'
    
    textSourceFile = '/media/ak/Transcend1/GENERAL_ARCHIVE_EXTERNAL_DISC_FROM_01_02_2024_CURRENT_MAIN/ARCHIVE_MYSQL_PROJS_DB/PRJ_021/LOGIC_BACKUP/labba__Дамп_структуры_БД_локального_PC_27_04_2024_07_29.struct'
    
    
    fileTarget = '/home/ak/projects/P029_book_lib_site_simple_tg_django/PRJ029_DB_Structures/PRJ029_BD_structures.txt'
    
    textReplaceDic = {
        
        '/*!40101 SET character_set_client = @saved_cs_client */;' : '',
        '/*!40101 SET @saved_cs_client     = @@character_set_client */;' : '',
        '/*!40101 SET character_set_client = utf8 */;' : '',
    }


    ProgrammingHelpers.devide_db_dump_by_given_marker_static (textSourceFile, srchMarker, fileTarget, breakLine = '\n', linetimes = 3, before = True, textReplaceDic = textReplaceDic)





    # # КОМЕНТИРОВАТЬ ВСЕГДА !!!
    # # ПРОРАБОТКА: Перенос картинок из установочного директория скачивания картиноки и документов во внутренний директорий проекта
    # # С проверкой на существование уже этих картинок
    
    
    # insideProjDir = '/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django/telegram_monitor/static/telegram_monitor/audio_books/books_img_downloaded/ch_1'
    
    # outsideProjDir = '/media/ak/Transcend1/GENERAL_ARCHIVE_EXTERNAL_DISC_FROM_01_02_2024_CURRENT_MAIN_!!!/TELEGRAM_AUDIO_LIBRARIES/CHANNEL_ID_1'
    
    # fileSizeLimit = 500 # байт
    
    # # Фильтруем по расширению (пока можно фильтровать только по одному расширению. Поэтому , если надо несколько расширений, то создаем списки и конкатинируем их)
    # filterFileExt = 'jpg' 
    
    # copiedFilesList = ProgrammingHelpers.copy_img_files_from_src_to_dest_dir (outsideProjDir, insideProjDir, filterFileExt, fileSizeLimit )
    
    # print(f"PR_A170 --> copiedFilesList = {copiedFilesList}")
    





    # # ПРОРАБОТКА: Получение ориентировочного значения кол-ва загруженных и зарегестрированных в БД сообщений в каналена данный момент 
    # # (естественно они не включают новые появившиеся сообщения в канале)
    
    
    # minMaxList, resMaxMinIdsDelta = LocalFunctions.get_delta_detween_max_and_min_ids_in_registration_messages_tabeles_simple()
    
    # print(f"PR_A178 --> resMaxMinIdsDelta = {resMaxMinIdsDelta}")





    






    # # ЗАПУСК МЕТОДА: Перенос картинок из директории скачивания аудио-книг во внутренний проектный директорий
    
    # insideProjDir = '/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django/telegram_monitor/static/telegram_monitor/audio_books/books_img_downloaded/ch_1'
    
    # outsideProjDir = '/media/ak/ADATA HD710/ARCHIVES_PROJECTS_MAIN_!!!!_FROM_11_01_2024/TELEGRAM_AUDIO_LIBRARIES/CHANNEL_ID_1'
    
    # fileSizeLimit = 500 # байт
    
    # # Фильтруем по расширению (пока можно фильтровать только по одному расширению. Поэтому , если надо несколько расширений, то создаем списки и конкатинируем их)
    # filterFileExt = 'jpg' 
    
    # copiedFilesList = ProgrammingHelpers.copy_img_files_from_src_to_dest_dir (outsideProjDir, insideProjDir, filterFileExt, fileSizeLimit )
    
    # print(f"PR_A170 --> copiedFilesList = {copiedFilesList}")
    
    
    



    # #  !!!! ПРИМ: ВСЕГДА КОММЕНТИРОВАТЬ КОМАНДЫВ ЭТОМ БЛОКЕ  !!!! Иначе может испортить БД
    # # ЗАПУСК МЕТОДА: Очистка таблиц  proceeded
    # # Очистить таблицы с корнем  'proceeded' 
    # ProgrammingHelpers.clear_proceeded_messages_from_system_021()



    # # ПРВЕРКА:  make_mem
    
    # sample = 'tegram_telethon_sessions_rus_'
    # mem =ProgrammingHelpers.make_mem(sample)
    # print(mem)



