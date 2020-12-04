select distinct p.name as name, m.year - p.deathYear as gap
	from people as p
	inner join has_position as h on h.person_id = p.person_id
	inner join movies as m on m.movie_id = h.movie_id
	where h.position='writer'
	and m.year>p.deathYear
order by gap desc, p.name
limit 10;