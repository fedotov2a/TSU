import scipy.io
import numpy as np

def main():
    dta = scipy.io.loadmat('var1',squeeze_me=True,struct_as_record=False)
    a = dta['a']
    P= dta['P']
    G = dta['G']
    print(a, P, G)

if __name__ == '__main__':
    main()

