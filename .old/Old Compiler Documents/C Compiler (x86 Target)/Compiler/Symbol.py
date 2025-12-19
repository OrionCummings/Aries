from pathlib import Path

class Symbol:

    def __init__(self, sym: str, path: Path):
        self.sym = sym
        self.path = path
        self.resolved = False

    def __str__(self):
        return str({
            "sym": str(self.sym),
            "path": str(self.path),
            "resolved": str(self.resolved),
        })

    def resolve(self):
        self.resolved = True

if __name__ == "__main__":

    s1 = Symbol("normalize", Path(""))
    s2 = Symbol("x", Path())
    s3 = Symbol("test", Path())

    s2.resolve()

    print(s1)
    print(s2)
    print(s3)