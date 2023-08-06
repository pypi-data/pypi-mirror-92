#ifndef __DHE_CORE_H__
#define __DHE_CORE_H__

typedef double TBrineRoutine(const void* self,
			     const double *T_soil,
			     double *T_U,
			     double *Q_wall,
			     unsigned int dim_ax,
			     double T_sink);
TBrineRoutine T_brine_stationary, T_brine_dynamic;

typedef struct {
  unsigned int n_sub_steps;
  double kappa_ax;
  double *kappa_rad;
  double *lambda_brine;
} TBrineDynamicParameters;

typedef struct {
  double *T_soil_tensor;
  double *L;
  TBrineRoutine *T_brine_refresh;
  void *T_brine_parameters;
} TSoilParameters;

typedef struct
{
  double L;
  double R;
  double x, y;
  double *g;
  double *d_lambda_soil;
  unsigned int n_steps;
  double L1_on;
  TSoilParameters pump_dependent_parameters[2];
} DHECore;

typedef struct
{
  double *Q;
  double *T_soil;
  double *T_U;
  double T_sink;
} DHEState;

typedef struct {
  double *kappa_brine;
  double *kappa_soil;
  double *L;
} TBrineStationaryParameters;

typedef struct {
  double g_coefs[6];
  double u_min, L, go_const;
}
  g_func_parameters;

#define default_go_const 6.84

typedef void GRoutine(const void *self,
		      const double *t,
		      unsigned int dim_t,
		      const double *c_V_soil,
		      const double *lambda_soil,
		      unsigned int dim_ax,
		      unsigned int dim_rad,
		      const double *r,
		      double *out_g
		      );

GRoutine g_func, g_cone;

struct _CalcPOutput{
  double *T_sink;
  double *T_source;
  double *T_soil;
};

typedef struct _CalcPOutput CalcPOutput;

void calc_P_core(double *P, double *U_brine,
		 unsigned int dim_ax, unsigned int dim_rad,
		 unsigned int dim_t,
		 unsigned int n_DHE,
		 const DHECore *dhe,
		 DHEState *dhe_states,
		 double *sum_Q0,
		 double *Q_wall,
		 unsigned int n_boundary_refresh,
		 double precision,
		 CalcPOutput *restrict out);

#endif // __DHE_CORE_H__
