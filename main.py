from docplex.mp.model import *
from docplex.mp.solution import SolveSolution

from PbInstance import RankingInstance

def make_problem(prob, instance : RankingInstance , buckets):
    n = instance.size
    w = instance.w
    w_ = instance.w_
    x = prob.binary_var_matrix([i for i in range(n)], [i for i in range(n)], name=lambda i: "x_"+str(i[0])+"_"+str(i[1]))
    x_eq = prob.binary_var_matrix([i for i in range(n)], [i for i in range(n)], name=lambda i: "x_eq_"+str(i[0])+"_"+str(i[1]))

    #bucket control
    tr = prob.binary_var_matrix([i for i in range(n)], [i for i in range(n)], name=lambda i: "tr_"+str(i[0])+"_"+str(i[1]))
    nb_arcs = prob.integer_var(name="nb_arcs")

    # Objective : for each query if it's there count it's interest
    prob.set_objective("min", sum([w_[b][a]*x[a,b] + w_[a][b]*x[b,a] + w[a][b] * x_eq[a,b] + w[b][a] * x_eq[a,b] + tr[a,b] for idx, a in enumerate(range(n)) for b in range(n)]))


    for a in range(n):
        for b in range(a + 1):
            prob.add_constraint(x[a,b] + x[b,a] + x_eq[a,b] == 1, ctname='x_eq_sym')


    for a in range(n):
        for b in range(n):
            for c in range(n):
                if not (a == b or b == c or c == a):
                    prob.add_constraint(x[a,c] - x[a,b] - x[b,c] >= -1, ctname='cstr_trans')
                    prob.add_constraint(2*x[a,b] + 2* x[b,a] + 2*x[b,c] + 2*x[c,b] - x[a,c] - x[c, a] >= 0, ctname='cstr_trans_ties')

    # bucket control
    prob.add_constraint(sum([x_eq[b, a] for idx, a in enumerate(range(n)) for b in range(a + 1, n)]) == nb_arcs)
    prob.add_constraint(nb_arcs - sum([tr[a, b] for idx, a in enumerate(range(n)) for b in range(n)]) == n - buckets)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                if not (a == b or b == c or c == a):
                    prob.add_constraint(tr[a,c] - x_eq[a,b] - x_eq[b,c] >= -1)
                    #prob.add_constraint(2*x[a,b] + 2* x[b,a] + 2*x[b,c] + 2*x[c,b] - trans[a,c] - trans[c,a] >= 0)


    return x, x_eq



if __name__ == '__main__':
    ist = RankingInstance("./instances/patrick_ist_2.txt")


    problem = Model(name="Opt Rank (" + ist.file + ")")
    x, x_eq = make_problem(problem, ist, 3)

    problem.print_information()
    solution = problem.solve()
    problem.print_solution()
    print("nb_arcs", problem.get_var_by_name("nb_arcs").solution_value)