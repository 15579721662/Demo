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
    welcome_text = page.text_content('body', timeout=3000)  # 获取欢迎信息
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

    # 切换到评审中状态
    page.click(
        "#app > div > div.content > div.ivu-layout > div.content-wrapper.ivu-layout-content > div.rd_page > div.rd_page-top.fs-0 > div.rd_page-status > div > label:nth-child(4)")
    page.wait_for_load_state('networkidle')  # 等待页面加载完成


    # 定位表格中的第一行第三个单元格
    first_cell_selector = f"#app > div > div.content > div.ivu-layout > div.content-wrapper.ivu-layout-content > div.rd_page > div.rd_page-table > div > div.ivu-table.ivu-table-default.ivu-table-border > div.ivu-table-body.ivu-table-overflowY.ivu-table-overflowX > table > tbody > tr:nth-child(1) > td:nth-child(3) > div"
    page.wait_for_selector(first_cell_selector, state="attached", timeout=5000)

    # 获取第一行第三个单元格的文本内容
    first_cell_element = page.query_selector(first_cell_selector)
    if first_cell_element:
        first_sales_order_text = first_cell_element.text_content()
        print(f"第一行的销售单号数据: {first_sales_order_text}")
    else:
        print("未找到销售单号的数据")

    time.sleep(2)

    #进入采购模块-待采购列表
    page.click("#app > div > div.header-con.ivu-layout-header > div > div.header-menu > ul > li:nth-child(4) > span")
    time.sleep(0.5)
    page.click("#app > div > div.content > div.left-sider.ivu-layout-sider > div.ivu-layout-sider-children > div.side-menu-wrapper.no-scrollbar > ul > li.ivu-menu-submenu.ivu-menu-opened > ul > li:nth-child(1) > span")
    time.sleep(1)
    #输入检索对应销售单号
    danhao=first_sales_order_text
    page.fill(
        '#app > div > div.content > div.ivu-layout > div.content-wrapper.ivu-layout-content > div.rd_page.wait-purshase-details > div.rd_page-top.fs-0 > div.rd_page-search.b-flex > div:nth-child(1) > div > input',
        first_sales_order_text)
    page.click("#app > div > div.content > div.ivu-layout > div.content-wrapper.ivu-layout-content > div.rd_page.wait-purshase-details > div.rd_page-top.fs-0 > div.rd_page-search.b-flex > div:nth-child(1) > button.btn-primary.mgl10.ivu-btn.ivu-btn-default > span")
    time.sleep(2)

    # 选择零件新建采购单
    page.click(
        "#app > div > div.content > div.ivu-layout > div.content-wrapper.ivu-layout-content > div.rd_page.wait-purshase-details > div.rd_page-table > div > div.vxe-table--render-wrapper > div.vxe-table--main-wrapper > div.vxe-table--body-wrapper.body--wrapper > table > tbody > tr > td.vxe-body--column.col_41.col--center.col--checkbox.col--ellipsis > div")
    time.sleep(1)
    page.click(
        "#app > div > div.content > div.ivu-layout > div.content-wrapper.ivu-layout-content > div.rd_page.wait-purshase-details > div.rd_page-table-header.fs-0 > div > div.btn > button.btn-primary.ivu-btn.ivu-btn-default > span")
    time.sleep(1)
    # 选择供应商
    page.click(
        "body > div:nth-child(21) > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.mgb10 > form > div > div:nth-child(1) > div > div > div > input")
    time.sleep(1)
    # 定位输入框并输入内容
    input_selector = ".ivu-input.ivu-input-default[placeholder='供应商名称/供应商代码']"
    page.fill(input_selector, "zhiwen测试供应商")
    time.sleep(0.5)
    page.click("body > div:nth-child(25) > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div.ivu-row > div.flex.ivu-col.ivu-col-span-8 > button.btn-primary.mgl10.ivu-btn.ivu-btn-default > span")
    time.sleep(0.5)

    # 定位表格中的第一行第三个单元格
    first_cell1_selector = "body > div:nth-child(25) > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div.mgt15 > div > div.ivu-table.ivu-table-default.ivu-table-border > div.ivu-table-body > table > tbody > tr:nth-child(1)> td:nth-child(3) > div"
    page.wait_for_selector(first_cell1_selector, state="attached", timeout=5000)

    # 获取第一行第三个单元格的文本内容
    first_cell1_element = page.query_selector(first_cell1_selector)
    if first_cell1_element:
        cell_text = first_cell1_element.text_content()
        print(f"第一行第三个单元格的文本内容: {cell_text}")
    else:
        print("未找到第一行第三个单元格")

    # 点击该单元格
    page.click(first_cell1_selector)
    time.sleep(0.5)
    page.click("body > div:nth-child(25) > div.ivu-modal-wrap > div > div > div.ivu-modal-footer > div > div > button.btn-primary.ivu-btn.ivu-btn-default")
    time.sleep(2)

    # 选择供应商交期
    page.click("body > div:nth-child(21) > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.mgb10 > form > div > div:nth-child(5) > div > div > div.ivu-date-picker > div.ivu-date-picker-rel > div > input")
    page.press("body > div:nth-child(21) > div.ivu-modal-wrap > div > div > div.ivu-modal-body > div > div.mgb10 > form > div > div:nth-child(5) > div > div > div.ivu-date-picker > div.ivu-date-picker-rel > div > input", "Enter")
    time.sleep(1)

    # 提交采购单
    page.click(
        "body > div:nth-child(21) > div.ivu-modal-wrap > div > div > div.ivu-modal-footer > div > div:nth-child(2) > button.btn-primary.ivu-btn.ivu-btn-default > span")
    time.sleep(2)
    print("新建采购单成功！")

    # 进入采购列表，查询对应订单
    page.click(
        "#app > div > div.content > div.left-sider.ivu-layout-sider > div.ivu-layout-sider-children > div.side-menu-wrapper.no-scrollbar > ul > li.ivu-menu-submenu.ivu-menu-item-active.ivu-menu-opened.ivu-menu-child-item-active > ul > li:nth-child(2) > span")
    time.sleep(1)
    page.fill(
        '#app > div > div.content > div.ivu-layout > div.content-wrapper.ivu-layout-content > div.rd_page > div.rd_page-top.fs-0 > div.rd_page-search.b-flex > div:nth-child(1) > div > input',
        first_sales_order_text)  # 填写订单号
    page.click(
        "#app > div > div.content > div.ivu-layout > div.content-wrapper.ivu-layout-content > div.rd_page > div.rd_page-top.fs-0 > div.rd_page-search.b-flex > div:nth-child(1) > button.btn-primary.mgl10.ivu-btn.ivu-btn-default > span")
    time.sleep(2)

    # 选择采购单号进入详情
    # 定位表格中的第一行第2个单元格
    first_cell2_selector = f"#app > div > div.content > div.ivu-layout > div.content-wrapper.ivu-layout-content > div.rd_page > div.rd_page-table > div > div.ivu-table.ivu-table-default.ivu-table-border > div.ivu-table-body.ivu-table-overflowX > table > tbody > tr:nth-child(1)> td:nth-child(2) > div "
    page.wait_for_selector(first_cell2_selector, state="attached", timeout=5000)

    # 获取第一行第2个单元格的文本内容
    first_cell2_element = page.query_selector(first_cell2_selector)
    if first_cell2_element:
        first_sales2_order_text = first_cell2_element.text_content()
        print(f"第一行的采购单号数据: {first_sales2_order_text}")
    else:
        print("未找到采购单号的数据")

    # 定位单号字段并点击
    target_sales2_order = first_sales2_order_text
    sales_order2_selector = f"text={target_sales2_order}"
    page.wait_for_selector(sales_order2_selector, state="attached", timeout=5000)  # 等待单号字段出现
    sales_order2_element = page.query_selector(sales_order2_selector)
    assert sales_order2_element is not None, f"未找到单号 {target_sales2_order}"
    sales_order2_element.click()

    # 等待弹窗页面加载完成
    page.wait_for_load_state('networkidle')
    time.sleep(2)
    # 进入采购单详情
    page.click(
        "body > div.details_c.v-transfer-dom > div.ivu-drawer-wrap > div > div > div > div.tabs-area.flex1--h.rd_tabs.ivu-tabs.ivu-tabs-card > div.ivu-tabs-bar > div > div > div > div > div.ivu-tabs-tab.ivu-tabs-tab-active.ivu-tabs-tab-focused")
    time.sleep(1)
    # 新建收货单
    page.click(
        "body > div.details_c.v-transfer-dom > div.ivu-drawer-wrap > div > div > div > div.tabs-area.flex1--h.rd_tabs.ivu-tabs.ivu-tabs-card > div.ivu-tabs-bar > div > div > div > div > div:nth-child(6)")
    time.sleep(1)
    page.click(
        "body > div.details_c.v-transfer-dom > div.ivu-drawer-wrap > div > div > div > div.tabs-area.flex1--h.rd_tabs.ivu-tabs.ivu-tabs-card > div.ivu-tabs-content.ivu-tabs-content-animated > div:nth-child(5) > div > div > div:nth-child(2) > div.b-flex.mgb10.tr > button > span")
    time.sleep(0.5)
    page.click(
        "body > div:nth-child(23) > div.ivu-modal-wrap > div > div > div.ivu-modal-footer > button.btn-primary.ivu-btn.ivu-btn-default > span")
    time.sleep(1)
    page.click(
        "body > div:nth-child(25) > div.ivu-modal-wrap > div > div > div.ivu-modal-footer > button.btn-primary.ivu-btn.ivu-btn-default > span")
    time.sleep(2)
    print("新建收货单成功")
    # 进入质检详情，录入质检结果
    page.click(
        "body > div:nth-child(21) > div.ivu-drawer-wrap > div > div > div > div.tabs-area.flex1--h.rd_tabs.ivu-tabs.ivu-tabs-card > div.ivu-tabs-bar > div > div > div > div > div.ivu-tabs-tab.ivu-tabs-tab-active.ivu-tabs-tab-focused")
    time.sleep(3)






if __name__ == "__main__":
    pytest.main()