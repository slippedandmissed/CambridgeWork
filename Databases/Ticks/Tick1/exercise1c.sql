select r1.role as role, p.name as name, m1.title as movie_title, m2.title as tv_movie_title
	from people as p
	inner join plays_role as r1 on r1.person_id = p.person_id
	inner join plays_role as r2 on r2.person_id = p.person_id
	inner join movies as m1 on r1.movie_id = m1.movie_id
	inner join movies as m2 on r2.movie_id = m2.movie_id
	where m1.type='movie'
	and m2.type='tvMovie'
	and r1.role=r2.role
order by r1.role, p.name, m1.title, m2.title;