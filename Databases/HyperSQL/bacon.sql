WITH RECURSIVE counter(pid, bacon_number) AS
(
	VALUES(CAST('nm0000102' AS VARCHAR(255)), 0)

	UNION ALL

	SELECT DISTINCT p2.person_id, min(c1.bacon_number+1) FROM counter AS c1
		INNER JOIN plays_role AS a1 ON a1.person_id=c1.pid
		INNER JOIN plays_role AS a2 ON a1.movie_id=a2.movie_id
		INNER JOIN people as p2 ON p2.person_id=a2.person_id
	WHERE
		c1.bacon_number < 7 -- DESIRED BACON NUMBER GOES HERE
	GROUP BY p2.person_id
)
SELECT DISTINCT pid FROM counter AS c1
WHERE
	bacon_number = (SELECT min(c2.bacon_number) FROM counter AS c2 WHERE c2.pid=c1.pid) AND
	bacon_number = (SELECT max(c2.bacon_number) FROM counter AS c2)
ORDER BY pid
;