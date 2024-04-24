

import sys
sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')

from telegram_monitor.local_classes.book_library_funcs import BookLibraryFuncs
from beeprint import pp

import json

# Глобальная переменная
blf = BookLibraryFuncs()


class LibAudioVolume ():
    """ 
    Класс: аудио-том книги в библиотеке
    """



    def __init__(self, volumeTbId = None, volumeMessageId = None, jsonBookVolumeObj = None):
        pass


        dicLibBookData = {}
    
        if volumeTbId:
            dicLibVolumeData = blf.get_dic_of_full_volume_data_by_alfa_id_blf(volumeTbId)
            
        if volumeMessageId:
            dicLibVolumeData = blf.get_dic_of_full_volume_data_by_message_id_blf(volumeMessageId)
    
    
        # Если обьект создается на бавзе JSON    
        if jsonBookVolumeObj:
            
            if isinstance(jsonBookVolumeObj, str):
                dicLibVolumeData =  json.loads(jsonBookVolumeObj)
            elif isinstance(jsonBookVolumeObj, dict):
                dicLibVolumeData = jsonBookVolumeObj
    
        # self.dicLibVolumeData = dicLibVolumeData




        # A. Прописываем данные обьекта по таблице 'lib_book_audio_volumes' 
        
        self.id = dicLibVolumeData['id']
        
        self.books_alfa_id = dicLibVolumeData['books_alfa_id']
        
        self.volume_file_name = dicLibVolumeData['volume_file_name']
        
        self.volume_order = dicLibVolumeData['volume_order']
        
        self.volume_descr = dicLibVolumeData['volume_descr']
        
        self.volume_photo = dicLibVolumeData['volume_photo']
        
        self.date_reg_calend = dicLibVolumeData['date_reg_calend']
        
        self.date_reg_unix = dicLibVolumeData['date_reg_unix']


        self.date_issue_calend = dicLibVolumeData['date_issue_calend']
        
        self.date_issue_unix = dicLibVolumeData['date_issue_unix']
        
        self.volume_message_id = dicLibVolumeData['volume_message_id']
        
        # TODO: Расшифровать с названием btype_creation_id
        self.btype_creation_id = dicLibVolumeData['btype_creation_id']
        
        self.volume_title = dicLibVolumeData['volume_title']
        
        
        self.source_id = dicLibVolumeData['source_id']
        
        
        # Если обьект создается на бавзе JSON
        if volumeTbId or volumeMessageId:
            origSourceTgChannelid = blf.get_book_original_source_tg_channel_id_by_tbid_blf(self.source_id)
            self.source_tg_channel_id = origSourceTgChannelid
        elif jsonBookVolumeObj:
            self.source_tg_channel_id = dicLibVolumeData['source_tg_channel_id']













if __name__ == '__main__':
    pass


    # # # ПРОРАБОТКА: проверка обьекта класса
    
    bookvolumeTbId = 4547
    
    lVolume = LibAudioVolume(volumeMessageId = bookvolumeTbId)
    
    print(f"PR_B081 --> ")
    pp(lVolume)
    
    







