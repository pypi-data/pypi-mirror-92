#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdio.h>

#include "c_dhe.h"
#include "c_dhe_core.h"
#include "numerics.h"

static TBrineMethodNew T_brine_dynamic_new, T_brine_stationary_new;
static TBrineMehtodFree T_brine_dynamic_free, T_brine_stationary_free;

const TBrineMethod T_BRINE_DYNAMIC = (TBrineMethod){
						    .new = &T_brine_dynamic_new,
						    .destroy = &T_brine_dynamic_free,
						    .calc = &T_brine_dynamic
};
const TBrineMethod T_BRINE_STATIONARY = (TBrineMethod){
						       .new = &T_brine_stationary_new,
						       .destroy = &T_brine_stationary_free,
						       .calc = &T_brine_stationary
};

static double* arange(double x0, double x1, double dx, unsigned int *out_n);

typedef struct {
  double *sum_g;
  double *dg;
  const DHECore *dhe;
  unsigned int n_DHE;
} DHEField;

static unsigned int optimal_n_steps(double* L, double* C, unsigned int dim_ax, unsigned int dim_rad, double dt, double c);
static double R_1(double dl, double *r, double *rz, double alpha, double lambda_fill, double Ra, double Rb);
static double* R_2(double dl, double *r, double *rz, double lambda_fill, double *lambda_soil, unsigned int dim_ax, double Ra, double Rb);
static void stateful_dhe_new(const DHE *dhe, const GlobalParameters *env, const double *t_boundary_refresh, unsigned int dim_t, DHECore *out_dhe, DHEState *out_state);
static void free_dhe_state(DHEState *state);
static void free_dhe(DHECore *dhe, const TBrineMethod* method);

void calc_P(double *t, double *P, unsigned int dim_t, DHE *dhe, unsigned int n_DHE, GlobalParameters *env, double precision, CalcPOutput *out)
{
  // state->T_U
  unsigned int i;
  unsigned int n_boundary_refresh;
  double *t_boundary_refresh = arange(
				      t[0] + env->dt_boundary_refresh, t[dim_t-1] + env->dt_boundary_refresh, env->dt_boundary_refresh, &n_boundary_refresh); // free [x]
  double U_brine_on = 0.;
  for(i=0; i<n_DHE; i++) U_brine_on += dhe[i].brine_properties.c * dhe[i].Phi_m;
  double *U_brine = malloc(dim_t*sizeof(double));  // free [x]
  for(i=0; i<dim_t; i++)
    U_brine[i] = P[i] > 0.? U_brine_on: 0.;
  DHECore *dhe_ = malloc(n_DHE*sizeof(DHECore));   // free [x]
  DHEState *states = malloc(n_DHE*sizeof(DHEState));  // free [x]
  for(i=0; i<n_DHE; i++) stateful_dhe_new(&dhe[i], env, t_boundary_refresh, n_boundary_refresh, &dhe_[i], &states[i]); // free [x]
  free(t_boundary_refresh);
  double *sum_Q0 = calloc(env->dim_ax, sizeof(double));  // free [x]
  double *Q_wall = calloc(env->dim_ax, sizeof(double));  // free [x]
  calc_P_core(P, U_brine, env->dim_ax, env->dim_rad,
	      dim_t,
	      n_DHE,
	      dhe_, states,
	      sum_Q0,
	      Q_wall,
	      (env->dt_boundary_refresh / env->dt),
	      precision,
	      out);
  free(U_brine);
  for(i=0; i<n_DHE; i++) {
    free_dhe_state(&states[i]);
    free_dhe(&dhe_[i], env->T_brine_method);
  }
  free(dhe_);
  free(states);
  free(sum_Q0);
  free(Q_wall);
}



static double* T_soil_evolution(double *L, double* C, double dt_step, unsigned int dim_ax, unsigned int dim_rad);
static void sample_soil_layers(SoilLayerProperties *layers, unsigned int n_layers, double L_DHE, unsigned int dim_ax, double *out_c_V_soil, double *out_lambda_soil);
static void L_pump(double dl, double* r, double* rz,unsigned int dim_r,  double L1_on, double L1_off, double* R2, double adiabat, unsigned int dim_ax, double* lambda_soil, double *out_L_on, double *out_L_off);
static double* C_matrix(double dl, double* r, unsigned int dim_ax, unsigned int dim_rad, double c_V_fill, double* c_V_soil);
static double* r_grid(double D_DHE, double D_borehole, double R, unsigned int dim_rad, double Gamma);
static double* rz_grid(double* r, unsigned int dim_r);
static double alpha0(double lambda_brine, double D);
static double alpha1(const FluidProperties *brine_properties, double Phi,
		     double D_DHE, double thickness_DHE);
#define DIM_G 5
static double g_poly(const double g[DIM_G], double d_DHE,
		     double d_DHE_ref /* = 10 */,
		     double d_DHE_delta /* = 0.05*/, double *out_g);
static double* T_soil_0(double t0, double g_coefs[DIM_G+1], unsigned int dim_ax, double dl, double* c_V_soil, double* lambda_soil, double* rz, unsigned int dim_r,
			double T_soil, double* q_drain,
			double T_grad /* = 0.03*/,
			double u_min);

static void stateful_dhe_new(const DHE *dhe, const GlobalParameters *env, const double *t_boundary_refresh, unsigned int dim_t, DHECore *out_dhe, DHEState *out_state) {
  unsigned int dim_ax = env->dim_ax;
  unsigned int dim_rad = env->dim_rad;
  unsigned int _a;
  double dl = dhe->L / dim_ax;  // [m]
  double *c_V_soil = malloc(dim_ax*sizeof(double)),  // free [x]
    *lambda_soil = malloc(dim_ax*sizeof(double));  // free [move]
  sample_soil_layers(env->soil_layers, env->n_soil_layers, dhe->L, dim_ax, c_V_soil, lambda_soil);
  double R_domain = env->R - 0.5 * dhe->D_borehole;
  double *r = r_grid(dhe->D, dhe->D_borehole,
		     R_domain, dim_rad, env->Gamma); // free [x]
  double *rz = rz_grid(r, dim_rad+1); // free [x]

  double d_DHE_ref = 10.;
  double d_DHE_delta = 0.05;
  double *q_drain = malloc(dim_ax*sizeof(double));  // free [x]
  for(_a=0; _a<dim_ax; _a++) q_drain[_a] = 0.;
  double g_values[DIM_G+1];
  double u_min = g_poly(dhe->T_soil_0_parameters.g_coefs,
			dhe->T_soil_0_parameters.d_DHE,
			d_DHE_ref, d_DHE_delta, g_values);
  double *T_soil = T_soil_0(
			    env->t0, g_values, dim_ax, dl, c_V_soil,
			    lambda_soil,
			    rz, dim_rad+2, env->soil_parameters.T_soil_mean,
			    q_drain,
			    env->soil_parameters.T_grad, u_min); // free [move]
  free(q_drain);
  double *T_U = malloc(2*dim_ax*sizeof(double));  // free [move]
  for(_a=0; _a<dim_ax; _a++)
    T_U[_a] = T_soil[_a];
  for(_a=0; _a<dim_ax; _a++)
    T_U[dim_ax + _a] = T_soil[dim_ax - 1 - _a];

  *out_state = (DHEState){ .T_U = T_U, .T_soil = T_soil, .T_sink = 0.,
			   .Q = calloc(dim_t * dim_ax, sizeof(double))};   // free [move]

  double U_brine = dhe->brine_properties.c * dhe->Phi_m;
  double alpha = alpha1(&dhe->brine_properties,
			dhe->Phi_m / dhe->brine_properties.rho,
			dhe->D, dhe->thickness);

  double R1 = dhe->R1;
  double lambda_fill = dhe->fill_properties.lambda;
  double c_V_fill = dhe->fill_properties.c * dhe->fill_properties.rho;
  double lambda_brine = dhe->brine_properties.lambda;
  if(R1 <= 0.)
    R1 = R_1(dl, r, rz, alpha, lambda_fill,
	     dhe->Ra, dhe->Rb);
  double *R2 = R_2(dl, r, rz, lambda_fill, lambda_soil, dim_ax,
		   dhe->Ra, dhe->Rb); // free [x]
  double L1_on = 1. / R1;
  double L1_off = 1. / (R1 + (1. / alpha0(lambda_brine, dhe->D) - 1. / alpha) / (8. * M_PI * r[0] * dl));

  double *L_on = malloc(dim_ax*(dim_rad+1)*sizeof(double)),  // free [x]
    *L_off = malloc(dim_ax*(dim_rad+1)*sizeof(double));  // free [x]
  L_pump(dl, r, rz, dim_rad+1, L1_on, L1_off,
	 R2, env->adiabat, dim_ax, lambda_soil, L_on, L_off); // (dim_rad+1) x dim_ax
  free(R2);
  free(rz);

  // Heat capacity
  double *C = C_matrix(dl, r, dim_ax, dim_rad, c_V_fill, c_V_soil); // free [x]
  free(r);
  unsigned int n_steps = optimal_n_steps(L_on, C, dim_ax, dim_rad, env->dt,
					 env->optimal_n_steps_multiplier);
  double dt_step = env->dt / n_steps;

  double C_brine = 2. * dhe->brine_properties.c * dhe->brine_properties.rho * M_PI * 0.25 * dhe->D * dhe->D * dl;  // J/K
  double Lm_min = C_brine / (U_brine>L1_on?U_brine:L1_on);
  unsigned int n_steps_on = (unsigned int)(env->n_steps_0 * dt_step / Lm_min) + 1;
  unsigned int n_steps_off = (unsigned int)(env->n_steps_0 * dt_step / C_brine * L1_off) + 1;
  double *L_on_0 = malloc(dim_ax*sizeof(double));  // free [move]
  double *L_off_0 = malloc(dim_ax*sizeof(double));  // free [move]
  for(_a=0; _a<dim_ax; _a++) {
    L_on_0[_a] = L_on[_a*(dim_rad+1)];
    L_off_0[_a] = L_off[_a*(dim_rad+1)];
  }

  void *T_brine_method_on = env->T_brine_method->new(dt_step, C_brine,
						     L_on_0,
						     dim_ax,
						     n_steps_on,
						     U_brine); // free [move]
  void* T_brine_method_off = env->T_brine_method->new(dt_step, C_brine,
						      L_off_0,
						      dim_ax,
						      n_steps_off,
						      0.); // free [move]
  double *g = malloc(dim_ax*(dim_rad+1)*dim_t*sizeof(double));  // free [move]
  env->g_method.method(&env->g_method, t_boundary_refresh, dim_t, c_V_soil, lambda_soil, dim_ax, 1, &env->R, g);
  for(_a=0; _a<dim_ax; _a++) lambda_soil[_a] *= dl; // lambda_soil -> d_lambda_soil
  *out_dhe = (DHECore)
    {
     .x = dhe->x,
     .y = dhe->y,
     .L = dhe->L,
     .R = env->R,
     .L1_on = L1_on,
     .n_steps = n_steps,
     .d_lambda_soil = lambda_soil,
     .g = g,
     .pump_dependent_parameters = {
				   (TSoilParameters){
						     .L = L_off_0,
						     .T_soil_tensor = T_soil_evolution(L_off, C, dt_step, dim_ax, dim_rad), // free [move]
						     .T_brine_refresh = env->T_brine_method->calc,
						     .T_brine_parameters = T_brine_method_off
				   },
				   (TSoilParameters){
						     .L = L_on_0,
						     .T_soil_tensor = T_soil_evolution(L_on, C, dt_step, dim_ax, dim_rad), // free [move]
						     .T_brine_refresh = env->T_brine_method->calc,
						     .T_brine_parameters = T_brine_method_on
				   }},
    };
  free(C);
  free(c_V_soil);
  free(L_on);
  free(L_off);
}
static void free_dhe_state(DHEState *state) {
  free(state->T_U);
  free(state->T_soil);
  free(state->Q);
}
static void free_dhe(DHECore *dhe, const TBrineMethod* method) {
  unsigned int i;
  for(i=0; i<2; i++) {
      free(dhe->pump_dependent_parameters[i].L);
      free(dhe->pump_dependent_parameters[i].T_soil_tensor);
      method->destroy(dhe->pump_dependent_parameters[i].T_brine_parameters);
      free(dhe->pump_dependent_parameters[i].T_brine_parameters);
    }
  free(dhe->d_lambda_soil);
  free(dhe->g);
}



static void* T_brine_dynamic_new(double dt,
				 double dC_brine,
				 double *L,
				 unsigned int dim_ax,
				 unsigned int n_sub_steps,
				 double U_brine) {
  double dt_step = dt / n_sub_steps;
  unsigned int i;
  double *lambda_brine = malloc(dim_ax*sizeof(double));  // free [move]
  double *kappa_rad = malloc(dim_ax*sizeof(double));  // free [move]
  for(i=0; i<dim_ax; i++) lambda_brine[i] = L[i] * 0.5 / n_sub_steps;
  for(i=0; i<dim_ax; i++) kappa_rad[i] = lambda_brine[i] * dt / dC_brine;
  TBrineDynamicParameters *prm = malloc(sizeof(TBrineDynamicParameters));  // free [move]
  *prm =
    (TBrineDynamicParameters) {
			       .kappa_ax = U_brine / dC_brine * dt_step,
			       .kappa_rad = kappa_rad,
			       .lambda_brine = lambda_brine,
			       .n_sub_steps = n_sub_steps
  };
  return prm;
}

static void T_brine_dynamic_free(void* prm) {
  TBrineDynamicParameters *p = prm;
  free(p->kappa_rad);
  free(p->lambda_brine);
}

static void* T_brine_stationary_new(double dt,
				    double dC_brine,
				    double *L,
				    unsigned int dim_ax,
				    unsigned int n_sub_steps,
				    double U_brine) {
  double *kappa_soil = malloc(dim_ax*sizeof(double));  // free [move]
  double *kappa_brine = malloc(dim_ax*sizeof(double));  // free [move]
  unsigned int i;
  for(i=0; i<dim_ax; i++) kappa_soil[i] = L[i] / (L[i] + 2. * U_brine);
  for(i=0; i<dim_ax; i++) kappa_brine[i] = U_brine / (0.5 * L[i] + U_brine);
  TBrineStationaryParameters *prm = malloc(sizeof(TBrineStationaryParameters));  // free [move]
  *prm =
    (TBrineStationaryParameters) {
				  .kappa_soil = kappa_soil,
				  .kappa_brine = kappa_brine,
				  .L = L
  };
  return prm;
}

static void T_brine_stationary_free(void* prm) {
  TBrineStationaryParameters *p = prm;
  free(p->kappa_soil);
  free(p->kappa_brine);
}

static void _LC(double* L, double* C, double dt, unsigned int dim_ax, unsigned int dim_rad, double *out_diag, double *out_offdiag) {
  // L: dim_ax * (dim_rad + 1)
  // C: dim_ax * dim_rad
  unsigned int s = dim_rad, a_, r_;
  for(a_=0; a_<dim_ax; a_++)
    for(r_=0; r_<dim_rad; r_++)
      out_diag[a_*s + r_] = 2. * C[a_*dim_rad + r_] + dt * (L[a_*(dim_rad+1) + r_ + 1] + L[a_*(dim_rad+1) + r_]);
  s = dim_rad - 1;
  for(a_=0; a_<dim_ax; a_++)
    for(r_=0; r_<dim_rad-1; r_++)
      out_offdiag[a_*s + r_] = -dt * L[a_*(dim_rad+1) + r_ + 1];
};

/// Returns B such that
/// T_new[.., 1..-1] = B T_old
/// If (dim_rad+2, dim_ax) is the shape of T_old, then
/// B has shape (dim_ax, dim_rad, dim_rad+2)
///
///  B is determined such that
///  sum_l A_arl T_new[.., 1..-1]_al = sum_l F_arl T_old_al
///        / * * 0 \        / * | * * 0 | 0 \
///  A_a = | * * * |  F_a = | 0 | * * * | 0 |
///        \ 0 * * /        \ 0 | 0 * * | * /
static double* T_soil_evolution(double *L, double* C, double dt_step, unsigned int dim_ax, unsigned int dim_rad) {
  double *A_diag = malloc(dim_ax * dim_rad * sizeof(double));  // free [x]
  double *A_offdiag = malloc(dim_ax * (dim_rad-1) * sizeof(double));  // free [x]
  _LC(L, C, dt_step, dim_ax, dim_rad, A_diag, A_offdiag);
  double *F_diag = malloc(dim_ax * dim_rad * sizeof(double));  // free [x]
  double *F_offdiag = malloc(dim_ax * (dim_rad-1) * sizeof(double));  // free [x]
  _LC(L, C, -dt_step, dim_ax, dim_rad, F_diag, F_offdiag);
  double *TT = malloc(dim_ax * (dim_rad+2) * dim_rad * sizeof(double));  // free [move]
  unsigned int s0 = dim_rad*(dim_rad+2), a_, r_, k;
  double *F = calloc((dim_rad+2) * dim_rad, sizeof(double));  // free [x]
  for(a_=0; a_<dim_ax; a_++) {
    // F_i00 = 2 dt L_i0
    F[0] = 2. * dt_step * L[a_*(dim_rad+1)];
    // F_i(dim_rad)(dim_rad+2) = 2 dt L_i(dim_rad)
    F[s0 - 1] = 2. * dt_step * L[(a_+1)*(dim_rad+1) - 1];
    for(r_=0; r_<dim_rad; r_++)
      F[(r_+1) * dim_rad + r_] = F_diag[dim_rad * a_ + r_];
    for(r_=0; r_<dim_rad-1; r_++) {
      F[(r_+1) * dim_rad + r_ + 1] = F_offdiag[(dim_rad-1) * a_ + r_];
      F[(r_+2) * dim_rad + r_] = F_offdiag[(dim_rad-1) * a_ + r_];
    }
    solve_tridiagonal(
		      &A_diag[a_*dim_rad],
		      &A_offdiag[a_*(dim_rad-1)],
		      &A_offdiag[a_*(dim_rad-1)],
		      F,
		      dim_ax,
		      dim_rad+2);
    // Transpose F into TT
    for(r_=0; r_<dim_rad; r_++)
      for(k=0; k<dim_rad+2; k++)
	TT[a_*s0 + r_*(dim_rad+2) + k] = F[k*dim_rad + r_];
  }
  free(A_diag);
  free(A_offdiag);
  free(F_diag);
  free(F_offdiag);
  free(F);
  return TT;
}

/// Given dim_l layers :param layers: of soil with parameters
/// (constant across single layers).
/// Calculate values for a number of dim_ax equispaced layers of total thickness
/// L_DHE. The output layers values are taken to be the length averages of the
/// input layer values over the ranges of the output layers.
static void sample_soil_layers(SoilLayerProperties *layers, unsigned int n_layers, double L_DHE, unsigned int dim_ax, double *out_c_V_soil, double *out_lambda_soil) {
  double L;
  SoilLayerProperties *layers_end = layers + n_layers;
  double L0_layer = 0.;
  SoilLayerProperties *layer = layers;
  double d_layer = layer->d;
  double L1_layer = layer->d;
  double c_V_layer = 0.;
  double lambda_layer = 0.;
  double d_L = L_DHE / dim_ax;
  unsigned int i;
  for(i=0; i<dim_ax; i++) {
    L = (i+1) * L_DHE / dim_ax;
    while(L1_layer < L) {
      c_V_layer += layer->c * layer->rho * d_layer;
      lambda_layer += layer->lambda * d_layer;
      layer++;
      if(layer != layers_end) d_layer = layer->d;
      else d_layer = INFINITY;
      L0_layer = L1_layer;
      L1_layer += d_layer;
    }
    c_V_layer += layer->c * layer->rho * (L - L0_layer);
    lambda_layer += layer->lambda * (L - L0_layer);
    out_c_V_soil[i] = c_V_layer / d_L;
    out_lambda_soil[i] = lambda_layer / d_L;
    c_V_layer = 0.;
    lambda_layer = 0.;
    d_layer -= L - L0_layer;
    L0_layer = L;
  }
}

/// Determine optimal value for n_steps
static unsigned int optimal_n_steps(double* L, double* C, unsigned int dim_ax, unsigned int dim_rad, double dt, double c) {
  double dt_min = C[0] / L[0];
  double x;
  unsigned int I[3][2] = {{0,0}, {0,1}, {1,1}};
  unsigned int i, a_;
  for(i=0;i<3;i++) {
    for(a_=0; a_<dim_ax; a_++) {
      x = C[a_* dim_rad + I[i][0]] / L[a_*(dim_rad+1) + I[i][1]];
      if(x < dt_min) dt_min = x;
    }
  }
  unsigned int out = (c * dt / dt_min);
  if(out == 0) return 1;
  return out;
}

/// Resistance R1 in bore hole
static double R_1(double dl, double *r, double *rz, double alpha, double lambda_fill, double Ra, double Rb) {
  if(Ra > 0. && Rb > 0.) return Ra / (4. * dl);
  if(Rb > 0.)
    return Rb / dl - 1. / (2. * M_PI * dl * lambda_fill)
      * log(r[1] / rz[1]);
  return (1. / (alpha * r[0])
	  + log((r[1] - rz[1]) / r[0]) / lambda_fill) / (8. * M_PI * dl);
}

/// Resistance R2 in bore hole
static double* R_2(double dl, double *r, double *rz, double lambda_fill, double *lambda_soil, unsigned int dim_ax, double Ra, double Rb) {
  double *out = malloc(dim_ax*sizeof(double));  // free [move]
  unsigned int a_;
  if(Ra > 0. && Rb > 0.)
    for(a_=0; a_<dim_ax; a_++)
      out[a_] = (Rb - 0.25 * Ra) / dl
	+ log(rz[2] / r[1]) / (2. * M_PI * dl * lambda_soil[a_]);
  else
    for(a_=0; a_<dim_ax; a_++)
      out[a_] = (log(r[1] / rz[1]) / lambda_fill +
		 log(rz[2] / r[1]) / lambda_soil[a_]) / (2. * M_PI * dl);
  return out;
}

/// Pump on / off
static void L_pump(double dl, double* r, double* rz,unsigned int dim_r,  double L1_on, double L1_off, double* R2, double adiabat, unsigned int dim_ax, double* lambda_soil, double *out_L_on, double *out_L_off) {
  // dim_r = dim_rad + 1
  unsigned int a_, r_;
  for(a_=0; a_<dim_ax; a_++) {
    out_L_on[a_ * dim_r] = L1_on;
    out_L_off[a_ * dim_r] = L1_off;
    out_L_on[a_ * dim_r + 1] = 1. / R2[a_];
    out_L_on[(a_ + 1)*dim_r - 1] = (1. - adiabat) * 2. * M_PI * dl
      * lambda_soil[a_] / log(r[dim_r-1] / rz[dim_r - 1]);
    for(r_=2; r_<dim_r-1; r_++)
      out_L_on[a_*dim_r + r_] = 2. * M_PI * dl * lambda_soil[a_]
	/ log(rz[r_+1] / rz[r_]);
    for(r_=1; r_<dim_r; r_++)
      out_L_off[a_*dim_r + r_] = out_L_on[a_*dim_r + r_];
  }
}

static double* C_matrix(double dl, double* r, unsigned int dim_ax, unsigned int dim_rad, double c_V_fill, double* c_V_soil) {
  double *C = malloc(dim_ax * dim_rad * sizeof(double));  // free [move]
  unsigned int a_, r_;
  for(a_=0; a_<dim_ax; a_++) {
    C[a_*dim_rad] = M_PI * c_V_fill * (r[1]*r[1] - 4. * r[0]*r[0]) * dl;
    for(r_=1; r_<dim_rad; r_++) {
      C[a_*dim_rad + r_] = M_PI * dl * c_V_soil[a_]
	* (r[r_+1]*r[r_+1] - r[r_]*r[r_]);
    }
  }
  return C;
}

/// :param R: Domain of computation
/// :param Gamma: Grid parameter
static double* r_grid(double D_DHE, double D_borehole, double R, unsigned int dim_rad, double Gamma) {
  double *r = malloc((dim_rad+1) * sizeof(double));  // free [move]
  r[0] = 0.5 * D_DHE;
  r[1] = 0.5 * D_borehole;
  double c = R * (1. - Gamma) / (1. - pow(Gamma, dim_rad - 1));
  double x = 0.;
  unsigned int i;
  double Gamma_pow = 1.;
  for(i=2; i<dim_rad+1; i++) {
    x += Gamma_pow;
    Gamma_pow *= Gamma;
    r[i] = r[1] + c * x;
  }
  return r;
}

static double* rz_grid(double* r, unsigned int dim_r) {
  unsigned int l = dim_r + 1;
  double *rz = malloc(l * sizeof(double));  // free [move]
  unsigned int r_;
  for(r_=1; r_<dim_r; r_++)
    rz[r_] = sqrt(0.5 *(r[r_]*r[r_] + r[r_-1]*r[r_-1]));
  rz[0] = r[0];
  rz[l-1] = r[dim_r-1];
  return rz;
}

/// Heat transfer if pump is off
static double alpha0(double lambda_brine, double D) {
  return 2. * lambda_brine / (D * (1. - sqrt(0.5)));
}


/// Heat transfer brine backfill, when pump is on
/// :param thickness_DHE: Thickness DHE pipe
static double alpha1(const FluidProperties *brine_properties, double Phi,
		     double D_DHE, double thickness_DHE) {
  double c_V_brine = brine_properties->c * brine_properties->rho;
  double nu_brine = brine_properties->nu;
  double lambda_brine = brine_properties->lambda;
  double Di = D_DHE - 2. * thickness_DHE;
  double v = 2. * Phi / (Di*Di) / M_PI;
  double Re = v * Di / nu_brine;  // Reynolds number
  double Pr = nu_brine * c_V_brine / lambda_brine;  // Prandtl number
  double Pr_3 = pow(Pr, 1./3.);
  //  Xi: pressure loss coefficient by Petukhov (1970)
  double Xi = 1. / 1.82 * log(Re*Re / log(10.) - 1.64);
  //  Stanton number by Petukhov (1970), valid for at turbulent speed
  double K1 = 1. + 27.2 * Xi / 8.;
  double K2 = 11.7 + 1.8 / Pr_3;
  double St = Xi / 8. / (K1 + K2 * sqrt(Xi / 8.) *
			 (Pr_3*Pr_3 - 1.));  // Stanton number
  //  Stanton number by Petukhov at the border turbulence/transition zone
  double Xi0 = 0.031437;
  double K10 = 1.106886;
  double ST0 = Xi0 / 8. / (K10 + K2 * sqrt(Xi0 / 8.) * (Pr_3*Pr_3 - 1.));
  double Nu0 = ST0 * 10000. * Pr;  // Nusselt number on transition turbulence/transition zone
  double Nu_turbulent = St * Re * Pr;  // Nusselt number for turbulent zone
  double Nu_laminar = 4.36;  // Nusselt number for laminar zone
  double Nu = 0.;
  if(Re >= 10000.) Nu = Nu_turbulent; // turbulent
  if(Re <= 2300.) Nu = Nu_laminar;  // laminar
  // Transition zone laminar/turbulent
  else if(Re < 10000.) Nu = Nu_laminar
			 * exp(log(Nu0 / Nu_laminar) / log(10000. / 2300.) * log(Re / 2300.));
  return Nu * lambda_brine / Di;
}

static double g_poly(const double g[DIM_G], double d_DHE,
		     double d_DHE_ref /* = 10 */,
		     double d_DHE_delta /* = 0.05*/, double *out_g) {
  double *_g = malloc(DIM_G*sizeof(double));  // free [x]
  unsigned int i;
  for(i=0; i<DIM_G; i++) _g[i] = g[i];
  if(fabs(d_DHE - d_DHE_ref) > d_DHE_delta) {
    // Extrapolation of the g function
    double BH = d_DHE / d_DHE_ref;
    if(BH < 0.4) { printf("BH out of bounds"); return NAN; }
    double ExA = g[4] - 6.29;
    double ExB = -log((g[2] - 6.29) / (g[4] - 6.6)) / 27.;
    double g0[DIM_G] = {4.82, 5.69, 6.29, 6.57, 6.6};
    double g_exp[DIM_G] = {343., 125., 27., 1., 0.};
    for(i=0; i<DIM_G; i++) {
      _g[i] = g0[i] + fmax(0., ExA / BH *
			   exp(-BH * ExB * g_exp[i]));
    }
    // e Extrapolation g-Function
  }
  // Calculates g function from 4 sampling points g1,g2,g3,g4
  #define N_X 6
  double x[N_X] = {-4., -2., 0., 2.5, 3., fmin(-4.5, -4. - (_g[0] - 4.82) / 2.)};
  double y[N_X] = {_g[0], _g[1], _g[2], _g[3], _g[4] * 0.99,
		   (log(0.5 / 0.0005) + 0.5 * x[5]) * 0.95};
  free(_g);
  y[3] = (y[3] + y[4]) / 2. * 0.99;
  double u_min = fmax(x[5] + 0.5, -6.);
  solve_vandermonde(x, y, N_X, out_g);
  #undef N_X
  return u_min;
}

/// :param T_grad: Gradient of Temperature axial [K/m]
/// :q_drain: Heat drained par layer. Shape: (dim_ax,)
///
/// :return: numpy array of shape (dim_rad + 2, dim_ax)
static double* T_soil_0(double t0, double g_coefs[DIM_G+1], unsigned int dim_ax, double dl, double* c_V_soil, double* lambda_soil, double* rz, unsigned int dim_r,
			double T_soil, double* q_drain,
			double T_grad /* = 0.03*/,
			double u_min) {
  unsigned int r_, a_, l=0;
  double *Rq = calloc(dim_ax * dim_r, sizeof(double)); // free [x]
  if(t0 != 0.) {
    GFuncParameters g_prm = {.u_min=u_min, .L=dim_ax*dl, .go_const = 6.907755};
    for(r_=0; r_<DIM_G+1; r_++) g_prm.g_coefs[r_] = g_coefs[r_];
    double *g = malloc(dim_ax*dim_r*sizeof(double)); // free [x]
    g_func(&g_prm, &t0, 1, c_V_soil, lambda_soil, dim_ax, dim_r, rz, g);
    for(r_=0; r_<dim_r; r_++) {
      for(a_=0; a_<dim_ax; a_++) {
	Rq[r_*dim_ax + a_] = g[a_*dim_r + r_] / (2. * M_PI * lambda_soil[a_]);
      }
    }
    free(g);
  }
  double *out = malloc(dim_ax * dim_r * sizeof(double)); // free [move]
  for(r_=0; r_<dim_r; r_++) {
      for(a_=0; a_<dim_ax; a_++) {
	  out[l] = T_soil + T_grad * dl * (a_ + 0.5) - Rq[r_*dim_ax + a_] * q_drain[a_] / dl;
	  l += 1;
	}
    }
  free(Rq);
  return out;
}

static double* arange(double x0, double x1, double dx, unsigned int *out_n) {
  unsigned int n = ((x1 - x0) / dx) + 1;
  double *out = malloc(n*sizeof(double)); // free [move]
  unsigned int i;
  for(i=0; i<n; i++) out[i] = x0 + i*dx;
  *out_n = n;
  return out;
}


void free_global_parameters(GlobalParameters *env) {
  if(env != NULL) {
    if(env->soil_layers != NULL) free(env->soil_layers);
    if(env->g_method.data != NULL) free(env->g_method.data);
    free(env);
  }
}
