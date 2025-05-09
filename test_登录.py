# -*- coding: utf-8 -*-
import logging
from conftest import logger  # 确保 conftest.py 文件在同一个目录下
from playwright.sync_api import sync_playwright
import pytest

def test_example():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 打开浏览器
        logger.info("浏览器已启动")
        page = browser.new_page()  # 打开新页面
        logger.info("新页面已打开")
        try:
            logger.info("设置视口大小")
            page.set_viewport_size({"width": 1492, "height": 721})
            logger.info("导航到登录页面")
            page.goto("http://218.17.90.148:8092/#/login")  # 替换为实际的页面 URL
            page.wait_for_load_state('networkidle')  # 等待页面所有网络请求完成
            logger.info("页面加载完成")

            logger.info("等待用户名输入框可见")
            page.wait_for_selector(
                '#app > div > div.login-con > div > div.ivu-card-body > div > form > div:nth-child(1) > div > div > input',
                timeout=2000)

            logger.info("填写用户名")
            page.fill(
                '#app > div > div.login-con > div > div.ivu-card-body > div > form > div:nth-child(1) > div > div > input',
                'root')

            logger.info("填写密码")
            page.fill(
                '#app > div > div.login-con > div > div.ivu-card-body > div > form > div:nth-child(2) > div > div > input',
                'rd1234567')

            logger.info("点击登录按钮")
            page.click(
                '#app > div > div.login-con > div > div.ivu-card-body > div > form > div.mgb15.ivu-form-item > div > button > span')

            logger.info("等待页面跳转完成")
            page.wait_for_load_state('networkidle')

            logger.info("获取欢迎信息")
            welcome_text = page.text_content('body', timeout=3000)
            assert '欢迎登录快速供应链系统' in welcome_text  # 验证欢迎信息
            logger.info("欢迎信息验证通过")
        except Exception as e:
            logger.error(f"测试失败：{e}")
            pytest.fail(f"测试失败：{e}")
        finally:
            logger.info("关闭浏览器")
            browser.close()
