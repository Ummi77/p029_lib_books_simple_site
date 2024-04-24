

from noocube.bonds_main_manager import BondsMainManager
# from bonds_dj_app.local_classes.project_bonds_funcs import ProjectBondsFunctions
import noocube.funcs_general as FG

import sys
sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')
import settings_bdp_main as ms # общие установки для всех модулей
import math
from numbers import Integral, Real

from noocube.pandas_manager import PandasManager

from noocube.files_manager import FilesManager

import pandas as pd

from telegram_monitor.local_classes.book_library_funcs import BookLibraryFuncs

# from noocube.django_view_manager_v3 import DjangoViewManager_V3

from noocube.sqlite_pandas_processor_speedup import SqlitePandasProcessorSpeedup

from beeprint import pp

from telegram_monitor.local_classes.tg_local_funcs import TgLocalFuncs



class ColumnsFormattingBda ():
    """ 
    Формтирование, декорирование . калькулирование колонок в фрейме или в выходной таблице (если надо просто 
    отдекорировать формат вывода данных.)
    для модуля /home/ak/projects/P19_Bonds_Django/bonds_django_proj/bonds_dj_app  (bda - аббревиатура)
    Прим: Обертка для вывода отличается от калькулирования полей для функционального процессинга с колонкоами фрейма отличается лишь тем, в каком декораторе производится
    форматирование колонки. Если производить форматирование в декораторе типа @DecoratorsJangoCube.df_assoc_titles_and_calcs() -  то скалькулированные данные в колонах 
    будут использоваться или могут использоваться в функциональном процессинге с фреймом. А если применять на уровне декоратора подготовки таблицы где фрейм уже прошел все обработки,
    то это будет просто декоративное оформление колонок в выходнйо таблице !!!
    Поэтому предварительно нужно проанализировать для чего необходима форматирование коллонок фрейма и в соотвествии с этим определить в каком декораторе и в какой последовательности
    форматировать колонки фрейма
    """
    tlf = TgLocalFuncs()
    blf = BookLibraryFuncs()

    def __init__(self):
        pass
        self.blf = BookLibraryFuncs()
        self.spps = SqlitePandasProcessorSpeedup(ms.DB_CONNECTION)
        self.tlf = TgLocalFuncs()





        #### XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  PRJ_021  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX




    @staticmethod
    def html_for_img_entry_new_calc_col(row, inx, **dicThrough):
        """ 
        Сформировать код для вывода картинок в таблице на выходе на сайте из сохраненного пути источника , куда были скачены файлы картинок аудио-книг при
        первичной обработке канала CH_1 ("Аудиокниги фантастика")
        
        ОПИСАНИЕ АЛГОРИТМА ФОРМАТТЕРА:
        
        Первичный директорий-источник скачивания аудил-книг для канала CH_1 является: 
        ~ /media/ak/ADATA HD710/ARCHIVES_PROJECTS_MAIN_!!!!_FROM_11_01_2024/TELEGRAM_AUDIO_LIBRARIES/CHANNEL_ID_1
        И в БД корневым каталого является данный каталог
        Картинки из этого источника вторично были в полу-автоматическом режиме были скопированны во внутренний проектный директорий для канала CH_1 с таким адресом:
        ~ /home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django/telegram_monitor/static/telegram_monitor/audio_books/books_img_downloaded/ch_1
        
        Поэтому в данной функции необходимо взять полный путь первичного файла из БД из скрытого поля поступающего на вход форматтера фрейма,
        получить имя файла из этого пути, соединить его с вторичным проектным внутренним диреторием , обернуть полученынй адрес файла в HTML-формат 
        вывода картинки в колонке выходной тайблицы на сайте и выдать результат на выходе данной функции форматтера
        
        """
        
        # Исходный полный путь файла из первичного источника скачивания , который бурется из фрейма (а в фрейме он берется из БД)
        srcFilePath = row['HIDDEN__file_path'] 
        messageText = row['Текст_сообщения'] # Текст сообщения из телеграм канала CH_1
        
        x = ''
        
        # Вторичный внутренний проектный директорий для скаченных картинок сообщений канала CH_1
        insideProjCh1Dir = dicThrough['projImgsCh1Dir']
    
        if messageText == None: # Если в сообщении ТГ канада нет текста (то есть , это не сообщение с картинкой, а , скорее всего, аудио-том)
            x = '' # Текст в поле аудио-тома
            
        else:
            
            print(f"PR_A933 --> srcFilePath = {srcFilePath}")
            
            # Получить полный целевой для подобного файла теперь уже из вторичного внутреннего проектного директория для скаченных картинок сообщений канала CH_1
            imgFileName = FilesManager.get_file_name_from_path (srcFilePath) # Название файла из полног оадреса файла
            
            if srcFilePath == 'None':
                x = 'В БД в поле для названия файла присвоено строковое "None"'
                
            else:
            
                # Полный путь файла-картинки с именем из первичного источника в БД , но с рутовой директорией из вторичного внутреннего проектного каталога для картинок для канала CH_1 
                insideImgFileFullPath = insideProjCh1Dir + imgFileName
                
                print(f"PR_A171 --> insideImgFileFullPath = {insideImgFileFullPath}")
                
                # Обернутый в HTML-тэг файл картинки для показа ее в выходной таблице на сайте 
                x = f'<img src="{insideImgFileFullPath}" class="img-fluid aos-init aos-animate" alt="" data-aos="zoom-in">'
                
            
        # x = ''
        # x = f'<img src="{insideImgFileFullPath}" class="img-fluid aos-init aos-animate" alt="" data-aos="zoom-in">'

            
        return x





    @staticmethod
    def html_for_img_book_complects_column(row, inx, **dicThrough):
        """ 
        Сформировать код для вывода картинок в таблице на выходе на сайте из сохраненного пути источника , куда были скачены файлы картинок аудио-книг при
        первичной обработке канала CH_1 ("Аудиокниги фантастика")
        
        View: show_book_complects_formed_from_downloaded_tg_chat_messages()
        
        """
        
        
        
        # Исходный полный путь файла из первичного источника скачивания , который бурется из фрейма (а в фрейме он берется из БД)
        srcFilePath = row['HIDDEN__file_path'] 
        
        x = ''
        
        # Вторичный внутренний проектный директорий для скаченных картинок сообщений канала CH_1
        insideProjCh1Dir = dicThrough['projImgsCh1Dir']    
    

        # Получить полный целевой для подобного файла теперь уже из вторичного внутреннего проектного директория для скаченных картинок сообщений канала CH_1
        imgFileName = FilesManager.get_file_name_from_path (srcFilePath) # Название файла из полног оадреса файла
        
        if srcFilePath == 'None':
            x = 'В БД в поле для названия файла присвоено строковое "None"'
            
        else:
        
            # Полный путь файла-картинки с именем из первичного источника в БД , но с рутовой директорией из вторичного внутреннего проектного каталога для картинок для канала CH_1 
            insideImgFileFullPath = insideProjCh1Dir + imgFileName
            
            print(f"PR_A171 --> insideImgFileFullPath = {insideImgFileFullPath}")
            
            # Обернутый в HTML-тэг файл картинки для показа ее в выходной таблице на сайте 
            x = f'<img src="{insideImgFileFullPath}" class="img-fluid aos-init aos-animate" alt="" data-aos="zoom-in">'
            
            
        # x = ''
        # x = f'<img src="{insideImgFileFullPath}" class="img-fluid aos-init aos-animate" alt="" data-aos="zoom-in">'

            
        return x




    @staticmethod
    def book_complect_volumes_column(row, inx, **dicTrough):
        """ 
        Добавочная колонка с переченем аудио-томов книжного комплекта в таблице с книжными комплектами 
        View: show_book_complects_formed_from_downloaded_tg_chat_messages()
        """

        msgId = row['Mssg_ID']
        
        bookComplectVolumes = dicTrough['dicBookcomplectVolumes']
        
        if not isinstance(bookComplectVolumes, int) and msgId in bookComplectVolumes:
        
            listVolumesNames = bookComplectVolumes[msgId]
            
            listVolumesNames.sort() # Сортировка

            x = '<br>'.join(listVolumesNames)
            
        else: 
            
            x = ''

        
        
        return x







    @staticmethod
    def book_complects_add_column_author(row, inx, **dicTrough):
        """
        ColumnsFormattingBda
        Для форматтера : COLS_FORMATERS_FOR_BOOKS_COMPLEXTS , VIEW: show_downloaded_automatically_proccessed_books()
        ПРИМ: Словарь dicTrough['dicAlfaBookAuthors'] имеет формат: 'book_alfa_id' -> 'author_full_name'
        """
        
        print(f"PR_A445 --> START: book_complects_add_column_author()")
        
        alfaId = row['aid']
        
        print(f"PR_B221 --> alfaId = {alfaId}")
        
        if 'dicAlfaBookAuthors' in dicTrough and len(dicTrough['dicAlfaBookAuthors']) > 0:
        
            # Словарь с форматом: 'book_alfa_id' -> 'author_full_name'
            dicAlfaBookAuthors = dicTrough['dicAlfaBookAuthors']
            
            print(f"PR_B205 --> dicAlfaBookAuthors = ")
            pp(dicAlfaBookAuthors)
            
            
            if alfaId in dicAlfaBookAuthors:
                listAuthorFullNames = dicAlfaBookAuthors[alfaId]
            else:
                listAuthorFullNames = []
            
            # print(f"PR_A435 --> listAuthorFullNames = {listAuthorFullNames}")
            
            listAuthorFullNames.sort() # Сортировка
            

            y = '<br>'.join(listAuthorFullNames)
            
            # print(f"PR_A446 --> END: book_complects_add_column_author()")
            
        else:
            y = ''


        return y






    @staticmethod
    def book_complects_add_column_open_edit_page(row, inx, **fkwargs):
        """
        ColumnsFormattingBda
        Для форматтера : COLS_FORMATERS_FOR_BOOKS_COMPLEXTS , VIEW: show_downloaded_automatically_proccessed_books()

        """
        
        alfaId = row['aid']
        
        y = f'''<a tabindex="0" href="http://127.0.0.1:6070/telegram_monitor/edit_book_complect?alfa_id={alfaId}" target="_blank"  class="funcs_li" style="cursor:pointer"><img src="/static/telegram_monitor/imgs/edit.png"  class = "class1 classImg"   title="Редактировать" width="20" height="20"></a>'''

        
        return y



    # @staticmethod
    def book_complects_add_column_book_image(self, row, inx, **dicTrough):
        """
        ColumnsFormattingBda
        Для форматтера : COLS_FORMATERS_FOR_BOOKS_COMPLEXTS , VIEW: show_downloaded_automatically_proccessed_books()

        """
        
        # # Постоянная проектная составляющая пути до подпространства хранения картинок библиотеки, начиная со static
        fixedImgPath = dicTrough['fixedImgPath']
        
        
        
        print(f"PR_A388 --> fixedImgPath = {fixedImgPath}")
        
        alfaId = row[0]
        
        print(f'PR_A869 -->  alfaId = {alfaId}')
        
        
        print(f"PR_A868 -->  ")
        pp(dicTrough['dicAlfaBookImgsNames'])
        
        
        qnDicAlfaBookImgsNames = len(dicTrough['dicAlfaBookImgsNames'])
        
        
        print(f"PR_A870 --> dicTrough['dicAlfaBookImgsNames'] = {dicTrough['dicAlfaBookImgsNames']}")
        
        
        if alfaId in dicTrough['dicAlfaBookImgsNames'] and not 'ОШИБКА' in dicTrough['dicAlfaBookImgsNames'][alfaId][0]:
            
            
            print(f"PR_A871--> dicTrough['dicAlfaBookImgsNames'][alfaId][0] = {dicTrough['dicAlfaBookImgsNames'][alfaId][0]}")
        
            
            # Название файла с расширением
            imgName = dicTrough['dicAlfaBookImgsNames'][alfaId][0]
            
            # Относительный директорий файла в подмножестве, начиная с заданнйо фиксированной директории для картинок к книгам (fixedImgPath)
            relDir = dicTrough['dicAlfaBookImgsRelDirs'][alfaId][0]
            
            

            bookImgPathFull = f"{fixedImgPath}/{relDir}/{imgName}"
            
            # print(f"PR_A340 --> listBookDescrImgs = {listBookDescrImgs}")
            
            # x = f'''<a tabindex="0" data-isin="{x}"  class="funcs_li" style="cursor:pointer"  data-bs-toggle="popover"><img src="{bookImg}"  class = "class1 classImg"   title="Редактировать"></a>'''
            y = f'<a tabindex="0" href="http://127.0.0.1:6070/telegram_monitor/open_book_inf_page?alfa_id={alfaId}" target="_blank"  class="funcs_li" style="cursor:pointer"  data-bs-toggle="popover"><img src="{bookImgPathFull}" class="img-fluid aos-init aos-animate" alt="" data-aos="zoom-in"></a>'
            
        
        
        else:
        
            y = 'Какая-то ошибка с картинкой'
        
        
        return y






    # @staticmethod
    def prepare_params_for_edit_alfa_books_view (self, objAfterPagination):
        """ 
        Подготовить словарь с томами альфа-книг библиотеки и записать его в сквозной словарь dicThrough, который виден во всех форматерах
        Подготовка параметров для форматирования фрейма на базе постраничной выборки после пагинатора
        ПРИМ: запускается только один раз, при загрузке страницы (а не по каждой строке фрейма, как при форматировании). 
        ПРИМ: ВАЖНО !!! Любые полученные фреймы или иные массивы ниже в этом методе должны фильтроваться этим кортежем: tupleAlfaIds  с ids книг, 
        которые принадлежат подмножетву книг на текущей странице талицы (цель - ограничить передаваемые данные только теми элементами, коорые представлены 
        на текущей странице табюлицы, а не полным массивом подобных данных из таблиц БД !!!)
        FOR VIEW: show_downloaded_automatically_proccessed_books()
        RET:
        obj.dicThrough['dicAlfaBookVolumes'] - словарь с томами книг. Записать его в сквозной словарь dicThrough, который виден во всех форматерах
        """
        print(f"PR_A432 --> START: prepare_params_for_edit_alfa_books_view()")
        
        obj = objAfterPagination # Пока так, что бы название параметро сохраняло в себе суть (временно)
        
        dfPage = obj.dicThrough['df'] # странияный выходной фрейм после пагинатора
        
        # Получить кортеж tuple alfaIds из текущего страничного фрейма
        # Колонка, по которой нужно получить список из фрейма
        colName = 'aid' 
        
        # ПРИМ: ВАЖНО !!! Любые полученные фреймы ниже в этом методе должны фильтроваться этим кортежем с ids книг, которые принадлежат подмноеству книг на 
        # текущей странице талицы 
        # Кортеж alfa_ids книг, представленных на текущей странице таблицы сайта
        tupleAlfaIds = tuple(PandasManager.get_columns_vals_as_list_static(dfPage, colName))
        
        
        # print(f"PR_A431 --> dfPage = {dfPage}")
        
        # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfPage, True, colsIndxed = True, 
        #                                                     marker = "PR_A562 --> dfPage")

        # Избавляемя от запятой в тапле с сингулярным набором (если один элемент - конвертация в тапбл идет с запятой)
        if len(tupleAlfaIds) == 1:
            tupleAlfaIds = f"({tupleAlfaIds[0]})"
        

        # A. Подготовить параметры словаря книги-тома для сквозного словаря для дальнейшего форматирования фрейма 

        # Словарь книги-тома в размере только тех, которые проработал пагинатор для одной текущей выходной страницы с таблицей (max кол-во задается в установках пагинатора)
        dicAlfaBookVolumes = self.blf.get_lib_alfa_books_volumes_dic_sliced_with_keys_list (tupleAlfaIds)
        
        
        # передача словаря dicBookVolumes в сквозной словарь параметров
        obj.dicThrough['dicAlfaBookVolumes'] = dicAlfaBookVolumes
        
        # END A. Подготовить параметры словаря книги-тома для сквозного словаря для дальнейшего форматирования фрейма 
        
        
        # B. ПОдготовить параметры словаря книги-авторы. Записать его в сквозной словарь dicThrough, который виден во всех форматерах
        
        # Словарь книги-авторы в размере только тех, которые проработал пагинатор для одной текущей выходной страницы с таблицей (max кол-во задается в установках пагинатора)
        dicAlfaBookAuthors = self.blf.get_lib_alfa_books_authors_dic_filtered_by_keys_list(tupleAlfaIds)
        
        # передача словаря dicBookVolumes в сквозной словарь параметров
        obj.dicThrough['dicAlfaBookAuthors'] = dicAlfaBookAuthors
        
        # END B. ПОдготовить параметры словаря книги-авторы. Записать его в сквозной словарь dicThrough, который виден во всех форматерах

        
        # C. Данные о картинках к описаниям книг
        
        sql = f"""
                SELECT * FROM {ms.TB_LIB_BOOK_IMAGES} as lbi, {ms.TB_LIB_BOOKS_IMAGES}  as lbis 
                WHERE lbis.book_image_id = lbi.id AND lbis.book_alfa_id IN {tupleAlfaIds}
        """
        
        # Словарь с названиями файлов-картинок соответствующих alfaId
        dicAlfaBookImgsNames = self.spps.read_sql_to_dic_like_group_by_spps (sql, 'book_alfa_id', 'image_name') 
        obj.dicThrough['dicAlfaBookImgsNames'] = dicAlfaBookImgsNames
        
        # Словарь с относительными директориями файлов-картинок соответствующих alfaId
        dicAlfaBookImgsRelDirs = self.spps.read_sql_to_dic_like_group_by_spps (sql, 'book_alfa_id', 'relative_subdir') 
        obj.dicThrough['dicAlfaBookImgsRelDirs'] = dicAlfaBookImgsRelDirs
        
        
        # D. ПОдготоваить словарь со статусами для книг на табличной странице, типа {alfa_book_id : <список названий статусов, присвоенных книге>} для 
        # книг из текущей страницы, чьи alfaId находятся в tupleAlfaIds (id книг, которые выводятся на текущей странице выходной таблицы, или фрейма, соответствующему текущей странице)
        
        
        
        # Словарь книги-статусы в размере только тех, которые проработал пагинатор для одной текущей выходной страницы с таблицей (max кол-во задается в установках пагинатора)
        dicAlfaBookStatuses = self.blf.get_lib_books_statuses_dic_filtered_by_keys_list(tupleAlfaIds)
        
        # передача словаря dicBookVolumes в сквозной словарь параметров
        obj.dicThrough['dicAlfaBookStatuses'] = dicAlfaBookStatuses
        
        
        # Словарь книги-статусы в размере только тех, которые проработал пагинатор для одной текущей выходной страницы с таблицей (max кол-во задается в установках пагинатора)
        dicAlfaBookStatusesIds = self.blf.get_lib_books_statuses_ids_dic_filtered_by_keys_list(tupleAlfaIds)
        
        # передача словаря dicBookVolumes в сквозной словарь параметров
        obj.dicThrough['dicAlfaBookStatusesIds'] = dicAlfaBookStatusesIds
        
        
        
        
        # E. Составить словарь тех книг из предстваленных на текущей странице сайта (tupleAlfaIds), которые уже обладают статусом 'ALLOWED_TO_PUBLIC'
        
        # id статуса по его названию
        filterStatusId = self.blf.get_book_status_id_by_status_name_blf('ALLOWED_TO_PUBLIC')
        
        listBooksIdsWithAllowedPublishStatus = self.blf.filter_input_books_source_with_given_status_blf (tupleAlfaIds, filterStatusId)
        
        # print(f"PR_A572 --> listBooksIdsWithAllowedPublishStatus = {listBooksIdsWithAllowedPublishStatus}")

        obj.dicThrough['listBooksIdsWithAllowedPublishStatus'] = listBooksIdsWithAllowedPublishStatus
        
        
        # F. Составить словарь с никами телеграм-чатов. с которых была скачана книга (если источником книги был ТГ чат). то есть которые являлись источником книги
        
        dicBooksTgSourceChatNicks = self.blf.obtain_books_source_tg_chat_nicks_dic_filtered_by_keys_list(tupleAlfaIds)
        
        print(f"PR_A586 --> dicBooksTgSourceChatNicks = {dicBooksTgSourceChatNicks}")
        
        obj.dicThrough['dicBooksTgSourceChatNicks'] = dicBooksTgSourceChatNicks
        
        
        
        
        # G. ПОдготоваить словарь с категориями для книг на табличной странице, типа {alfa_book_id : <список названий категорий, присвоенных книге>} для 
        # книг из текущей страницы, чьи alfaId находятся в tupleAlfaIds (id книг, которые выводятся на текущей странице выходной таблицы, или фрейма, соответствующему текущей странице)

        # Словарь книги-статусы в размере только тех, которые проработал пагинатор для одной текущей выходной страницы с таблицей (max кол-во задается в установках пагинатора)
        dicAlfaBookCategories = self.blf.get_lib_books_categories_dic_filtered_by_keys_list(tupleAlfaIds)
        
        # передача словаря dicAlfaBookCategories в сквозной словарь параметров
        obj.dicThrough['dicAlfaBookCategories'] = dicAlfaBookCategories
        
        
        
        # h. ПОдготоваить словарь с дикторами для книг на табличной странице, типа {alfa_book_id : <список дикторов, присвоенных книге>} для 
        # книг из текущей страницы, чьи alfaId находятся в tupleAlfaIds (id книг, которые выводятся на текущей странице выходной таблицы, или фрейма, соответствующему текущей странице)

        # Словарь книги-статусы в размере только тех, которые проработал пагинатор для одной текущей выходной страницы с таблицей (max кол-во задается в установках пагинатора)
        dicAlfaBooksNarrators = self.blf.get_lib_books_narrators_dic_filtered_by_keys_list(tupleAlfaIds)
        
        # передача словаря dicAlfaBooksNarrators в сквозной словарь параметров
        obj.dicThrough['dicAlfaBooksNarrators'] = dicAlfaBooksNarrators
        
        
        
        
        
        
        

        print(f"PR_A433 --> END: prepare_params_for_edit_alfa_books_view()")
        
        
        
        
    # # @staticmethod
    # def prepare_params_for_VIEW_A001 (self, objAfterPagination):
    #     """ 
    #     Подготовить словарь с томами альфа-книг библиотеки и записать его в сквозной словарь dicThrough, который виден во всех форматерах
    #     Подготовка параметров для форматирования фрейма на базе постраничной выборки после пагинатора
    #     ПРИМ: запускается только один раз, при загрузке страницы (а не по каждой строке фрейма, как при форматировании). 
    #     ПРИМ: ВАЖНО !!! Любые полученные фреймы или иные массивы ниже в этом методе должны фильтроваться этим кортежем: tupleAlfaIds  с ids книг, 
    #     которые принадлежат подмножетву книг на текущей странице талицы (цель - ограничить передаваемые данные только теми элементами, коорые представлены 
    #     на текущей странице табюлицы, а не полным массивом подобных данных из таблиц БД !!!)
    #     FOR VIEW: show_downloaded_automatically_proccessed_books()
    #     RET:
    #     obj.dicThrough['dicAlfaBookVolumes'] - словарь с томами книг. Записать его в сквозной словарь dicThrough, который виден во всех форматерах
    #     """
        
        
    #     obj = objAfterPagination # Пока так, что бы название параметро сохраняло в себе суть (временно)
        
    #     dfPage = obj.dicThrough['df'] # странияный выходной фрейм после пагинатора
        
        
    #     # print(f"PR_B295 --> dfPage = {dfPage}")
        
        
    #     # Получить кортеж tuple alfaIds из текущего страничного фрейма
    #     # Колонка, по которой нужно получить список из фрейма
    #     colName = 'tbid' 
        
    #     # ПРИМ: ВАЖНО !!! Любые полученные фреймы ниже в этом методе должны фильтроваться этим кортежем с ids книг, которые принадлежат подмноеству книг на 
    #     # текущей странице талицы 
    #     # Кортеж alfa_ids книг, представленных на текущей странице таблицы сайта
    #     tupleAlfaIds = tuple(PandasManager.get_columns_vals_as_list_static(dfPage, colName))
        
        
    #     print(f"PR_A431 --> dfPage = {dfPage}")
        
    #     # PandasManager.print_df_gen_info_pandas_IF_DEBUG_static(dfPage, True, colsIndxed = True, 
    #     #                                                     marker = "PR_A562 --> dfPage")

    #     # Избавляемя от запятой в тапле с сингулярным набором (если один элемент - конвертация в тапбл идет с запятой)
    #     if len(tupleAlfaIds) == 1:
    #         tupleAlfaIds = f"({tupleAlfaIds[0]})"
        
        
    #     # 1. Словарь ссылок на источник в зависимости от tbid сообщения
    #     dicMessagesSourcesLinks = self.blf.get_source_links_dic_sliced_with_mssg_ids_list (tupleAlfaIds)
        
        
        
        
        




    @staticmethod
    def lib_alfa_books_add_column_volumes(row, inx, **dicTrough):
        """
        ColumnsFormattingBda
        Для форматтера : COLS_FORMATERS_FOR_BOOKS_COMPLEXTS , 
        VIEW: show_downloaded_automatically_proccessed_books()
        """
        # 
        
        print(f"PR_A438 --> START: lib_alfa_books_add_column_volumes()")
        
        alfaId = row['aid']
        
        bookAlfaVolumes = dicTrough['dicAlfaBookVolumes']
        
        print(f"PR_A668 --> bookAlfaVolumes = {bookAlfaVolumes}")
        
        if not isinstance(bookAlfaVolumes, int) and  alfaId in bookAlfaVolumes:
        
            listVolumesNames = bookAlfaVolumes[alfaId]
            
            print(f"PR_A435 --> listVolumesNames = {listVolumesNames}")
            
            listVolumesNames.sort() # Сортировка
            
            # Вычленить название тома от маркеров и расширения в названии файла
            listVolumesNames = [x.split('_')[0] for x in listVolumesNames] 

            x = '<br>'.join(listVolumesNames)
            
        else:
            
            x = ''
        
        print(f"PR_A439 --> END: lib_alfa_books_add_column_volumes()")

        
        return x











    @staticmethod
    def book_complects_add_column_book_statuses(row, inx, **dicTrough):
        """
        ColumnsFormattingBda
        добавить колонку со статусами книги
        VIEW: show_lib_books_to_allow_public_repositories_downloading()
        """
        # 
        
        print(f"PR_A551 --> START: book_complects_add_column_book_statuses()")
        
        alfaId = row['aid']
        
        # dicAlfaBookStatuses = dicTrough['dicAlfaBookStatuses']
        
        # listStatusesNames = dicAlfaBookStatuses[alfaId]
        
        dicAlfaBookStatusesIds = dicTrough['dicAlfaBookStatusesIds']
        
        listStatusesIds = dicAlfaBookStatusesIds[alfaId]
        
        # print(f"PR_A435 --> listVolumesNames = {listVolumesNames}")
        
        listStatusesIds.sort() # Сортировка
        
        listStatusesIds = [str(x) for x in listStatusesIds]
        
        # # Вычленить название тома от маркеров и расширения в названии файла
        # listVolumesNames = [x.split('_')[0] for x in listVolumesNames] 

        x = '<br>'.join(listStatusesIds)
        
        print(f"PR_A552 --> END: book_complects_add_column_book_statuses()")

        
        return x







    @staticmethod
    def book_complects_add_column_book_categories(row, inx, **dicTrough):
        """
        ColumnsFormattingBda
        добавить колонку с категориями книги
        VIEW: show_lib_books_to_allow_public_repositories_downloading()
        """
        # 
        
        print(f"PR_A769 --> START: book_complects_add_column_book_statuses()")
        
        alfaId = row['aid']
        
        dicAlfaBookCategories = dicTrough['dicAlfaBookCategories']
        
        if alfaId in dicAlfaBookCategories:
        
            listBookCategories = dicAlfaBookCategories[alfaId]
            
        else:
            
            listBookCategories = []
        
        # print(f"PR_A435 --> listVolumesNames = {listVolumesNames}")
        
        listBookCategories.sort() # Сортировка
        
        # # Вычленить название тома от маркеров и расширения в названии файла
        # listVolumesNames = [x.split('_')[0] for x in listVolumesNames] 

        y = ',<br>'.join(listBookCategories)
        
        # JS136^^ -  открыть редактор категорий при нажатии на поле в таблице с перечнем категорий         
        x = f'<div class="tbrd_edit_categ_view01" balfa_id = {alfaId}>{y}</dix>' 
        
        print(f"PR_A770 --> END: book_complects_add_column_book_statuses()")

        
        return x






    @staticmethod
    def book_complects_add_column_book_narrators(row, inx, **dicTrough):
        """
        ColumnsFormattingBda
        добавить колонку с  дикторами книги
        VIEW: show_lib_books_to_allow_public_repositories_downloading()
        """
        # 
        
        print(f"PR_A771 --> START: book_complects_add_column_book_statuses()")
        
        alfaId = row['aid']
        
        dicAlfaBooksNarrators = dicTrough['dicAlfaBooksNarrators']
        
        if alfaId in dicAlfaBooksNarrators:
        
            listBookNarrators = dicAlfaBooksNarrators[alfaId]
            
        else:
            
            listBookNarrators = []
        
        # print(f"PR_A435 --> listVolumesNames = {listVolumesNames}")
        
        listBookNarrators.sort() # Сортировка
        
        # # Вычленить название тома от маркеров и расширения в названии файла
        # listVolumesNames = [x.split('_')[0] for x in listVolumesNames] 

        x = ',<br>'.join(listBookNarrators)
        
        print(f"PR_A772 --> END: book_complects_add_column_book_statuses()")

        
        return x










    @staticmethod
    def book_complects_add_column_publish_checkboxes(row, inx, **dicThrough):
        """
        ColumnsFormattingBda
        Добавить колонку с  checkbox для добавления статуса с разрешением на публикацию во внешних репозиториях
        VIEW: show_lib_books_to_allow_public_repositories_downloading()
        """
        # 
        
        print(f"PR_A554 --> START: book_complects_add_column_publish_checkboxes()")
        
        alfaId = row['aid']
        
        # список alfaIds тех книг из предстваленных на текущей странице сайта (tupleAlfaIds), которые уже обладают статусом 'ALLOWED_TO_PUBLIC' для выделения checkbox
        listBooksIdsWithAllowedPublishStatus = dicThrough['listBooksIdsWithAllowedPublishStatus'] 
        
        # выделяем checkbox selected , если текущая alfaId входит в список книг со статусом 'ALLOWED_TO_PUBLIC'
        if alfaId in listBooksIdsWithAllowedPublishStatus:
            checked = 'checked'
        else:
            checked = ''
        
        x = f'<input type="checkbox" class="chb_allow_to_publick" name="allow_to_publick_{alfaId}" value="{alfaId}" {checked}>'
        
        print(f"PR_A555 --> END: book_complects_add_column_publish_checkboxes()")

        
        return x







    @staticmethod
    def book_complects_add_column_open_src_tg_message(row, inx, **dicThrough):
        """
        ColumnsFormattingBda
        Открыть сайт телеграма с текущим по ряду в таблице сообщением
        Для форматтера : COLS_FORMATERS_FOR_BOOKS_COMPLEXTS , VIEW: show_downloaded_automatically_proccessed_books()

        """
        
        alfaId = row['aid']
        
        # словарь с никами телеграм-чатов. с которых была скачана книга
        dicBooksTgSourceChatNicks = dicThrough['dicBooksTgSourceChatNicks'] 
        
        srcTgchatNick = dicBooksTgSourceChatNicks[alfaId]
        
        tgMssgId = row['HIDDEN__mssgId']
        
        tgSrclink = f"https://t.me/{srcTgchatNick}/{tgMssgId}"
        
        
        
        
        y = f'''<a tabindex="0" href="{tgSrclink}" target="_blank"  class="funcs_li" style="cursor:pointer"  data-bs-toggle="popover"><img src="/static/telegram_monitor/imgs/tg1.png"  class = "class1 classImg"   title="Источник в ТГ" width="20" height="20"></a>'''

        
        return y




    @staticmethod
    def book_complects_add_icon_delete(row, inx, **dicThrough):
        """
        ColumnsFormattingBda
        добавить иконку со значком удалить и при нажатии Удалить обьект из библиотечных функциональных таблиц в тебл lib_objects_removed исторических архивов 
        по кдаленным обьектам 
        
        Для форматтера : COLS_FORMATERS_FOR_BOOKS_COMPLEXTS , VIEW: show_downloaded_automatically_proccessed_books()

        """
        
        alfaId = row['aid']
        
        
        
        
        # JS137^^
        y = f'''<img src="/static/telegram_monitor/imgs/delete1.png"  alfa_id="{alfaId}" class = "class1 del_reg_book_complect" style="cursor:pointer"  title="Источник в ТГ" width="20" height="20">''' 

        
        return y







    @staticmethod
    def book_complects_add_icon_book_volumes(row, inx, **dicThrough):
        """
        JS141^^
        ColumnsFormattingBda
        добавить иконку для показа списка всех аудио-томов , принадлежащих текущему описанию книги
        
        Для форматтера : COLS_FORMATERS_FOR_BOOKS_COMPLEXTS , VIEW: show_downloaded_automatically_proccessed_books()

        """
        
        alfaId = row['aid']
        
        
        
        y = f'''<img src="/static/telegram_monitor/imgs/doubles2.png"  alfa_id="{alfaId}" class = "class1 show_book_volums_icon " style="cursor:pointer"  title="Аудио-тома книги JS141^^" width="20" height="20">''' 


        # y = """
        #     <button id="opener" class="opener">Open Dialog</button>
        # """

        
        return y








    @staticmethod
    def lib_add_download_icon(row, inx, **dicThrough):
        """
        ColumnsFormattingBda
        добавить иконку для повтора загрузки отдельного сообщения (который был скоррее всего загружен с ошибкой по тому или иному признаку)
        
        Для View : : check_errors_in_downloaded_messages()

        """
        
        mpid = row['mpid']
        
        
        
        y = f'''<img src="/static/telegram_monitor/imgs/transfer2.png"  mpid="{mpid}" class = "class1 reload_message_icon" style="cursor:pointer"  title="Перезагрузить сообщение" width="20" height="20">''' 


        # y = """
        #     <button id="opener" class="opener">Open Dialog</button>
        # """

        
        return y







    @staticmethod
    def lib_add_hidden_color_col(row, inx, **dicThrough):
        """
        ColumnsFormattingBda
        Добавить колонку для управления цветом ряда
        Цветовая дифференциация рядов таблицы
        
        Для View : : check_errors_in_downloaded_messages()

        """
        # INI
        # mpid = row['mpid']
        statusId = row['Ст id']
        volumeName = row['MP3']
        # image = row['Image']
        
        # id сатус сообщения из табл 'tg_message_proc_statuses' : 2 и 5 - сообщения с ошибками
        # Если статус сообщения = 5 (за исключением тех сообщений, которые - пустышки с фрагментом в названии 'ждем следующий том') ('DOCUMENT_DOWNLOADING_ERROR_')
        if statusId == 5 and volumeName and not ('ждем следующий том' in volumeName):
            y = "row_color_error_doc_downloaded" #  дифф класс цвета ряда
        # Если статус сообщения = 2 ('IMAGE_DOWNLOADING_ERROR_')
        elif statusId == 2:
            y = "row_color_error_img_downloaded" #  дифф класс цвета ряда
            
        else:
            y = "row_color_fine_downloaded" #  дифф класс цвета ряда
        
        
        
        
        


        # y = """
        #     <button id="opener" class="opener">Open Dialog</button>
        # """

        
        return y







    @staticmethod
    def lib_add_message_id_column (row, inx, **dicThrough):
        """
        ColumnsFormattingBda
        добавить колонку message id 
        
        Для View : : check_errors_in_downloaded_messages()

        """
        
        msid = row['HIDDEN__mssgId']
        
        
        return msid




    @staticmethod
    def add_message_tg_link_column_VIEW_A001 (row, inx, **dicThrough):
        """
        ColumnsFormattingBda
        добавить колонку tgLink - ссылка на данное сообщение в оригинальном тг-канале
        """
        
        msid = row['tbid']
        
        tgMssgId = row['Mssg_ID']
        
        srcLink = row['HIDDEN__src_link']
        
        mssgSrcLink = f"{srcLink}/{tgMssgId}"
        
        y = f'''<a tabindex="0" href="{mssgSrcLink}" target="_blank"  class="funcs_li" style="cursor:pointer"><img src="/static/telegram_monitor/imgs/tg1.png"  class = ""   title="Источник в ТГ" width="20" height="20"></a>'''

        
        return y






    @staticmethod
    def add_column_publish_checkboxes_VIEW_A001(row, inx, **dicThrough):
        """
        ColumnsFormattingBda
        Добавить колонку с  checkbox для удаления сообщения
        VIEW: show_downloqded_tg_messages_with_logic_errors()
        """
        # 
        
        print(f"PR_B297 --> START: add_column_publish_checkboxes_VIEW_A001()")
        
        mssg_tbid = row['tbid']
        

        
        x = f'<input type="checkbox" class="chb_mssg_execute_va001" name="mssg_delete_{mssg_tbid}" value="{mssg_tbid}">'
        
        print(f"PR_B298 --> END: add_column_publish_checkboxes_VIEW_A001()")

        
        return x










        ##### XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  END PRJ_021  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX














if __name__ == '__main__':
    pass

    






















