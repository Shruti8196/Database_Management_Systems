select distinct bar as Bar from Sells where price = (select max(price) from Sells);

/*
+-----------+
| Bar       |
+-----------+
| Joe's bar |
+-----------+
1 row in set (0.00 sec)
*/