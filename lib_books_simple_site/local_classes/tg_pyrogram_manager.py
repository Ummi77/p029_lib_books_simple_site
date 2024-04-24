
import sys
sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')
import settings_bdp_main as ms # общие установки для всех модулей


import asyncio

from pyrogram import Client

from noocube.switch import Switch


from telegram_monitor.local_classes.book_library_funcs import BookLibraryFuncs

from pyrogram.types import InputMediaPhoto, InputMediaVideo


import time

# from telegram.constants import ParseMode


class TgPyrogramManager ():
    """
    Класс для  Payogram API Client bot manager
    ~ https://docs.pyrogram.org/intro/quickstart
    ~ https://docs.pyrogram.org/api/methods/send_audio#pyrogram.Client.send_audio
    ~ https://docs.pyrogram.org/api/methods/
    """

    def __init__(self, auth = {}, dicThrough={}):
        pass
        
    

    @staticmethod
    async def pyrogram_start_func_marker_differenciator_tpm (mFunc : str, **dicThrowgh):
        """ 
        TgPyrogramManager
        Запустить заданную функцию (метод) в контексте Pyogram, используя дифференциатор Switch по маркеру заданного на запуск метода mFunc
        mFunc - маркер задаваемого на реализацию метода
        """
        
        async with Client(*ms.AUTH_PYROGRAM_CLIENT) as app:
            
            # Дифференциатор по маркеру метода
            for case in Switch(mFunc):
                
                # RUN METHOD: Отправка локального аудиj-файла в чат заданного ТГ-канала
                if case('send_audio'): 
                
                    chat = -1001811098741 # Моя библиотека
                        
                    
                    fileRoot = '/media/ak/Transcend1/GENERAL_ARCHIVE_EXTERNAL_DISC_FROM_01_02_2024_CURRENT_MAIN/TELEGRAM_AUDIO_LIBRARIES/CHANNEL_ID_1'

                    fileName = '19. ждем книгу.mp3'
                    # fileName = '3. Эндшпиль.mp3' # > 50Mb
                    # fileName = '3. Endshpil.mp3'
                    
                    # caption = '3. Endshpil'

                    file = f"{fileRoot}/{fileName}"
                    
                    dicThrowgh = {
                        'caption' : "audio caption",
                    }
                    
                    TgPyrogramManager.send_audio_tpm(chat, file, **dicThrowgh)
                
                    break

                if case(): # default
                    print('Другое число')
                    break




    @staticmethod
    def send_audio_tpm (chat, fileAudio, **dicThrowgh):
        """ 
        TgPyrogramManager
        Отправить сообщение с аудио-файлом в ТГ-канал
        Параметры подобны параметрам метода send_audio() из Pyogram фреймворка: ~ https://docs.pyrogram.org/api/methods/send_audio
        """
        
        async def func():
            async with Client(*ms.AUTH_PYROGRAM_CLIENT) as app:
                
                await app.send_audio(chat, fileAudio, **dicThrowgh)
                
                # print(f"PR_A605 --> info = {info}")

        asyncio.run(func())
        
        
        
        
    @staticmethod
    def send_media_group_tpm (chat, listMediaGroup : list, **dicThrowgh):
        """ 
        TgPyrogramManager
        Отправить сообщение с  медиа группой в ТГ-канал
        В группе могуь быть любые сущности следующих типов: InputMediaPhoto, InputMediaVideo, InputMediaAudio and InputMediaDocument)
        Параметры подобны параметрам метода send_audio() из Pyogram фреймворка: ~ https://docs.pyrogram.org/api/methods/send_media_group
        ПРИМ: всписке может быть всего одна картинка
        Список медиа-группы:
        
        [
            InputMediaPhoto("photo1.jpg"),
            InputMediaPhoto("photo2.jpg", caption="photo caption"),
            InputMediaVideo("video.mp4", caption="video caption")
        ]
        RET:
        List of Message – On success, a list of the sent messages is returned.
        """
        
        async def func():
            async with Client(*ms.AUTH_PYROGRAM_CLIENT) as app:
                
                retMessages = await app.send_media_group(
                    chat, 
                    listMediaGroup
                )
                
            return retMessages
                
        retMessages = asyncio.run(func())
        
        return retMessages
        
        
        
        
        
        

    @staticmethod
    def send_photo_tpm (chat, filePhoto, **dicThrowgh):
        """ 
        TgPyrogramManager
        Отправить сообщение с картинкой и возможным описанием (caption) в ТГ-канал
        Параметры подобны параметрам метода send_photo() из Pyogram фреймворка: ~ https://docs.pyrogram.org/api/methods/send_photo
        """
        
        async def func():
            async with Client(*ms.AUTH_PYROGRAM_CLIENT) as app:
                
                retMessage = await app.send_photo(
                    chat, 
                    filePhoto, 
                    **dicThrowgh
                    )
                
                return retMessage
                
                # print(f"PR_A605 --> retMessage = {retMessage}")

        retMessage = asyncio.run(func())
        
        return retMessage
        
        
        
        

        
        
        
        
        
        
        
        
    @staticmethod
    def get_all_chat_messages_ids_tpm (chat : int|str, **dicThrowgh) -> list:
        """ 
        TgPyrogramManager
        Получить список ids всех сообщений заданного канала
        Все параметры подобны тождественным параметрам фреймворка Pyogram: ~ https://docs.pyrogram.org/api/methods/send_audio
        """
        
        messagesIds : list = []
        
        async def func():
            async with Client(*ms.AUTH_PYROGRAM_CLIENT) as app:
                
                messages =  app.get_chat_history(chat, **dicThrowgh)
                
                # цикл по сообщениям чата
                async for m in messages:

                    messagesIds.append(m.id)
                    
        asyncio.run(func())
        
        return messagesIds
        
        
                


    @staticmethod
    def clear_chat_delete_all_messages_tpm (chat : int|str, **dicThrowgh) -> list:
        """ 
        TgPyrogramManager
        Удалить все сообщения в чате
        Все параметры подобны тождественным параметрам фреймворка Pyogram: ~ https://docs.pyrogram.org/api/methods/send_audio
        """
        
        # Получить список ids всех сообщений в чате
        messagesIds = TgPyrogramManager.get_all_chat_messages_ids_tpm (chat)
        
        async def func():
            async with Client(*ms.AUTH_PYROGRAM_CLIENT) as app:
                # Удалить все сообщения в чате из списка messagesIds
                await app.delete_messages(chat, messagesIds)

        asyncio.run(func())
        
        return messagesIds





################## VI. Методы и алгоритмы для формирования содержания телеграм-каналов ===============================

    @staticmethod
    def prepare_book_img_file_path_by_img_name_tpm (fileImgName, **kwargs):
        """ 
        TgPyrogramManager
        Подготовить атрибуты для обьекта типа Photo из Pyrogram-фреймвока  для книжного комплекта из словаря Публикации книги bookPublishDic
        А именно подготовить полный путь картинки к описанию книги и само описание книги в конечном формате для публикации 
        
        Тип Pyrogram's Photo: ~ https://docs.pyrogram.org/api/methods/send_photo#pyrogram.Client.send_photo
        
        ПРИМ: Словарь публикации книги bookPublishDic формируется методом: obtain_book_complect_full_data_dict_to_tg_public_blf() из модуля telegram_monitor/local_classes/book_library_funcs.py
        Формат словаря на данный момент указан в описании метода obtain_book_complect_full_data_dict_to_tg_public_blf()
        
        RET: photoMessageParams - паарметры для отправки сообщения типа Photo (в окумейне фреймворка Pyrogram) в формате:
        
            photoMessageParams = {
                
                'bookDescr' : bookDescr ,
                'uploadImgFullPath' : uploadImgFullPath
            }
            
        """
        
        # INI

        # Book img
        # fileImgName = bookPublishDic['bookImages'][0]
        # Book Description (ПРИМ: В этом описании должна быть вся информация о книге, отворматированная и конечная, 
        # так как это сообщение подразумевает только картинку и Caption под ней)
        # bookDescr =  bookPublishDic['bookData']['book_description']


        # A. Найти файл в пространстве картинок к книгам
        
        listFiles = BookLibraryFuncs.find_img_full_path_by_name_in_lib_img_storage_recursive_blf(fileImgName)
        
        # Анализ результата поиска файла по названию в пространстве проекта с картинками к книгам
        
        # Если файл не найден в Хранилище картинок
        if len(listFiles) == 0:
            
            print(f"PR_A616 --> SYS LOG: Файл с названием {fileImgName} не найден в  хранилище картинок к книгам в директории {ms.LIB_BOOK_IMAGE_STORAGE}. Загрзите файл в хранилище!!!")

            raise Exception(f"PR_A619 --> SYS LOG: Файл с названием {fileImgName} не найден в  хранилище картинок к книгам в директории {ms.LIB_BOOK_IMAGE_STORAGE}. Загрзите файл в хранилище!!!") 
            
        # Если найдено несколько файлов с одними тем же названием в Хранилище
        elif len(listFiles) > 2:
        
            print(f"PR_A617 --> SYS LOG: Найдены несколько файлов с названием {fileImgName} в  хранилище картинок к книгам в директории {ms.LIB_BOOK_IMAGE_STORAGE}. Необходимо, что бы в Хранилище находилься только один файл!!!")

            raise Exception(f"PR_A620 --> SYS LOG: Найдены несколько файлов с названием {fileImgName} в  хранилище картинок к книгам в директории {ms.LIB_BOOK_IMAGE_STORAGE}. Необходимо, что бы в Хранилище находилься только один файл!!!") 

        # Работаем с найденным файлом в рамках текущих алгоритмов
        else:
            
            print(f"PR_A618 --> SYS LOG: Найден файл с названием {fileImgName} в  проектном хранилище картинок к книгам. Этот файл будет выгружен в сообщении с описанием книги")

            # INI
            # Полный абсолютный путь к картинке для описания текущего книжного комплекта
            uploadImgFullPath = listFiles[0]
            # print(f"PR_A615 --> listFiles = {listFiles}")
            
        return uploadImgFullPath




    







################## END VI. Методы и алгоритмы для формирования содержания телеграм-каналов ========









    ##### II. ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ

    @staticmethod
    async def progress(current, total):
        """ 
        TgPyrogramManager
        Отражение прогресса выполнения текущего метода
        Keep track of the progress while uploading
        """
        print(f"{current * 100 / total:.1f}%")
        
        
        

        
        
    ##### END II. ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ







    
    
    
    
    
    
if __name__ == '__main__':
    pass





    # # ПРОРАБОТКА: Отправка описания комплекта книги с картинкой и дополнительными атрибутами комплекта
    # # https://docs.pyrogram.org/api/methods/send_photo#pyrogram.Client.send_photo
    
    # chat = -1001811098741 # Моя библиотека
    
    # fileImgName = 'ch1_m4378_gr1_book_descr_photo.jpg'
    
    
    
    # # A. Найти файл в пространстве картинок к книгам
    
    # # prjImgStorage = ms.LIB_BOOK_IMAGE_STORAGE
    
    # from noocube.files_manager import FilesManager
    
    # listFiles = FilesManager.find_file_in_dir_by_name_recursively(ms.LIB_BOOK_IMAGE_STORAGE, fileImgName)
    
    # # Анализ результата поиска файла по названию в пространстве проекта с картинками к книгам
    
    # # Если файл не найден в Хранилище картинок
    # if len(listFiles) == 0:
        
    #     print(f"PR_A621 --> SYS LOG: Файл с названием {fileImgName} не найден в  хранилище картинок к книгам в директории {ms.LIB_BOOK_IMAGE_STORAGE}. Загрзите файл в хранилище!!!")
    
    # # Если найдено несколько файлов с одними тем же названием в Хранилище
    # elif len(listFiles) > 2:
    
    #     print(f"PR_A622 --> SYS LOG: Найдены несколько файлов с названием {fileImgName} в  хранилище картинок к книгам в директории {ms.LIB_BOOK_IMAGE_STORAGE}. Необходимо, что бы в Хранилище находилься только один файл!!!")

    # # Работаем с найденным файлом в рамках текущих алгоритмов
    # else:
        
    #     print(f"PR_A623 --> SYS LOG: Найден файл с названием {fileImgName} в  проектном хранилище картинок к книгам. Этот файл будет выгружен в сообщении с описанием книги")
    
    #     # Полный абсолютный путь к картинке для описания текущего книжного комплекта
    #     uploadImgFullPath = listFiles[0]
        

    
    #     # print(f"PR_A615 --> listFiles = {listFiles}")
    #     dicThrowgh = {
            
    #         'caption' : 'Текст сообщения с описанием книги' ,
            
    #     }
        
            
    #     TgPyrogramManager.send_photo_tpm(chat, uploadImgFullPath, **dicThrowgh)





    # # ПРОРАБОТКА: Удаление всех сообщений из чата
    # # delete_messages() : https://docs.pyrogram.org/api/methods/delete_messages#pyrogram.Client.delete_messages
    
    
    # chat = -1001811098741 # Моя библиотека
    
    # TgPyrogramManager.clear_chat_delete_all_messages_tpm (chat)
    





    # # ПРОРАБОТКА: получить список  ids всех сообщений канала
    # # get_chat_history() :  https://docs.pyrogram.org/api/methods/get_chat_history#pyrogram.Client.get_chat_history
    # # Message : https://docs.pyrogram.org/telegram/types/message



    # chat = -1001811098741 # Моя библиотека
    
    # messagesIds = TgPyrogramManager.get_all_chat_messages_ids_tpm (chat)
    
    # print(f"PR_A609 --> messagesIds = {messagesIds}")





    # # V. ПРОРАБОТКА: send_audio_tpm()
    
    
    
    # chat = -1001811098741 # Моя библиотека
        
    
    # fileRoot = '/media/ak/Transcend1/GENERAL_ARCHIVE_EXTERNAL_DISC_FROM_01_02_2024_CURRENT_MAIN/TELEGRAM_AUDIO_LIBRARIES/CHANNEL_ID_1'

    # fileName = '19. ждем книгу.mp3'
    # # fileName = '3. Эндшпиль.mp3' # > 50Mb
    # # fileName = '3. Endshpil.mp3'
    
    # # caption = '3. Endshpil'

    # file = f"{fileRoot}/{fileName}"
    
    # dicThrowgh = {
    #     'caption' : "audio caption", # пометка сообщения
    #     'progress' : TgPyrogramManager.progress # Прогресс-отображатель
    # }
    
    # TgPyrogramManager.send_audio_tpm(chat, file, **dicThrowgh)
    
    
    # # END V. ПРОРАБОТКА: start_pyogram_async_method()




    # # ПРОРАБОТКА: отправить группу с аудио-томами или с фото-видео альбомом
    # # https://docs.pyrogram.org/api/methods/send_media_group
    
    
    # chat = -1001811098741 # Моя библиотека
    
    
    # fileImgPath = '/media/ak/Transcend1/GENERAL_ARCHIVE_EXTERNAL_DISC_FROM_01_02_2024_CURRENT_MAIN/TELEGRAM_AUDIO_LIBRARIES/CHANNEL_ID_1/ch1_m4378_gr1_book_descr_photo.jpg'
    
    # # uploadImgFullPath = TgPyrogramManager.prepare_book_img_file_path_by_img_name_tpm(fileImgName)
    
    
    # fileRoot = '/media/ak/Transcend1/GENERAL_ARCHIVE_EXTERNAL_DISC_FROM_01_02_2024_CURRENT_MAIN/TELEGRAM_AUDIO_LIBRARIES/CHANNEL_ID_1'

    # fileName = '19. ждем книгу.mp3'
    # # fileName = '3. Эндшпиль.mp3' # > 50Mb
    # # fileName = '3. Endshpil.mp3'
    
    # # caption = '3. Endshpil'

    # file = f"{fileRoot}/{fileName}"


    # dicThrowgh = {
    #     # 'caption' : "audio caption", # пометка сообщения
    #     'progress' : TgPyrogramManager.progress # Прогресс-отображатель
    # }

    # from pyrogram.types import InputMediaPhoto, InputMediaVideo, InputMediaAudio
    
    # listMediaGroupForimgsandVideo = [
        
    #     InputMediaPhoto(fileImgPath, caption="photo caption"),
    #     InputMediaPhoto(fileImgPath, caption="photo caption"),
    #     InputMediaPhoto(fileImgPath, caption="photo caption"),
    # ]
    
    
    # listMediaGroupForAudio = [
        
    #     InputMediaAudio(file, caption="video caption"),
    #     InputMediaAudio(file, caption="video caption"),
    # ]
    
    
    
    # TgPyrogramManager.send_media_group_tpm (chat, listMediaGroupForAudio, **dicThrowgh)
    




    # # # II. ###  ПРОРАБОТКА: Считать сообщения с канала
    

    # api_id = 20460272
    # api_hash = '9e6f44844a41f717e5c035cb0add2984'

    # # 'anon' - название файла сессии, который появляется в рабочем катологе проекта
    
    # # # chatName = 'Аудиокниги фантастика' 
    # # chatName = 'А-библиотека: Фантастика'
    # # chatLink = 'https://t.me/akniga'
    
    # # # chatId = -1001911157001 # 'Аудиокниги фантастика'
    # # chatId = -1001811098741 # Моя библиотека
    # # ownBotChatId = 4104980551
    
    # chatSolov = -1001911157001  #  Соловьев
    
    
    # async def main():
    #     async with Client("my_account2", api_id, api_hash) as app:
            
    #         inx = 0
    #         async for message in app.get_chat_history(chatSolov, 10):
    #             print(f"PR_A624 --> {inx+1}. {message.text}")
    #             print(f"PR_A625 --> {inx+1}. {message.caption}")
    #             # print(f"PR_A625 --> {inx+1}. {message.caption}")
                
    #             inx += 1
                
    #             # time.sleep(2)
                


    # asyncio.run(main())














