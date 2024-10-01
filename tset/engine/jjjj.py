import tse_connect as tse_connect
import tse_analize
import my_sql
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
import tse_time
import extract_save
from time import sleep
from multiprocessing import pool

index_list = my_sql.read.index()
namadha_list = []
for i in index_list:
    namadha_list.append(my_sql.search.names(i))
    pass
pool1 = pool.ThreadPool(processes= 40)
namadha_list = pool1.map(my_sql.search.names, index_list)
print(namadha_list)