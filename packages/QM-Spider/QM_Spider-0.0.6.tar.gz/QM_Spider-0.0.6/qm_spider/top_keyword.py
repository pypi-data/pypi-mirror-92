from qm_spider import *

class get_top_keyword:
    def __init__(self, appid, keyword_hot_start, start_time, end_time):
        self.keyword_hot_start = keyword_hot_start
        self.keyword_hot_end = 15000000
        self.appid = appid
        self.start_time = datetime.date.fromisoformat(start_time)
        self.end_time = datetime.date.fromisoformat(end_time)
        self.one_day = datetime.timedelta(days=1)

    def get_all_top(self):
        self.app_name = get_app_appinfo(self.appid).get_subname()
        self.t1_all_list = []
        self.t2_all_list = []
        self.t3_all_list = []
        self.t5_all_list = []
        self.t10_all_list = []
        self.date_list = []
        self.now_app_list = []
        while self.start_time <= self.end_time:
            res = get_app_keyword(self.appid, self.start_time).get_keywordDetail()
            if res.json()['msg'] == '成功' and len(res.json()['data']) > 0:
                df_keyword = qimai_outside_tool(res.json()['data']).json_to_df()
                df_keyword.columns = ['关键词ID', '关键词', '排名', '变动前排名', '排名变动值', '指数', '结果数', '未知1', '未知2']

                t1_all_num = df_keyword[(df_keyword['排名'] <= 1) & (df_keyword['指数'] >= self.keyword_hot_start) & (df_keyword['指数'] <= self.keyword_hot_end) & (df_keyword['排名变动值'] != 'lost')].shape[0]
                t2_all_num = df_keyword[(df_keyword['排名'] <= 2) & (df_keyword['指数'] >= self.keyword_hot_start) & (df_keyword['指数'] <= self.keyword_hot_end) & (df_keyword['排名变动值'] != 'lost')].shape[0]
                t3_all_num = df_keyword[(df_keyword['排名'] <= 3) & (df_keyword['指数'] >= self.keyword_hot_start) & (df_keyword['指数'] <= self.keyword_hot_end) & (df_keyword['排名变动值'] != 'lost')].shape[0]
                t5_all_num = df_keyword[(df_keyword['排名'] <= 5) & (df_keyword['指数'] >= self.keyword_hot_start) & (df_keyword['指数'] <= self.keyword_hot_end) & (df_keyword['排名变动值'] != 'lost')].shape[0]
                t10_all_num = df_keyword[(df_keyword['排名'] <= 10) & (df_keyword['指数'] >= self.keyword_hot_start) & (df_keyword['指数'] <= self.keyword_hot_end) & (df_keyword['排名变动值'] != 'lost')].shape[0]

                print('【%s】产品在【%s】%s+t3词有【%s】个' % (self.appid, self.start_time, self.keyword_hot_end, t3_all_num))
                self.t1_all_list.append(t1_all_num)
                self.t2_all_list.append(t2_all_num)
                self.t3_all_list.append(t3_all_num)
                self.t5_all_list.append(t5_all_num)
                self.t10_all_list.append(t10_all_num)
                self.date_list.append(str(self.start_time))
                self.now_app_list.append(self.appid)
            else:
                print('【%s】产品在【%s】%s+t3词有【%s】个' % (self.appid, self.start_time, self.keyword_hot_end, 0))
                self.t1_all_list.append(0)
                self.t2_all_list.append(0)
                self.t3_all_list.append(0)
                self.t5_all_list.append(0)
                self.t10_all_list.append(0)
                self.date_list.append(str(self.start_time))
                self.now_app_list.append(self.appid)

            self.start_time += self.one_day

        return pd.DataFrame({
            'AppID': self.now_app_list,
            '日期': self.date_list,
            'T1数量': self.t1_all_list,
            'T2数量': self.t2_all_list,
            'T3数量': self.t3_all_list,
            'T5数量': self.t5_all_list,
            'T10数量': self.t10_all_list
        })