
import collections


class TgRenderManager ():
    """
    Класс для рендеринга сообщений для ТГ-entities (каналов, чатов и т.д.)

    """

    def __init__(self):
        pass
        



    @staticmethod
    def render_template_for_ch_book_descr_message (mssgBookdescrTemplate, bookPublishDic):
        """ 
        TgRenderManager
        Рендеринг шаблона для сообщения с описанием книги и одной картинки 
        mssgBookdescrTemplate - шаблон для сообщения с описанием книги
        """
        
        
        # Вставка описания книги
        bookDescr = bookPublishDic['bookData']['book_description']
        bookDescrMark = '$%BOOK_DESCRIPTION%$'
        finalBookDescr = mssgBookdescrTemplate.replace(bookDescrMark, bookDescr)
        
        # Вставка названия книги
        bookTitleMark = '$%BOOK_TITLE%$'
        bookTitle = bookPublishDic['bookData']['book_title']
        finalBookDescr = finalBookDescr.replace(bookTitleMark, bookTitle)
        
        
        # Вставка авторов книги
        
        bookAuthorsMark = '$%BBOOK_AUTHOR%$'
        listBookAuthors = bookPublishDic['bookAuthorsFullNames']
        # Проверяем, что есть список. Если нет, значит автор не задан (такое тоже возможно, хотя не желательно)
        if isinstance(listBookAuthors, collections.abc.Iterable):
            bookAuthors = ",".join(listBookAuthors)
            finalBookDescr = finalBookDescr.replace(bookAuthorsMark, bookAuthors) # Замещаем маркер авторов $%BBOOK_AUTHOR%$ строкой с авторами
        else:
            finalBookDescr = finalBookDescr.replace(bookAuthorsMark, '') # Удаляем маркер из общего текста
            finalBookDescr = finalBookDescr.replace('Авторы:', '')
            
            
        
        # Вставка категорий книги
        bookCategoriesMark = '$%BOOK_CATEGORIES%$'
        listBookCategories = bookPublishDic['bookCategories']
        bookCategories = ''
        for category in listBookCategories:
            bookCategories += f"#{category},"
        bookCategories = bookCategories.rstrip(',')
        # print(f"PR_A752 --> bookCategories = {bookCategories}")
        finalBookDescr = finalBookDescr.replace(bookCategoriesMark, bookCategories)
        
        
        
        # вставка информации о донатах
        bookDonationMark = '$%DONATION_INFOR%$'
        donationInfor = ''
        finalBookDescr = finalBookDescr.replace(bookDonationMark, donationInfor)
        

        return finalBookDescr
        







if __name__ == '__main__':
    pass





