from resources.connection import DBConnection
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from utils.driver_utils import DriverUtils


def init_report(test_name):
        DBConnection.get_block(test_name)
        DBConnection.get_block_run()
        DBConnection.get_block_run_step()


def get_block_data(test_name):
        DBConnection.get_block(test_name)

def get_block_run_data():
       DBConnection.get_block_run()


def get_block_run_step_data():
       DBConnection.get_block_run_step()

def run_sql_func():
        DBConnection.run_exec()


def test_start():
    DBConnection.test_start()
    DBConnection.test_start_row_value()

def test_end_report():
    DBConnection.test_end()

def action_start():
        DBConnection.action_starterd()


def action_end():
    DBConnection.action_ended()

def test_status_passsed():
    DBConnection.test_passed()
    test_end_report

def find_element_report_func(locator,browser,child_locator):
    DBConnection.action_starterd()
    DBConnection.web_element_find_element()
    DBConnection.find_element_row_value(locator, browser, child_locator)
    DBConnection.html_element_row()
    DBConnection.html_row()
    # DBConnection.web_element_find_element_row_value(locator)
    DBConnection.action_ended()

def find_elements_report_func(locator,browser,child_locator):
    DBConnection.action_starterd()
    DBConnection.web_element_find_elements()
    DBConnection.web_element_find_elements_row_value(locator, browser, child_locator)
    DBConnection.html_row()
    DBConnection.action_ended()

def driver_find_elements_report_func(browser,locator):
    DBConnection.action_starterd()
    DBConnection.web_driver_find_elements()
    DBConnection.web_driver_find_elements_row_value(browser,locator)
    DBConnection.html_row()
    DBConnection.action_ended()

def driver_find_element_report_func(browser,locator):
    DBConnection.action_starterd()
    DBConnection.web_driver_find_element()
    DBConnection.driver_find_element_row_value(locator,browser)
    DBConnection.html_element_row()
    DBConnection.html_row()
    DBConnection.action_ended()

def clear_element_report_func(locator,browser):
    DBConnection.action_starterd()
    DBConnection.web_element_clear_element()
    DBConnection.web_element_clear_element_row_value(locator,browser)
    DBConnection.action_ended()

def driver_get_action(browser,url):
    DBConnection.action_starterd()
    DBConnection.driver_get()
    DBConnection.driver_get_action_row_value_func(browser,url)
    DBConnection.action_ended()

def web_element_click_report_func(browser,locator):
    DBConnection.action_starterd()
    DBConnection.web_element_click()
    DBConnection.web_element_click_row_value(browser,locator)
    DBConnection.action_ended()

def web_element_send_keys_report_func(locator,browser,charSequence):
        DBConnection.action_starterd()
        DBConnection.web_element_send_keys()
        DBConnection.web_element_send_keys_row_value(locator,browser,charSequence)
        DBConnection.action_ended()



# def keys_down_up_report_func(browser,charSequence):
#     action_key_down_report_func(browser,charSequence)
#     action_key_up_report_func(browser,charSequence)
        # DBConnection.action_starterd()
        # DBConnection.action_key_down_report()
        # DBConnection.action_ended()
        # DBConnection.action_starterd()
        # DBConnection.action_key_up_report()
        # DBConnection.action_ended()


def driver_quit_report_func(browser):
            DBConnection.action_starterd()
            DBConnection.driver_quit_report()
            DBConnection.driver_quit_report_row_value(browser)
            DBConnection.action_ended()


def driver_close_report_func(browser):
    DBConnection.action_starterd()
    DBConnection.driver_close_report()
    DBConnection.driver_close_row_value(browser)
    DBConnection.action_ended()


def action_click_element_report_func():
    DBConnection.action_starterd()
    DBConnection.action_click_element_report()
    DBConnection.action_ended()


def action_click_report_func(locator,offset_x,offset_y,browser):
    action_move_to_element_report_func(locator)
    action_move_to_element_by_offset_report_func(offset_x,offset_y,browser)
    DBConnection.action_starterd()
    DBConnection.action_click_report()
    DBConnection.action_click_row_value(browser)
    DBConnection.action_ended()

def action_double_click_element_report_func(locator):
    DBConnection.action_starterd()
    DBConnection.action_double_click_element_report()
    DBConnection.action_double_click_element_row_value(locator)
    action_move_to_element_report_func(locator)
    DBConnection.action_ended()

def action_move_to_element_report_func(lcoator):
    DBConnection.action_starterd()
    DBConnection.action_move_to_element_report()
    DBConnection.action_move_to_element_row_value(lcoator)
    DBConnection.action_ended()

def action_move_to_element_by_offset_report_func(offset_x,offset_y,browser):
    DBConnection.action_starterd()
    DBConnection.action_move_to_element_by_offset_report()
    DBConnection.action_move_to_element_by_offset_row_value( offset_x, offset_y, browser)
    DBConnection.action_ended()

def action_key_down_report_func(browser,charSequence):
    DBConnection.action_starterd()
    DBConnection.action_key_down_report()
    DBConnection.action_key_down_row_value(browser,charSequence)
    DBConnection.action_ended()

def action_key_up_report_func(browser,charSequence):
    DBConnection.action_starterd()
    DBConnection.action_key_up_report()
    DBConnection.action_key_up_row_value(browser,charSequence)
    DBConnection.action_ended()

def press_keys_report_func(browser,charSequence):
        DBConnection.action_starterd()
        DBConnection.actions_send_keys_report()
        DBConnection.actions_send_keys_row_value(browser,charSequence)
        action_key_down_report_func(browser,charSequence)
        action_key_up_report_func(browser,charSequence)
        DBConnection.action_ended()


def actions_send_keys_element_report_func(browser,locator,charSequenc):
    DBConnection.action_starterd()
    DBConnection.actions_send_keys_element_report()
    DBConnection.actions_send_keys_element_row_value(locator,charSequenc)
    DBConnection.action_starterd()
    DBConnection.action_click_element_report()
    DBConnection.action_click_element_row_value(locator)
    action_move_to_element_report_func(locator)
    DBConnection.action_ended()
    DBConnection.action_starterd()
    DBConnection.actions_send_keys_report()
    DBConnection.actions_send_keys_row_value(browser,charSequenc)
    for i in range(0,len(charSequenc)):
        action_key_down_report_func(browser,charSequenc[i])
        action_key_up_report_func(browser,charSequenc[i])
    DBConnection.action_ended()
    DBConnection.action_ended()


def action_click_and_hold_report_func(source):
    DBConnection.action_starterd()
    DBConnection.action_click_and_hold_report()
    DBConnection.action_click_and_hold_row_value(source)
    action_move_to_element_report_func(source)
    # action_move_to_element_report_func(source)
    DBConnection.action_ended()

def action_drag_and_drop_by_offset_report_func(browser,locator,xoffset,yoffset):
    DBConnection.action_starterd()
    DBConnection.action_drag_and_drop_by_offset_report()
    DBConnection.action_drag_and_drop_by_offset_row_value(locator,xoffset,yoffset)
    action_click_and_hold_report_func(locator)
    action_move_to_element_by_offset_report_func(xoffset,yoffset,browser)
    DBConnection.action_ended()

def action_drag_and_drop_element_to_element_report_func(browser , source,target):
    DBConnection.action_starterd()
    DBConnection.action_drag_and_drop_element_to_element_report()
    DBConnection.action_drag_and_drop_element_to_element_row_value(browser , source,target)
    action_click_and_hold_report_func(source)
    # action_move_to_element_report_func(source)
    action_move_to_element_report_func(target)#release
    DBConnection.action_ended()


def remote_close_report_func():
    DriverUtils.get_current_driver().close();

def driver_find_element_func(locator):
    return DriverUtils.get_current_driver().find_element_by_id(locator)

# def driver_find_element_func(by ,locator):
#     DriverUtils.get_current_driver().find_element(by,locator)

def get_child_func(parent_locator , locator):
    element = DriverUtils.get_current_driver().find_element_by_id(parent_locator)
    element.find_element_by_id(locator)

def get_childs_func(parent_locator , locator):
    # element = DriverUtils.get_current_driver().find_element(By.CLASS_NAME, "#pancakes")
    element = DriverUtils.get_current_driver().find_element_by_id(parent_locator)
    return  element.find_elements_by_class_name(locator)

def get_element_x(element):
    return element.location.get('x')

def action_send_keys_func(keys_to_send):
    actions = ActionChains(DriverUtils.get_current_driver())
    # actions.key_down(keys.Keys.SHIFT)
    actions.send_keys(keys_to_send)
    # actions.key_up(keys.Keys.SHIFT)
    actions.perform()

def action_send_keys_element_func(element,keys):
    actions = ActionChains(DriverUtils.get_current_driver())
    actions.send_keys_to_element(element,keys)
    actions.perform()



# row value func
def driver_get_action_row_value(browser,url):
    DBConnection.driver_get_action_row_value_func(browser,url)





