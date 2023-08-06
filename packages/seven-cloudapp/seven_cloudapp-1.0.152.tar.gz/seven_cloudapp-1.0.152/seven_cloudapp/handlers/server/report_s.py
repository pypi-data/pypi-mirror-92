# -*- coding: utf-8 -*-
"""
:Author: CaiYouBin
:Date: 2020-06-05 17:27:26
:LastEditTime: 2021-01-18 18:42:35
:LastEditors: HuangJingCan
:description: 
"""
from copy import deepcopy
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.db_models.behavior.behavior_log_model import *
from seven_cloudapp.models.db_models.behavior.behavior_orm_model import *
from seven_cloudapp.models.db_models.behavior.behavior_report_model import *
from seven_cloudapp.models.db_models.machine.machine_info_model import *


class ReportTotalHandler(SevenBaseHandler):
    """
    :description: 各类总数统计
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        :description: 各类总数统计
        :param act_id：活动id
        :return dict
        :last_editors: LaiKaiXiang
        """
        act_id = int(self.get_param("act_id", 0))

        behavior_report_model = BehaviorReportModel()

        sum_visit = behavior_report_model.get_dict("act_id=%s and key_name=%s", field="sum(key_value) as key_value", params=[act_id, "VisitManCountEveryDayIncrease"])
        sum_lottery = behavior_report_model.get_dict("act_id=%s and key_name=%s", field="sum(key_value) as key_value", params=[act_id, "LotteryAddUserCount"])
        sum_reward = behavior_report_model.get_dict("act_id=%s and key_name=%s", field="sum(key_value) as key_value", params=[act_id, "TotalRewardCount"])

        data_list = []
        data = {}
        data["title"] = "总访问人数"
        data["value"] = int(sum_visit["key_value"]) if sum_visit["key_value"] else 0
        data_list.append(data)
        data = {}
        data["title"] = "总抽奖人数"
        data["value"] = int(sum_lottery["key_value"]) if sum_lottery["key_value"] else 0
        data_list.append(data)
        data = {}
        data["title"] = "奖励发放总量"
        data["value"] = int(sum_reward["key_value"]) if sum_reward["key_value"] else 0
        data_list.append(data)

        self.reponse_json_success(data_list)


class ReportInfoHandler(SevenBaseHandler):
    """
    :description: 报表信息
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        :description: 报表信息
        :param act_id：活动id
        :param start_date：开始时间
        :param end_date：结束时间
        :return: 列表
        :last_editors: CaiYouBin
        """
        act_id = int(self.get_param("act_id", 0))
        start_date = self.get_param("start_date")
        end_date = self.get_param("end_date")

        condition = ""
        params = []

        condition += "act_id=%s"
        params.append(act_id)

        if start_date != "":
            condition += " AND create_date>=%s"
            params.append(start_date)
        if end_date != "":
            condition += " AND create_date<=%s"
            params.append(end_date)

        behavior_orm_model = BehaviorOrmModel()
        behavior_report_model = BehaviorReportModel()
        behavior_orm_list = behavior_orm_model.get_list("is_common=1 OR act_id=%s", order_by="id asc", params=act_id)

        behavior_report_list = behavior_report_model.get_dict_list(condition, group_by="key_name", field="key_name,SUM(key_value) AS key_value", params=params)

        #公共映射组（未去重）
        common_groups_1 = [orm.group_name for orm in behavior_orm_list if orm.is_common == 1]
        #公共映射组(去重)
        common_groups = list(set(common_groups_1))
        common_groups.sort(key=common_groups_1.index)

        big_group_list = []
        common_group_data_list = []
        index = 0
        big_group1 = {}
        big_group1["group_name"] = "访问数据"
        big_group1["group_data_list"] = []
        big_group2 = {}
        big_group2["group_name"] = "全部开盒"
        big_group2["group_data_list"] = []

        for common_group in common_groups:
            group_data = {}
            group_data["group_name"] = common_group
            data_list = []
            for behavior_orm in behavior_orm_list:
                if behavior_orm.group_name == common_group:
                    data = {}
                    data["title"] = behavior_orm.key_value
                    data["value"] = 0
                    for behavior_report in behavior_report_list:
                        if behavior_report["key_name"] == behavior_orm.key_name:
                            if behavior_orm.value_type == 2:
                                data["value"] = behavior_report["key_value"]
                            else:
                                data["value"] = int(behavior_report["key_value"])

                    data_list.append(data)
            group_data["data_list"] = data_list

            if index == 0:
                big_group1["group_data_list"].append(group_data)
            else:
                big_group2["group_data_list"].append(group_data)
            index += 1

        big_group_list.append(big_group1)
        big_group_list.append(big_group2)

        machine_info_model = MachineInfoModel()
        machine_info_list = machine_info_model.get_list("act_id=%s AND is_release=1", params=act_id)

        for machine_info in machine_info_list:
            group_data = {}
            group_data["group_name"] = machine_info.machine_name
            data_list = []
            for behavior_orm in behavior_orm_list:
                if behavior_orm.key_name == "openCount_" + str(machine_info.id) or behavior_orm.key_name == "openUserCount_" + str(machine_info.id):
                    data = {}
                    data["title"] = behavior_orm.key_value
                    data["value"] = 0
                    for behavior_report in behavior_report_list:
                        if behavior_report["key_name"] == behavior_orm.key_name:
                            if behavior_orm.value_type == 2:
                                data["value"] = behavior_report["key_value"]
                            else:
                                data["value"] = int(behavior_report["key_value"])
                    data_list.append(data)
            group_data["data_list"] = data_list
            big_group_list.append(group_data)

        self.reponse_json_success(big_group_list)


class ReportInfoListHandler(SevenBaseHandler):
    """
    :description: 数据列表
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        :description: 报表信息
        :param act_id：活动id
        :param start_date：开始时间
        :param end_date：结束时间
        :return: 列表
        :last_editors: CaiYouBin
        """
        act_id = int(self.get_param("act_id", 0))
        start_date = self.get_param("start_date")
        end_date = self.get_param("end_date")

        date_list = self.get_date_list(start_date, end_date)

        condition = ""
        params = []

        condition += "act_id=%s"
        params.append(act_id)

        if start_date != "":
            condition += " AND create_date>=%s"
            params.append(start_date)
        if end_date != "":
            condition += " AND create_date<=%s"
            params.append(end_date)

        behavior_orm_model = BehaviorOrmModel()
        behavior_report_model = BehaviorReportModel()
        behavior_orm_list = behavior_orm_model.get_list("is_common=1 OR act_id=%s", order_by="id asc", params=act_id)

        behavior_report_list = behavior_report_model.get_dict_list(condition, field="key_name,key_value,DATE_FORMAT(create_date,'%%Y-%%m-%%d') AS create_date", params=params)

        #公共映射组（未去重）
        common_groups_1 = [orm.group_name for orm in behavior_orm_list if orm.is_common == 1]
        #公共映射组(去重)
        common_groups = list(set(common_groups_1))
        common_groups.sort(key=common_groups_1.index)

        common_group_data_list = []

        for common_group in common_groups:
            group_data = {}
            group_data["group_name"] = common_group
            data_list = []
            for behavior_orm in behavior_orm_list:
                if behavior_orm.group_name == common_group:
                    data = {}
                    data["title"] = behavior_orm.key_value
                    data["value"] = []

                    for date_day in date_list:
                        behavior_date_report = {}
                        for behavior_report in behavior_report_list:
                            if behavior_report["key_name"] == behavior_orm.key_name and behavior_report["create_date"] == date_day:
                                if behavior_orm.value_type != 2:
                                    behavior_report["key_value"] = int(behavior_report["key_value"])
                                behavior_date_report = {"title": behavior_orm.key_value, "date": date_day, "value": behavior_report["key_value"]}
                                break
                        if not behavior_date_report:
                            behavior_date_report = {"title": behavior_orm.key_value, "date": date_day, "value": 0}
                        data["value"].append(behavior_date_report)

                    data_list.append(data)
            group_data["data_list"] = data_list
            common_group_data_list.append(group_data)

        self.reponse_json_success(common_group_data_list)


class ReportInfo2Handler(SevenBaseHandler):
    """
    :description: 报表信息
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        :description: 报表信息
        :param act_id：活动id
        :param start_date：开始时间
        :param end_date：结束时间
        :return: 列表
        :last_editors: CaiYouBin
        """
        act_id = int(self.get_param("act_id", 0))
        start_date = self.get_param("start_date")
        end_date = self.get_param("end_date")

        condition = ""
        params = []

        condition += "act_id=%s"
        params.append(act_id)

        if start_date != "":
            condition += " AND create_date>=%s"
            params.append(start_date)
        if end_date != "":
            condition += " AND create_date<=%s"
            params.append(end_date)

        behavior_orm_model = BehaviorOrmModel()
        behavior_report_model = BehaviorReportModel()
        behavior_orm_list = behavior_orm_model.get_list("is_common=1 OR act_id=%s", order_by="id asc", params=act_id)

        behavior_report_list = behavior_report_model.get_dict_list(condition, group_by="key_name", field="key_name,SUM(key_value) AS key_value", params=params)

        #公共映射组（未去重）
        common_groups_1 = [orm.group_name for orm in behavior_orm_list if orm.is_common == 1]
        #公共映射组(去重)
        common_groups = list(set(common_groups_1))
        common_groups.sort(key=common_groups_1.index)

        big_group_list = []
        common_group_data_list = []

        big_group = {}
        big_group["group_name"] = "全部开盒"
        big_group["group_data_list"] = []

        for common_group in common_groups:
            group_data = {}
            group_data["group_name"] = common_group
            data_list = []
            for behavior_orm in behavior_orm_list:
                if behavior_orm.group_name == common_group:
                    data = {}
                    data["title"] = behavior_orm.key_value
                    data["value"] = 0
                    for behavior_report in behavior_report_list:
                        if behavior_report["key_name"] == behavior_orm.key_name:
                            if behavior_orm.value_type == 2:
                                data["value"] = behavior_report["key_value"]
                            else:
                                data["value"] = int(behavior_report["key_value"])

                    data_list.append(data)
            group_data["data_list"] = data_list

            big_group["group_data_list"].append(group_data)

        big_group_list.append(big_group)

        machine_info_model = MachineInfoModel()
        machine_info_list = machine_info_model.get_list("act_id=%s AND is_release=1", params=act_id)

        for machine_info in machine_info_list:
            group_data = {}
            group_data["group_name"] = machine_info.machine_name
            group_data["group_data_list"] = deepcopy(big_group["group_data_list"])
            data_list = []
            for behavior_orm in behavior_orm_list:
                if behavior_orm.key_name == "openCount_" + str(machine_info.id) or behavior_orm.key_name == "openUserCount_" + str(machine_info.id):
                    data = {}
                    if "openCount_" in behavior_orm.key_name:
                        data["title"] = deepcopy("开盒次数")
                    if "openUserCount_" in behavior_orm.key_name:
                        data["title"] = deepcopy("开盒人数")

                    data["value"] = 0
                    for behavior_report in behavior_report_list:
                        if behavior_report["key_name"] == behavior_orm.key_name:
                            if behavior_orm.value_type == 2:
                                data["value"] = behavior_report["key_value"]
                            else:
                                data["value"] = int(behavior_report["key_value"])
                    data_list.append(data)

            group_data["group_data_list"][2]["data_list"] = data_list
            big_group_list.append(group_data)

        self.reponse_json_success(big_group_list)