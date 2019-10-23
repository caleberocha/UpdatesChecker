from itertools import zip_longest

class Version:
    def __init__(self, version, delimiter="."):
        self.version = version
        self.delimiter = delimiter

    def __eq__(self, other):
        return self.version == other.version

    def __ne__(self, other):
        return self.version != other.version

    def __lt__(self, other):
        for i in zip_longest(self.version.split(self.delimiter), other.version.split(self.delimiter), fillvalue=-2147483648):
            if int(i[0]) < int(i[1]):
                return True
            elif int(i[0]) > int(i[1]):
                return False
        return False

    def __le__(self, other):
        for i in zip_longest(self.version.split(self.delimiter), other.version.split(self.delimiter), fillvalue=-2147483648):
            if int(i[0]) < int(i[1]):
                return True
            elif int(i[0]) > int(i[1]):
                return False
        return True

    def __gt__(self, other):
        for i in zip_longest(self.version.split(self.delimiter), other.version.split(self.delimiter), fillvalue=-2147483648):
            if int(i[0]) > int(i[1]):
                return True
            elif int(i[0]) < int(i[1]):
                return False
        return False    

    def __ge__(self, other):
        for i in zip_longest(self.version.split(self.delimiter), other.version.split(self.delimiter), fillvalue=-2147483648):
            if int(i[0]) > int(i[1]):
                return True
            elif int(i[0]) < int(i[1]):
                return False
        return True


if __name__ == "__main__":
    versions = [
        ("1.0", "1.1"),
        ("2.1", "2.1.2"),
        ("9.1", "10.0"),
        ("2.0.1234.5", "3.0"),
        ("2.0.124.5", "2.1"),
        ("2.123", "2.123"),
        ("3.5", "3.4"),
        ("4.0", "3.1"),
        ("40.1", "40.0.9")
    ]

    for v in versions:
        print(f"{str(v[0]):>10} == {str(v[1]):10}\t{str(Version(v[0]) == Version(v[1]))}")
        print(f"{str(v[0]):>10} != {str(v[1]):10}\t{str(Version(v[0]) != Version(v[1]))}")
        print(f"{str(v[0]):>10} <  {str(v[1]):10}\t{str(Version(v[0]) < Version(v[1]))}")
        print(f"{str(v[0]):>10} <= {str(v[1]):10}\t{str(Version(v[0]) <= Version(v[1]))}")
        print(f"{str(v[0]):>10} >  {str(v[1]):10}\t{str(Version(v[0]) > Version(v[1]))}")
        print(f"{str(v[0]):>10} >= {str(v[1]):10}\t{str(Version(v[0]) >= Version(v[1]))}")
        print()