import unittest
import pytest
import time
from playwright.sync_api import expect
from playwright.sync_api import sync_playwright

# 定义 Playwright fixture
@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p

# 定义浏览器 fixture
@pytest.fixture(scope="module")
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    try:
        yield browser
    finally:
        browser.close()

# 定义页面 fixture
@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

def test_select_option(browser):
    # 创建新页面
    page = browser.new_page()
    page.set_viewport_size({"width": 1492, "height": 721})  # 设置为常见的屏幕分辨率
    # 获取登录页面信息
    page.goto('http://218.17.90.148:8092/#/login')  # 替换为实际的页面 URL
    page.wait_for_load_state('networkidle')  # 等待页面所有网络请求完成
    expect(page.locator(
        '#app > div > div.login-con > div > div.ivu-card-body > div > form > div:nth-child(1) > div > div > input')).to_be_visible(
        timeout=2000)  # 显式等待元素可见
    page.fill(
        '#app > div > div.login-con > div > div.ivu-card-body > div > form > div:nth-child(1) > div > div > input',
        'root')  # 填写用户名
    page.fill(
        '#app > div > div.login-con > div > div.ivu-card-body > div > form > div:nth-child(2) > div > div > input',
        'rd1234567')  # 填写密码
    page.click(
        '#app > div > div.login-con > div > div.ivu-card-body > div > form > div.mgb15.ivu-form-item > div > button > span')  # 点击登录按钮
    page.wait_for_load_state('networkidle')  # 等待页面跳转完成
    welcome_text = page.text_content('body', timeout=2000)  # 获取欢迎信息
    assert '欢迎登录快速供应链系统' in welcome_text  # 验证欢迎信息

    # 进入系统模块
    expect(page.locator(
        '#app > div > div.header-con.ivu-layout-header > div > div.header-menu > ul > li:nth-child(2)')).to_be_visible(
        timeout=2000)  # 显式等待元素可见
    page.click("#app > div > div.header-con.ivu-layout-header > div > div.header-menu > ul > li:nth-child(2)")
    expect(page.locator(
        '#app > div > div.content > div.left-sider.ivu-layout-sider > div.ivu-layout-sider-children > div.side-menu-wrapper.no-scrollbar > ul > li:nth-child(2) > div')).to_be_visible(
        timeout=1000)  # 显式等待元素可见
    page.click(
        "#app > div > div.content > div.left-sider.ivu-layout-sider > div.ivu-layout-sider-children > div.side-menu-wrapper.no-scrollbar > ul > li:nth-child(2) > div")
    expect(page.locator(
        "#app > div > div.content > div.ivu-layout > div.content-wrapper.ivu-layout-content > div.rd_page > div.rd_page-top.fs-0 > div.rd_page-search.b-flex > div:nth-child(2) > button.btn-primary.ivu-btn.ivu-btn-default > span")).to_be_visible(
        timeout=2000)  # 显式等待元素可见

    # 新建销售单-编辑信息
    page.click(
        "#app > div > div.content > div.ivu-layout > div.content-wrapper.ivu-layout-content > div.rd_page > div.rd_page-top.fs-0 > div.rd_page-search.b-flex > div:nth-child(2) > button.btn-primary.ivu-btn.ivu-btn-default > span")
    xiaoshou_text = page.text_content(
        'body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body',
        timeout=2000)  # 获取新建页面信息
    assert '基本信息产品信息订单注意事项基本信息销售订单号' in xiaoshou_text  # 验证新建销售单页面信息
    page.click(
        "body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-base-info.mgb10 > form > div.form-base > div:nth-child(2) > div > div > div.ivu-select-selection > div > input")
    expect(page.locator(
        'body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-base-info.mgb10 > form > div.form-base > div:nth-child(2) > div > div > div.ivu-select-dropdown > ul.ivu-select-dropdown-list > li:nth-child(1)')).to_be_visible(
        timeout=2000)  # 显式等待元素可见
    page.click(
        "body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-base-info.mgb10 > form > div.form-base > div:nth-child(2) > div > div > div.ivu-select-dropdown > ul.ivu-select-dropdown-list > li:nth-child(1)")
    page.click(
        "body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-base-info.mgb10 > form > div.form-base > div:nth-child(5) > div > div > div.ivu-date-picker-rel > div > input")
    expect(page.locator(
        'body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-base-info.mgb10 > form > div.form-base > div:nth-child(5) > div > div > div.ivu-select-dropdown > div > div > div > div:nth-child(2) > div > span:nth-child(32) > em')).to_be_visible(
        timeout=1000)  # 显式等待元素可见
    page.click(
        "body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-base-info.mgb10 > form > div.form-base > div:nth-child(5) > div > div > div.ivu-select-dropdown > div > div > div > div:nth-child(2) > div > span:nth-child(32) > em")
    page.fill(
        'body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-base-info.mgb10 > form > div:nth-child(2) > div > div > div > textarea',
        '这个是一个重要的交代事项：需要加急，检验要严格！')  # 填写重要交代事项
    page.click(
        "body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-product-info.mgb10 > div.mgt20.ivu-row > div.ivu-col.ivu-col-span-3 > button > span")
    expect(page.locator(
        'body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-product-info.mgb10 > div.table > div > div.vxe-table--render-wrapper > div.vxe-table--main-wrapper > div.vxe-table--body-wrapper.body--wrapper > table > tbody > tr > td.vxe-body--column.col_13.col--center.col--edit.col--ellipsis > div > input')).to_be_visible(
        timeout=1000)  # 等待产品明细信息
    page.click(
        "body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-product-info.mgb10 > div.table > div > div.vxe-table--render-wrapper > div.vxe-table--main-wrapper > div.vxe-table--body-wrapper.body--wrapper > table > tbody > tr > td.vxe-body--column.col_13.col--center.col--edit.col--ellipsis > div > input")
    # 填写零件名称
    page.fill(
        'body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-product-info.mgb10 > div.table > div > div.vxe-table--render-wrapper > div.vxe-table--main-wrapper > div.vxe-table--body-wrapper.body--wrapper > table > tbody > tr > td.vxe-body--column.col_13.col--center.col--edit.col--ellipsis.col--active > div > div > input',
        'test001')

    # 将鼠标悬停在目标元素上&选择零件材料
    page.hover("body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-product-info.mgb10 > div.table > div > div.vxe-table--render-wrapper > div.vxe-table--main-wrapper > div.vxe-table--body-wrapper.body--wrapper > table > tbody > tr > td.vxe-body--column.col_15.col--center.col--edit.col--ellipsis")
    time.sleep(0.5)
    page.click("body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-product-info.mgb10 > div.table > div > div.vxe-table--render-wrapper > div.vxe-table--main-wrapper > div.vxe-table--body-wrapper.body--wrapper > table > tbody > tr > td.vxe-body--column.col_15.col--center.col--edit.col--ellipsis.col--active > div > div > div > div > input")
    time.sleep(0.5)
    page.click("body > div.ivu-select-dropdown.ivu-select-dropdown-transfer.vxe-table--ignore-clear > ul.ivu-select-dropdown-list > li:nth-child(2)")
    # 将鼠标悬停在目标元素上&选择报关名称
    page.hover(
        "body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-product-info.mgb10 > div.table > div > div.vxe-table--render-wrapper > div.vxe-table--main-wrapper > div.vxe-table--body-wrapper.body--wrapper > table > tbody > tr > td.vxe-body--column.col_16.col--center.col--edit.col--ellipsis")
    time.sleep(1)
    page.click("body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-product-info.mgb10 > div.table > div > div.vxe-table--render-wrapper > div.vxe-table--main-wrapper > div.vxe-table--body-wrapper.body--wrapper > table > tbody > tr > td.vxe-body--column.col_16.col--center.col--edit.col--ellipsis.col--active > div > div")
    page.click(
        "body > div.ivu-select-dropdown.ivu-cascader-transfer.vxe-table--ignore-clear > div > span > ul > li:nth-child(1)")
    time.sleep(1)
    page.click("body > div.ivu-select-dropdown.ivu-cascader-transfer.vxe-table--ignore-clear > div > span > span > ul > li:nth-child(1)")
    time.sleep(0.5)
    #将鼠标悬停在目标元素上&选择未注公差
    page.hover(
        "body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-product-info.mgb10 > div.table > div > div.vxe-table--render-wrapper > div.vxe-table--main-wrapper > div.vxe-table--body-wrapper.body--wrapper > table > tbody > tr > td.vxe-body--column.col_19.col--center.col--edit.col--ellipsis")
    time.sleep(1)
    page.click("body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-product-info.mgb10 > div.table > div > div.vxe-table--render-wrapper > div.vxe-table--main-wrapper > div.vxe-table--body-wrapper.body--wrapper > table > tbody > tr > td.vxe-body--column.col_19.col--center.col--edit.col--ellipsis > div")
    time.sleep(0.5)
    page.click("body > div.ivu-select-dropdown.ivu-select-dropdown-transfer.vxe-table--ignore-clear > ul.ivu-select-dropdown-list > li:nth-child(2)")
    time.sleep(0.5)

    # 将鼠标悬停在目标元素上&选择光洁度
    page.hover(
        "body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-product-info.mgb10 > div.table > div > div.vxe-table--render-wrapper > div.vxe-table--main-wrapper > div.vxe-table--body-wrapper.body--wrapper > table > tbody > tr > td.vxe-body--column.col_20.col--center.col--edit.col--ellipsis")
    time.sleep(1)
    page.click(
        "body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-product-info.mgb10 > div.table > div > div.vxe-table--render-wrapper > div.vxe-table--main-wrapper > div.vxe-table--body-wrapper.body--wrapper > table > tbody > tr > td.vxe-body--column.col_20.col--center.col--edit.col--ellipsis > div")
    time.sleep(0.5)
    page.click("body > div.ivu-select-dropdown.ivu-select-dropdown-transfer.vxe-table--ignore-clear > ul.ivu-select-dropdown-list > li:nth-child(1)")

    #编辑输入零件单价
    page.click("body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-product-info.mgb10 > div.table > div > div.vxe-table--render-wrapper > div.vxe-table--main-wrapper > div.vxe-table--body-wrapper.body--wrapper > table > tbody > tr > td.vxe-body--column.col_22.col--center.col--ellipsis > div > div > input")
    page.fill(
        'body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.pdt10.anchor-product-info.mgb10 > div.table > div > div.vxe-table--render-wrapper > div.vxe-table--main-wrapper > div.vxe-table--body-wrapper.body--wrapper > table > tbody > tr > td.vxe-body--column.col_22.col--center.col--ellipsis > div > div > input',
        '10')
    #提交并确认销售单
    page.click("body > div.new-sales-order-modal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-footer > button.btn-primary.ivu-btn.ivu-btn-default")
    time.sleep(0.5)
    page.click("body > div.rd_simpleModal.v-transfer-dom > div.ivu-modal-wrap > div > div > div.ivu-modal-footer > button.btn-primary.ivu-btn.ivu-btn-default")
    time.sleep(1)
    print("新建订单成功！")
    time.sleep(2)

if __name__ == "__main__":
    pytest.main()
