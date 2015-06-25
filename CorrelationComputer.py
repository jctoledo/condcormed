from __future__ import division

__author__ = 'jose'

import sys
from collections import defaultdict


class Patient:
    def __init__(self, **kwargs):
        self.conditions = kwargs.get("conditions")
        self.medications = kwargs.get("medications")

    def __str__(self):
        r = "patient\n"
        r += "conditions : "
        for c in self.conditions:
            r += c + " "
        r+= "\n"
        r += "medications : "
        for m in self.medications:
            r += m + " "
        r += "\n"
        return r


class ComputeCorrelations:

    def __init__(self, **kwargs):
        self.patients = kwargs.get("patient_list")
        #initialize maps
        self.condition_patient_map = self.create_condition_patient_map()
        self.medication_patient_map = self.create_medication_patient_map()

    def correlate_condition_to_medication(self, a_condition, a_medication):
        '''
        Compute the proportion of patients with a_condition which where given a_medication
        :param a_condition: a medical conditon
        :param a_medication: a prescribed medication
        :return: the proportion of patients with a_condition which were given a_medication
        '''
        #get the patients with a_condition
        pc = self.condition_patient_map[a_condition]
        #get the patients with a_medication
        pm = self.medication_patient_map[a_medication]
        numerator = len(list(set(pm) & set(pc)))
        denominator = len(pc)
        rm = numerator/denominator
        return rm

    def create_condition_patient_map(self):
        '''
        a dict where the key is a condition and the value are the list of patients with that condition
        :return: a dict
        '''
        rm = defaultdict(list)
        for p in self.patients:
            #get the conditions
            conds = p.conditions
            for c in conds:
                if c not in rm:
                    rm[c] = [p]
                else:
                    rm[c].append(p)
        return rm


    def create_medication_patient_map(self):
        '''
        a dict where the key is a medication and the values are lists of patients that were given that medication
        :return: a dict
        '''
        rm = defaultdict(list)
        for p in self.patients:
            #get the medications
            meds = p.medications
            for m in meds:
                if m not in rm:
                    rm[m] = [p]
                else:
                    rm[m].append(p)
        return rm


def main(argv):
    #create some conditions and medications
    c1 = ['c1', 'c2', 'c3', 'c4']
    m1 = ['m1', 'm2', 'm3']

    c2 = ['c29', 'c2', 'c88', 'c4']
    m2 = ['m3', 'm4','m1','m8']

    c3 = ['c8', 'c1', 'c77', 'c11']
    m3 = ['m1', 'm4', 'm8', 'm2']

    c4 = ['c77', 'c4']
    m4 = ['m6', 'm4']

    #create some patients
    p1 = Patient(conditions=c1, medications=m1)
    p2 = Patient(conditions=c2, medications=m2)
    p3 = Patient(conditions=c3, medications=m3)
    p4 = Patient(conditions=c4, medications=m4)

    #create a list of patients
    pl = [p1,p2,p3, p4]

    #create a ComputeCorrelation object
    cc = ComputeCorrelations(patient_list=pl)
    c1m1_correlation = cc.correlate_condition_to_medication('c1', 'm1')
    c29m3_correlation = cc.correlate_condition_to_medication('c29', 'm3')
    c4m8_correlation = cc.correlate_condition_to_medication('c4', 'm8')
    c77m3_correlation = cc.correlate_condition_to_medication('c77', 'm3')

    print c1m1_correlation  # prints 1.0
    print c29m3_correlation  # prints 1.0
    print c4m8_correlation  # prints 0.3333
    print c77m3_correlation  # prints 0.0



if __name__ == "__main__":
	main(sys.argv)