import requests,datetime,time,warnings,json,calendar,math,os
from datetime import date
from dateutil.relativedelta import relativedelta
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np
from scipy.stats import norm, mstats
warnings.filterwarnings("ignore")

# 保持会话；
session = requests.session()

# 请求头；
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
}

# 钉钉推送；
class DingDing_Push:
    def __init__(self, push_title, *args, push_status='执行成功', now_time=str(datetime.datetime.now())[:19], push_url='https://oapi.dingtalk.com/robot/send?access_token=f3a590b8c5f4c4777fe0f217067f15132091bff53e2a2143a5daa981d795159d'):
        self.push_title = push_title
        self.push_status = push_status
        self.now_time = now_time
        self.push_url = push_url
        self.other_var = args
        self.headers = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }

    def status_push(self):
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": "【%s】%s" %(self.now_time[:10], self.push_title),
                "text": "**推送事件**：%s\n\n**推送时间**：%s\n\n**推送状态**：%s" %(self.push_title, self.now_time, self.push_status)
            }
        }
        payload = json.dumps(payload)
        res = requests.post(self.push_url, data=payload, headers=self.headers)

    def app_rank_abnormal_push(self):
        self.samePubApp_link = 'https://www.qimai.cn/app/samePubApp/appid/%s/country/cn' %(self.other_var[0])
        self.app_rank_link = 'https://www.qimai.cn/app/rank/appid/%s/country/cn' %(self.other_var[0])
        self.app_keyword_link = 'https://www.qimai.cn/app/keyword/appid/%s/country/cn' %(self.other_var[0])
        # self.app_name = self.other_var[1]
        # self.samePubApp_name = self.other_var[2]
        # self.offline_time = self.other_var[3]
        # self.offline_yesterday_rank = self.other_var[4]
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": "【%s】%s" %(self.now_time[:10], self.push_title),
                "text": "**推送事件**：%s\n\n**抓取时间**：%s\n\n**App名称**：[%s](%s)\n\n**开发商名称**：[%s](%s)\n\n**下架/清榜时间**：%s\n\n**下架/清榜前一日总榜**：%s" %(self.push_title, self.now_time, self.other_var[1], self.app_rank_link, self.other_var[2], self.samePubApp_link, self.other_var[3], self.other_var[4])
            }
        }
        payload = json.dumps(payload)
        res = requests.post(self.push_url, data=payload, headers=self.headers)

    def app_args_push(self):
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": "%s" %(self.push_title),
                "text": "%s" %(self.other_var[0])
            }
        }
        payload = json.dumps(payload)
        res = requests.post(self.push_url, data=payload, headers=self.headers)

# 自动登录；
class Sing_Qimai:
    def __init__(self, user_id, user_pwd):
        self.user_id = user_id
        self.user_pwd = user_pwd

    def login_qm(self):
        url = 'https://api.qimai.cn/account/signinForm'
        payload = "username=%s&password=%s" %(self.user_id, self.user_pwd)
        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"
        }
        res = session.post(url, headers=headers, data=payload)

# 计算七麦外的其他备用工具；
class Qimai_Outside_Tool:
    def __init__(self, *args):
        self.data_info = args

    def json_to_df(self):
        self.json_df = json_normalize(self.data_info[0])
        return self.json_df

    def list_to_df(self):
        self.list_df = pd.DataFrame(self.data_info[0])
        return self.list_df

    def unix_time(self):
        # 世界标准时间
        date_now = datetime.datetime.strptime(self.data_info[0], '%Y-%m-%d %H:%M:%S')
        # 北京时间UTC+8
        cst_time = date_now.astimezone(datetime.timezone(datetime.timedelta(hours=-8))).strftime("%Y-%m-%d %H:%M:%S")
        return cst_time

    def time_to_date(self):
        if len(str(self.data_info[0])) == 13:
            self.run_time = int(self.data_info[0]/1000)
        else:
            self.run_time = self.data_info[0]
        timeArray = time.localtime(self.run_time)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

    def date_to_time(self):
        if len(str(self.data_info[0])) == 10:
            self.run_date = self.data_info[0] + ' 00:00:00'
        timeArray = time.strptime(self.run_date, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

    def get_month_time(self):
        day_start = datetime.date.fromisoformat(str(self.data_info[0]))
        day_end = datetime.date.fromisoformat(str(self.data_info[1]))
        # monthRange_start = calendar.monthrange(day_start.year, day_start.month)
        monthRange_end = calendar.monthrange(day_end.year, day_end.month)
        start_time = str(day_start)[:8] + str('01')
        end_time = str(day_end)[:8] + str(monthRange_end[1])
        return start_time, end_time

    def calc_interval_time(self):
        spider_time_datetime = datetime.datetime.strptime(str(self.data_info[0]), '%Y-%m-%d %H:%M:%S')
        rank_out_datetime = datetime.datetime.strptime(str(self.data_info[1]), '%Y-%m-%d %H:%M:%S')
        interval_seconds = (rank_out_datetime - spider_time_datetime).seconds
        m, s = divmod(interval_seconds, 60)
        h, m = divmod(m, 60)
        interval_time = "%02d小时%02d分钟%02d秒" % (h, m, s)  # 计算间隔时间；
        return interval_time

    def calc_overlap_days(self, s1, e1, s2, e2):
        latest_start = max(s1, s2)
        earliest_end = min(e1, e2)
        self.overlap = (earliest_end - latest_start).days + 1
        if self.overlap < 0:
            self.overlap = 0
        s1_days = (e1 - s1).days + 1
        s2_days = (e2 - s2).days + 1
        self.s1_scale = self.overlap / s1_days
        self.s2_scale = self.overlap / s2_days
        return self.overlap, self.s1_scale, self.s2_scale

    def trend_analysis(self):
        self.alpha = 0.05
        n = len(self.data_info[0])
        s = 0
        for k in range(n - 1):
            for j in range(k + 1, n):
                s += np.sign(self.data_info[0][j] - self.data_info[0][k])
        unique_x, tp = np.unique(self.data_info[0], return_counts=True)
        g = len(unique_x)
        if n == g:
            var_s = (n * (n - 1) * (2 * n + 5)) / 18
        else:  # there are some ties in data
            var_s = (n * (n - 1) * (2 * n + 5) - np.sum(tp * (tp - 1) * (2 * tp + 5))) / 18
        if s > 0:
            z = (s - 1) / np.sqrt(var_s)
        elif s < 0:
            z = (s + 1) / np.sqrt(var_s)
        else:  # s == 0:
            z = 0
        p = 2 * (1 - norm.cdf(abs(z)))  # two tail test
        h = abs(z) > norm.ppf(1 - self.alpha / 2)
        if (z < 0) and h:
            self.trend = '下降', p, g, z
        elif (z > 0) and h:
            self.trend = '上升', p, g, z
        else:
            self.trend = '无趋势', p, g, z
        return self.trend

# 计算七麦内的备用工具；
class Qimai_Intside_Tool:
    def rank_ios10_type(self, price):
        if price == '0.00' or price == '免费':
            return '总榜(免费)'
        else:
            return '总榜(付费)'

    def old_rank_num(self, rank_data, rank_name='总榜(免费)'):
        for app_rank in rank_data['data']['list']:
            if app_rank['name'] == rank_name:
                return app_rank['data'][0][0]
        else:
            return 0

    def new_rank_num(self, rank_data, rank_name='总榜(免费)'):
        for app_rank in rank_data['data']['list']:
            if app_rank['name'] == rank_name:
                return app_rank['data'][-1][0]
        else:
            return 0

# 常用的自定义参数；
class Qimai_Diy_Var:
    def __init__(self, country='cn', rank_type='all', version='ios12', device='iphone', search_type='all', brand='all', day=1, appRankShow=1, subclass='all', simple=1, rankEchartType=1, rankType='day', run_time=datetime.date.today(), status=6, keyword_hot_start=4605, typec='day', star='five', delete=-1, orderType='time', commentType='default', genre_type=36, status_type=3, clear_type=1, filter='offline', search_word='', export_type='rank_clear_words', sort_field='beforeClearNum', sort_type='desc', option=4, app_status_str='all', app_status_sdate='', app_status_edate='', app_status_order='', app_status_sort='', preOrder_order=1):
        self.country = country
        self.rank_type = rank_type
        self.version = version
        self.device = device
        self.search_type= search_type
        self.brand = brand
        self.day = day
        self.appRankShow = appRankShow
        self.subclass = subclass
        self.simple = simple
        self.rankEchartType = rankEchartType
        self.rankType = rankType
        self.run_time = run_time
        self.one_day = datetime.timedelta(days=1)
        self.status = status
        self.keyword_hot_start = keyword_hot_start
        self.typec = typec
        self.star = star
        self.delete = delete
        self.orderType = orderType
        self.commentType = commentType
        self.clear_type = clear_type
        self.status_type = status_type
        self.genre_type = genre_type
        self.search_word = search_word
        self.filter = filter
        self.export_type = export_type
        self.sort_field = sort_field
        self.sort_type = sort_type
        self.option = option
        self.app_status_str = app_status_str
        self.app_status_sdate = app_status_sdate
        self.app_status_edate = app_status_edate
        self.app_status_order = app_status_order
        self.app_status_sort = app_status_sort
        self.preOrder_order = preOrder_order

# 获取基础信息相关数据；
class Get_App_Appinfo(Qimai_Diy_Var):
    def __init__(self, appid):
        Qimai_Diy_Var.__init__(self)
        self.appid = appid

    def get_appinfo(self):
        url = 'https://api.qimai.cn/app/appinfo?appid=%s&country=%s' %(self.appid, self.country)
        res = session.get(url, headers=headers)
        self.appinfo = res.json()
        return self.appinfo

    def get_subname(self):
        self.get_appinfo()
        self.subname = self.appinfo['appInfo']['subname']
        return self.subname

# 获取榜单相关数据；
class Get_App_Rank(Qimai_Diy_Var):
    def __init__(self, appid, start_time, end_time):
        Qimai_Diy_Var.__init__(self)
        self.appid = appid
        self.start_time = start_time
        self.end_time = end_time

    def get_rank_info(self):
        url = 'https://api.qimai.cn/app/rankMore?appid=%s&country=%s&brand=%s&day=%s&appRankShow=%s&subclass=%s&simple=%s&sdate=%s&edate=%s&rankEchartType=%s&rankType=%s&device=%s' %(self.appid, self.country, self.brand, self.day, self.appRankShow, self.subclass, self.simple, self.start_time, self.end_time, self.rankEchartType, self.rankType, self.device)
        res = session.get(url, headers=headers)
        self.rank_info = res.json()
        return self.rank_info

    def all_rank(self):
        self.get_rank_info()
        try:
            return self.rank_info['data']['list']
        except:
            return []

    def clear_rank(self):
        self.get_rank_info()
        try:
            return self.rank_info['data']['clear']
        except:
            return []

# 获取开发商相关数据；
class Get_App_SamePubApp(Get_App_Appinfo, Qimai_Diy_Var):
    def __init__(self, appid):
        Get_App_Appinfo.__init__(self, appid)
        Qimai_Diy_Var.__init__(self)

    def get_samePubApp(self):
        url = 'https://api.qimai.cn/app/samePubApp?appid=%s&country=%s' %(self.appid, self.country)
        res = session.get(url, headers=headers)
        self.app_samePubApp = res.json()['samePubApps']
        return self.app_samePubApp

    def get_app_genName(self):
        self.get_samePubApp()
        for info in self.app_samePubApp:
            if str(info['appInfo']['appId']) == str(self.appid):
                self.app_total_genid = info['total']['brand']
                self.app_class_genid = info['class']['brand']
                return self.app_total_genid, self.app_class_genid

    def samePubApp_sorce(self):
        self.get_samePubApp()
        cp_quanzhong_list = []
        for x in self.app_samePubApp:
            all_rank_num = x['total']['ranking']
            all_rank_quanzhong = round(1 - int(all_rank_num) / 1500, 4)
            if all_rank_quanzhong == 1:
                cp_quanzhong_list.append(0)
            else:
                cp_quanzhong_list.append(all_rank_quanzhong)

        return max(cp_quanzhong_list)

# 获取关键词的相关数据；
class Get_Keyword_Info(Qimai_Diy_Var):
    def __init__(self, keyword):
        Qimai_Diy_Var.__init__(self)
        self.keyword = keyword

    def get_keyword_search(self):
        url = 'https://api.qimai.cn/search/getWordInfo?country=%s&device=%s&search=%s&version=%s&date=%s&search_type=%s&status=%s&edate=%s' %(self.country, self.device, self.keyword, self.version, self.run_time, self.search_type, self.status, self.run_time-self.one_day)
        res = session.get(url, headers=headers)
        self.keyword_serch_index = res.json()
        return self.keyword_serch_index

    def get_keyword_WordInfo(self):
        url = 'https://api.qimai.cn/search/getWordInfo?device=%s&country=%s&search=%s&version=%s&date=%s&search_type=%s&status=%s&edate=%s' %(self.device, self.country, self.keyword, self.version, self.run_time, self.search_type, self.status, self.run_time-self.one_day)
        res = session.get(url, headers=headers)
        self.keyword_WordInfo = res.json()
        return self.keyword_WordInfo

    def get_keyword_hints(self):
        self.get_keyword_WordInfo()
        self.hints = self.keyword_WordInfo['wordInfo']['hints']
        return self.hints

# 获取产品的关键词相关数据；
class Get_App_Keyword(Qimai_Diy_Var):
    def __init__(self, appid):
        Qimai_Diy_Var.__init__(self)
        self.appid = appid

    def get_keywordDetail(self):
        url = 'https://api.qimai.cn/app/keywordDetail?country=%s&appid=%s&version=%s&sdate=%s&device=%s&edate=' %(self.country, self.appid, self.version, self.run_time, self.device)
        res = session.get(url, headers=headers)
        self.app_keywordDetail = res.json()
        return self.app_keywordDetail

    def get_keywordSummary(self):
        url = 'https://api.qimai.cn/app/keywordSummary?country=%s&appid=%s&version=%s&sdate=%s&device=%s&edate=' %(self.country, self.appid, self.version, self.run_time, self.device)
        res = session.get(url, headers=headers)
        self.app_keywordSummary = res.json()
        return self.app_keywordSummary

    def get_AnalysisDataKeyword(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        url = 'https://api.qimai.cn/account/getAnalysisDataKeyword?appid=%s&country=%s&device=%s&sdate=%s&edate=%s&version=%s&hints=%s' %(self.appid, self.country, self.device, self.start_time, self.end_time, self.version, self.keyword_hot_start)
        res = session.get(url, headers=headers)
        self.app_AnalysisDataKeyword = res.json()
        return self.app_AnalysisDataKeyword

    def get_keywordDetail_to_df(self):
        self.get_keywordDetail()
        self.json_df = json_normalize(self.app_keywordDetail['data'])
        self.json_df.columns = ['关键词ID', '关键词', '排名', '变动前排名', '排名变动值', '指数', '结果数', '未知1', '未知2']
        return self.json_df

    def app_cover_regular(self):
        self.get_keywordSummary()
        for keywordSummary_info in self.app_keywordSummary['keywordSummary']:
            title = keywordSummary_info['title']
            if title == '合计':
                all_keyword = keywordSummary_info['all']['num']
                top3_keyword = keywordSummary_info['top3']['num']
                top10_keyword = keywordSummary_info['top10']['num']
                if int(all_keyword) >= 3000:
                    return ['覆盖合格', all_keyword, top3_keyword, top10_keyword]
                else:
                    return ['覆盖不合格', all_keyword, top3_keyword, top10_keyword]

# 获取产品评论的相关接口；
class Get_App_Comment(Qimai_Diy_Var):
    def __init__(self, appid, start_time, end_time):
        Qimai_Diy_Var.__init__(self)
        self.appid = appid
        self.start_time = start_time
        self.end_time = end_time

    def get_commentRateNum(self):
        url = 'https://api.qimai.cn/app/commentRateNum?appid=%s&country=%s&sdate=%s&edate=%s&typec=%s' %(self.appid, self.country, self.start_time, self.end_time, self.typec)
        res = session.get(url, headers=headers)
        self.app_commentRateNum = res.json()
        return self.app_commentRateNum

    def get_commentNum(self):
        url = 'https://api.qimai.cn/app/commentNum?appid=%s&country=%s&delete=%s&sdate=%s&edate=%s' %(self.appid, self.country, self.delete, self.start_time, self.end_time)
        res = session.get(url, headers=headers)
        self.app_commentNum = res.json()
        return self.app_commentNum

    def get_comment(self):
        url = 'https://api.qimai.cn/app/comment?appid=%s&country=%s&sword=&sdate=%s+00:00:00&edate=%s+23:59:59&orderType=%s&commentType=%s' %(self.appid, self.country, self.start_time, self.end_time, self.orderType, self.commentType)
        res = session.get(url, headers=headers)
        self.app_comment = res.json()
        return self.app_comment

    def get_all_commentRateNum(self):
        self.get_commentRateNum()
        df = pd.DataFrame({})
        for comment_info in self.app_commentRateNum['rateInfo']:
            df_new = Qimai_Outside_Tool(comment_info['data']).list_to_df()
            df = pd.concat([df, df_new])
        df.columns = ['日期', '评论数']
        df['日期'] = df['日期'].apply(lambda x: Qimai_Outside_Tool(x).time_to_date())
        df = df.groupby('日期').sum()
        return df

    def get_Star_commentRateNum(self, star_value='五星'):
        self.get_commentRateNum()
        df = pd.DataFrame({})
        for comment_info in self.app_commentRateNum['rateInfo']:
            if comment_info['name'] == star_value:
                df_new = Qimai_Outside_Tool(comment_info['data']).list_to_df()
                df = pd.concat([df, df_new])
        df.columns = ['日期', '评论数']
        df['日期'] = df['日期'].apply(lambda x: Qimai_Outside_Tool(x).time_to_date())
        df = df.groupby('日期').sum()
        return df

# 获取清榜列表相关数据；
class Get_Clear_Rank_List(Qimai_Diy_Var):
    def __init__(self, start_time, end_time):
        Qimai_Diy_Var.__init__(self)
        self.start_time = start_time
        self.end_time = end_time

    def get_clear_rank(self):
        self.clear_rank_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/rank/clear?1=&sdate=%s&edate=%s&page=%s&type=%s&genre=%s&status=%s' %(self.start_time, self.end_time, page_num, self.clear_type, self.genre_type, self.status_type)
            res = session.get(url, headers=headers)
            self.clear_rank_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.clear_rank_list

# 获取清词列表相关数据；
class Get_Clear_Keyword_List(Qimai_Diy_Var):
    def __init__(self, start_time, end_time):
        Qimai_Diy_Var.__init__(self)
        self.start_time = start_time
        self.end_time = end_time

    def get_clear_keyword(self):
        self.clear_word_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/rank/clearWords?edate=%s&page=%s&genre=%s&sdate=%s&filter=%s&export_type=%s&sort_field=%s&sort_type=%s&search=%s' %(self.end_time, page_num, self.genre_type, self.start_time, self.filter, self.export_type, self.sort_field, self.sort_type, self.search_word)
            res = session.get(url, headers=headers)
            self.clear_word_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.clear_word_list

# 获取下架产品列表相关数据；
class Get_App_Offline_List(Qimai_Diy_Var):
    def __init__(self, start_time, end_time):
        Qimai_Diy_Var.__init__(self)
        self.start_time = start_time
        self.end_time = end_time

    def get_app_offline(self):
        self.app_offline_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/rank/offline?date=%s_%s&country=%s&genre=%s&option=%s&search=%s&sdate=%s&edate=%s&page=%s' % (self.start_time, self.end_time, self.country, self.genre_type, self.option, self.search_word, self.start_time, self.end_time, page_num)
            res = session.get(url, headers=headers)
            self.app_offline_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.app_offline_list

# 获取预订App列表；
class Get_PreOrder_AppList(Qimai_Diy_Var):
    def __init__(self):
        Qimai_Diy_Var.__init__(self)

    def get_preOrder_applist(self):
        self.preOrder_applist_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/rank/preOrder?genre=%s&country=%s&order=%s&page=%s' %(self.genre_type, self.country, self.preOrder_order, page_num)
            res = session.get(url, headers=headers)
            self.preOrder_applist_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.preOrder_applist_list

# 获取产品被精品推荐及上热搜情况列表；
class Get_App_Recommend(Qimai_Diy_Var):
    def __init__(self, appid):
        Qimai_Diy_Var.__init__(self)
        self.appid = appid

    def get_app_featured(self):
        url = 'https://api.qimai.cn/app/featured?country=%s&appid=%s' %(self.country, self.appid)
        res = session.get(url, headers=headers)
        self.app_featured = res.json()
        return self.app_featured

    def get_app_engagement(self, start_time, end_time):
        url = 'https://api.qimai.cn/app/engagement'
        payload='app_id=%s&s_date=%s&e_date=%s' %(self.appid, start_time, end_time)
        res = session.post(url, data=payload, headers=headers)
        self.app_engagement = res.json()
        return self.app_engagement

    def featured_match(self):
        self.get_app_featured()
        tuijian_num = len(self.app_featured['featured'])
        if tuijian_num > 0:
            return ['有推荐', tuijian_num]
        else:
            return ['无推荐', tuijian_num]

# 获取App不同状态列表；
class Get_App_Status(Qimai_Diy_Var):
    def __init__(self, appid):
        Qimai_Diy_Var.__init__(self)
        self.appid = appid

    def get_all_appStatusList(self):
        self.app_status_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/app/appStatusList'
            payload='appid=%s&country=%s&status=all&sdate=%s&edate=%s&page=1&order=%s&sort=%s' %(self.appid, self.country, self.app_status_sdate, self.app_status_edate, self.app_status_order, self.app_status_sort)
            res = session.post(url, data=payload, headers=headers)
            self.app_status_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.app_status_list

    def get_status_appStatusList(self):
        self.app_status_list = []
        page_num = 1
        while True:
            url = 'https://api.qimai.cn/app/appStatusList'
            payload='appid=%s&country=%s&status=%s&sdate=%s&edate=%s&page=1&order=%s&sort=%s' %(self.appid, self.country, self.app_status_str, self.app_status_sdate, self.app_status_edate, self.app_status_order, self.app_status_sort)
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            res = session.post(url, data=payload, headers=headers)
            self.app_status_list.append(res.json())
            page_num += 1
            if page_num > res.json()['maxPage']:
                break
        return self.app_status_list

    def get_new_status_info(self):
        self.get_status_appStatusList()
        for status_list in self.app_status_list:
            if status_list['msg'] == '成功':
                if len(status_list['data']) > 0:
                    sdate_time = status_list['data'][0]['sdate']
                    return sdate_time
                else:
                    return ''
            return ''

    def get_old_status_info(self):
        self.get_status_appStatusList()
        for status_list in self.app_status_list:
            if status_list['msg'] == '成功':
                if len(status_list['data']) > 0:
                    sdate_time = status_list['data'][-1]['sdate']
                    return sdate_time
                else:
                    return ''
            return ''







