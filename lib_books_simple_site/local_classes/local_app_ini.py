
import sys
sys.path.append('/home/ak/projects/P21_Telegram_Channel_Parsing_Django/telegram_channel_parsing_django')
import settings_bdp_main as ms # общие установки для всех модулей

class LocalAppIni ():
    """ 
    Класс инициализации в локальном приложении (модуле)
    """


    def __init__(self, dicTrough={}):

        self.dicTrough = dicTrough



    def view_context_inicialization_lai (self):
        """ 
        Инициализация дефолтных парметров контекста View
        """
        
        # Раскрытие раздела левой панели навигации в зависимости от названия текущего View
        if self.dicTrough['appView'] in ms.LEFT_NAVIGATOR_ACTIVE_:
            leftNavActive = ms.LEFT_NAVIGATOR_ACTIVE_[self.dicTrough['appView']] # dicDecor['appView'] - Название текущего View задает маркер раскрытия левого навигатора
        else:
            leftNavActive = ''
        
        
        # Формирование кода таблицы в контексте, если таблица предусмотрена
        if 'tableCode' in self.dicTrough:
            tbCode = self.dicTrough['tableCode']
        else:
            tbCode = ''
            
        # Формирование кол-ва рядов исходного для подсчета рядов фрейма, если фрейм и таблица предусмотрены View
        if 'dfQn' in self.dicTrough:
            dfQn = self.dicTrough['dfQn']
        else:
            dfQn = ''
            
        # Стандартные параметры для контекста вывода таблиц по фрейму на сайт
        baseContext = {
            'tbCode' : tbCode,
            'left_nav_view' : leftNavActive, # Открывающийся раздел в левом навигаторе
            'df_qn' : dfQn,
            # 'dfPackages' : self.bmms.get_index_packages_df_BMMS(), # фрейм с индексными пакетами 
            # 'srch_str' : srch_str,
        }
        
        
        # Для выделения подразделов левого навигатора и прочих применений
        baseContext['view'] = self.dicTrough['appView']
        # print(f"LLLLLLLLLLL   PR_119 baseContext['view'] = {baseContext['view']}")
        
        # Вставка элемента в зависимости от его присутствия в self.requestDic
        
        # Добавить месяц в baseContext
        if 'payment_month' in self.dicTrough['requestDic']:
            baseContext['payment_month'] = self.dicTrough['requestDic']['payment_month']
            
        # Добавить поисковый текстовый фрагмент
        if 'srch_str' in self.dicTrough['requestDic']:
            baseContext['srch_str'] = self.dicTrough['requestDic']['srch_str']
            
            
        # Добавить наименование текущей страницы сайта
        if 'pg_title' in self.dicTrough:
            baseContext['pg_title'] = self.dicTrough['pg_title']
            
        # context['left_nav']['inx_pckgs']
        # # Добавить словари с  разделами-подразделами левого навигатора , сожержащихся в context['left_nav'] словаре. Прим: context['left_nav']['inx_pckgs'] - подразделы раздела Индексных пакетов
        # baseContext = ProjectBondsFunctions.add_to_context_left_nav_dict(baseContext) 

            
        # # добавить динамические разделы -подразделы левого меню
        # inxPckgs = 

        return baseContext















if __name__ == '__main__':
    pass












