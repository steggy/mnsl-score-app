
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
    
    def FetchShooterIfScore(self,sess):
        sql=f"""select (select concat(fname,' ',lname) as name from shooters where shooterid=id) as name 
        from scores where score > 0 and leaguenum={sess} group by name;"""
        #result = self.db2.fetch(f"select * from shooters where concat(fname,' ',lname) = '{self.name}'")
        result = self.db2.fetch(sql)
        return result
    
    def FetchShooterId(self,name):
        self.name = name
        result = self.db2.fetch(f"select id from shooters where concat(fname,' ',lname) = '{name}'")
        if len(result) < 1:
            return 0
        else:
            return result[0]['id']

    def FetchShooterScoresByDate(self,sid,sess,dte=None):
        #result = self.db2.fetch(f"select dte from scores where leaguenum = {sess} group by dte order by dte desc")
        self.dte = dte
        if len(self.dte) < 1:
            self.dte = '%'
        sql = f"""select scores.id,shooterid,scores.dte,event.name as eventname,division.name as divname,cal,score 
        from scores,event,division where shooterid = {sid} and dte like '{self.dte}' and leaguenum={sess} 
        and scores.eid = event.id and scores.did=division.id order by id desc;"""
        result = self.db2.fetch(sql)
        return result
    
    def FetchSessionDates(self,sess):
        #self.sess = sess
        result = self.db2.fetch(f"select dte from scores where leaguenum like {sess} group by dte order by dte desc")
        return result
    
    def FetchSession(self):
        result = self.db2.fetch(f"select leaguenum from scores group by leaguenum order by leaguenum desc limit 1;")
        return result[0]['leaguenum']
    def Fetchweeks(self,sess):
        result = self.db2.fetch(f"select count(distinct dte) as tot from scores where leaguenum={sess};")
        return result[0]['tot']

    def FetchSessionList(self):
        result = self.db2.fetch(f"select leaguenum from scores group by leaguenum order by leaguenum desc;")
        return result
    
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
    
    def FetchScoreBySSD(self,sid=None,dte=None,sess=None):
        qvlist = [sid,dte,sess]
        cnt = 0
        for i in qvlist:
            if i == '' or i == 0:
                cnt += 1
        if cnt == 3:
            return 0
        sqlh = """select (select concat(fname,' ',lname)as name from shooters where id=shooterid) as name, 
        (select name from event where event.id=eid) as evt,
        (select name from division where division.id=did) as divv,dte,leaguenum as lnum,cal,score """
        sql= "from scores where"
        qklist = ['shooterid','dte','leaguenum']
        for i,v in enumerate(qvlist):
            if str(qvlist[i]) != '' and str(qvlist[i]) != '0':
                if len(sql) > 17:
                    sql += " and"
                if qklist[i] == 'dte':
                    sql += f" {qklist[i]}='{qvlist[i]}'"
                else:    
                    sql += f" {qklist[i]}={qvlist[i]}"
        sql += " order by dte desc"
        sqlh += sql
        result = self.db2.fetch(sqlh)
        return result




