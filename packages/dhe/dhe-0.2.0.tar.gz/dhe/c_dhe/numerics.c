#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

#include "numerics.h"

_Bool solve_tridiagonal(const double *diag,
			const double *upper,
			const double *lower,
			double *b,
			unsigned int n,
			unsigned int m
			) {
  unsigned int i, k;
  if(diag[0] == 0.0) {
    printf("Error 1 in tridiag");
    return false;
  } //If this happens then you should rewrite your equations as a set of order N − 1, with u_1 trivially eliminated.
  double *bet = malloc(n*sizeof(double));  // free [x]
  // One vector of workspace, gam is needed.
  double *gam = malloc(n*sizeof(double));  // free [x]
  bet[0] = diag[0];
  for(i=1; i<n; i++) {
    // Decomposition and forward substitution.
    gam[i] = upper[i - 1] / bet[i - 1];
    bet[i] = diag[i] - lower[i - 1] * gam[i];
    if(bet[i] == 0.0) {
      printf("Error 2 in tridiag");
      free(bet);
      free(gam);
      return false;
    }
    // Algorithm fails; see below
  }
  for(k=0; k<m; k++) {
    double *b_k = &b[k * n];
    b_k[0] /= bet[0];
    for(i=1; i<n; i++) {
      b_k[i] = (b_k[i] - lower[i - 1] * b_k[i - 1]) / bet[i];
    }
    for(i=n-1; i>0; i--)
      b_k[i-1] -= gam[i] * b_k[i];
    // Backsubstitution.
  }
  free(bet);
  free(gam);
  return true;
}

/// Solves the Vandermonde linear system
/// \sum_{i=1}^N x_k^i w_i = q_k (k = 0, ... , N-1). Input consists of
/// the vectors x[0..n-1] and q[0..n-1] ; the vector w[0..n-1] is output.
void solve_vandermonde(const double *x, const double *q, unsigned int n, double *w) {
  if(n == 1) {
    w[0] = q[0];
    return;
  }
  unsigned int i, j;
  double b, t, xx;
  double *a = malloc(n*sizeof(double)); // free [x]
  double *c = calloc(n, sizeof(double)); // free [x]
  for(i=0; i<n; i++) a[i] = 1.;
  for(i=0; i<n; i++) w[i] = 0.;
  c[n - 1] = -x[0];
  // Coefficients of the master polynomial are found by recursion.
  for(i=1; i<n; i++) {
    xx = -x[i];
    for(j=n-i-1; j<n-1; j++)
      c[j] += xx * c[j + 1];
    c[n - 1] += xx;
  }
  // w[j] = \sum_i A_{i j} q_i
  for(i=0; i<n; i++) {
    // Each subfactor in turn
    xx = x[i];
    t = 1.0;
    b = 1.0;
    for(j=n-1; j>0; j--) {
      //    for k in (1..n).rev() {
      // is synthetically divided,
      b = c[j] + xx * b;
      a[j - 1] = b; // A_{i j-1} = b / t_i
      // matrix-multiplied by the right-hand side,
      t = xx * t + b;
    }
    for(j=0; j<n; j++) w[j] += a[j] * q[i] / t;
    // <- A_{i n-1} = 1/t_i
  }
  free(a);
  free(c);
}
