class Regatta:
    def __init__(self,district,index,name,club_name):
        self.district = district
        self.index = index
        self.name = name
        self.club_name = club_name

    def __str__(self):
       return f"Περιφέρεια: {self.district}  index: {self.index}  Όμιλος:{self.club_name}"
    def __repr__(self):
        return f"Περιφέρεια: {self.district}  index: {self.index}  Όμιλος:{self.club_name}"

class Race:
    def __init__(self, stdate, sttime, course, length):
        self.stdate = stdate
        self.sttime = sttime
        self.course = course
        self.length = length

    def __str__(self):
        return f"Ημερ:{self.stdate} {self.sttime}  Διαδρομή: {self.course} Απόσταση:{self.length}"

    def __repr__(self):
        return f"Ημερ:{self.stdate} {self.sttime}  Διαδρομή: {self.course} Απόσταση:{self.length}"

class RaceType1(Regatta,Race):
    def __init__(self,district,index,name,club_name,stdate,sttime,course,length):
        Regatta.__init__(self,district,index,name,club_name)
        Race.__init__(self, stdate, sttime, course, length)

    def __repr__(self):
        return f" {Regatta.__repr__(self)} {Race.__repr__(self)}"

    def __str__(self):
        return f" {Regatta.__str__(self)} {Race.__str__(self)}"

class RaceType2(Regatta,Race):

    def __init__(self,district,index,name,club_name,stdate, sttime,course,length,todate):
        Regatta.__init__(self,district,index,name,club_name)
        Race.__init__(self,stdate,sttime,course,length)
        self.todate = todate

    def __str__(self):
        return f"{Regatta.__str__(self)} Ημερ:{self.stdate} {self.sttime} ΕΩΣ  {self.todate}  Διαδρομή: {self.course} Απόσταση:{self.length}"
    def __repr__(self):
        return f"{Regatta.__repr__(self)} Ημερ:{self.stdate} {self.sttime} ΕΩΣ  {self.todate}  Διαδρομή: {self.course} Απόσταση:{self.length}"


class RaceType3(Regatta,Race):

    def __init__(self,district,index,name,club_name):
        Regatta.__init__(self,district,index,name,club_name)
        self.races = []

    def __str__(self):
        st = Regatta.__str__(self)
        for race in self.races:
            st += f"\n\t\t\t\t\t\t\t\t\t\t\t{race.__str__()} "
        return st

    def __repr__(self):
        st = Regatta.__repr__(self)
        for race in self.races:
            st += f"\n\t\t\t\t\t\t\t\t\t\t\t{race.__repr__()} "
        return st
