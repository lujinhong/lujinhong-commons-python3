#coding=utf-8

input_file = '/Users/ljhn1829/Downloads/g83na/g83na_pltv.txt'
output_file = '/Users/ljhn1829/Downloads/g83na/g83na_pltv_result.txt'


class PltvSampling:

    @staticmethod
    def sampling(self):
        inf = open(input_file, 'r')
        outf = open(output_file, 'a')

        for line in inf:
            ss = line.split('\t')
            udid = ss[0]
            if len(udid) == 16 or len(udid) == 36:
                probability = ss[1]
                pay = ss[2]
                if float(probability) > 0.6 or float(pay) > 0:
                    outf.write(udid + '\n')
        inf.close()
        outf.close()


if __name__ == '__main__':
    p = PltvSampling()
    p.sampling()

