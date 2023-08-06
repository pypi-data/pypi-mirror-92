本模块是pyzabbix模块的升级版，结合官方zabbix api实现了更加复杂的功能，但是调用起来相当方便：

1. *根据主机名获取对应的hostID*，对应函数get_hostID

2. *根据模板名获取对应的templateID*，**get_templateID**

3. *根据群组名获取对应的groupID*，get_groupID

4. *根据群组名获取所有主机详情，hostID，主机可见名称，主机名，interfaceid，ip地址*，**get_host_group_name**

5. *根据模板名获取所有主机详情，hostID，主机可见名称，主机名，interfaceid，ip地址，**get_host_template_name**

6. *根据群组名获取所有图形详情，graphid，图名称*，**get_graph_group_name**

7. *根据主机名获取所有主机详情，graphid，图名称*，**get_graph_host_name**

8. *根据群组名获取所有监控项详情，itemid，监控项名称*，**get_item_group_name**

9. *根据主机名获取所有监控项详情，itemid，监控项名称*，**get_item_host_name**

10. *根据图形名获取所有监控项详情，itemid，监控项名称*，**get_item_graph_name**

11. *根据群组名获取所有触发器详情，triggerid，触发器描述*，**get_trigger_group_name**

12. *根据主机名获取所有触发器详情，triggerid，触发器描述*，**get_trigger_host_name**

13. *根据监控项名获取所有触发器详情，triggerid，触发器描述*，**get_trigger_item_name**

14. *根据主机名和接口名称获取对应的接口键值详情*，**get_if_item_key**

15. *增加组信息，如果存在，则返回相应信息*，**add_group**

16. *灵活根据群组和模板创建非代理主机*，**create_host_without_proxy**

17. *根据主机名删除主机*，**delete_host**

18. *根据主机名和监控项名获取历史数据。data_type可能的值：0-数字浮点；1-字符；2-日志；3-无符号数字；4-文本。默认值：3*，**get_history_item_name**

19. *根据itemID获取历史数据。data_type可能的值：0-数字浮点；1-字符；2-日志；3-无符号数字；4-文本。默认值：3*，**get_history_itemID**

20. *根据拓扑图名字获取对应数据*，**get_map**

21. *根据监控项ID获取相应信息*，**get_item_value**

22. *根据设备主机名和监控项ID获取相应值*，**get_item_value_host**

    

以上功能使用首先实例化类，然后调用各个函数调用，也可以根据 需求查看源码进行二次开发使用：

```
from pyzabbixAll import zabbix_api

if __name__=="__main__":
    # 测试zabbix操作
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
```

以上是部分测试代码，大家可以放心使用