from itertools import zip_longest

class Version:
    def __init__(self, version, delimiter="."):
        self.version = version
        self.delimiter = delimiter
        # self.version_int = self._convert(self.version)
        # print(self.version_int)

    def _convert(self, version):
        len_version_part = 3
        v = version.split(".")
        for p in v[1:]:
            if len(p) > len_version_part:
                len_version_part = len(p)
        
        divisor = 10**int(len_version_part) #((len_version_part//3+1)*3)

        version_int = float(v[0])
        for i, p in enumerate(v[1:]):
            version_int += int(p) / ((i+1) * divisor)
        
        return version_int

    def __eq__(self, other):
        return self.version == other.version

    def __ne__(self, other):
        return self.version != other.version

    def __le__(self, other):
        for i in zip_longest(self.version.split(self.delimiter), other.version.split(self.delimiter), fillvalue=-2147483648):
            if int(i[0]) < int(i[1]):
                return True
            elif int(i[0]) > int(i[1]):
                return False
        return True

    def __ge__(self, other):
        for i in zip_longest(self.version.split(self.delimiter), other.version.split(self.delimiter), fillvalue=-2147483648):
            if int(i[0]) > int(i[1]):
                return True
            elif int(i[0]) < int(i[1]):
                return False
        return True

    def __lt__(self, other):
        for i in zip_longest(self.version.split(self.delimiter), other.version.split(self.delimiter), fillvalue=-2147483648):
            if int(i[0]) > int(i[1]):
                return False
            elif int(i[0]) < int(i[1]):
                return True
        return False

    def __gt__(self, other):
        for i in zip_longest(self.version.split(self.delimiter), other.version.split(self.delimiter), fillvalue=-2147483648):
            if int(i[0]) < int(i[1]):
                return False
            elif int(i[0]) > int(i[1]):
                return True
        return False


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