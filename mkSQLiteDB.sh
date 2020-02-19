sqlite3 blinds.db

CREATE TABLE "hashtable" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"hash"	TEXT,
	"url"	TEXT,
        "expire_date" INTEGER,
	"uid"	INTEGER
);

CREATE TABLE "identities" (
	"uid"	INTEGER,
	"user"	TEXT,
	"certFingerprint"	TEXT
);
