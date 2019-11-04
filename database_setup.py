import sqlite3

new_db = sqlite3.connect("database.db")
c = new_db.cursor()

c.execute('CREATE TABLE "tblUsers" (	"UserID"	INTEGER,	"UserName"	text,	"Password"	text,	"TeamNum"	text,	"Admin"	INT,	PRIMARY KEY("UserID" AUTOINCREMENT))')
c.execute('CREATE TABLE "tblEvents" (	"EventID"	TEXT,	"EventName"	TEXT,	"City"	TEXT,	"Postcode"	TEXT,	"Season"	TEXT,	"Date"	TEXT)')
c.execute('CREATE TABLE "tblMatches" (	"EventID"	TEXT,	"MatchNum"	INTEGER,	"MatchLevel"	INTEGER,	"RedTeam1"	TEXT,	"RedTeam2"	TEXT"'
          '",	"BlueTeam1"	TEXT,	"BlueTeam2"	TEXT,	"RedScore"	INTEGER,	"BlueScore"	INTEGER)')
c.execute('CREATE TABLE "tblTeams" (	"TeamNum"	TEXT,	"TeamName"	TEXT,	"City"	TEXT,	"Country"	TEXT,	"SkillRating"	REAL)')

new_db.commit()