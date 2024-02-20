import os
import datetime
import pandas
import time

import pandas as pd


class ConvertTimeCode:
    PATH_IN: str = 'data_in'
    PATH_OUT: str = 'data_out'
    OUTPUT_FILE: str = ''

    # YT
    YT_output: pd.DataFrame
    YT_links: pd.DataFrame
    YT_erid: pd.DataFrame
    YT_without_int: pd.DataFrame

    def __init__(self):
        self.INPUT_FILE = os.listdir(self.PATH_IN)[0]
        self.FILE = pandas.read_csv(f"{self.PATH_IN}/{self.INPUT_FILE}", encoding='utf-16', header=0, sep=r'\t', engine='python').iloc[:, [0, 2]]
        self.FILE.columns = ['marker', 'in']
        self.FILE['in'] = list(map(lambda x: ':'.join(x.split(':')[:-1]),self.FILE['in']))
        self.FILE['in'] = pd.to_datetime(self.FILE['in'])
        self.FILE['in'] = self.FILE['in'].dt.time

        # TODO: убрать или оставить часы в доп ексельках зависит от main файла
        # YT
        self.YT_output = self.youtube_integration(data=self.FILE)
        self.YT_output = self._hour_check(data=self.YT_output)

        self.YT_links = self.youtube_links(data=self.FILE)
        self.YT_links = self._hour_check(data=self.YT_links)

        self.YT_erid = self.youtube_erid(data=self.FILE)
        self.YT_erid = self._hour_check(data=self.YT_erid)

    def _hour_check(self, data) -> pandas.DataFrame:
        if data.tail(1).reset_index().iloc[0]['in'].hour:
            return data
        data['in'] = data['in'].apply(lambda x: f"{self._refactor_digit(x.minute)}:{self._refactor_digit(x.second)}")
        return data

    @staticmethod
    def _refactor_digit(dig):
        dig = str(dig)
        if len(dig) == 1:
            return f'0{dig}'
        return dig

    def youtube_integration(self, data) -> pandas.DataFrame:
        new_data = [data.iloc[i] for i in range(data.shape[0]) if self._check_youtube(data.iloc[i][0])]
        return pd.DataFrame(new_data)

    @staticmethod
    def youtube_links(data) -> pandas.DataFrame:
        new_data = [data.iloc[i] for i in range(data.shape[0]) if 'http' in data.iloc[i][0]]
        return pd.DataFrame(new_data)

    @staticmethod
    def youtube_erid(data) -> pandas.DataFrame:
        new_data = [data.iloc[i] for i in range(data.shape[0]) if 'erid' in data.iloc[i][0]]
        return pd.DataFrame(new_data)

    # TODO: дописать функцию для видео без интеграции
    def youtube_without_int(self, data) -> pandas.DataFrame:
        new_data = [data.iloc[i] for i in range(data.shape[0]) if 'erid' in self._data.iloc[i][0]]
        return pd.DataFrame(new_data)



    @staticmethod
    def _check_youtube(ser):
        if 'erid' in ser:
            return False
        if 'http' in ser:
            return False

        return True


    def _check_youtube_without_int(self, ser):
        ConvertTimeCode._check_youtube(self._check_youtube)
        if 'интеграция' in ser.lower():
            return False

        return True


    # def without_integration():
    #     txt = integration(el=elems)
    #     w_elems = []
    #     new_elems = []
    #     for i in range(len(txt)):
    #         first_space = txt[i].find(' ')
    #         w_elems.append([txt[i][:first_space], txt[i][first_space + 1:]])
    #     time = datetime.timedelta(minutes=0, seconds=0)
    #     cumsum = datetime.timedelta(hours=0, minutes=0, seconds=0)
    #     integr_time = 0
    #
    #     for i in range(len(w_elems)):
    #
    #         if 'интеграция' not in w_elems[i][1].lower():
    #             t = w_elems[i][0].split(':')
    #             if len(t) == 2:
    #                 time = datetime.timedelta(minutes=int(t[0]), seconds=int(t[1]))
    #             else:
    #                 time = datetime.timedelta(hours=int(t[0]), minutes=int(t[1]), seconds=int(t[2]))
    #             if integr_time != 0:
    #                 cumsum += time-integr_time
    #             time = time-cumsum
    #             new_elems.append([str(time), w_elems[i][1]])
    #             integr_time = 0
    #
    #         else:
    #             t = w_elems[i][0].split(':')
    #             if len(t) == 2:
    #                 integr_time = datetime.timedelta(minutes=int(t[0]), seconds=int(t[1]))
    #             else:
    #                 integr_time = datetime.timedelta(hours=int(t[0]), minutes=int(t[1]), seconds=int(t[2]))
    #
    #     without_elems = []
    #     new_elems = list(map(lambda x: ' '.join(x), new_elems))
    #     for i in range(len(new_elems)):
    #         first_space = new_elems[i].find(' ')
    #         without_elems.append([new_elems[i][:first_space], new_elems[i][first_space + 1:]])
    #
    #     elems_list = list(map(lambda x: [x[0].split(':'), x[1]], without_elems))
    #     hour = True if int(elems_list[-1][0][0]) > 0 else False
    #
    #     if hour:
    #         txt2 = list(map(lambda x: f"{':'.join(x[0])} {x[1]}" if int(x[0][0])>9 else f"0{':'.join(x[0])} {x[1]}", elems_list))
    #     else:
    #         txt2 = list(map(lambda x: f"{':'.join(x[0][1:])} {x[1]}", elems_list))
    #
    #     return 'С интеграцией' + '\n' '\n' + '\n'.join(txt) + '\n' + '\n' + 'Без интеграции' + '\n' + '\n' + '\n'.join(txt2)
    #
    # try:
    #     with open('data_out/result_time_codes.txt', 'w', encoding='utf-8') as rslt:
    #         rslt.write(without_integration())
    #     print("Результат получен и сохранён в файл 'result_time_codes.txt'")
    # except:
    #     'Неподходящий формат строк файла. Требуются строки вида: "00:00:00:00 Приветики" и с окончанием строки в виде переноса'


if __name__ == '__main__':
    ConvertTimeCode().YT_output.to_csv(f"{ConvertTimeCode.PATH_OUT}/YT/YT.csv", index=False)
    ConvertTimeCode().YT_links.to_csv(f"{ConvertTimeCode.PATH_OUT}/YT/YT_links.csv", index=False)
    ConvertTimeCode().YT_erid.to_csv(f"{ConvertTimeCode.PATH_OUT}/YT/YT_erid.csv", index=False)
