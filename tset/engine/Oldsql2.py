# -*- coding: utf-8 -*-
import _sqlite3 as sql
#in tabe baraye vared kardane etelaat jadid be db mibashad
def write(namadha):
    #vasl shodan be sql va neveshtane etelaat
    con = sql.connect(r"C:\moneymaker\db\saham.db")
    cur = con.cursor()
    b = cur.execute("INSERT INTO '%s'(date, kh, hk, fh, hf, fk) "
                    "VALUES('%s', '%s', '%s', '%s', '%s', '%s')"
                    %(namadha[0], namadha[1], namadha[2], namadha[3], namadha[4], namadha[5], namadha[6]))
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
        return(result)
    except:
        return(None)
    pass
def avarageshow(name):
    con = sql.connect(r"C:\moneymaker\db\saham.db")
    cur = con.cursor()
    result = cur.execute(r"SELECT hk,hf,avarage FROM '%s' ORDER BY date DESC"
                         %(name))
    hk = 0
    hf = 0
    var = []
    result = result[0:7]
    for i in result:
        hk += i[0]
        hf += i[1]
        pass
    if hf > 8000000 or hk > 8000000:
        hk = int(hk*1000)
        hk = hk/1000
        var.append(hk)
        var.append(hf)
        pass
    else:
        return(None)
    for i in result:
        if i[2] == None:
            continue
        else:
            var.append(i[2])
            con.commit()
            con.close()
            return(var)
        pass
    pass
def readfk(name, count0, count1):
    #sql
    con = sql.connect(r"C:\moneymaker\db\saham.db")
    cur = con.cursor()
    dateresult = cur.execute(r"SELECT date FROM '%s' ORDER BY date DESC"
                             %(name))
    dateresult = dateresult.fetchall()
    #check kardan tarikh
    datelen = len(dateresult)
    if datelen > count0:
        if (dateresult[count0][0] - dateresult[count1][0]) <= 105:
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
        for i in fkresult[count0 : count1]:
            mul += i[0]
            result.append(dateresult[count0][0])
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
    result = cur.execute(r"SELECT fs FROM '%s' ORDER BY date"
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
    return(dates)

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
