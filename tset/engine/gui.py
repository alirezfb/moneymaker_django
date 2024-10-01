# -*- coding: utf-8 -*-
import pytse_client as tse
from mysql import *
import datetime
import sys



def run():
    today = datetime.datetime.now()
    if today.month < 10:
        todaystr = str(today.year)+'0'+str(today.month)
        if today.day < 10:
            todaystr = todaystr+'0'+str(today.day - 1)
            pass
        else:
            todaystr = todaystr + str(today.day - 1)
            pass
        pass
    elif today.day < 10:
        todaystr = str(today.year)+str(today.month)+'0'+str(today.day - 1)
        pass
    else:
        pass
    donedate = doneread()
    highest = donedate[0]
    skipcount = 0
    today = int(todaystr)
    donecheck = False
    del todaystr
    #khandane nam namadha
    namadha = readnames()
    log = []
    logcount = 0
    #blacklist
    bl = blacklistread()
    #main loop
    for i in namadha:
        print(i)
        #check kardane blacklist
        if (i in bl):
            continue
        else:pass
        date = checkdates(i)
        #dorost kardane object tset va jologiri az error
        errorcount = 0
        while errorcount < 6:
            try:
                namad = tse.Ticker(i)
                break
            except:
                errorcount += 1
                if errorcount == 5:
                    print('Error on',i)
                    log.append('Error on'+i)
                    print(sys.exc_info()[0])
                    result = blacklistwrite(i)
                    print('Added',i,'into BLACKLIST')
                    log.append('Error on '+ i + '. added into blacklist.')
                    pass
                pass
            pass
        del errorcount
        #daryaft parametere date
        namaddt = namad.client_types.date
        if int(namaddt[0]) == donedate[0] and highest <= donedate[0]:
            print('skip')
            log.append(i+' skip')
            skipcount += 1
            if donedate[1] == 1 and skipcount >= 25:
                donecheck = True
                break
            else:pass
            continue
        else:pass
        if int(namaddt[0]) > highest:
            highest = int(namaddt[0])
            print(highest)
            pass
        else:pass
        #taiin kardane meghdar row hayi ke bayad save behsan
        writenum = 0
        for j in namaddt:
            if int(j) > date:
                writenum += 1
                pass
            else:
                pass
            pass
        #save kardane namade baste emrooz
        print(namaddt[0])
        print(date)
        if writenum == 0:
            log.append(i+' ya save shode ya baste ast.')
            print('ya save shode ya baste ast.')
            continue
            pass
        else:pass
        datecount = 0
        #loop baraye save kardane tarikh va etelaat
        namadkh = namad.client_types.individual_buy_count
        namadhk = namad.client_types.individual_buy_vol
        namadfh = namad.client_types.individual_sell_count
        namadhf = namad.client_types.individual_sell_vol
        namadkho = namad.client_types.corporate_buy_count
        namadhkho = namad.client_types.corporate_buy_vol
        namadfho = namad.client_types.corporate_sell_count
        namadhfho = namad.client_types.corporate_sell_value
        while datecount < writenum:
            temp = []

            #Section mohasebat va meghdardehi haghighi
            #kharidar haghighi
            kh = int(namadkh[datecount])
            #hajme kharid
            hk = int(namadhk[datecount])
            #forooshande haghighi
            fh = int(namadfh[datecount])
            #hajme foroosh
            hf = int(namadhf[datecount])
            #mohasebe fk(moghayese kharid va foroosh)
            # check kardane 0 naboodan
            if kh != 0 and hk != 0 and fh != 0 and hf != 0:
                fk = (fh * hf) / (kh * hk)
                pass
            else:
                fk = 0
                pass

            #secgtion mohasebat va meghdardehi hoghooghi
            #kharidar hoghooghi
            kho = int(namadkho[datecount])
            #hajme kharid hoghooghi
            hkho = int(namadhkho[datecount])
            #foroshande hoghoghi
            fho = int(namadfho[datecount])
            #hajme forosh hoghoghi
            hfho = int(namadhfho[datecount])
            # mohasebe fk(moghayese kharid va foroosh)
            # check kardane 0 naboodan
            if kho != 0 and hkho != 0 and fho != 0 and hfho != 0:
                fkho = (fho * hfho) / (kho * hkho)
                pass
            else:
                fkho = 0
                pass


            
            #vared kardane etelaat haghighi be list baraye save kardan dar database
            temp.append(kh)
            temp.append(hk)
            temp.append(fh)
            temp.append(hf)
            temp.append(fk)

            #vared kardane etelaat hoghooghi be list baraye save kardan dar database
            temp.append(kho)
            temp.append(hkho)
            temp.append(fho)
            temp.append(hfho)
            temp.append(fkho)


            #save kardan etelaat dar database
            write(i, int(namaddt[datecount]), temp)
            print('done')
            logcount += 1
            
            #hazf kardan mtheghayer haye gheyre ghabel estefadeh
            del temp
            del kh
            del hk
            del fh
            del hf
            del fk
            del kho
            del hkho
            del fho
            del hfho
            del fkho

            #progress
            datecount += 1
            pass
        pass
    if donedate[0] != highest and donecheck == False:
        doneresult = donewrite(highest, 1)
        print(doneresult)
        pass
    else:
        print('All Done')
        pass
    log.append(logcount)
    return('data has been updated')
