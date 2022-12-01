
import dbhelper as db
import readwriteconfig as CF

class MNSLQuery():
    def __init__(self,confFile):
        self.confFile = confFile
        configdict = dict(CF.Config(confFile).Fetch('database'))
        configlist = list(configdict.values())
        self.session = str(CF.Config(confFile).Fetch('session')[0][1])
        self.db2 = db.dbh(*configlist)

    def FetchShooter(self,name):
        self.name = name
        result = self.db2.fetch(f"select * from shooters where concat(fname,' ',lname) = '{self.name}'")
        return result
    
    def FetchShooterId(self,name):
        self.name = name
        result = self.db2.fetch(f"select id from shooters where concat(fname,' ',lname) = '{name}'")
        if len(result) < 1:
            return 0
        else:
            return result[0]['id']

    def FetchShooterScoresByDate(self,sid,dte):
        #result = self.db2.fetch(f"select dte from scores where leaguenum = {sess} group by dte order by dte desc")
        sql = f"""select scores.id,shooterid,scores.dte,event.name as eventname,division.name as divname,cal,score 
        from scores,event,division where shooterid = {sid} and dte ='{dte}' and scores.eid = event.id and scores.did=division.id;"""
        result = self.db2.fetch(sql)
        return result
    
    def FetchSessionDates(self,sess):
        #self.sess = sess
        result = self.db2.fetch(f"select dte from scores where leaguenum = {sess} group by dte order by dte desc")
        return result
    
    def FetchSession(self):
        result = self.db2.fetch(f"select leaguenum from scores group by leaguenum order by leaguenum desc limit 1;")
        return result[0]['leaguenum']
    
    def FetchSessionStart(self):
        result = self.db2.fetch(f"select min(dte) as sstart from scores where leaguenum ={self.session};")
        return result
    
    def FetchAllShooters(self):
        result = self.db2.fetch(f"select concat(fname,' ',lname) as name from shooters order by fname")
        return result
    
    def FetchCaliber(self):
        result = self.db2.fetch(f"select name from caliber")
        return result
    
    def FetchScoresByDate(self,dte):
        result = self.db2.fetch(f"""select concat(fname, ' ', lname) as name,event.name as evt,division.name as divv,cal,score from scores,shooters,event,division where shooterid = shooters.id and eid=event.id and did=division.id and scores.dte='{dte}' order by fname,lname,scores.id;""")
        return result
    
    def AddShooter(self,sname):
        sn = sname.split()
        sql = f"insert into shooters (fname, lname) values ('{sn[0].title()}','{' '.join(sn[1:]).title()}')"
        try:
            self.db2.execute(sql)
            return 1
        except:
            return 0

    def UpdateShooter(self,infodict):
        sql = f"""update shooters set fname ='{infodict['fname']}',
        lname='{infodict['lname']}',
        gender={infodict['gender']},
        junior={infodict['junior']},
        staff={infodict['staff']},
        phone='{infodict['phone']}',
        email='{infodict['email']}'
        where id = {infodict['id']}"""
        self.db2.execute(sql)
        return
    
    def UpdateScore(self,scoredictlist):
            for i in scoredictlist:
                if i['delete']:
                    sql = f"delete from scores where id = {i['id']}"
                else:    
                    sql = f"update scores set eid={i['eid']},did={i['did']},cal='{i['cal']}',score={i['score']} where id = {i['id']}"
                self.db2.execute(sql)
            return
            
    def AddScore(self,sdict):
            sql = f"""Insert into scores (dte,leaguenum,eid,did,cal,score,shooterid) values 
                ('{sdict['dte']}',{sdict['lnum']},{sdict['eid']},{sdict['did']},'{sdict['cal']}',{sdict['score']},{sdict['sid']});"""
            self.db2.execute(sql)
            return
    
    def ScoreByShooter(self,id,dte=None,session=None):
        if dte is not None:
            result = self.db2.fetch(f"select * from scores where shooterid = {id} and dte ='{dte}'")
        elif session is not None:
            result = self.db2.fetch(f"select * from scores where shooterid = {id} and leaguenum ={session}")
        else:
            result = self.db2.fetch(f"select * from scores where shooterid = {id} ")
        return result
