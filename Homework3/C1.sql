create view Beers2Bars as select b.name as Beer, b.manf as Manufacturer,s.bar as Bar,s.price as Price from Beers b join Sells s on b.name = s.beer;

/*
Query OK, 0 rows affected (0.02 sec)

select * from Beers2Bars;
+------------+----------------+------------+-------+
| Beer       | Manufacturer   | Bar        | Price |
+------------+----------------+------------+-------+
| Bud        | Anheuser-Busch | Bob's bar  |     3 |
| Summerbrew | Pete's         | Bob's bar  |     3 |
| Bud        | Anheuser-Busch | Joe's bar  |     3 |
| Bud Lite   | Anheuser-Busch | Joe's bar  |     3 |
| Michelob   | Anheuser-Busch | Joe's bar  |     3 |
| Summerbrew | Pete's         | Joe's bar  |     4 |
| Bud        | Anheuser-Busch | Mary's bar |  NULL |
| Bud Lite   | Anheuser-Busch | Mary's bar |     3 |
| Budweiser  | Heineken       | Mary's bar |     2 |
+------------+----------------+------------+-------+
9 rows in set (0.01 sec)
*/