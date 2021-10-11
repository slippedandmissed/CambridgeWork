#!/usr/bin/python3.9

import ucamcl

GRADER = ucamcl.autograder('https://markmy.solutions', course='scicomp').subsection('ex0')

q = GRADER.fetch_question('q0')
ans = [q.x] * q.n
GRADER.submit_answer(q, ans)
