from persiantools.jdatetime import JalaliDate
from hijri_converter import convert
import datetime

class important_dates:
    #Print--Persian--Date-- 
    def toPersian(self):
        MyDate=datetime.datetime.now()
        Date_slice=str(MyDate)[0:10]
        MainDate_=Date_slice.split("-")
        return JalaliDate.to_jalali(int(MainDate_[0]),int(MainDate_[1]),int(MainDate_[2]))

    #--Print--Gergorian--Date--
    def toGergorian(self):
        MainDate_=JalaliDate.to_gregorian(JalaliDate.today())
        return MainDate_

    #--Print--Hijri--Date--
    def toHijri(self):
        Date_Gergorian=JalaliDate.to_gregorian(JalaliDate.today())
        MainDate_=str(Date_Gergorian).split("-")
        MainDate_=convert.Gregorian(int(MainDate_[0]),int(MainDate_[1]),int(MainDate_[2])).to_hijri()
        return MainDate_
class Conver_Date:
    #--Convert--PersianDate--To--GergorianDate--
    def ConvertPersian2Gergorian(self,Date):
        self.Date=Date
        if(Date[4]=="-" and Date[7]=="-"):
            MainDate_=Date.split("-")
            return JalaliDate(int(MainDate_[0]),int(MainDate_[1]),int(MainDate_[2])).to_gregorian()
    #--Convert--GergorianDate--To--PersianDate--
    def ConvertGergorian2Persian(self,Date):
        self.Date=Date
        if(Date[4]=="-" and Date[7]=="-"):
            MainDate_=Date.split("-")
            return JalaliDate.to_jalali(int(MainDate_[0]),int(MainDate_[1]),int(MainDate_[2]))
    #--Convert--HijriDate--To--GergorianDate--
    def ConvertHijri2Gergorian(self,Date):
        self.Date=Date
        if(Date[4]=="-" and Date[7]=="-"):
            MainDate__=Date.split("-")
            return convert.Hijri(int(MainDate__[0]),int(MainDate__[1]),int(MainDate__[2])).to_gregorian()
    #--Convert--GergorianDate--To--HijriDate--
    def ConvertGergorian2Hijri(self,Date):
        self.Date=Date
        if(Date[4]=="-" and Date[7]=="-"):
            MainDate_=Date.split("-")
            return convert.Gregorian(int(MainDate_[0]),int(MainDate_[1]),int(MainDate_[2])).to_hijri()
    #--Convert--PersianDate--To--HijriDate--
    def ConvertPersian2Hijri(self,Date):
            self.Date=Date
            if(Date[4]=="-" and Date[7]=="-"):
                MainDate_=Date.split("-")
                Ger_Date=JalaliDate(int(MainDate_[0]),int(MainDate_[1]),int(MainDate_[2])).to_gregorian()
                Gertohijri=str(Ger_Date)
                ListofDate=Gertohijri.split("-")
                MainDate_=ListofDate
                return convert.Gregorian(int(MainDate_[0]),int(MainDate_[1]),int(MainDate_[2])).to_hijri()
    #--Convert--HijriDate--To--PersianDate--
    def ConvertHijri2Persian(self,Date):
        self.Date=Date
        if(Date[4]=="-" and Date[7]=="-"):
            MainDate_=Date.split("-")
            Ger_Date=convert.Hijri(int(MainDate_[0]),int(MainDate_[1]),int(MainDate_[2])).to_gregorian()
            Main_=str(Ger_Date)
            MainDate_=Main_.split("-")
            return JalaliDate.to_jalali(int(MainDate_[0]),int(MainDate_[1]),int(MainDate_[2]))
