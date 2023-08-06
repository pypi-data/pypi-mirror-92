#Author:Hanson
from .myzabbix import zabbix_api

if __name__=="__main__":
    # 华北zabbix操作
    url = 'http://###/zabbix'
    username = "###"
    password = "###"

    huabei_zabbix_api = zabbix_api(url, username, password)
    # aaa = huabei_zabbix_api.get_host_list(48, "none")
    # bbb = huabei_zabbix_api.get_name_ip_all(48, "none")
    # print(aaa)
    # print(bbb)

    # ccc = huabei_zabbix_api.get_groupID("机房-B28")
    # ddd = huabei_zabbix_api.get_templateID("NOC-HB-Network")
    # dd = huabei_zabbix_api.get_hostID("2B-B28-F1-H3C-5800-CNC-2698")
    # eee = huabei_zabbix_api.get_host_group_name("NOC-HB-Network-Group")
    # fff = huabei_zabbix_api.get_host_template_name("NOC-HB-Network")
    # ggg = huabei_zabbix_api.get_host_template_name("NOC-HB-Network-Huawei_CloudEngine_8800")
    # hhh = huabei_zabbix_api.get_graph_group_name("机房-B28")
    # iii = huabei_zabbix_api.get_item_group_name("机房-B28")
    # jjj = huabei_zabbix_api.get_trigger_group_name("机房-B28")
    # kkk = huabei_zabbix_api.get_graph_host_name("2B-B28-F1-H3C-5800-CNC-2698")
    # ll = huabei_zabbix_api.get_item_host_name("2B-B28-F1-H3C-5800-CNC-2698")
    # mm = huabei_zabbix_api.get_item_graph_name("2B-B28-F1-H3C-5800-CNC-2698", "Interface Ten-GigabitEthernet1/1/4: Network traffic")
    # nn = huabei_zabbix_api.get_trigger_host_name("2B-B28-F1-H3C-5800-CNC-2698")
    # oo = huabei_zabbix_api.get_trigger_item_name("2B-B28-F1-H3C-5800-CNC-2698", "ICMP response time")
    # pp = huabei_zabbix_api.get_history_item_name("2B-B28-F1-H3C-5800-CNC-2698", "Interface Ten-GigabitEthernet1/1/4: Bits received", "2020-09-09 08:00:00", "2020-09-09 09:00:00")
    # qq = huabei_zabbix_api.get_history_itemID(89557, "2020-08-01 00:00:00", "2020-08-31 23:59:00")
    rr = huabei_zabbix_api.get_map("网络拓扑图demo1")
    # print(ccc, ddd, dd)
    # print(len(eee), eee)
    # print(len(fff), fff)
    # print(len(ggg), ggg)
    # print(len(hhh), hhh)
    # print(len(iii), iii)
    # print(len(jjj), jjj)
    # print(len(kkk), kkk)
    # print(len(ll), ll)
    # print(len(mm), mm)
    # print(len(nn), nn)
    # print(len(oo), oo)
    # print(len(pp), pp)
    # for i in pp:
    #     value = i['value']
    #     last_time = timestamp_to_time(i['clock'])
    #     print(value, last_time)
    # print(len(qq), qq)
    # for i in qq:
    #     value = i['value']
    #     last_time = timestamp_to_time(i['clock'])
    #     print(value, last_time)
    print(len(rr), rr)