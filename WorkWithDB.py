import csv

class ProcessingRequest:

    def __init__(self):
        self.query_part_number = ''
        self.detail_dict = {}
        self.ans = []
        self.dictation_preprocess()

    def make_new_part_num(self, part_number):
        self.query_part_number = part_number

    def dictation_preprocess(self):
        with open('DB.tsv') as tsvFile:
            reader = csv.DictReader(tsvFile, dialect='excel-tab')
            for row in reader:
                the_next_detail_pt_num = row['part_number']
                if the_next_detail_pt_num in self.detail_dict:
                    self.add_to_dict(the_next_detail_pt_num, [row['supplier'], float(row['price'])])

                else:
                    self.detail_dict[the_next_detail_pt_num] = list()
                    self.add_to_dict(the_next_detail_pt_num, [row['supplier'], float(row['price'])])

    def add_to_dict(self, key, det_info):
        self.detail_dict[key].append(det_info)

    #'ZVC403-4'

    def data_proc(self):
        if self.query_part_number in self.detail_dict:
            self.ans = self.detail_dict[self.query_part_number]
            return sorted(self.ans, key=lambda i: i[1], reverse=True)
        else:
            return 'Sorry, there is no given part number :('
