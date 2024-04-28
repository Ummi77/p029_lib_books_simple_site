

from noocube.sqlite_connection import MysqlConnection


DEBUG_ = True


# Подключение к SQLite

DB_CONNECTION = MysqlConnection(dbName = 'books_site')




# Названия таблиц системы




# TB_LIB_BOOK_SERIAL_ILBN = 'lib_book_serial_ilbn'

TB_LIB_BOOKS_ALFA  = 'lib_books_alfa'

TB_LIB_BOOKS_ALFA_EXT = 'lib_books_alfa_ext'

TB_LIB_AUTHORS = 'lib_authors'

TB_LIB_BOOKS_AUTHORS = 'lib_books_authors'



TB_LIB_NARRATORS = 'lib_narrators'

TB_LIB_BOOKS_NARRATORS = 'lib_books_narrators'



TB_LIB_BOOKS_STATUSES = 'lib_books_statuses' # МКМ (многие-ко-многим)

TB_LIB_BOOK_STATUSES = 'lib_book_statuses'

TB_LIB_BOOK_AUDIO_VOLUMES = 'lib_book_audio_volumes'

TB_LIB_VOLUMES_VOLUME_STATUSES  = 'lib_volumes_volume_statuses'

TB_LIB_BOOK_IMAGES = 'lib_book_images'

TB_LIB_BOOKS_IMAGES = 'lib_books_images'

TB_LIB_ORIG_SOURCES = 'lib_orig_sources'


TB_LIB_CATEGORIES = 'lib_categories'

TB_LIB_BOOKS_CATEGORIES = 'lib_books_categories'

TB_LIB_BOOK_CATEGORIES_VOCABILARY = 'lib_book_categories_vocabulary'


TB_LIB_OBJECTS_REMOVED = 'lib_objects_removed'

TB_LIB_OBJ_REMOVED_TYPES = 'lib_obj_removed_types'




TB_LIB_AUDIO_VOLUMES_LOADED_TO_REPOSITORIES = 'lib_audio_volumes_loaded_to_repositories'


TB_LIB_BOOKS_LOADED_TO_REPOSITORIES = 'lib_books_loaded_to_repositories'


# TODO: Не должно быть абсолютных названий таблиц этого рода. Они должны задаваться динамически путем прибавления индекса в конце названия-базы TB_LIB_REPOSIT_AUDIO_VOLUMES_REGISTR_
TB_LIB_REPOSIT_AUDIO_VOLUMES_REGISTR_1 = 'lib_reposit_audio_volumes_registr_1'
TB_LIB_REPOSIT_BOOKS_REGISTR_1 = 'lib_reposit_books_registr_1'

TB_LIB_REPOSIT_AUDIO_VOLUMES_REGISTR_2 = 'lib_reposit_audio_volumes_registr_2'
TB_LIB_REPOSIT_BOOKS_REGISTR_2 = 'lib_reposit_books_registr_2'


TB_LIB_REPOSITORIES = 'lib_repositories'




TB_LIB_REPOSIT_BOOKS_REGISTR_ = 'lib_reposit_books_registr_'


TB_LIB_REPOSIT_AUDIO_VOLUMES_REGISTR_ = 'lib_reposit_audio_volumes_registr_'

TB_LIB_BOOK_JSON_ARCHIVE_REGISTR = 'lib_book_json_archive_registr'






TB_LIB_SOURCES_ASSIGNED_REPOSITORIES = 'lib_sources_assigned_repositories'


TB_LIB_BOOKS_ASSIGNED_REPOSITORIES = 'lib_books_assigned_repositories'




TB_TG_BOOK_COMPLECTS_CH_01 = 'tg_book_complects_ch_01'

TB_TG_BOOK_COMPLECT_VOLUMES_CH_01 = 'tg_book_complect_volumes_ch_01'

TB_TG_MESSAGE_PROCEEDED_EXT = 'tg_message_proceeded_ext'

TB_TG_AUXILARY_MSSGS_PROCEEDED_EXT_ = 'tg_auxilary_messages_proceeded_ext'

TB_TG_MESSAGE_TYPE = 'tg_message_types'

TB_TG_MESSAGE_PROC_STATUS = 'tg_message_proc_statuses'


TB_TG_SAMPLES_MARKERS = 'tg_samples_markers'


TB_MSSGS_PROCEEDED_ = 'tg_messages_proceeded'
TB_MSSGS_PROCEEDED_EXT_ = 'tg_message_proceeded_ext'

TB_AUXILARY_MSSGS_PROCEEDED_ = 'tg_auxilary_messages_proceeded'
TB_AUXILARY_MSSGS_PROCEEDED_EXT_ = 'tg_auxilary_messages_proceeded_ext'


TB_TG_PROCCEEDED_ERR = 'tg_messages_proceeded_err'

TB_TG_PROCCEEDED_ERR_EXT = 'tg_message_proceeded_err_ext'


# END Названия таблиц системы









