#!/usr/bin/env python3

import sys
import time
import os
import csv

# Class to initialize all values that will be needed throughout program
class WFF:
    def __init__ (self):
        self.nVar = 0
        self.nClause = 0
        self.clauses = []
        self.probNum = 0
        self.satisfiable = 'U'
        self.maxLiterals = 0
        self.execTime = 0
        self.lits = set()
        self.expected = '?'
        self.validArg = []
        self.agreement = 0


#  Reads in the wff from the specified file
def readWFF(wff, line, input_file):

    # gets problem number from comment lines -- starts with a 'c'
    wff.probNum, wff.maxLiterals, wff.expected = int(line[1]), int(line[2]), line[3]

    # gets infomration about the WFF from the file -- starts with a 'p'
    line = input_file.readline().rstrip().split(" ")
    wff.nVar, wff.nClause = int(line[2]), int(line[3])
    

    for _ in range(wff.nClause):
        line = input_file.readline().rstrip().split(",")
        # doesn't add centinel 0 to the array by slicing line
        wff.clauses.append(list(map(int, (line[:-1]))))
    

# Generates the next possible assignment for the current WFF
def nextPossAssignment(nVar, curr):
    # num: number of variables in WFF
    
    assignments = []
    s  = '{0:0{1}b}'.format(curr, nVar)

    for c in s:
        assignments.append(int(c))
        
    return assignments
    


# Takes a WFF and an assignment and returns whether or not it satisfies
def verify (wff):
    for i in range(pow(2, int(wff.nVar))):
        assignment = nextPossAssignment(wff.nVar, i)
        found = True
            
        # sees if the assignment satisfies the wff
        for clause in wff.clauses:
            bool_clause = []

            for x in clause:
                if x not in wff.lits:
                    wff.lits.add(x)
                if x < 0:
                    xbool = not bool(assignment[abs(x)-1])
                else:
                    xbool = bool(assignment[x-1])
                bool_clause.append(xbool)

            if True not in bool_clause:
                found = False

        if found:
            wff.validArg = assignment
            return True

    return False


# Creates the output line for the wff in the desired format
def wffFormat(wff, writer, numWffs):
    if wff.satisfiable == 'S':
        writer.writerow([wff.probNum, wff.nVar, wff.nClause, wff.maxLiterals, len(wff.lits), wff.satisfiable, wff.agreement, (1000000*wff.execTime), *wff.validArg])
    else:
        writer.writerow([wff.probNum, wff.nVar, wff.nClause, wff.maxLiterals, len(wff.lits), wff.satisfiable, wff.agreement, (1000000*wff.execTime)])
    # Write the last line of the CSV file at the end of the loop in main

def main ():

    # opens the input file
    ipf_name = sys.argv[1] 
    input_file = open(ipf_name, "r")
    # opens output file and a csv writer object
    output_file = open ('outputfile.CSV',  "w")
    writer = csv.writer(output_file)
    numWffs = 0
    netId = 'dshield2'
    numSatisfy = 0
    numUnsat = 0
    numAnsProv = 0
    numCorrect = 0

    while True:
        # Creates an instance of the class WFF()
        wff = WFF()
        numWffs += 1

        line = input_file.readline().rstrip().split(" ")
        if line == ['']:
            break

        # reads in each problem in input_file
        readWFF(wff, line, input_file)

        start_time = time.time()
        valid = verify (wff)
        

        if (valid):
            wff.satisfiable = 'S'
            numSatisfy += 1
        
        else:
            numUnsat += 1
        
        #computes the exec time of creating and verifying or not finding a valid assignment
        wff.execTime = time.time() - start_time
        
        # Determines whether the calculated prediction of satisfiability matches that of the input document
        wff.agreement = 0
        if wff.expected == '?':
            wff.agreement = -1
        elif wff.expected == wff.satisfiable:
            wff.agreement = 1
            numCorrect += 1
            numAnsProv += 1
        else:
            wff.agreement = 0
            numAnsProv += 1

        # write CSV data from the each of thecomputations to an output file
        wffFormat(wff, writer, numWffs)

    # write final line to output file
    writer.writerow([ipf_name, netId, numWffs, numSatisfy, numUnsat, numAnsProv, numCorrect])
    
    
                

if __name__=='__main__':
    main()