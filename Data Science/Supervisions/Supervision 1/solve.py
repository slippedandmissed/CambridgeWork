(a, b1, b2, e1, e2, e3, e4, e5) = linear_model.LinearRegression( fit_intercept=False).fit(
	numpy.column.stack(
		numpy.ones(len(temp)),
		numpy.sin(2 * numpy.pi * t),
		numpy.cos(2 * numpy.pi * t),
		numpy.where(u="decase_1980s", 1, 0),
		numpy.where(u="decase_1990s", 1, 0),
		numpy.where(u="decase_2000s", 1, 0),
		numpy.where(u="decase_2010s", 1, 0),
		numpy.where(u="decase_2020s", 1, 0)
	),
	temp
)


