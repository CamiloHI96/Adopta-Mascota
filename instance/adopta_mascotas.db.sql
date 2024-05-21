BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"lastname"	INTEGER NOT NULL,
	"phone"	TEXT NOT NULL,
	"email"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "refugios" (
	"id"	INTEGER,
	"nombre"	TEXT NOT NULL,
	"direccion"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "mascotas" (
	"id"	INTEGER,
	"id_refugio"	INTEGER,
	"foto_url"	TEXT,
	"nombre"	TEXT,
	"edad"	INTEGER,
	"raza"	TEXT,
	"tipo"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_refugio") REFERENCES "refugios"("id")
);
INSERT INTO "users" VALUES (1,'Camilo','Hernandez','321','camilo@gmail.com','pbkdf2:sha256:600000$s6xg3NmJHzfUBi5v$6c49613fcc6257cfddced8b463865668c1c8e4e6bc0de57bca98fb672b844496');
INSERT INTO "users" VALUES (2,'Milo','Hernandez','321','camilohi@gmail.com','pbkdf2:sha256:600000$dsu8MV5YLzBReMjU$e695ece5f84333d0d24e991472d0fad85c31c80aabba4d2b8f72c36aecaae73d');
INSERT INTO "users" VALUES (3,'a','a','a','a@gmail.com','pbkdf2:sha256:600000$mFAQUhF5pW2zKORP$892a94c03c50a8e9340b5971e17d5f5d86395a2203e4c167880ecdfba847b649');
INSERT INTO "users" VALUES (4,'Camilo','Hernandez','321','camiloh@gmail.com','pbkdf2:sha256:600000$MN8S9kZHE5rH8l49$ff99eb146693f6cbdca41835004cfe31956767bf75089834cff4fcffb13504f2');
INSERT INTO "users" VALUES (5,'Pepe','Lopez','33333333','pepe@gmail.com','pbkdf2:sha256:600000$ZEZRNKrPK1DQQkzC$e3cd2d136ddd90a047e9342afdc79181e12a658e8b8a6239ff0c53803f9edb3b');
INSERT INTO "refugios" VALUES (7,'Camilo','camilo');
INSERT INTO "refugios" VALUES (8,'cristian','cristian');
INSERT INTO "refugios" VALUES (9,'Huellitas','Mz 4 Cs 18');
INSERT INTO "refugios" VALUES (10,'Okumari','Zoológico');
INSERT INTO "refugios" VALUES (11,'Felipe','Calle 15');
INSERT INTO "mascotas" VALUES (4,7,'C:\Users\Camilo Hernandez\Documents\GitHub\Adopta-Mascotas\instance\foto-mascotas\perro.jpg','Piti',2,'Persa','Gato');
INSERT INTO "mascotas" VALUES (5,11,'Jgttkkkk','Barto',6,'Angora','Gato');
COMMIT;
