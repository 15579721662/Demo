# -*- coding: utf-8 -*-
import pytest
import os
import io
from io import StringIO
import logging
import logging.config
import pytest_html
from pytest_html import extras
from datetime import datetime
from playwright.sync_api import sync_playwright

# 日志配置
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailedFormatter': {
            'format': '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'consoleHandler': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'detailedFormatter',
            'stream': 'ext://sys.stdout'
        },
        'fileHandler': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'detailedFormatter',
            'filename': 'test.log',
            'mode': 'a',
            'encoding': 'utf-8'
        }
    },
    'loggers': {
        'root': {
            'level': 'INFO',
            'handlers': ['consoleHandler', 'fileHandler'],
            'propagate': False
        }
    }
}

# 配置日志
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('root')  # 明确指定使用 'root' 日志记录器

@pytest.fixture(scope="function", autouse=True)
def capture_logs():
    # 获取日志记录器
    global logger
    logger = logging.getLogger('root')  # 确保使用的是 'root' 日志记录器
    original_stream = logger.handlers[1].stream  # 保存原始流
    logger.handlers[1].stream = io.StringIO()  # 替换为 StringIO

    yield

    # 恢复原始流
    logger.handlers[1].stream = original_stream


# 创建 reports 文件夹
def create_reports_folder():
    reports_folder = "reports"
    if not os.path.exists(reports_folder):
        os.makedirs(reports_folder)
    return reports_folder


# 配置 pytest-html 插件
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config):
    # 创建 reports 文件夹
    reports_folder = create_reports_folder()

    # 设置报告的路径和名称
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"test_report_{timestamp}.html"
    report_path = os.path.join(reports_folder, report_filename)

    # 配置 pytest-html 插件
    config.option.htmlpath = report_path
    config.option.self_contained_html = True  # 生成自包含的 HTML 报告


# 捕获日志并输出到 pytest-html 报告中
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    if pytest_html:
        extra = getattr(item, 'extra', [])
        if call.when == "call":
            # 获取日志内容
            log_file_path = "test.log"  # 指定日志文件路径
            if os.path.exists(log_file_path):
                with open(log_file_path, "r", encoding="utf-8") as log_file:
                    log_content = log_file.read()
                # 添加日志到报告中
                extra.append(pytest_html.extras.text(log_content, name="日志内容"))
        item.extra = extra


# 自定义 HTML 报告内容
@pytest.hookimpl(tryfirst=True)
def pytest_html_results_summary(prefix, summary, postfix):
    # 指定日志文件路径
    log_file_path = "test.log"

    # 检查日志文件是否存在
    if not os.path.exists(log_file_path):
        logger.error(f"日志文件 {log_file_path} 不存在")
        return

    # 读取日志文件内容
    with open(log_file_path, "r", encoding="utf-8") as log_file:
        log_file_content = log_file.read()

        # 添加到报告的前缀部分
        prefix.extend([
            '<style>'
            'body {'
            '  background-image: url("file:///C:/Users/RDPJEQK/Pictures/Camera%20Roll/Snipaste_2025-05-09_17-03-01.png");'
            '  background-size: cover;'
            '  background-repeat: no-repeat;'
            '  background-attachment: fixed;'
            '  font-family: Arial, sans-serif;'
            '  color: #333;'
            '  padding: 20px;'
            '}'
            'h1, h2 {'
            '  text-align: center;'
            '  color: #333;'
            '  font-size: 28px;'
            '}'
            'p {'
            '  font-size: 18px;'
            '  color: #555;'
            '}'
            'pre {'
            '  font-size: 16px;'
            '  background-color: #f9f9f9;'
            '  padding: 10px;'
            '  border-radius: 5px;'
            '  color: #333;'
            '  font-family: Courier New, monospace;'
            '}'
            '</style>',
            f'<h1 style="color: #333; font-size: 28px; text-align: center; font-family: Arial, sans-serif;">测试报告</h1>',
            f'<p style="color: #555; font-size: 18px; font-family: Arial, sans-serif;">测试环境：供应链系统 8092内测环境</p>',
            f'<p style="color: #555; font-size: 18px; font-family: Arial, sans-serif;">测试时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>',
            f'<p style="color: #555; font-size: 18px; font-family: Arial, sans-serif;">日志文件名称：{log_file_path}</p>',
            f'<pre style="background: none; border: none; color: #fff; font-size: 16px; font-family: Courier New, monospace;">{log_file_content}</pre>'
        ])
        # 添加到报告的后缀部分
        postfix.extend([
            f'<h2 style="color: #333; font-size: 24px; text-align: center; font-family: Arial, sans-serif;">测试总结</h2>',
            f'<p style="color: #555; font-size: 18px; font-family: Arial, sans-serif;">所有测试用例均已执行完毕。</p>'
        ])