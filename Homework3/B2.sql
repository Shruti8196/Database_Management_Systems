select distinct(name) as Drinker from Drinkers where name not in (select distinct(drinker) from Frequents);

/*
Empty set (0.01 sec)
*/