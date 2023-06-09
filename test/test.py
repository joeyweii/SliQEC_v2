import sys
import subprocess
import json
from tqdm import tqdm

if __name__ == '__main__':
    nQubit = 5
    nGate = 100

    for approach in range(2):
        approachName = ""
        if(approach == 0):
            approachName = "construct miter"
        elif(approach == 1):
            approachName = "construct functionality"
        else:
            assert(0)

        for eq in range(2):
            eqName = ""
            if(eq == 0):
                eqName = "NEQ cases"
            elif(eq == 1):
                eqName = "EQ cases"
            else:
                assert(0)

            for seed in tqdm(range(100), desc='{} | {}'.format(eqName, approachName)):
                genUCommand = "python3 ./genRandom.py {} {} U.qasm {}".format(nQubit, nGate, seed)
                subprocess.run(genUCommand, shell=True)
                if(eq == 1):
                    genVCommand = "python3 ./replaceCCX.py U.qasm V.qasm"
                    subprocess.run(genVCommand, shell=True)
                elif(eq == 0):
                    genVtemCommand = "python3 ./replaceCCX.py U.qasm V_tem.qasm"
                    subprocess.run(genVtemCommand, shell=True)
                    genVCommand = "python3 ./removeGates.py V_tem.qasm V.qasm 5 {}".format(seed)
                    subprocess.run(genVCommand, shell=True)
                    subprocess.run("rm V_tem.qasm", shell=True)

                checkCommand = "../SliQEC_v2 --circuit1 U.qasm --circuit2 V.qasm --approach {}".format(approach)
                checkOutput = subprocess.getoutput(checkCommand)
                checkOutputJSON = json.loads(checkOutput)
                if(eq == 1):
                    if(checkOutputJSON["equivalence"] == "not_equivalent"):
                        print("Test failed.")
                        exit()
                elif(eq == 0):
                    if(checkOutputJSON["equivalence"] == "equivalent"):
                        print("Test failed.")
                        exit()

                subprocess.run("rm U.qasm V.qasm", shell=True)

    print("Test passed.")