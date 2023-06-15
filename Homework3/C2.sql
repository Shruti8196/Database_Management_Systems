select Manufacturer,avg(Price) as Average from Beers2Bars group by Manufacturer;

/*
+----------------+---------+
| Manufacturer   | Average |
+----------------+---------+
| Anheuser-Busch |       3 |
| Heineken       |       2 |
| Pete's         |     3.5 |
+----------------+---------+
3 rows in set (0.01 sec)
*/