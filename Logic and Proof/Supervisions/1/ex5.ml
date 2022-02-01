type proposition =
    | Atom of int
    | Negation of proposition
    | Conjunction of proposition * proposition
    | Disjunction of proposition * proposition;;

type interpretation = bool list;;

let rec holds interp = function
    | Atom x -> List.nth interp x
    | Negation p -> (let q = holds interp p in not q)
    | Conjunction (p1, p2) -> (
        let q1 = holds interp p1
        and q2 = holds interp p2
        in q1 && q2
    )
    | Disjunction (p1, p2) -> (
        let q1 = holds interp p1
        and q2 = holds interp p2
        in q1 || q2
    )
    
let rec nnf = function
    | Atom x -> Atom x
    | Negation p -> (
        match p with
        | Atom x -> nnf (Negation p)
        | Negation q -> nnf q
        | Conjunction (q1, q2) -> nnf (Disjunction (Negation q1, Negation q2))
        | Disjunction (q1, q2) -> nnf (Conjunction (Negation q1, Negation q2))
    )
    | Conjunction (p1, p2) -> Conjunction (nnf p1, nnf p2)
    | Disjunction (p1, p2) -> Disjunction (nnf p1, nnf p2);;