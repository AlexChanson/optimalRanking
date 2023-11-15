def load_instance(file):
    with open(file) as f:
        n = int(f.readline())
        D = []
        for i in range(n):
            d = []
            for e in f.readline().split(" "):
                d.append(int(e))
            D.append(d)
        D_ = []
        for i in range(n):
            d = []
            for e in f.readline().split(" "):
                d.append(int(e))
            D_.append(d)
    return n, D, D_


class RankingInstance:

    def __init__(self, file):
        n, D, D_ = load_instance(file)
        self.file = file
        self.size = n
        self.w = D
        self.w_ = D_

    def __repr__(self) -> str:
        return "Instance of Size " + str(self.size) + " from '" + self.file + "'"

