from .new_dreal import newDRealSolver
from ..solver.z3 import Z3Solver
from ..solver.dreal import dRealSolver
from ..solver.flowstar import FlowStarSolverUnsatCoreMerging, FlowStarSolverUnsatCore
from ..solver.spaceex import *


class SolverFactory:
    def __init__(self):
        self.solver_type = None

    def generate_solver(self, config):
        common_section = config.get_section("common")
        self.solver_type = common_section.get_value("solver")
        is_reach = common_section.get_value("reach")
        if self.solver_type == 'z3':
            return Z3Solver()
        elif self.solver_type == 'dreal':
            if is_reach == "true":
                return newDRealSolver()
            else:
                return dRealSolver()
        elif 'flowstar' in self.solver_type:
            return FlowStarSolverUnsatCore()
        elif "spaceex" in self.solver_type:
            return SpaceExSolverUnsatCore()
        else:
            # Yices import is deferred so the tool starts without libyices.dylib
            # when using z3, dreal, or other solvers.
            try:
                from ..solver.yices import YicesSolver
                return YicesSolver()
            except Exception as e:
                raise RuntimeError(
                    f"Yices solver requested but could not be loaded: {e}\n"
                    "Install Yices2 (libyices.dylib) or use --solver z3."
                ) from e