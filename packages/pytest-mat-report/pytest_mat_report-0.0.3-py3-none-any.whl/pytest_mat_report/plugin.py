import pytest
import requests
import jsonpath
import json
import os
import sys
from _pytest.reports import TestReport

from py.io import TerminalWriter

def pytest_addoption(parser):
    parser.addoption(
        "--mat_report",
        action="store",
        default="on",
        help="'Default 'off' for change, option: on or off"
    )

def pytest_runtest_makereport(item, call):
    out = yield
    w = TerminalWriter()
    print("asdasd")
    print(item)
    print(call)
    print(out.get_result())

    report = out.get_result()
    if report.when == "call" and report.outcome != 'passed':
        nodeid = item.nodeid
        num = int(item.name.replace(item.originalname,'').replace('params','').strip('[').strip(']'))
        used_fixtures = sorted(getattr(item, "fixturenames", []))
        f = {}
        if used_fixtures:
            for i in used_fixtures:
                f[i] = item.funcargs[i]
        print('\n')
        length = w.fullwidth
        name = item.nodeid.center(length,"_")
        color = 'red'
        w.write(name, **{color: True})
        print(('\n\n运行结果: %s' % report.outcome))
        print('\n ---  \033[32mfixtrue数据为\033[0m：' + str(f))
        case = item.module.report[item.originalname][num]
        print('\n ---  \033[33m接口请求数据为\033[0m：' + str(case['request']))
        print('\n ---  \033[36m接口返回数据为\033[0m：' + str(case['respone']))
        if 'assert' in report.longreprtext:
            index = report.longreprtext.index('assert')
            print('\n ---  \033[31m断言结果为\033[0m：\n     ' + str(report.longreprtext[index:]))
            print('\n')

