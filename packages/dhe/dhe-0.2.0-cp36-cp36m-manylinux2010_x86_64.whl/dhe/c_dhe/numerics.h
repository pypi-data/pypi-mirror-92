#ifndef _NUMERICS_H_
#define _NUMERICS_H_

_Bool solve_tridiagonal(const double *diag,
			const double *upper,
			const double *lower,
			double *b,
			unsigned int n,
			unsigned int m
			);

void solve_vandermonde(const double *x, const double *q, unsigned int n, double *w);

#endif // _NUMERICS_H_
