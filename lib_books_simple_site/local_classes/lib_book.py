# import sys
# sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')
# import settings_bdp_main as ms # общие установки для всех модулей

from telegram_monitor.local_classes.book_library_funcs import BookLibraryFuncs
from beeprint import pp

from telegram_monitor.local_classes.lib_audio_volume import LibAudioVolume

from telegram_monitor.local_classes.log_manager import LogManager

import json




# Глобальная переменная
blf = BookLibraryFuncs()

class LibBook ():
    """ 
    Класс: книга в библиотеке
    """
    

    
    def __init__(self, bookAlfaId = None, bookMessageId = None, jsonBookObj = None):
        pass
    
        self.lm = LogManager()
    
        dicLibBookData = {}
    
        if bookAlfaId:
            dicLibBookData = blf.get_dic_of_full_book_data_by_alfa_id_blf(bookAlfaId)
            
        if bookMessageId:
            dicLibBookData = blf.get_dic_of_full_book_data_by_message_id_blf(bookMessageId)
            
        # Если обьект создается на бавзе JSON    
        if jsonBookObj:
            
            if isinstance(jsonBookObj, str):
                dicLibBookData =  json.loads(jsonBookObj)
            elif isinstance(jsonBookObj, dict):
                dicLibBookData = jsonBookObj
            
    
    
        # Флаг сохранения JSON-обьекта в файле. В случае вывления каких-то логических ошибок в обьекте, которые доказывают, 
        # что это не обьект книга с аудио-томами, этот флаг устанавливается в False и тогда этот обьект не будет сохранен в файле как json-обьект
        self.flagSaveJsonObj = False


        # self.dicLibBookData = dicLibBookData
    
        # A. Берем характеристические данные по обьекту и фиксируем их в собственных переменных из таблиц 'lib_books_alfa' и 'lib_books_alfa_ext'
        
        # ТАБЛИЦА 'lib_books_alfa'
        self.id = dicLibBookData['id']
        
        self.liter_group_z = dicLibBookData['liter_group_z']
        
        self.liter_group_y = dicLibBookData['liter_group_y']
        
        self.liter_group_x = dicLibBookData['liter_group_x']
        
        self.final_ilbn = dicLibBookData['final_ilbn']
        
        self.date_reg_calend = dicLibBookData['date_reg_calend']
        
        self.date_reg_unix = dicLibBookData['date_reg_unix']
        
        
        # TODO: Расшифровать с названием btype_creation_id
        self.btype_creation_id = dicLibBookData['btype_creation_id']
        
        self.parent_book_id = dicLibBookData['parent_book_id']
        
        self.child_part_order = dicLibBookData['child_part_order']
        
        # TODO: Проверить, там два serial_id выходят
        self.serial_id = dicLibBookData['serial_id']
        
        # END ТАБЛИЦА 'lib_books_alfa'
        
        
        
        
        # ТАБЛИЦА 'lib_books_alfa_ext'
        # Если обьект создается на бавзе JSON
        if bookAlfaId or bookMessageId:
            self.book_tb_ext_id = dicLibBookData['id_1'] # id в таблице 'lib_books_alfa_ext'
        elif jsonBookObj:
            self.book_tb_ext_id = dicLibBookData['book_tb_ext_id']
            
        
        self.books_alfa_id = dicLibBookData['books_alfa_id']
        
        self.book_title = dicLibBookData['book_title']
        
        self.book_description = dicLibBookData['book_description']
        
        self.book_message_id = dicLibBookData['book_message_id']
        
        
        self.book_orig_source_id = dicLibBookData['book_orig_source_id']
        
        
        if bookAlfaId or bookMessageId:
            origSourceTgChannelid = blf.get_book_original_source_tg_channel_id_by_tbid_blf(self.book_orig_source_id)
            self.book_orig_source_tg_channel_id = origSourceTgChannelid
        # Если обьект создается на бавзе JSON
        elif jsonBookObj:
            self.book_orig_source_tg_channel_id = dicLibBookData['book_orig_source_tg_channel_id']
        
        
        
        
        self.date_issue_calend = dicLibBookData['date_issue_calend']
        
        self.date_issue_unix = dicLibBookData['date_issue_unix']
        
        self.language_id = dicLibBookData['language_id']
        
        self.serial_id = dicLibBookData['serial_id']

        self.language_relation_id = dicLibBookData['language_relation_id']
        
        # END ТАБЛИЦА 'lib_books_alfa_ext'
        
        

        # ТАБЛИЦА 'lib_book_authors' и 'lib_authors'
        # B. Прописываем авторов книги из 'lib_book_authors' и 'lib_authors'
        if bookAlfaId or bookMessageId:
            
            listBookAuthors = blf.get_authors_of_book_by_alfa_id(self.books_alfa_id)
            if not isinstance(listBookAuthors, int):
                listBookAuthorsIds = [x[1] for x in listBookAuthors]
            else:
                listBookAuthorsIds = []
                
            self.lib_books_authors = listBookAuthorsIds
            
            if not isinstance(listBookAuthors, int):
                listBookAuthorsFIO = [x[-1] for x in listBookAuthors]
            else:
                listBookAuthorsFIO = []
                
            self.lib_authors_fio = listBookAuthorsFIO
            
        # Если обьект создается на бавзе JSON
        elif jsonBookObj:
            
            self.lib_authors_fio = dicLibBookData['lib_authors_fio']
            
        # END ТАБЛИЦА 'lib_book_authors' и 'lib_authors'
            
            
        
        # C.  Прописываем  статусы книги из 'lib_books_statuses' 
        if bookAlfaId or bookMessageId:
            listBookStatuses = blf.get_book_statuses_by_alfa_id(self.books_alfa_id)
            listBookStatusesIds = [x[1] for x in listBookStatuses]
            self.lib_books_statuses = listBookStatusesIds
            listBookStatusesNames = [x[-1] for x in listBookStatuses]
            self.lib_books_statuses_names = listBookStatusesNames
            
        # Если обьект создается на бавзе JSON
        elif jsonBookObj:
            self.lib_books_statuses_names = dicLibBookData['lib_books_statuses_names']
            




        # ТАБЛИЦА 'lib_books_images'  
        # D. Прописываем картинки описания книги из 'lib_books_images'  
        if bookAlfaId or bookMessageId:
            # listBookImages = blf.get_book_descr_images_by_alfa_id_for_book_object_creation_blf(self.books_alfa_id)
            dfBookImages = blf.get_df_book_descr_images_by_alfa_id_for_book_object_creation_blf(self.books_alfa_id)
            # listBookImagesIds = [x[1] for x in listBookImages]
            listBookImagesIds = list(dfBookImages['book_image_id'])
            self.lib_books_images = listBookImagesIds
            # listBookImagesFileNames = [x[-2] for x in listBookImages]
            listBookImagesFileNames = list(dfBookImages['image_name'])
            self.lib_book_images = listBookImagesFileNames
            
            orig_source_id = list(dfBookImages['orig_source_id'])
            self.orig_source_id = orig_source_id
            
            tg_message_id = list(dfBookImages['tg_message_id'])
            self.tg_message_id = tg_message_id
            
            
        # Если обьект создается на бавзе JSON
        elif jsonBookObj:
            self.lib_book_images = dicLibBookData['lib_book_images']

        # END ТАБЛИЦА 'lib_books_images'  
        
        
        
        
        # E.  Прописываем выгрузки книги в наших ТГ- репозиториях 'lib_books_loaded_to_repositories'  
        if bookAlfaId or bookMessageId:

            listBookDRepositoriesDownloadedTo = blf.get_our_repositories_where_book_downloaded_to_by_alfa_id_blf(self.books_alfa_id)
            
            if not isinstance(listBookDRepositoriesDownloadedTo, int):
            
                listBookDRepositoriesDownloadedToIds = [x[1] for x in listBookDRepositoriesDownloadedTo]
                self.lib_books_loaded_to_repositories = listBookDRepositoriesDownloadedToIds
                listBookDRepositoriesDownloadedToTgChannelId = [x[-4] for x in listBookDRepositoriesDownloadedTo]
                # Наши ТГ репозитории
                self.lib_repositories = listBookDRepositoriesDownloadedToTgChannelId
                
            else: 
                
                self.lib_books_loaded_to_repositories = None
                self.lib_repositories = None
            
        # Если обьект создается на бавзе JSON
        elif jsonBookObj:
            self.lib_books_loaded_to_repositories = dicLibBookData['lib_books_loaded_to_repositories']
            self.lib_repositories = dicLibBookData['lib_repositories']

        
        
        
        # F.  Прописываем дикторов книги 'lib_books_narrators'   
        if bookAlfaId or bookMessageId:

            listBookNarrators = blf.get_narrators_of_book_by_alfa_id(self.books_alfa_id)
            
            if not isinstance(listBookNarrators, int):
            
                listBookNarratorsIds = [x[1] for x in listBookNarrators]
                
                self.lib_books_narrators = listBookNarratorsIds
                
                listBookDRepositoriesDownloadedToTgChannelFIO = [x[-1] for x in listBookNarrators]

                # Наши ТГ репозитории
                self.lib_narrators = listBookDRepositoriesDownloadedToTgChannelFIO
                
            else: 
                
                self.lib_books_narrators = None
                self.lib_narrators = None
            
        # Если обьект создается на бавзе JSON
        elif jsonBookObj:
            self.lib_books_narrators = dicLibBookData['lib_books_narrators']
            self.lib_narrators = dicLibBookData['lib_narrators']

        
        
        
        # G. Прописываем категории книги 'lib_books_categories'   
        if bookAlfaId or bookMessageId:

            listBooksCategories = blf.get_book_categories_by_alfa_id(self.books_alfa_id)
            
            if not isinstance(listBooksCategories, int):
            
                listBooksCategoriesIds = [x[1] for x in listBooksCategories]
                
                
                self.lib_books_categories = listBooksCategoriesIds
                
                
                listBooksCategoriesNames = [x[-1] for x in listBooksCategories]

                # Наши ТГ репозитории
                self.lib_categories = listBooksCategoriesNames
                
            else: 
                
                self.lib_books_categories = None
                self.lib_categories = None
            
        # Если обьект создается на бавзе JSON
        elif jsonBookObj:
            self.lib_books_categories = dicLibBookData['lib_books_categories']
            self.lib_categories = dicLibBookData['lib_categories']

        
        
        # I.  Прописываем обьекты аудио-томов книги, по alfa_id книги    CURR
        
        
        if bookAlfaId or bookMessageId:
        
            listBookAudioVolumesTbids = blf.get_book_volumes_tbids_list_by_alfa_id_blf(self.books_alfa_id)
            
            bookAudioVolumes = []
            
            if not isinstance(listBookAudioVolumesTbids, int):
                
                for bookVolumTbidFull in listBookAudioVolumesTbids:
                    
                    bookVolumTbid = bookVolumTbidFull[1]
                
                    lBookVolumeObj = LibAudioVolume(volumeTbId = bookVolumTbid)
                    
                    bookAudioVolumes.append(lBookVolumeObj)
                    
            # Если запрос не вернул listBookAudioVolumesTbids как список, это значит, что у книги нет аудио-томов. Этого система просто так пропустить не 
            # может. Логируем ошибку как логическую ошибку библиотеки labba
            else:
                
                errMessage = f"""PR_B260 --> SYS LOG: Система обнаружела ллогическую ошибку в пространстве библиотеки  LABBIE. 
                            Обнаружена сообщение типа картинка-описание книги с id = {bookAlfaId}, у которой нет аудио-томов. Скорее всего - это псевдо-книга"""
                print(errMessage)
                
                # Сохранить информацию о логической ошибке в лог-файле
                self.lm.log_labba_logic_errors_lm(errMessage, 'PR_B260')
                
                
                
                # Флаг сохранения JSON-обьекта в файле
                self.flagSaveJsonObj = False
                    
        elif jsonBookObj:
            
            bookAudioVolumes = []        
                
            # Сисок Джейсон-словарей аудио-томов книги для класса LibAudioVolume (уже преобразованных в словари ?)
            listJsonBookVolumesDics = dicLibBookData['lib_book_audio_volumes']
                
            for jsonBookVolumesDic in listJsonBookVolumesDics:
                
            
                lBookVolumeObj = LibAudioVolume(jsonBookVolumeObj = jsonBookVolumesDic)
                
                bookAudioVolumes.append(lBookVolumeObj)
                
                
                
                
        
        self.lib_book_audio_volumes = bookAudioVolumes
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
























if __name__ == '__main__':
    pass


    # # # # ПРОРАБОТКА: проверка обьекта класса
    
    # bookAlfaId = 4528
    
    # lBook = LibBook(bookMessageId = bookAlfaId)
    
    # print(f"PR_B080 --> ")
    # pp(lBook)
    
    # print(f"PR_B083 --> ")
    # pp(lBook.lib_book_audio_volumes[0].volume_message_id)
    
    


    # ПРОРАБОТКА: Дампинг обьекта в JSON
    # ~ https://www.pythonforbeginners.com/basics/custom-json-encoder-in-python#htoc-create-custom-json-encoder-using-the-default-parameter
    
    bookAlfaId = 4528
    
    lBook = LibBook(bookMessageId = bookAlfaId)
    
    # print(f"PR_B080 --> ")
    # pp(lBook)
    


    import json

    class ComplexEncoderClass(json.JSONEncoder):
            def default(self, obj):
                objDict=obj.__dict__
                typeDict={"__type__":type(obj).__name__} # Задаем тип для выделения сложных обьектов вложенных от главного обьекта
                return {**objDict,**typeDict}
        
        
        
    json_str = json.dumps(lBook, cls=ComplexEncoderClass)

    print(json_str)
    # pp(json_str)








