select name from Drinkers where name not in (select l1.drinker from Likes l1,Likes l2 where l1.drinker = l2.drinker and l1.beer = "Bud" and l2.beer="Summerbrew") and name in (select distinct l1.drinker from Likes l1);

/*
+----------+
| name     |
+----------+
| Bill     |
| Jennifer |
+----------+
2 rows in set (0.00 sec)
*/