"""
Centroidal Patch Tesselation. Mimics the definition of Centroidal
Voronoi Tessellations for which the generator and centroid of each Voronoi
region coincide. From

Long Chen, Michael Holst,
Efficient mesh optimization schemes based on Optimal Delaunay
Triangulations,
Comput. Methods Appl. Mech. Engrg. 200 (2011) 967–984,
<https://doi.org/10.1016/j.cma.2010.11.007>.
"""
import numpy
import scipy.sparse.linalg

from ..meshplex.mesh_tri import MeshTri
from .helpers import get_new_points_volume_averaged, runner


def _build_graph_laplacian(mesh):
    i = mesh.idx_hierarchy
    row_idx = numpy.array([i[0], i[1], i[0], i[1]]).flat
    col_idx = numpy.array([i[0], i[1], i[1], i[0]]).flat
    a = numpy.ones(i.shape[1:], dtype=int)
    val = numpy.array([+a, +a, -a, -a]).flat

    # Create CSR matrix for efficiency
    n = mesh.node_coords.shape[0]
    matrix = scipy.sparse.coo_matrix((val, (row_idx, col_idx)), shape=(n, n))
    matrix = matrix.tocsr()

    # Apply Dirichlet conditions.
    verts = numpy.where(mesh.is_boundary_node)[0]
    # Set all Dirichlet rows to 0.
    for i in verts:
        matrix.data[matrix.indptr[i] : matrix.indptr[i + 1]] = 0.0
    # Set the diagonal and RHS.
    d = matrix.diagonal()
    d[mesh.is_boundary_node] = 1.0
    matrix.setdiag(d)
    return matrix


# The density-preserving CPT is exactly Laplacian smoothing.
def linear_solve_density_preserving(points, cells, *args, **kwargs):
    def get_new_points(mesh, tol=1.0e-10):
        matrix = _build_graph_laplacian(mesh)

        n = mesh.node_coords.shape[0]
        rhs = numpy.zeros((n, mesh.node_coords.shape[1]))
        rhs[mesh.is_boundary_node] = mesh.node_coords[mesh.is_boundary_node]

        out = scipy.sparse.linalg.spsolve(matrix, rhs)

        # PyAMG fails on circleci.
        # ml = pyamg.ruge_stuben_solver(matrix)
        # # Keep an eye on multiple rhs-solves in pyamg,
        # # <https://github.com/pyamg/pyamg/issues/215>.
        # out = numpy.column_stack(
        #     [ml.solve(rhs[:, 0], tol=tol), ml.solve(rhs[:, 1], tol=tol)]
        # )
        return out

    mesh = MeshTri(points, cells)
    runner(
        get_new_points,
        mesh,
        *args,
        **kwargs,
        method_name="exact Laplacian smoothing"
    )
    return mesh.node_coords, mesh.cells["nodes"]


def fixed_point_uniform(points, cells, *args, **kwargs):
    """Idea:
    Move interior mesh points into the weighted averages of the centroids
    (barycenters) of their adjacent cells.
    """

    def get_new_points(mesh):
        return get_new_points_volume_averaged(mesh, mesh.cell_barycenters)

    mesh = MeshTri(points, cells)
    runner(
        get_new_points,
        mesh,
        *args,
        **kwargs,
        method_name=(
            "Centroidal Patch Tesselation (CPT), uniform density, "
            "fixed-point variant"
        )
    )
    return mesh.node_coords, mesh.cells["nodes"]


def jac_uniform(X, cells):
    """The approximated Jacobian is

      partial_i E = 2/(d+1) (x_i int_{omega_i} rho(x) dx - int_{omega_i} x rho(x) dx)
                  = 2/(d+1) sum_{tau_j in omega_i} (x_i - b_{j, rho}) int_{tau_j} rho,

    see Chen-Holst. This method here assumes uniform density, rho(x) = 1, such that

      partial_i E = 2/(d+1) sum_{tau_j in omega_i} (x_i - b_j) |tau_j|

    with b_j being the ordinary barycenter.
    """
    dim = 2
    mesh = MeshTri(X, cells)

    jac = numpy.zeros(X.shape)
    for k in range(mesh.cells["nodes"].shape[1]):
        i = mesh.cells["nodes"][:, k]
        vals = (
            mesh.node_coords[i] - mesh.cell_barycenters
        ).T * mesh.cell_volumes
        # numpy.add.at(jac, i, vals)
        jac += numpy.array(
            [numpy.bincount(i, val, minlength=jac.shape[0]) for val in vals]
        ).T

    return 2 / (dim + 1) * jac


def solve_hessian_approx_uniform(X, cells, rhs):
    """As discussed above, the approximated Jacobian is

      partial_i E = 2/(d+1) sum_{tau_j in omega_i} (x_i - b_j) |tau_j|.

    To get the Hessian, we have to form its derivative. As a simplifications,
    let us assume again that |tau_j| is independent of the node positions. Then we get

       partial_ii E = 2/(d+1) |omega_i| - 2/(d+1)**2 |omega_i|,
       partial_ij E = -2/(d+1)**2 |tau_j|.

    The terms with (d+1)**2 are from the barycenter in `partial_i E`. It turns out from
    numerical experiments that the negative term in `partial_ii E` is detrimental to the
    convergence. Hence, this approximated Hessian solver only considers the off-diagonal
    contributions from the barycentric terms.
    """
    dim = 2
    mesh = MeshTri(X, cells)

    # Create matrix in IJV format
    row_idx = []
    col_idx = []
    val = []

    cells = mesh.cells["nodes"].T
    n = X.shape[0]

    # Main diagonal, 2/(d+1) |omega_i| x_i
    a = mesh.cell_volumes * (2 / (dim + 1))
    for i in [0, 1, 2]:
        row_idx += [cells[i]]
        col_idx += [cells[i]]
        val += [a]

    # terms corresponding to -2/(d+1) * b_j |tau_j|
    a = mesh.cell_volumes * (2 / (dim + 1) ** 2)
    for i in [[0, 1, 2], [1, 2, 0], [2, 0, 1]]:
        edges = cells[i]
        # Leads to funny osciilatory movements
        # row_idx += [edges[0], edges[0], edges[0]]
        # col_idx += [edges[0], edges[1], edges[2]]
        # val += [-a, -a, -a]
        # Best so far
        row_idx += [edges[0], edges[0]]
        col_idx += [edges[1], edges[2]]
        val += [-a, -a]

    row_idx = numpy.concatenate(row_idx)
    col_idx = numpy.concatenate(col_idx)
    val = numpy.concatenate(val)

    # Set Dirichlet conditions on the boundary
    matrix = scipy.sparse.coo_matrix((val, (row_idx, col_idx)), shape=(n, n))
    # Transform to CSR format for efficiency
    matrix = matrix.tocsr()

    # Apply Dirichlet conditions.
    # Set all Dirichlet rows to 0.
    for i in numpy.where(mesh.is_boundary_node)[0]:
        matrix.data[matrix.indptr[i] : matrix.indptr[i + 1]] = 0.0
    # Set the diagonal and RHS.
    d = matrix.diagonal()
    d[mesh.is_boundary_node] = 1.0
    matrix.setdiag(d)

    rhs[mesh.is_boundary_node] = 0.0

    out = scipy.sparse.linalg.spsolve(matrix, rhs)

    # PyAMG fails on circleci.
    # ml = pyamg.ruge_stuben_solver(matrix)
    # # Keep an eye on multiple rhs-solves in pyamg,
    # # <https://github.com/pyamg/pyamg/issues/215>.
    # tol = 1.0e-10
    # out = numpy.column_stack(
    #     [ml.solve(rhs[:, 0], tol=tol), ml.solve(rhs[:, 1], tol=tol)]
    # )
    return out


def quasi_newton_uniform(points, cells, *args, **kwargs):
    """Like linear_solve above, but assuming rho==1. Note that the energy gradient

        \\partial E_i = 2/(d+1) sum_{tau_j in omega_i} (x_i - b_j) \\int_{tau_j} rho

    becomes

        \\partial E_i = 2/(d+1) sum_{tau_j in omega_i} (x_i - b_j) |tau_j|.

    Because of the dependence of |tau_j| on the point coordinates, this is a nonlinear
    problem.

    This method makes the simplifying assumption that |tau_j| does in fact _not_ depend
    on the point coordinates. With this, one still only needs to solve a linear system.
    """

    def get_new_points(mesh):
        # do one Newton step
        # TODO need copy?
        x = mesh.node_coords.copy()
        cells = mesh.cells["nodes"]
        jac_x = jac_uniform(x, cells)
        x -= solve_hessian_approx_uniform(x, cells, jac_x)
        return x

    mesh = MeshTri(points, cells)
    runner(
        get_new_points,
        mesh,
        *args,
        **kwargs,
        method_name=(
            "Centroidal Patch Tesselation (CPT), uniform density, "
            "quasi-Newton variant"
        )
    )
    return mesh.node_coords, mesh.cells["nodes"]
