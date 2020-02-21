sqlite3 blinds.db

CREATE TABLE "hashtable" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	"hash"	TEXT UNIQUE,
	"url"	TEXT,
        "expire_date" INTEGER,
	"uid"	INTEGER
);

CREATE TABLE "identities" (
	"uid"	INTEGER,
	"user"	TEXT,
	"certFingerprint"	TEXT UNIQUE
);
