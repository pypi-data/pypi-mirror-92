#![allow(non_snake_case)]

use ndarray;
use numpy::{IntoPyArray, PyArray2, PyArray4, PyReadonlyArray1};
use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::{pyclass, pymethods, pymodule, Py, PyCell, PyErr, PyModule, PyResult, Python};
use pyo3::types::{PyAny, PySequence};
use pyo3::{FromPyObject, ToPyObject};

use libdhe::{self as dhe, GParametersCore as BoundaryMethod};

fn make_error<E: std::fmt::Debug + Sized>(e: E) -> PyErr {
    PyErr::new::<PyRuntimeError, _>(format!("{:?}", e))
}

/// FromPyObject trait for foreign type
/// (we cannot implement FromPyObject for foreign types)
/// Instead FromPyObject is automatically implemented for Foreign<T: _FromPyObject>
trait _FromPyObject<'source>: Sized {
    fn _extract(ob: &'source PyAny) -> PyResult<Self>;
}
macro_rules! impl_from_py_object_builtin {
    ($($t:ty),+) => { $(
	impl _FromPyObject<'_> for $t {
	    fn _extract(ob: &PyAny) -> PyResult<Self> { type T = $t; T::extract(ob) }
	}
    )* }
}
impl_from_py_object_builtin!(f64, usize, [f64; 5]);

/// Wrapper type for Foreign types, so FromPyObject can be implemented on them indirectly
struct Foreign<T>(T);
impl<'src, T: _FromPyObject<'src>> FromPyObject<'src> for Foreign<T> {
    fn extract(ob: &'src PyAny) -> PyResult<Self> {
        T::_extract(ob).map(Foreign)
    }
}

macro_rules! impl_from_py_object {
    ($t:ty, $($f_from:ident -> $f_to:ident),+) => {
	impl _FromPyObject<'_> for $t {
	    fn _extract(ob: &PyAny) -> PyResult<Self> {
		let gil = Python::acquire_gil();
		let py = gil.python();
		let o = ob.to_object(py);
		type T = $t;
		println!(stringify!($t));
		let out = T{
		    $($f_to: <_>::_extract(&o.getattr(py, stringify!($f_from))?.as_ref(py))?,)*
		};
		Ok(out)
	    }
	}
    }
}
impl_from_py_object!(dhe::model::MaterialProperties, rho->rho, c -> c, lambda_ -> lambda);
impl_from_py_object!(dhe::FluidProperties, rho -> rho, c -> c, lambda_ -> lambda, nu -> nu);
impl_from_py_object!(dhe::SoilLayerProperties, rho -> rho, c -> c, lambda_ -> lambda, d -> d);
impl_from_py_object!(dhe::model::SoilParameters, T_soil_mean -> T_soil_mean, T_grad -> T_grad);
impl_from_py_object!(dhe::model::TSoil0Parameters, d_DHE->d_DHE, g_coefs -> g_coefs);
impl_from_py_object!(dhe::DHE, x->x, y->y, L->L, D->D, D_borehole->D_borehole, thickness->thickness, Ra->Ra, Rb->Rb, R1->R1, fill_properties->fill_properties, T_soil_0_parameters->T_soil_0_parameters, brine_properties->brine_properties, Phi_m->Phi_m);
impl_from_py_object!(dhe::GlobalParameters, dim_ax->dim_ax, dim_rad->dim_rad, soil_layers->soil_layers, R->R, optimal_n_steps_multiplier->optimal_n_steps_multiplier, Gamma->Gamma, adiabat->adiabat, n_steps_0->n_steps_0, dt_boundary_refresh->dt_boundary_refresh, dt->dt, t0->t0, soil_parameters->soil_parameters);

impl _FromPyObject<'_> for BoundaryMethod {
    fn _extract(any: &PyAny) -> PyResult<Self> {
        println!("BoundaryMethod");
        if let Ok(g) = any.downcast::<PyCell<GFuncParameters>>() {
            Ok(BoundaryMethod::GFunc(g.borrow().wrapped.clone()))
        } else {
            Ok({
                any.downcast::<PyCell<GConeParameters>>()?;
                BoundaryMethod::GCone(dhe::GConeParameters {})
            })
        }
    }
}

fn extract_sequence<'s, T>(seq: &'s PySequence) -> PyResult<Vec<T>>
where
    T: _FromPyObject<'s>,
{
    println!("extract_sequence");
    let mut v = Vec::with_capacity(seq.len().unwrap_or(0) as usize);
    for item in seq.iter()? {
        v.push(<_>::_extract(item?)?);
    }
    Ok(v)
}
impl<'a, T: _FromPyObject<'a>> _FromPyObject<'a> for Vec<T> {
    fn _extract(ob: &'a PyAny) -> PyResult<Self> {
        extract_sequence(ob.downcast()?)
    }
}

type CalcMethod = fn(
    &[f64],
    &[f64],
    &[dhe::DHE],
    &dhe::GlobalParameters,
    &BoundaryMethod,
    f64,
    &mut [dhe::CalcPOutputRef],
) -> Result<(), dhe::error::Error>;

#[pyclass]
#[derive(Clone)]
struct TBrineMethod {
    method: CalcMethod,
}

struct GlobalParameters {
    env: dhe::GlobalParameters,
    calc_method: CalcMethod,
    g_method: BoundaryMethod,
}

impl FromPyObject<'_> for GlobalParameters {
    fn extract(ob: &PyAny) -> PyResult<Self> {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let o = ob.to_object(py);
        println!("GlobalParameters");
        Ok(GlobalParameters {
            calc_method: o
                .getattr(py, "T_brine_method")?
                .extract::<TBrineMethod>(py)?
                .method,
            g_method: o
                .getattr(py, "g_method")?
                .extract::<Foreign<BoundaryMethod>>(py)?
                .0,
            env: <_>::_extract(ob)?,
        })
    }
}

#[pyclass]
struct GFuncParameters {
    wrapped: dhe::GFuncParametersCore,
}
#[pymethods]
impl GFuncParameters {
    #[new]
    fn new(g_coefs: (f64, f64, f64, f64, f64, f64), u_min: f64, L: f64, go_const: f64) -> Self {
        Self {
            wrapped: dhe::GFuncParametersCore {
                g_coefs: [
                    g_coefs.0, g_coefs.1, g_coefs.2, g_coefs.3, g_coefs.4, g_coefs.5,
                ],
                u_min,
                L,
                go_const,
            },
        }
    }
}

#[pyclass]
struct GConeParameters {}
#[pymethods]
impl GConeParameters {
    #[new]
    fn new() -> Self {
        Self {}
    }
}

#[pymodule]
fn dhe(py: Python, m: &PyModule) -> PyResult<()> {
    #![allow(clippy::type_complexity)]
    #[pyfn(m, "calc_P")]
    fn calc_P(
        py: Python,
        t: PyReadonlyArray1<f64>,
        P: PyReadonlyArray1<f64>,
        dhe: Foreign<Vec<dhe::DHE>>,
        env: GlobalParameters,
        precision: f64,
    ) -> PyResult<(Py<PyArray2<f64>>, Py<PyArray2<f64>>, Py<PyArray4<f64>>)> {
        let GlobalParameters {
            env,
            g_method,
            calc_method,
        } = env;
        let dim_t = P.len();
        let dhe = dhe.0;
        let n_DHE: usize = dhe.len();
        let dim_ax = env.dim_ax;
        let dim_rad = env.dim_rad;

        let mut out_T_sink = vec![0.; n_DHE * dim_t];
        let mut out_T_source = vec![0.; n_DHE * dim_t];
        let mut out_T_soil = vec![0.; n_DHE * dim_t * (dim_rad + 2) * dim_ax];
        let chunk_size_T_soil = dim_t * (dim_rad + 2) * dim_ax;
        let mut out: Vec<dhe::CalcPOutputRef> = out_T_sink
            .chunks_exact_mut(dim_t)
            .zip(out_T_source.chunks_exact_mut(dim_t))
            .zip(out_T_soil.chunks_exact_mut(chunk_size_T_soil))
            .map(|((T_sink, T_source), T_soil)| {
                Ok(dhe::CalcPOutputRef {
                    T_sink,
                    T_source,
                    T_soil,
                })
            })
            .collect::<Result<Vec<dhe::CalcPOutputRef>, PyErr>>()?;
        calc_method(
            t.as_slice()?,
            P.as_slice()?,
            &dhe,
            &env,
            &g_method,
            precision,
            &mut out,
        )
        .map_err(make_error)?;
        let py_out_T_sink = ndarray::Array::from_shape_vec((n_DHE, dim_t), out_T_sink)
            .unwrap()
            .into_pyarray(py);
        let py_out_T_source = ndarray::Array::from_shape_vec((n_DHE, dim_t), out_T_source)
            .unwrap()
            .into_pyarray(py);
        let py_out_T_soil =
            ndarray::Array::from_shape_vec((n_DHE, dim_t, dim_rad + 2, dim_ax), out_T_soil)
                .unwrap()
                .into_pyarray(py);
        Ok((
            py_out_T_sink.to_owned(),
            py_out_T_source.to_owned(),
            py_out_T_soil.to_owned(),
        ))
    }

    m.add(
        "T_BRINE_METHOD_DYNAMIC",
        PyCell::new(
            py,
            TBrineMethod {
                method: dhe::calc_P::<dhe::TBrineCalcMethodDynamic, _>,
            },
        )?,
    )?;
    m.add(
        "T_BRINE_METHOD_STATIONARY",
        PyCell::new(
            py,
            TBrineMethod {
                method: dhe::calc_P::<dhe::TBrineCalcMethodStationary, _>,
            },
        )?,
    )?;
    m.add_class::<GFuncParameters>()?;
    m.add_class::<GConeParameters>()?;
    Ok(())
}
