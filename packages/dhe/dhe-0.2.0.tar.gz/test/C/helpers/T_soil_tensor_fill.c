void T_soil_tensor_fill(double ***B, unsigned int dim_ax, unsigned int dim_rad, double *T_soil_tensor)
{
  unsigned int i, j, k, l=0;
  for(i=1; i<=dim_ax; i++)
    for(j=1; j<=dim_rad; j++)
      for(k=0; k<dim_rad+2; k++)
	T_soil_tensor[l++] = B[i][j][k];
}
void T_soil_tensor_fill_id(unsigned int dim_ax, unsigned int dim_rad, double *T_soil_tensor)
{
  unsigned int i, j, k, l=0;
  double val;
  for(i=0; i<dim_ax; i++)
    for(j=0; j<dim_rad; j++)
      for(k=0; k<dim_rad+2; k++) {
	  val = (j+1 == k);
	  T_soil_tensor[l] = val;
	  T_soil_tensor[l] = val;
	  l++;
	}
}
