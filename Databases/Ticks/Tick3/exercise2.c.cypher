match path=allshortestpaths(
          (m:Person {name : "Steven Spielberg"} ) -[:PRODUCED*]- (n:Person))
     where n.person_id <> m.person_id
     return length(path)/2 as spielberg_number,
            count(distinct n.person_id) as total
order by spielberg_number;
