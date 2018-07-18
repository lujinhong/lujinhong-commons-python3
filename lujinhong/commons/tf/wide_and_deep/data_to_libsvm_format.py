
train_file = '../../../data/g10_predict.txt'
mytrain_file = '../../../data/mypredict.txt'
index_file = '../../../data/myfeatindex.txt'
def csv_format():
    f = open(train_file)
    fout = open(mytrain_file, 'a')
    for line in f:
        filter_feature = ''
        label = line.split(',')[0].strip()
        features = line.split(',')[1].split(' ')
        for s in features:
            if not '_' in s and int(s.split(':')[0])<1299901 and  '801101' not in s:
                filter_feature += ' ' + s.split(':')[0] + ':1'
        fout.write(label)
        fout.write(filter_feature + '\n')
        fout.flush()
    f.close()

def index_format():
    f = open(index_file,'a')
    for i in range(1299901):
        f.write('0:' + str(i) + ' ' + str(i) + '\n')
        f.flush()
    f.close()

if __name__ == '__main__':
    csv_format()
    #index_format()