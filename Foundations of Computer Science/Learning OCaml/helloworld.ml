let rec gcd a b =
    if a = 0 || b = 0 then 0
    else if a < 0 || b < 0 then gcd (abs a) (abs b)
    else if a = b then a
    else if a mod 2=0 then
        if b mod 2=0 then 2 * (gcd (a/2) (b/2))
        else gcd (a/2) b
    else if b mod 2=0 then gcd a (b/2)
    else gcd b (abs (a/2 - b/2));;