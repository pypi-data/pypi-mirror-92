#Author:Hanson

import time
from pyzabbix import ZabbixAPI


def time_to_timestamp(time1): #对应time_data1
    #传入可读正常日期时间,比如'2019-08-01 00:00:00'，类型为str
    data_str = time.strptime(time1, "%Y-%m-%d %H:%M:%S")  #定义时间格式
    time_int = int(time.mktime(data_str))  #正常时间转换为时间戳
    return time_int             #返回传入时间的时间戳，类型为int

def timestamp_to_time(timestamp1): #对应time_data2
    #传入时间的时间戳，比如'1583909443',类型为int
    data_str = time.localtime(int(timestamp1))  #时间戳转换为正常时间
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", data_str)  #定义时间格式
    return time_str  #返回可读正常日期，类型为str


class zabbix_api(object):
    #初始化参数
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
    #进行zabbix登录认证，返回zapi模块，进行后续函数功能调用
    def authenticate(self):
        zapi = ZabbixAPI(self.url)
        zapi.login(self.username, self.password)
        return zapi

    def get_hostID(self, host_name):
        # 根据主机名获取对应的hostID
        host_list = self.authenticate().host.get(output=["hostid", "name", "host"],
                                                 filter={'name': host_name}
                                          )
        if host_list != []:
            hostID = host_list[0]['hostid']
            return hostID
        else:
            return "主机名称(" + host_name + ")错误，找不到对应ID"

    def get_templateID(self, template_name):
        # 根据模板名获取对应的templateID
        template_list = self.authenticate().template.get(output=["host", "name", "templateid"],
                                                         filter={'name': template_name}
                                          )
        if template_list != []:
            templateID = template_list[0]['templateid']
            return templateID
        else:
            return "模板名称(" + template_name + ")错误，找不到对应ID"

    def get_groupID(self, group_name):
        # 根据群组名获取对应的groupID
        group_list = self.authenticate().hostgroup.get(output=["host", "name", "templateid"],
                                                         filter={'name': group_name}
                                                       )
        if group_list != []:
            groupID = group_list[0]['groupid']
            return groupID
        else:
            return "群组名称(" + group_name + ")错误，找不到对应ID"


    def get_host_group_name(self, group_name):
        # 根据群组名获取所有主机详情，hostID，主机可见名称，主机名，interfaceid，ip地址，另外可以根据需求自定义功能函数
        groupID = self.get_groupID(group_name)
        host_list = self.authenticate().host.get(output=["hostid", "name", "host"],
                                  selectInterfaces=["interfaceid", "ip"],
                                  groupids=groupID
                                  )
        if host_list != []:
            return host_list
        else:
            return "群组名称(" + group_name + ")错误，找不到主机列表"

    def get_host_template_name(self, template_name):
        # 根据模板名获取所有主机详情，hostID，主机可见名称，主机名，interfaceid，ip地址，另外可以根据需求自定义功能函数
        templateID = self.get_templateID(template_name)
        host_list = self.authenticate().host.get(output=["hostid", "name", "host"],
                                  selectInterfaces=["interfaceid", "ip"],
                                  templateids=templateID
                                  )

        if host_list != []:
            return host_list
        else:
            return "模板名称(" + template_name + ")错误，找不到主机列表"



    def get_graph_group_name(self, group_name):
        # 根据群组名获取所有图形详情，graphid，图名称，另外可以根据需求自定义功能函数
        groupID = self.get_groupID(group_name)
        graph_list = self.authenticate().graph.get(output=["graphid", "name"],
                                  #selectInterfaces=["interfaceid","ip"],
                                  groupids=groupID
                                  )

        if graph_list != []:
            return graph_list
        else:
            return "群组名称(" + group_name + ")错误，找不到图列表"

    def get_graph_host_name(self, host_name):
        # 根据主机名获取所有主机详情，graphid，图名称，另外可以根据需求自定义功能函数
        hostID = self.get_hostID(host_name)
        graph_list = self.authenticate().graph.get(output=["graphid", "name"],
                                  #selectInterfaces=["interfaceid","ip"],
                                  hostids=hostID
                                  )

        if graph_list != []:
            return graph_list
        else:
            return "主机名称(" + host_name + ")错误，找不到图列表"


    def get_item_group_name(self, group_name):
        # 根据群组名获取所有监控项详情，itemid，监控项名称，另外可以根据需求自定义功能函数
        groupID = self.get_groupID(group_name)
        item_list = self.authenticate().item.get(output=["itemid", "name"],
                                  #selectInterfaces=["interfaceid","ip"],
                                  groupids=groupID
                                  )

        if item_list != []:
            return item_list
        else:
            return "群组名称(" + group_name + ")错误，找不到监控项列表"

    def get_item_host_name(self, host_name):
        # 根据主机名获取所有监控项详情，itemid，监控项名称，另外可以根据需求自定义功能函数
        hostID = self.get_hostID(host_name)
        item_list = self.authenticate().item.get(output=["itemid", "name"],
                                  #selectInterfaces=["interfaceid","ip"],
                                  hostids=hostID
                                  )

        if item_list != []:
            return item_list
        else:
            return "主机名称(" + host_name + ")错误，找不到监控项列表"

    def get_item_graph_name(self, host_name, graph_name):
        # 根据图形名获取所有监控项详情，itemid，监控项名称，另外可以根据需求自定义功能函数
        hostID = self.get_hostID(host_name)
        graph_list = self.authenticate().graph.get(output=["graphid", "name"],
                                                   filter={'name': graph_name},
                                                   hostids=hostID
                                                   )
        if graph_list != []:
            graphID = graph_list[0]["graphid"]
            print("图形名称(" + graph_name + ")的ID为：" + graphID)
        else:
            return "主机名称(" + host_name + ")或者图形名称(" + graph_name + ")错误，找不到图形列表"

        item_list = self.authenticate().item.get(output=["itemid", "name"],
                                                 graphids=graphID
                                                 )
        if item_list != []:
            return item_list
        else:
            return "图形ID(" + graphID + ")错误，找不到监控项列表"


    def get_trigger_group_name(self, group_name):
        # 根据群组名获取所有触发器详情，triggerid，触发器描述，另外可以根据需求自定义功能函数
        groupID = self.get_groupID(group_name)
        trigger_list = self.authenticate().trigger.get(output=["triggerid", "description", "expression"],
                                  #selectInterfaces=["interfaceid","ip"],
                                  groupids=groupID
                                  )

        if trigger_list != []:
            return trigger_list
        else:
            return "群组名称(" + group_name + ")错误，找不到触发器列表"

    def get_trigger_host_name(self, host_name):
        # 根据主机名获取所有触发器详情，triggerid，触发器描述，另外可以根据需求自定义功能函数
        hostID = self.get_hostID(host_name)
        trigger_list = self.authenticate().trigger.get(output=["triggerid", "description", "expression"],
                                  #selectInterfaces=["interfaceid","ip"],
                                  hostids=hostID
                                  )

        if trigger_list != []:
            return trigger_list
        else:
            return "主机名称(" + host_name + ")错误，找不到监控项列表"

    def get_trigger_item_name(self, host_name, item_name):
        # 根据监控项名获取所有触发器详情，triggerid，触发器描述，另外可以根据需求自定义功能函数
        hostID = self.get_hostID(host_name)
        item_list = self.authenticate().item.get(output=["itemid", "name"],
                                                 filter={'name': item_name},
                                                 hostids=hostID
                                                 )
        if item_list != []:
            itemID = item_list[0]["itemid"]
            print("监控项(" + item_name + ")的ID为：" + itemID)
        else:
            return "主机名称(" + host_name + ")或者监控项名称(" + item_name + ")错误，找不到图形列表"

        trigger_list = self.authenticate().trigger.get(output=["triggerid", "description", "expression"],
                                                       itemids=itemID
                                                       )
        if trigger_list != []:
            return trigger_list
        else:
            return "监控项ID(" + itemID + ")错误，找不到监控项列表"


    def get_if_item_key(self, host_name, if_name):
        # 根据主机名和接口名称获取对应的接口键值详情，另外可以根据需求自定义功能函数
        if_tmp_list = []
        if_name_in = "Interface " + if_name + ": Bits received"
        if_name_out = "Interface " + if_name + ": Bits sent"
        if_name_in_item_list = self.authenticate().item.get(
                                            output=['itemid', 'name', 'key_', 'lastvalue', 'status_codes'],
                                            #output="extend",
                                            host=host_name,
                                            filter={'name': if_name_in}
                               )
        if_name_out_item_list = self.authenticate().item.get(
                                            output=['itemid', 'name', 'key_', 'lastvalue', 'status_codes'],
                                            #output="extend",
                                            host=host_name,
                                            filter={'name': if_name_out}
                                )
        if if_name_in_item_list == [] or if_name_out_item_list == []:
            print(str(if_name) + "端口不存在")
        #print(if_name_in_item_list,if_name_out_item_list)
        status_in = if_name_in_item_list[0]['status_codes']
        status_out = if_name_out_item_list[0]['status_codes']
        if status_in == "200" and status_out == "200":
            key_in = if_name_in_item_list[0]['key_']
            key_out = if_name_out_item_list[0]['key_']
            if_tmp_list.append(key_in)
            if_tmp_list.append(key_out)
        return if_tmp_list

    def add_group(self, tag, name):
        # 增加组信息，如果存在，则返回相应信息
        all_name = str(tag) + "-" + str(name)
        group_list1 = self.authenticate().hostgroup.get(output="extend",
                                         )
        print(group_list1)
        for i in group_list1:
            graph_name = i['name']
            if all_name == graph_name:
                print("已存在分组:" + str(all_name))
                return i['groupid']
        else:
            group_list = self.authenticate().hostgroup.create(name=all_name,
                                               )
            print("已创建分组:" + str(all_name))
            return group_list['groupids'][0]

    def create_host_without_proxy(self, host_name, name, ip, description, group_id, template_id):
        # 灵活根据群组和模板创建非代理主机
        if group_id == "none":
            host_create = self.authenticate().host.create(
                {
                    "host": host_name,  # 主机名
                    "name": name,  # 可见名称
                    "templates": template_id,
                    "description": description,
                    "interfaces": [
                        {
                            "type": 1,  # 接口类型，从1到4分别是 Zabbix_agent代理程序的接口，SNMP接口，JMX接口，IPMI接口
                            "main": 1,
                            "useip": 1,
                            "ip": ip,  # 主机IP地址
                            "dns": "",
                            "port": "10050"  # 接口类型对应端口号
                        }
                    ],
                    "status": 0
                }
            )

        elif template_id == "none":
            host_create = self.authenticate().host.create(
                {
                    "host": host_name,  # 主机名
                    "name": name,  # 可见名称
                    "groups": [{"groupid": group_id}],
                    "description": description,
                    "interfaces": [
                        {
                            "type": 1,  # 接口类型，从1到4分别是 Zabbix_agent代理程序的接口，SNMP接口，JMX接口，IPMI接口
                            "main": 1,
                            "useip": 1,
                            "ip": ip,  # 主机IP地址
                            "dns": "",
                            "port": "10050"  # 接口类型对应端口号
                        }
                    ],
                    "status": 0
                }
            )

        elif group_id == "none" and template_id == "none":
            host_create = self.authenticate().host.create(
                {
                    "host": host_name,  # 主机名
                    "name": name,  # 可见名称
                    "description": description,
                    "interfaces": [
                        {
                            "type": 1,  # 接口类型，从1到4分别是 Zabbix_agent代理程序的接口，SNMP接口，JMX接口，IPMI接口
                            "main": 1,
                            "useip": 1,
                            "ip": ip,  # 主机IP地址
                            "dns": "",
                            "port": "10050"  # 接口类型对应端口号
                        }
                    ],
                    "status": 0
                }
            )

        else:
            host_create = self.authenticate().host.create(
                {
                    "host": host_name,  # 主机名
                    "name": name,  # 可见名称
                    "groups": [{"groupid": group_id}],
                    "templates": template_id,
                    "description": description,
                    "interfaces": [
                        {
                            "type": 1,  # 接口类型，从1到4分别是 Zabbix_agent代理程序的接口，SNMP接口，JMX接口，IPMI接口
                            "main": 1,
                            "useip": 1,
                            "ip": ip,  # 主机IP地址
                            "dns": "",
                            "port": "10050"  # 接口类型对应端口号
                        }
                    ],
                    "status": 0
                }
            )
        return host_create

    def delete_host(self, host_name):
        # 根据主机名删除主机
        hostID = self.get_hostID(host_name)
        host_list = self.authenticate().host.delete(hostID)
        return host_list

    def get_history_item_name(self, host_name, item_name, time_from_1, time_till_1, data_type=3):
        # 根据主机名和监控项名获取历史数据。data_type可能的值：0-数字浮点；1-字符；2-日志；3-无符号数字；4-文本。默认值：3
        hostID = self.get_hostID(host_name)
        item_list = self.authenticate().item.get(output=["itemid", "name"],
                                                 filter={'name': item_name},
                                                 hostids=hostID
                                                 )
        if item_list != []:
            itemID = item_list[0]["itemid"]
            print("监控项(" + item_name + ")的ID为：" + itemID)
        else:
            return "主机名称(" + host_name + ")或者监控项名称(" + item_name + ")错误，找不到监控项列表"

        history_list = self.authenticate().history.get(#output="extend",
                                                       output=["itemid", "value", "clock"],
                                                       itemids=itemID,
                                                       time_from=time_to_timestamp(time_from_1),
                                                       time_till=time_to_timestamp(time_till_1),
                                                       history=data_type, #可能的值：0-数字浮点；1-字符；2-日志；3-无符号数字；4-文本。默认值：3
                                                       sortfield="clock", #分类标准字段
                                                       sortorder="ASC", #升序ASC，降序DESC
                                                       #limit=10,
                                                       )
        if history_list != []:
            return history_list
        else:
            #print(history_list)
            return "监控项ID(" + itemID + ")错误，找不到历史数据列表"

    def get_history_itemID(self, itemID, time_from_1, time_till_1, data_type=3):
        # 根据itemID获取历史数据。data_type可能的值：0-数字浮点；1-字符；2-日志；3-无符号数字；4-文本。默认值：3
        history_list = self.authenticate().history.get(#output="extend",
                                                       output=["value", "clock"],
                                                       itemids=itemID,
                                                       time_from=time_to_timestamp(time_from_1),
                                                       time_till=time_to_timestamp(time_till_1),
                                                       history=data_type, #可能的值：0-数字浮点；1-字符；2-日志；3-无符号数字；4-文本。默认值：3
                                                       sortfield="clock", #分类标准字段
                                                       sortorder="ASC", #升序ASC，降序DESC
                                                       #limit=10,
                                                       )
        if history_list != []:
            return history_list
        else:
            #print(history_list)
            return "监控项ID(" + itemID + ")错误，找不到历史数据列表"

    def get_map(self, map_name):
        # 根据拓扑图名字获取对应数据
        map_list = self.authenticate().map.get(output="extend",
                                               selectSelements="extend",
                                               selectLinks="extend",
                                               selectUsers="extend",
                                               selectUserGroups="extend",
                                               selectShapes="extend",
                                               selectLines="extend",
                                               #sysmapids="3"
                                               filter={"label": map_name}
                                               )
        if map_list != []:
            return map_list
        else:
            print(map_list)
            #return "监控项ID(" + itemID + ")错误，找不到历史数据列表"


    def get_item_value(self, item_id):
        # 根据监控项ID获取相应信息，另外可以根据需求自定义功能函数
        item_list = self.authenticate().item.get(output=["name",
                                                         "snmp_oid",
                                                         "lastvalue",
                                                         "units",
                                                         "lastclock",
                                                         "delay",
                                                         "value_type",
                                                         "status",  # 监控项网络设备状态
                                                         "state"  # 监控项状态，启用或者禁用
                                                         ],
                                                 itemids=item_id
                                                 )

        if item_list != []:
            return item_list
        else:
            return "监控项ID(" + item_id + ")错误，获取不到监控项信息"

    def get_item_value_host(self, host, item_name):
        # 根据设备主机名和监控项ID获取相应值，另外可以根据需求自定义功能函数
        item_list = self.authenticate().item.get(output=["name",
                                                         "snmp_oid",
                                                         "lastvalue",
                                                         "units",
                                                         "lastclock",
                                                         "delay",
                                                         "value_type",
                                                         "status",  # 监控项网络设备状态
                                                         "state"  # 监控项状态，启用或者禁用
                                                         ],
                                                 host=host,
                                                 filter={"name": item_name}
                                                 )

        if item_list != []:
            return item_list
        else:
            return "设备名称(" + host + ")或者监控项名称(" + item_name + ")错误，获取不到监控项信息"