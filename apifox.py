# -*- coding: utf-8 -*-
import requests
import json
import urllib3
import sys
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class InformRobot:
    def __init__(self):
        self.sess = requests.session()
        self.test_case_passing_rate = ""
        self.test_case_fail_rate = ""
        self.avg_api_response_rate = ""
        self.test_case_untested_rate = ""
        self.test_case_quantity_rate = ""

    def markdown_robot(
            self, webhook_url, report_url, principal, job_name, test_environment, STATUS
    ):
        """ 实现企业微信通知:企业微信token+报告地址+负责人名称+项目名称+环境名称+返回值"""
        data = {
            "msgtype": "markdown",  # 消息类型，此时固定为markdown
            "markdown": {
                # "content": f"### 提醒! <font color=\"info\"> {job_name} </font> 接口自动化测试反馈  \n "
                "content": "### 提醒! <font color=\"info\"> {0} </font> 接口自动化测试反馈  \n".format(job_name) +
                           f">环境：{test_environment} \n" +
                           f">测试用例结果：<font color=\"info\"> {STATUS} </font> \n" +
                           f">测试用例总数：<font color=\"info\"> {self.test_case_quantity_rate} </font> \n" +
                           f">平均接口请求耗时：<font color=\"info\"> {self.avg_api_response_rate} </font> \n" +
                           f">测试用例通过率：<font color=\"info\"> {self.test_case_passing_rate} </font> \n" +
                           f">测试用例失败率：<font color=\"#FF0000\"> {self.test_case_fail_rate} </font> \n" +
                           f">测试用例未测率：<font color=\"#FFCC33\"> {self.test_case_untested_rate} </font> \n" +
                           f">测试报告链接：[点击查看报告详情]({report_url}) \n" +
                           f">测试负责人：{principal}"
            }
        }
        re_post = self.sess.post(webhook_url, data=json.dumps(data), verify=False)
        print(re_post.content, data)
        return re_post

    def result_pass_rate(self, html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            report = f.read()

        pass_rate = re.search('<div class="col-md-4 text-label">通过率</div>\n\ +<div class="col-md-8">(.*?)</div>',
                              report)

        fail_rate = re.search('<div class="col-md-4 text-label">失败率</div>\n\ +<div class="col-md-8">(.*?)</div>',
                              report)
        avg_api_response_time = re.search(
            '<div class="col-md-4 text-label">平均接口请求耗时</div>\n\ +<div class="col-md-8">(.*?)</div>',
            report)

        case_untested_rate = re.search(
            '<div class="col-md-4 text-label">未测率</div>\n\ +<div class="col-md-8">(.*?)</div>', report)
        case_quantity_rate = re.search(
            '<div class="col-md-4 text-label">循环数</div>\n\ +<div class="col-md-4">(.*?)</div>', report)

        self.test_case_fail_rate = fail_rate.group(1)  # 用例失败率
        self.test_case_passing_rate = pass_rate.group(1)  # 用例通过率
        self.avg_api_response_rate = avg_api_response_time.group(1)  # 平均接口请求耗时
        self.test_case_untested_rate = case_untested_rate.group(1)  # 用例未测率
        self.test_case_quantity_rate = case_quantity_rate.group(1)  # 用例数量


if __name__ == '__main__':
    webhook_url = sys.argv[0]
    report_url = sys.argv[0]
    principal = sys.argv[0]
    job_name = sys.argv[0]
    test_environment = sys.argv[0]
    STATUS = sys.argv[0]
    build_number = sys.argv[0]

    path = "/Users/wangyuting/apifox-reports/apifox-report-2024-01-18-19-12-50-515-0.html".format(job_name, build_number)

    info_robot = InformRobot()
    info_robot.result_pass_rate(path)
    info_robot_res = info_robot.markdown_robot("https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=093dd020-6090-4358-ba1c-5f1025f416c1", "/Users/wangyuting/apifox-reports", "王玉婷", "SaaS", "测试环境", "Pass")
    print(info_robot_res)

    info_robot.sess.close()
