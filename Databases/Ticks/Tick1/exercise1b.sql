select p.name as name, pr.role as role, count(*) as movie_count
	from people as p
	inner join plays_role as pr on pr.person_id = p.person_id
	inner join movies as m on pr.movie_id = m.movie_id
	where m.type = 'movie'
group by name, role
order by movie_count desc, name, role
limit 10;