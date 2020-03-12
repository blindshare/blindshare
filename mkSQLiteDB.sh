sqlite3 blinds.db

CREATE TABLE "Access" (
	"fileID"	  INTEGER NOT NULL PRIMARY KEY,
	"userID"	  INTEGER NOT NULL,
	"expire_date"	  TEXT
);

CREATE TABLE "Files" (
	"fileID"	  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"hash"	          INTEGER NOT NULL UNIQUE,
	"url"	          TEXT NOT NULL
);

CREATE TABLE "Identities" (
	"userID"	  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	          TEXT,
	"certFingerprint" TEXT UNIQUE,
	"view"	          INTEGER,
	"upload"	  INTEGER
);
