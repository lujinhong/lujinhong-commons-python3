# coding=utf-8

class SortDictDemo:
    def sort_dict(self, dict):
        sorted_list = sorted(dict.items(), key=lambda item: item[1], reverse=True)
        return sorted_list


if __name__ == '__main__':
    dict = {"you": 12, "can't": 4, "eat": 10}
    sd = SortDictDemo()
    sorted_result = sd.sort_dict(dict)
    for item in sorted_result:
        print(item[0] + "\t" + str(item[1]))
