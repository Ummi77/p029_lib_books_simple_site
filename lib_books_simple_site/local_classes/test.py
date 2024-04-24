# import asyncio
# import time
# from aiohttp import ClientSession

# 








strText = """ 
CREATE TABLE `tg_message_proceeded_ext_err` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message_proceeded_ref_id` int(11) DEFAULT NULL,
  `channels_ref_id_ext` int(11) DEFAULT NULL,
  `message_own_id_ext` int(11) DEFAULT NULL,
  `message_text` text DEFAULT NULL,
  `message_img_loded_path` varchar(255) DEFAULT NULL,
  `message_img_name` varchar(100) DEFAULT NULL,
  `message_document_loded_path` varchar(254) DEFAULT NULL,
  `message_document_name` varchar(100) DEFAULT NULL,
  `message_document_size` int(11) DEFAULT NULL,
  `messages_grouped_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `message_proceeded_ref_id` (`message_proceeded_ref_id`),
  UNIQUE KEY `uk_channels_ref_id_ext_message_own_id_ext` (`channels_ref_id_ext`,`message_own_id_ext`),
  CONSTRAINT `tg_message_proceeded_ext_ibfk_1` FOREIGN KEY (`message_proceeded_ref_id`) REFERENCES `tg_messages_proceeded` (`id`) ON DELETE CASCADE,
  CONSTRAINT `tg_messages_proceeded_ext_ibfk_2` FOREIGN KEY (`channels_ref_id_ext`) REFERENCES `lib_orig_sources` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=354 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
"""


replaceedStr = strText.replace('`','')


print(replaceedStr)













# import subprocess

# username = 'the_username'
# password = 'the_password'
# database = 'my_fancy_database'

# with open('file.sql','w') as output:
#     c = subprocess.Popen(['mysqldump', '-u',username,'-p%s'%password,database],
#                             stdout=output, shell=True)
                









# async def get_weather(city):
#     async with ClientSession() as session:
#         url = f'http://api.openweathermap.org/data/2.5/weather'
#         params = {'q': city, 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}

#         async with session.get(url=url, params=params) as response:
#             weather_json = await response.json()
#             print(f'{city}: {weather_json["weather"][0]["main"]}')


# async def main(cities_):
#     tasks = []
#     for city in cities_:
#         tasks.append(asyncio.create_task(get_weather(city)))

#     for task in tasks:
#         await task


# cities = ['Moscow', 'St. Petersburg', 'Rostov-on-Don', 'Kaliningrad', 'Vladivostok',
#           'Minsk', 'Beijing', 'Delhi', 'Istanbul', 'Tokyo', 'London', 'New York']

# print(time.strftime('%X'))

# asyncio.run(main(cities))

# print(time.strftime('%X'))






# # TEST: mariaDB connection


# # Module Imports
# import mariadb
# import sys

# # Connect to MariaDB Platform
# try:
#     conn = mariadb.connect(
#         user="admin",
#         password="7731",
#         host="localhost",
#         port=3306,
#         database="labba"

#     )
#     print(f"PR_A392 --> Connection to mariaDB named: libba SUCSSESFUL")
# except mariadb.Error as e:
#     print(f"PR_A393 --> Error connecting to MariaDB Platform: {e}")
#     sys.exit(1)

# # Get Cursor
# cur = conn.cursor()






# # ТЕСТ: переименование одинаковых по названию колонок

# import pandas as pd

# import numpy as np

# #sample df with duplicate blah column
# df=pd.DataFrame(np.arange(2*5).reshape(2,5))
# df.columns=['blah','blah2','blah3','blah','blah']
# print(df)

# # you just need the following 4 lines to rename duplicates
# # df is the dataframe that you want to rename duplicated columns

# cols=pd.Series(df.columns)

# for dup in cols[cols.duplicated()].unique(): 
#     cols[cols[cols == dup].index.values.tolist()] = [dup + '.' + str(i) if i != 0 else dup for i in range(sum(cols == dup))]

# # rename the columns with the cols list.
# df.columns=cols

# print(df)













