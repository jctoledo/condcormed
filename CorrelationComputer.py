from __future__ import division
import sys
from collections import defaultdict
__author__ = 'jose cruz-toledo'


class Patient:
    def __init__(self, **kwargs):
        self.conditions = kwargs.get("conditions")
        self.medications = kwargs.get("medications")


class ComputeCorrelations:

    def __init__(self, **kwargs):
        self.patients = kwargs.get("patient_list")
        #initialize maps
        self.condition_patient_map = self.create_condition_patient_map()
        self.medication_patient_map = self.create_medication_patient_map()
        self.feature_patient_map = self.create_feature_patient_map()


    def correlate_condition_to_medication(self, a_condition, a_medication):
        '''
        Compute the proportion of patients with a_condition which were given a_medication
        :param a_condition: a medical conditon
        :param a_medication: a prescribed medication
        :return: the proportion of patients with a_condition which were given a_medication
        '''
        #get the condition to patients map
        pc = self.condition_patient_map[a_condition]
        #get the medication to patients map
        pm = self.medication_patient_map[a_medication]
        numerator = len(list(set(pm) & set(pc)))  # number of intersecting patients between maps
        denominator = len(pc)
        if denominator == 0:
            return "N/A"
        rm = numerator/denominator
        return rm

    def correlate_a_to_b(self, a, b):
        '''
        Compute the proportion of patients with a and b with respect to a
        :param a: a condition or medication
        :param b: a condition or medication
        :return: the proportion of patients with a and b with respect to a
        '''
        pa = self.feature_patient_map[a]
        #get the medication to patients map
        pb = self.feature_patient_map[b]
        numerator = len(list(set(pa) & set(pb)))  # number of intersecting patients between maps
        denominator = len(pa)
        if denominator == 0:
            return "N/A"
        rm = numerator/denominator
        return rm

    def correlate_all_against_all(self, a_list_of_features):
        '''
        Compute the correlation of all pairwise combinations of all features in a_list_of_features  and
        return dictionary sorted by correlation value
        :param a_list_of_features: a list of conditions and/or medications
        :return: dictionary of condition-medication pairs sorted by correlation value
        '''
        unsorted_corr = {}
        for c in a_list_of_features:
            for m in a_list_of_features:
                if m != c:
                    cm = self.correlate_a_to_b(c,m)
                    unsorted_corr[c+"-"+m] = cm

        #now sort by value
        rm = sorted(unsorted_corr.items(), key=lambda x:x[1])
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

    def create_feature_patient_map(self):
        '''
        Combine medication and condition maps into a single map
        :return: a combined map of medications and conditions
        '''
        rm = defaultdict(list)
        rm.update(self.medication_patient_map)
        rm.update(self.condition_patient_map)
        return rm


def main(argv):
    #create some conditions and medications
    cs1 = ['c1', 'c2', 'c3', 'c4']
    ms1 = ['m1', 'm2', 'm3']

    cs2 = ['c29', 'c2', 'c88', 'c4']
    ms2 = ['m3', 'm4','m1','m8']

    cs3 = ['c8', 'c1', 'c77', 'c11']
    ms3 = ['m1', 'm4', 'm8', 'm2']

    cs4 = ['c77', 'c4']
    ms4 = ['m6', 'm4']

    #create some patients
    p1 = Patient(conditions=cs1, medications=ms1)
    p2 = Patient(conditions=cs2, medications=ms2)
    p3 = Patient(conditions=cs3, medications=ms3)
    p4 = Patient(conditions=cs4, medications=ms4)

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
    print "*************"

    c1m1_correlation = cc.correlate_a_to_b('c1', 'm1')
    c29m3_correlation = cc.correlate_a_to_b('c29', 'm3')
    c4m8_correlation = cc.correlate_a_to_b('c4', 'm8')
    c77m3_correlation = cc.correlate_a_to_b('c77', 'm3')

    print c1m1_correlation  # prints 1.0
    print c29m3_correlation  # prints 1.0
    print c4m8_correlation  # prints 0.3333
    print c77m3_correlation  # prints 0.0
    print "*************"
    m1c1_correlation = cc.correlate_a_to_b('m1', 'c1')
    m3c29_correlation = cc.correlate_a_to_b('m3', 'c29')
    m8c4_correlation = cc.correlate_a_to_b('m8', 'c4')
    m3c77_correlation = cc.correlate_a_to_b('m3', 'c77')
    m8m3_correlation = cc.correlate_a_to_b('m3', 'm8')
    print m1c1_correlation  # prints 0.6667
    print m3c29_correlation  # prints 0.5
    print m8c4_correlation  # prints 0.5
    print m3c77_correlation  # prints 0.0
    print m8m3_correlation # prints 0.5
    print "*************"


    all_against_all_sorted = cc.correlate_all_against_all(['c4', 'm1', 'c1', 'm8'])
    print all_against_all_sorted #prints [('c4-c1', 0.3333333333333333), ('c4-m8', 0.3333333333333333), ('c1-m8', 0.5), ('m8-c4', 0.5), ('m8-c1', 0.5), ('c1-c4', 0.5), ('m1-m8', 0.6666666666666666), ('m1-c4', 0.6666666666666666), ('c4-m1', 0.6666666666666666), ('m1-c1', 0.6666666666666666), ('m8-m1', 1.0), ('c1-m1', 1.0)]



if __name__ == "__main__":
	main(sys.argv)