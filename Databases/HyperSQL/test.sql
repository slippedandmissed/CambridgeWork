SELECT DISTINCT g1.genre AS genre1, g2.genre AS genre2, COUNT(m.movie_id)
FROM Genres AS g1
INNER JOIN Has_Genre AS h1 ON g1.genre_id = h1.genre_id
INNER JOIN Movies AS m ON h1.movie_id = m.movie_id
INNER JOIN Has_Genre AS h2 ON m.movie_id = h2.movie_id
INNER JOIN Genres AS g2 ON h2.genre_id = g2.genre_id
WHERE g1.genre < g2.genre
GROUP BY g1.genre, g2.genre;