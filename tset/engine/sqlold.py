# -*- coding: utf-8 -*-
import _sqlite3 as sql
#in tabe baraye vared kardane etelaat jadid be db mibashad
def write(name, date, namadha):
    #vasl shodan be sql va neveshtane etelaat
    con = sql.connect(r"C:\moneymaker\db\saham.db")
    cur = con.cursor()
    b = cur.execute("INSERT INTO '%s'(date, kh, hk, fh, hf, fk) "
                    "VALUES('%s', '%s', '%s', '%s', '%s', '%s')"
                    %(name, date, namadha[0], namadha[1], namadha[2], namadha[3], namadha[4]))
    con.commit()
    con.close()
    pass
#in tabe baraye khandane nam haye namadha az db mibashad
def readnames():
    #baz kardane sql va khandane tblnamadha
    con = sql.connect(r"C:\moneymaker\db\saham.db")
    cur = con.cursor()
    result = cur.execute(r"SELECT name FROM tblnamadha")
    result = result.fetchall()
    con.commit()
    con.close()
    del cur
    del con
    #loop baraye estekhraj kardane esme namadha
    namadha = []
    for i in result:
        namadha.append(i[0])
        pass
    return(namadha)
def avaragecheck(name):
    #sql
    try:
        con = sql.connect(r"C:\moneymaker\db\saham.db")
        cur = con.cursor()
        result = cur.execute(r"SELECT date,avarage FROM '%s' ORDER BY date DESC"
                             %(name))
        result = result.fetchall()
        con.commit()
        con.close()
        #bargardandane natayeje 10 rooze akhar
        return(result[0:10])
    except:
        return(None)
    pass
def avarageshow(name):
    con = sql.connect(r"C:\moneymaker\db\saham.db")
    cur = con.cursor()
    result = cur.execute(r"SELECT hk,hf,avarage FROM '%s' ORDER BY date DESC"
                         %(name))
    result = result.fetchall()
    con.commit()
    con.close()
    #checking if avarage is there
    result = result[0:6]
    check = False
    var = []
    for i in result:
        if i[2] == None:
            pass
        else:
            var.append(i[2])
            check = True
            break
        pass
    if check == False:
        return(None)
    else:
        pass
    #mohasebe hf , hk
    hf = 0
    hk = 0
    for i in result:
        hk += i[0]
        hf += i[1]
        pass
    if hf > 8000000 and hk > 8000000 and hf/hk < 1.6:
        hf = int(hf/100000)
        hk = int(hk/100000)
        hf = hf/10
        hk = hk/10
        var.append(hk)
        var.append(hf)
        return(var)
    else:
        return(None)
    pass
def readfk(name):
    #sql
    con = sql.connect(r"C:\moneymaker\db\saham.db")
    cur = con.cursor()
    dateresult = cur.execute(r"SELECT date FROM '%s' ORDER BY date DESC"
                             %(name))
    dateresult = dateresult.fetchall()
    #check kardan tarikh
    datelen = len(dateresult)
    if datelen > 6:
        if (dateresult[0][0] - dateresult[6][0]) <= 105:
            check = True
            pass
        else:
            check = False
            pass
        pass
    else:
        check = False
        pass
    #bargardandane meghdare fk va date 8 rooze akhar
    if check == True:
        fkresult = cur.execute(r"SELECT fk FROM '%s' ORDER BY date DESC"
                               %(name))
        fkresult = fkresult.fetchall()
        mul = 0
        count = 0
        result = []
        for i in fkresult:
            mul += i[0]
            result.append(dateresult[count][0])
            result.append(fkresult[count][0])
            count += 1
            if count == 6:
                break
            else:
                pass
            pass
        result.append(mul)
        pass
    #agar tarikh ha ghadimi boodand
    else:
        result = None
        pass
    con.commit()
    con.close()
    return(result)
def writefk(name, avarage, date):
    #sql
    con = sql.connect(r"C:\moneymaker\db\saham.db")
    cur = con.cursor()
    #update kardan avarage dar tarikhe morede nazar
    cur.execute("UPDATE '%s' SET avarage = '%s' WHERE date = '%s';"
                %(name, avarage, date))
    con.commit()
    con.close()
    pass
#in tabe baraye bargardandane tarikh haye zakhire shode dar yek db ast
def checkdates(name):
    #vasl shodan be sql va khandane tarikhe namadha
    con = sql.connect(r"C:\moneymaker\db\saham.db")
    cur = con.cursor()
    result = cur.execute(r"SELECT date FROM '%s' ORDER BY date DESC"
                         %(name))
    result = result.fetchall()
    con.commit()
    con.close()
    del cur
    del con
    dates = []
    #loop baraye estekhraje tarikh ha
    for i in result:
        dates.append(i[0])
        pass
    return(dates[0])

#BLACKLIST: asamiyi ke nmishe etelaateshono gereft

#tabe baraye save kardan dar blacklist
def blacklistwrite(name):
    con = sql.connect(r"C:\moneymaker\db\saham.db")
    cur = con.cursor()
    b = cur.execute("INSERT INTO blacklist(name) "
                    "VALUES('%s')"
                    %(name))
    con.commit()
    con.close()
    pass
#tabe baraye khandane asami blacklistha
def doneread():
    con = sql.connect(r"C:\moneymaker\db\saham.db")
    cur = con.cursor()
    result = cur.execute(r"SELECT * FROM done ORDER BY date DESC")
    result = result.fetchall()
    con.commit()
    con.close()
    return(result[0])
def donewrite(highest, value):
    con = sql.connect(r"C:\moneymaker\db\saham.db")
    cur = con.cursor()
    result = cur.execute(r"INSERT INTO done(date,status)"
                         r"VALUES(%s,%s)"
                         %(highest, value))
    con.commit()
    con.close()
    return('writing in done is done')
def blacklistread():
    #sql save
    con = sql.connect(r"C:\moneymaker\db\saham.db")
    cur = con.cursor()
    result = cur.execute(r"SELECT name FROM blacklist")
    result = result.fetchall()
    con.commit()
    con.close()
    blacklist = []
    #estekhraj
    for i in result:
        blacklist.append(i[0])
        pass
    return(blacklist)
