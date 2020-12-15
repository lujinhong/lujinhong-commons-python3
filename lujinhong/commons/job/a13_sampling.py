# -*- coding: utf-8 -*-

"""
     AUTHOR: lujinhong
 CREATED ON: 2019年08月23日 09:48
    PROJECT: lujinhong-commons-python3
DESCRIPTION: TODO
"""

import math
in_file = '/Users/ljhn1829/Downloads/a13/2.txt'
out_file = '/Users/ljhn1829/Downloads/a13/2out.txt'

def sampling():
    print()
    inf = open(in_file,'r')
    outf = open(out_file,'a')
    for line in inf:

        ss = line.split('\t')
        udid = ss[0]
        features = ss[1]
        is_positive = ss[2]
        out_line = udid + '\t'
        for feature in features.split(' '):
            key = feature.split(':')[0]
            value = feature.split(':')[1]
            if key in ('GameCreate_ishave','GameModeInit_ishave','GameModeChange_ishave','GameOnlineReviewCreate_ishave','LoginRole_is_point_user'):
                out_line += (key + ':1:20190101 ')
            if key.startswith('CreateRole_os_name_') or key.startswith('CreateRole_device_model_') or key.startswith('CreateRole_network_') or key.startswith('CreateRole_isp_'):
                out_line += (key + ':1:20190101 ')
            if key in ('CreateRole_create_time','LoginRole_total_login_days','Prepaid_total_pay_days','Activation_activation_time','PageClick_total_click_days','PageClick_game_id_total_click_days','PageClick_topic_theme_ids_game_id_total_click_days','GameView_total_days','GamePlay_total_days','CreateRole_role_level','LoginRole_total_login_times','LoginRole_total_login_minutes','Prepaid_total_pay_times','Prepaid_total_yuanbao','Prepaid_total_cash','Prepaid_total_ciyuanquan','ItemBuy_total_item_buy_times','ItemBuy_total_item_buy_yuanbao','PageClick_total_click_times','PageClick_game_id_total_click_times','PageClick_topic_theme_ids_game_id_total_click_times','PageClick_sharing_channel_total_times','GameView_total_times','GameView_total_minutes','GamePlay_total_times','GamePlay_total_minutes','GameLike_total_times','GameFavorite_total_times','GameTopic_total_times','GameComment_total_times','GameModuleView_total_times','PageOnline_total_duration_minutes','GameOnline_total_duration_minutes','Share_total_times','GameLoading_total_times','GameLoading_total_minutes','MatchSignup_total_times','InvitationCode_total_times','EngineLog_total_times','EditorLog_total_times','IosLog_AndroidLog_total_times','GameFrame_total_times','TopicPlatform_total_times','TopicThemePlatform_total_times','CommunityOnline_total_minutes','TopicView_total_times','TopicRecommend_total_times','TopicAuthorInfoSync_topic_count','TopicAuthorInfoSync_follower_count','TopicAuthorInfoSync_click_count','TopicAuthorInfoSync_comment_count','TopicAuthorInfoSync_like_count','TopicAuthorInfoSync_favorite_count','TopicAuthorInfoSync_share_count','UserFocusPlatform_total_guanzhu_times','UserFocusPlatform_total_quguan_times','UserRecommendView_total_times'):
                bin_value = 0
                if '-127' in value:
                    bin_value = -1
                if float(value) > 0.1 :
                    bin_value = int(math.log2(int(value.split('.')[0]) + 2)) + 1
                out_line += (key + '_' + str(bin_value) + ':1:20190101 ')
                if key + '_' + str(bin_value) == 'PageOnline_total_duration_minutes_15':
                    print(udid)
            if key.startswith('PageClick_game_id_total_click_days_') or key.startswith('PageClick_topic_theme_ids_game_id_total_click_days_') or key.startswith('GameView_total_days_')  or key.startswith('GamePlay_total_days_') or key.startswith('ItemBuy_total_item_buy_times_') or key.startswith('ItemBuy_total_item_buy_yuanbao_') or key.startswith('PageClick_game_id_total_click_times_') or key.startswith('PageClick_topic_theme_ids_game_id_total_click_times_') or key.startswith('GameView_total_times_') or key.startswith('GameView_total_minutes_') or key.startswith('GamePlay_total_times_') or key.startswith('GamePlay_total_minutes_') or key.startswith('GameTopic_total_times_') or key.startswith('GameComment_total_times_') or key.startswith('GameModuleView_total_times_') or key.startswith('GameOnline_total_duration_minutes_'):
                bin_value = 0
                if float(value) > 0.1 :
                    bin_value = int(math.log2(int(value.split('.')[0]) + 2)) + 1
                out_line += (key + '_' + str(bin_value) + ':1:20190101 ')

        outf.write(out_line + '\t' + is_positive + '\n')

    inf.close()
    outf.close()



if __name__ == '__main__':
    sampling()