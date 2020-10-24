BEGIN TRANSACTION;
INSERT INTO $table VALUES (1,'time_zone','TimeZone de reference pour l''application et le Bot','Europe/Paris',CURRENT_TIMESTAMP,NULL);
INSERT INTO $table VALUES (2,'hour_start','Horaire de Debut de la Session de Trading','08:30',CURRENT_TIMESTAMP,NULL);
INSERT INTO $table VALUES (3,'hour_end','Horaire de Fin de la Session de Trading','18:30',CURRENT_TIMESTAMP,NULL);
COMMIT;
