import numpy as np
from scipy import sparse, optimize


class ImplicitEuler:
    def __init__(self, func, t0, y0, tend, step_size, first_step=1e-6, min_step=1e-12, max_step=1e-1, jacobian_recompute=1, jacobian_recompute_max=1, jacobian_recompute_min=1, tol=1e-6, args=()):
        self.func = func
        self.t0 = t0
        self.y0 = y0
        self.tend = tend
        self.step_size = step_size
        self.dt = step_size
        self.first_step = first_step
        self.min_step = min_step
        self.max_step = max_step

        self.args = args
        self.t = t0
        self.y = y0

        self.f = 0
        self.jac = self.jacobian(self.y)
        self.jacobian_recompute = jacobian_recompute
        self.jacobian_recompute_max = jacobian_recompute_max
        self.jacobian_recompute_min = jacobian_recompute_min

        self.jacobi_count = 0
        self.tol = tol

    def step(self):
        # print(self.jacobi_count, self.jacobian_recompute)
        if self.jacobi_count >= self.jacobian_recompute:
            self.jac = self.jacobian(self.y)
            self.jacobi_count = 0
        else:
            self.jacobi_count += 1

        ykp1, err = self.simplfied_newton()
        self.t += self.dt
        self.y = ykp1

        # Error
        # self.dt, self.jacobian_recompute = self.change_step_size(err)
        # ykp1 = scipy.optimize.newton(self.optimize_func, self.y,
        #                              maxiter=200,
        #                              tol=1e-3)

    def optimize_func(self, ykp1):
        dtp1 = self.t + self.dt
        return self.y + self.dt * self.func(dtp1, ykp1) - ykp1

    def simplfied_newton(self):
        A = np.identity(len(self.jac)) - self.dt * self.jac

        if self.args == ():
            f0 = self.func(self.t, self.y)
            f1 = self.func(self.t + self.dt, self.y)
        else:
            f0 = self.func(self.t, self.y, self.args)
            f1 = self.func(self.t + self.dt, self.y, self.args)

        dfdt = (f1 - f0) * (1. / self.dt)
        b = self.dt * f0 + self.dt * self.dt * dfdt
        dy = np.linalg.solve(A, b)
        y = self.y + dy

        return y, 0

    def jacobian(self, x0):
        t = self.t
        epsilon = 1e-8
        func = self.func
        if self.args == ():
            f0 = func(t, x0)
        else:
            f0 = func(t, x0, self.args)
        f0 = np.array(f0)
        jac = np.zeros([len(x0), len(f0)])
        dx = np.zeros(len(x0))
        for i in range(len(x0)):
            dx[i] = epsilon
            if self.args == ():
                f1 = func(t, x0 + dx)
            else:
                f1 = func(t, x0 + dx, self.args)
            jac[i] = (np.array(f1) - f0) / (epsilon)
            dx[i] = 0.0
        return jac.transpose()

    def change_step_size(self, err):
        if err < self.tol:
            dt = self.dt * 1.1
            jr = self.jacobian_recompute + 1
        else:
            dt = self.dt * 0.9
            jr = self.jacobian_recompute - 100

        if dt < self.min_step:
            dt = self.min_step
        elif dt > self.max_step:
            dt = self.max_step
        else:
            dt = dt

        if jr < self.jacobian_recompute_min:
            jr = self.jacobian_recompute_min
        elif jr > self.jacobian_recompute_max:
            jr = self.jacobian_recompute_max
        else:
            jr = jr

        return dt, jr


class Trapz(ImplicitEuler):
    def __init__(self, func, t0, y0, tend, step_size, first_step=1e-6, min_step=1e-12, max_step=1e-1, jacobian_recompute=1, jacobian_recompute_max=1, jacobian_recompute_min=1, tol=1e-6, args=()):
        ImplicitEuler.__init__(self, func, t0, y0,
                               tend, step_size, first_step, min_step, max_step, jacobian_recompute, jacobian_recompute_max, jacobian_recompute_min, tol, args)

    def simplfied_newton(self):
        if self.args == ():
            f0 = self.func(self.t, self.y)
        else:
            f0 = self.func(self.t, self.y, self.args)
        f0 = np.array(f0)
        A = 2 * np.identity(len(self.jac)) / self.dt - self.jac
        b = 2 * f0
        dy = np.linalg.solve(A, b)

        y = self.y + dy

        y_low = self.y + self.dt * f0
        err = np.linalg.norm(np.abs(y - y_low))

        return y, err


class Euler_Index3:
    def __init__(self, group, t0, tend, step_size, first_step=1e-6, err=1e-6, maxiter=50):
        self.group = group
        self.t0 = t0
        self.tend = tend
        self.step_size = step_size
        self.first_step = first_step
        self.h = first_step
        self.err = err
        self.maxiter = maxiter

        self.t = t0
        self.q = group.qglobal
        self.y = group.qglobal[0:self.group.dim_y]
        self.z = group.qglobal[self.group.dim_y:]

        self.la = group.lagrange_lambda(self.z)

    def step(self):
        # Update Group
        self.t += self.h
        self.group.update_system(self.t, self.q)

        # Paramters
        self.K = self.group.kinematic_matrix_global()

        # Update Lambda with Newton Raphson
        self.Jg, Jgpz = self.group.jacobi_constraint()
        M = self.group.solve
        self.la = self.optimize_lambda()
        # self.la = optimize.fsolve(self.nonlinear_constraint,
        #                           self.la)
        #self.la = sol.x
        # print(sol.nit)

        # External Forces
        self.group.update_body_forces()
        qe = self.group.forces_global

        # Constraint Forces
        qz = np.dot(self.Jg.T, self.la)

        # integrate dynamic ODE
        z = self.z + self.h * sparse.linalg.spsolve(M, qe + qz)

        # integrate kinematic ODE
        y = self.y + self.h * np.dot(self.K, z)

        # Update states
        self.y = y
        self.z = z
        self.q = np.concatenate((self.y, self.z))
        self.h = self.step_size

        # print(self.group.g_global())
        # self.group.update_system(self.t, self.q)
        # print(self.group.g_global())
        # print()

        return self.t, self.q

    def optimize_lambda(self):
        Jg = self.Jg
        M = self.group.solve
        dgdla = self.h**2 * np.dot(Jg, sparse.linalg.spsolve(M, Jg.T))
        la = self.la
        dla = 2 * self.err
        i = 0
        # while np.linalg.norm(dla) > self.err and i < self.maxiter:
        for i in range(0, 3):
            gla = self.nonlinear_constraint(la)
            dla = np.linalg.solve(dgdla, -gla)
            la += dla
        return la

    def nonlinear_constraint(self, la):
        K = self.K
        y = self.y
        z = self.z
        h = self.h
        M = self.group.solve
        qe = self.group.forces_global
        Jg = self.Jg
        yd = np.dot(K, z + h * sparse.linalg.spsolve(M, qe + np.dot(Jg.T, la)))
        yp1 = y + h * yd

        self.group.update_body_states(np.concatenate((yp1, z)))

        return self.group.g_global()
