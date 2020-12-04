match (:Movie {title: 'John Wick'}) <-[r2:ACTED_IN]- (p:Person) -[r1:ACTED_IN]-> (:Movie {title: 'The Matrix Reloaded'})
return p.name as name, r1.roles as roles1, r2.roles as roles2
order by name, roles1, roles2;