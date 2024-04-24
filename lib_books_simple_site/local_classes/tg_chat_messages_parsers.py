# Динамическое подключение settings_bdp_main в корне проекта
import sys
sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')
import settings_bdp_main as ms # общие установки для всех модулей

from noocube.text_formater import TextFormater

# from noocube.sqlite_processor_speedup import SqliteProcessorSpeedup
# from noocube.sqlite_pandas_processor_speedup import SqlitePandasProcessorSpeedup
# # # from noocube.django_view_manager import DjangoViewManager
# from noocube.bonds_main_manager_speedup import BondsMainManagerSpeedup
# from noocube.funcs_general_class import FunctionsGeneralClass


class TgChatMessagesParsers ():
    """ 
    Модуль отвечающий за обработку и парсинг сообщений от разных чатов ТГ-каналов, локальный
    Локальный - потому что каждый ТГ канал-чат может иметь индивидуальные форматы для парсинга данных по книге. Поэтому этот модуль не может быть общим
    """


    def __init__(self, **dicTrough):
        # self.db_uri = f"sqlite:///{ms.DB_CONNECTION.dataBase}" # Pandas по умолчанию работает через SQLAlchemy и может создавать сама присоединение к БД по формату адреса URI (см. в документации SQLAlchemy)
        # self.db_connection = ms.DB_CONNECTION
        # self.sps = SqliteProcessorSpeedup(self.db_connection) # Обьект класса SqliteProcessorSpeedup
        # self.spps = SqlitePandasProcessorSpeedup(self.db_connection) # Обьект класса SqlitePandasProcessorSpeedup
        # self.bmms = BondsMainManagerSpeedup(self.db_connection)
        # self.request = request
        self.dicTrough = dicTrough
        





    @staticmethod
    def parse_book_descr_from_cannel_chat_01_stat_bpm(bookDescr):
        """
        Парсинг описания книги исключительо с чата канала CH_01 ('Аудиокниги фантастика')
        bookDescr - описание книги с вышеукзанног канала CH_01 ('Аудиокниги фантастика')
        ПРИМ: индивидуальный метод только для описания книг в сообщении из чат-канала CH_01 ('Аудиокниги фантастика')
        """
        
        print(f"PR_A231 --> START: parse_book_descr_from_cannel_chat_01_stat_bpm()")
        
        # C. ПЕРВИЧНЫЙ ПАРСИНГ. Парсинг-модуль описания в сообщении по стандартной книге для канала CH_1 ('Аудиокниги фантастика') {ПАРСИНГ_МОДУЛЬ_ОПИСАНИЯ_КНИГИ_CH_1_}
        # Парсинг описания книги bookDescr. 

        tf = TextFormater()
        
        bookDescrLines = tf.get_str_lines_of_text_full(bookDescr)
        
        # Словарь для результата парсинга
        dicDescrParsing = {
            
            'bookTitle' : "",
            'authors' : "",
            'deletedLines' : "",
            'narrators' : "",
            'categories' : "",
            'description' : "",
            'dateissuedcalend' : "NULL",
            'authorSecondname' : "",
            'authorFirstname' : ""

        }
        
        # print(f"PR_A307 --> dicDescrParsing = {dicDescrParsing}")
        
        # Сортируем строки текста описания по расзным спискам для сортируемых строк (создаем наборы строк по смыслу из общего описания книги)
        for inx, line in enumerate(bookDescrLines):
            
            # для первой строки мы знаем, что в ней. название книги и имя автора
            if inx == 0:
                parts = line.split('.')
                dicDescrParsing['bookTitle'] += parts[0]   
                
                # Последняя часть из разделенных сегментов по точке (скорее всего это фамилия и имя. Но монут быть исключения. которые на данный 
                # момент придется анализировать в ручном режиме. TODO: В будущем подключить для анализа иформатирования REGEDIT и продумать, 
                # найти за что зацепится для распарсивания ФИО)          
                dicDescrParsing['authors'] += parts[-1] 
            
            # строка с донатом
            elif 'Поддержать канал' in line or 'Сбербанк' in line:
                dicDescrParsing['deletedLines'] += line 
                
            # Вычленияем строку с чтецом
            elif 'Чтец' in line :
                dicDescrParsing['narrators']+= line 
                
            # Строка с категориями
            elif 'Чтец' not in line and '#' in line:
                dicDescrParsing['categories']+= line 
                
            # оставшиеся строки - это строки описания книги
            else:
                dicDescrParsing['description']+= line 
                
            
            
            
        print(f"PR_A235 --> Словарь с распарсеными блоками строк из описания книги dicDescrParsing = {dicDescrParsing}")

        
        # D. Осуществить стандартизацию текстовых обьектов для регистрации в словаре парсинга dicDescrParsing. {ЧИСТИЛЬЩИК_ФОРМАТЕР}
        
        """ 
        Для описания: удалить все пробелы с концов.  Пеервести все кавычки к двойным
        
        Для года выпуска. если есть: 
        """ 
        
        # ЧИСТИЛЬЩИКИ:
        
        # 1. Чистильщик для авторов:  удалить все пробелы с концов. все точки и #. все пробелы внутри свести к одному пробелу. 
        # Все мульти-пробелы внутри свести к одному пробелу, включая tabs, newlines, etc
        resText = TextFormater.clear_multiple_spaces_stat (dicDescrParsing['authors'])
        dicDescrParsing['authors'] = resText.replace('.#', '').strip() # удалить все точки и #. Удалить пробелы с концов строки
        # print(f"PR_A239 --> authors = {dicDescrParsing['authors']}")
        
        # 2. Чистильщик для названия книги: удалить все пробелы с концов. все точки и #. все пробелы внутри свести к онодному пробелу. 
        # Все мульти-пробелы внутри свести к одному пробелу, включая tabs, newlines, etc
        resText = TextFormater.clear_multiple_spaces_stat (dicDescrParsing['bookTitle'])
        dicDescrParsing['bookTitle'] = resText.replace('.#', '').strip() # удалить все точки и #. Удалить пробелы с концов строки

        
        # 3. Чистильщик для диктора:  удалить все пробелы с концов. все точки . все пробелы внутри свести к одному пробелу. 
        # Все мульти-пробелы внутри свести к одному пробелу, включая tabs, newlines, etc
        resText = TextFormater.clear_multiple_spaces_stat (dicDescrParsing['narrators'])
        dicDescrParsing['narrators'] = resText.replace('.', '').strip() # удалить все точки и #. Удалить пробелы с концов строки
        # print(f"PR_A239 --> authors = {dicDescrParsing['authors']}")
        
        # Чистим описание книги dicDescrParsing['description']/ убираем спец-символы с начала и конца
        dicDescrParsing['description'] = dicDescrParsing['description'].strip('\n\t\r')

        
        
        
        # ВТОРИЧНЫЙ ПАРСИНГ
        
        # Разделить автора на фамилию и имя
        authors = dicDescrParsing['authors']
        parts = authors.split(' ')
        
        if len(parts) < 2: # Если ф фрагменте ФИО автора система распарсила только одно слово (по разным причинам это может случится)

            dicDescrParsing['authorFirstname'] = ''
            dicDescrParsing['authorSecondname'] = parts[0]
        
        else:
        
            dicDescrParsing['authorFirstname'] = parts[0]
            dicDescrParsing['authorSecondname'] = parts[1]
            
            
            
        # Разделить диктора на фамилию и имя
        narrators = dicDescrParsing['narrators']
        parts = narrators.split(' ')
    
        if len(parts) < 2: # Если ф фрагменте ФИО автора система распарсила только одно слово (по разным причинам это может случится)
            
            dicDescrParsing['narratorFirstname'] = ''
            dicDescrParsing['narratorSecondname'] = parts[0]
        
        else:
        
            dicDescrParsing['narratorFirstname'] = parts[0].replace('Чтец', '').replace(':', '').replace('#', '')
            dicDescrParsing['narratorSecondname'] = parts[1].replace('Чтец', '').replace(':', '').replace('#', '')
            
            
        # print(f"PR_A669 --> dicDescrParsing['authorSecondname'] = {dicDescrParsing['authorSecondname']}")
        
        


        # E. Продумать как парсить , если несколько аторов у одной книги
        
        
        
        # F. Вторичный парсинг категорий (разделить несколько ктаегорий и удалить, если в одной из категорий есть совпадение с фаимлией атвора, так как
        # на этом канале в категорию вставляют фамилию автора)
        
        categParts = dicDescrParsing['categories'].split('#')
        # categParts = ['', 'петухов ', 'этознатьнадо!этоклассика!\n']
        
        print(f"PR_A657 --> categParts = {categParts}")
        
        
        
        
        listCategs = []
        
        for categ in categParts:
            pass
        
            if len(categ)==0:
                continue
            
            
            x = categ.lower().strip(' ')
            y = dicDescrParsing['authorSecondname'].lower().strip(' ')

            # print(f"PR_A671 --> pattern = {pattern}")
            
            # print(f"PR_A672 --> text = {text}")
            
            # print(f"PPR_A674 --> match = {match}")
                
            if x in y:
                
                print(f"PR_A673 --> categ.lower() in dicDescrParsing['authorSecondname'].lower()  = TRUE")

                continue
            
            categ = categ.replace('\n','').strip(' ')
            
            listCategs.append(categ)
            
        
        print(f"PR_A670 --> SYS LOG: категории = {listCategs}")
        
        dicDescrParsing['categories'] = listCategs
            

        print(f"PR_A232 --> END: parse_book_descr_from_cannel_chat_01_stat_bpm()")
        
        return dicDescrParsing

        
        
        
        
        

    @staticmethod
    def parse_book_descr_from_cannel_chat_02_stat_bpm(bookDescr):
        """
        Парсинг описания книги исключительо с чата канала CH_02 ('Любимая Книга в Дорогу') ТГ-чат -1001894592463
        bookDescr - описание книги с вышеукзанног канала CH_02 ('Любимая Книга в Дорогу')
        ПРИМ: индивидуальный метод только для описания книг в сообщении из чат-канала CH_02 ('Любимая Книга в Дорогу')
        """
        
        print(f"PR_B197 --> START: parse_book_descr_from_cannel_chat_01_stat_bpm()")
        
        # C. ПЕРВИЧНЫЙ ПАРСИНГ. Парсинг-модуль описания в сообщении по стандартной книге для канала CH_1 ('Аудиокниги фантастика') {ПАРСИНГ_МОДУЛЬ_ОПИСАНИЯ_КНИГИ_CH_1_}
        # Парсинг описания книги bookDescr. 

        tf = TextFormater()
        
        bookDescrLines = tf.get_str_lines_of_text_full(bookDescr)
        
        # Словарь для результата парсинга
        dicDescrParsing = {
            
            'bookTitle' : "",
            'authors' : "",
            'deletedLines' : "",
            'narrators' : "",
            'categories' : "",
            'description' : "",
            'dateissuedcalend' : "NULL",
            'authorSecondname' : "",
            'authorFirstname' : ""

        }
        
        # print(f"PR_A307 --> dicDescrParsing = {dicDescrParsing}")
        
        # Сортируем строки текста описания по расзным спискам для сортируемых строк (создаем наборы строк по смыслу из общего описания книги)
        for inx, line in enumerate(bookDescrLines):
            
            
            # # ПЕРВИЧНЫЙ ПАРСИИНГ
            
            # строка с донатом  https://www.donationalerts.com/r/elbowscc
            if 'https://' in line or 'www' in line or 'donationalerts' in line:
                dicDescrParsing['deletedLines'] += line 

            # Строка с категориями
            elif  '#' in line:
                dicDescrParsing['categories']+= line 
                
            # оставшиеся строки - это всякие ненужные строки 
            else:
                dicDescrParsing['deletedLines']+= line 
                
            
            
            
        print(f"PR_B199 --> Словарь с распарсеными блоками строк из описания книги dicDescrParsing = {dicDescrParsing}")

        
        # D. Осуществить стандартизацию текстовых обьектов для регистрации в словаре парсинга dicDescrParsing. {ЧИСТИЛЬЩИК_ФОРМАТЕР}
        
        """ 
        Для описания: удалить все пробелы с концов.  Пеервести все кавычки к двойным
        
        Для года выпуска. если есть: 
        """ 
        
        # ЧИСТИЛЬЩИКИ:
        
        
        # ВТОРИЧНЫЙ ПАРСИНГ
        
        # print(f"PR_A669 --> dicDescrParsing['authorSecondname'] = {dicDescrParsing['authorSecondname']}")
        
        # F. Вторичный парсинг категорий (разделить несколько ктаегорий и удалить, если в одной из категорий есть совпадение с фаимлией атвора, так как
        # на этом канале в категорию вставляют фамилию автора)
        
        categParts = dicDescrParsing['categories'].split('#')
        # categParts = ['', 'петухов ', 'этознатьнадо!этоклассика!\n']
        
        print(f"PR_B200 --> categParts = {categParts}")
        
        listCategs = []
        
        for categ in categParts:
        
            if len(categ)==0:
                continue
            
            
            x = categ.lower().strip(' ')
            y = dicDescrParsing['authorSecondname'].lower().strip(' ')

                
            if x in y:
                
                print(f"PR_B201 --> categ.lower() in dicDescrParsing['authorSecondname'].lower()  = TRUE")

                continue
            
            categ = categ.replace('\n','').strip(' ')
            
            listCategs.append(categ)
            
        
        print(f"PR_B202 --> SYS LOG: категории = {listCategs}")
        
        dicDescrParsing['categories'] = listCategs
            

        print(f"PR_B198 --> END: parse_book_descr_from_cannel_chat_01_stat_bpm()")
        
        return dicDescrParsing

        
        












if __name__ == '__main__':
    pass


    # # # ПРОРАБОТКА: 

































        
        
        
        
        
        
        
        