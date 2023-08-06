from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
# def create_function(orgin_func,name, args):
#     def y():
#         print("s")
#         orgin_func(args)
#         pass
#
#
#     y_code = types.CodeType(orgin_func.__code__.co_argcount,
#                             orgin_func.__code__.co_kwonlyargcount,
#                             orgin_func.__code__.co_nlocals,
#                             orgin_func.__code__.co_stacksize,
#                             orgin_func.__code__.co_flags,
#                             y.__code__.co_code,
#                             orgin_func.__code__.co_consts,
#                             orgin_func.__code__.co_names,
#                             orgin_func.__code__.co_varnames,
#                             y.__code__.co_filename,
#                             name,
#                             y.__code__.co_firstlineno,
#                             y.__code__.co_lnotab)
#
#     return types.FunctionType(y_code, orgin_func.__globals__, name)
from selenium.webdriver.support.wait import WebDriverWait

from shield34_reporter.auth.sdk_authentication import SdkAuthentication
from shield34_reporter.container.run_report_container import RunReportContainer
from shield34_reporter.handler.action_chains import *
from shield34_reporter.handler.web_driver import DriverFindElements, DriverFindElement, DriverGetUrl, DriverQuit, \
    DriverClose
from shield34_reporter.handler.web_driver_wait import DriverWaitUntil
from shield34_reporter.handler.web_element import ElementFindElements, ElementFindElement, ElementClickHandler, \
    ElementSendKeysHandler, ElementClearHandler
from shield34_reporter.model.csv_rows.log_base_csv_row import DebugLogCsvRow
from shield34_reporter.utils.driver_utils import DriverUtils
from shield34_reporter.utils.reporter_proxy import ReporterProxy, ProxyServerNotInitializedException


class SeleniumOverrider(object):
    is_overrided= False

    @staticmethod
    def override():
        if not SeleniumOverrider.is_overrided and SdkAuthentication.isAuthorized:
            WebElementOverrider.override()
            WebDriverOverrider.override()
            ActionsOverrider.override()
            WebDriverWaitOverrider.override()
            SeleniumOverrider.is_overrided = True


class WebElementOverrider:
    @staticmethod
    def override():

        WebElement.org_find_elements = WebElement.find_elements
        WebElement.find_elements = lambda element, by, value=None: ElementFindElements(
            DriverUtils.get_current_driver(), element, WebElement.org_find_elements, by, value).do_handle()

        WebElement.org_find_element = WebElement.find_element
        WebElement.find_element = lambda element, by, value=None: ElementFindElement(
            DriverUtils.get_current_driver(), element, WebElement.org_find_element, by, value).do_handle()

        WebElement.org_click = WebElement.click
        WebElement.click = lambda element: ElementClickHandler(
            DriverUtils.get_current_driver(), element, WebElement.org_click).do_handle()

        WebElement.org_send_keys = WebElement.send_keys
        WebElement.send_keys = lambda element, keys: ElementSendKeysHandler(
            DriverUtils.get_current_driver(), element, WebElement.org_send_keys, keys ).do_handle()

        WebElement.org_clear = WebElement.clear
        WebElement.clear = lambda element: ElementClearHandler(
            DriverUtils.get_current_driver(), element, WebElement.org_clear).do_handle()


class WebDriverOverrider(object):
    @staticmethod
    def override():

        WebDriver.org_init = WebDriver.__init__

        def init_web_driver(self, command_executor='http://127.0.0.1:4444/wd/hub',
                 desired_capabilities=None, browser_profile=None, proxy=None,
                 keep_alive=False, file_detector=None, options=None):
            updated_desired_capabilities = desired_capabilities
            if SdkAuthentication.is_authorized():
                if updated_desired_capabilities is None:
                    updated_desired_capabilities = {}
                updated_desired_capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}
                updated_desired_capabilities['acceptInsecureCerts'] = True

                if ReporterProxy.start_proxy_management_server():
                    if options is None:
                        options = webdriver.ChromeOptions()
                    proxies_count = len(RunReportContainer.get_current_block_run_holder().proxyServers)
                    if proxies_count > 0:
                        RunReportContainer.get_current_block_run_holder().proxyServers[proxies_count-1].add_to_capabilities(updated_desired_capabilities)
                    else:
                        raise ProxyServerNotInitializedException()
                    if options is not None and isinstance(options, webdriver.ChromeOptions):
                        options.add_argument('--ignore-certificate-errors')
                        options.add_argument('--ignore-ssl-errors')
            RunReportContainer.current_driver = self
            RunReportContainer.driver_counter = RunReportContainer.driver_counter + 1
            WebDriver.org_init(self, command_executor, updated_desired_capabilities, browser_profile, proxy, keep_alive,
                               file_detector, options)

        WebDriver.__init__ = init_web_driver

        WebDriver.org_find_elements = WebDriver.find_elements
        WebDriver.find_elements = lambda obj, by, value=None: DriverFindElements(obj, WebDriver.org_find_elements, by, value).do_handle()

        WebDriver.org_find_element = WebDriver.find_element
        WebDriver.find_element = lambda obj, by, value=None: DriverFindElement(obj, WebDriver.org_find_element, by, value).do_handle()

        WebDriver.org_get = WebDriver.get
        WebDriver.get = lambda obj, url: DriverGetUrl(obj, WebDriver.org_get, url).do_handle()

        WebDriver.org_quit = WebDriver.quit
        WebDriver.quit = lambda obj: DriverQuit(obj, WebDriver.org_quit).do_handle()

        WebDriver.org_close = WebDriver.close
        WebDriver.close = lambda obj: DriverClose(obj, WebDriver.org_close).do_handle()

        WebDriver.org_execute_script = WebDriver.execute_script

        def shield_execute_script(obj, script, *args):
            if RunReportContainer.get_current_block_run_holder().action_started_count == 0:
                RunReportContainer.add_report_csv_row(DebugLogCsvRow(script))
            return WebDriver.org_execute_script(obj, script, *args)

        WebDriver.execute_script = shield_execute_script


class ActionsOverrider(object):

    @staticmethod
    def override():
        ActionChains.orig_click = ActionChains.click
        ActionChains.click = lambda action_chains, on_element=None: ActionChainsClick(
            DriverUtils.get_current_driver(), action_chains, ActionChains.orig_click, on_element).do_handle()

        ActionChains.orig_click_and_hold = ActionChains.click_and_hold
        ActionChains.click_and_hold = lambda action_chains, on_element=None: ActionChainsClickAndHold(
            DriverUtils.get_current_driver(), action_chains, ActionChains.orig_click_and_hold, on_element).do_handle()

        ActionChains.orig_context_click = ActionChains.context_click
        ActionChains.context_click = lambda action_chains, on_element=None: ActionChainsContextClick(
            DriverUtils.get_current_driver(), action_chains, ActionChains.orig_context_click, on_element).do_handle()

        ActionChains.orig_double_click = ActionChains.double_click
        ActionChains.double_click = lambda action_chains, on_element=None: ActionChainsDoubleClick(
            DriverUtils.get_current_driver(), action_chains, ActionChains.orig_double_click, on_element).do_handle()

        ActionChains.orig_drag_and_drop_by_offset = ActionChains.drag_and_drop_by_offset
        ActionChains.drag_and_drop_by_offset = lambda action_chains, source, xoffset, yoffset: \
            ActionChainsDragDropOffset(DriverUtils.get_current_driver(),
                                       action_chains,
                                       ActionChains.orig_drag_and_drop_by_offset,
                                       source,
                                       xoffset,
                                       yoffset).do_handle()

        ActionChains.orig_drag_and_drop = ActionChains.drag_and_drop
        ActionChains.drag_and_drop = lambda action_chains, source, target: \
            ActionChainsDragDrop(DriverUtils.get_current_driver(),
                                 action_chains,
                                 ActionChains.orig_drag_and_drop,
                                 source,
                                 target).do_handle()

        ActionChains.orig_key_down = ActionChains.key_down
        ActionChains.key_down = lambda action_chains, value, on_element=None: ActionChainsKeyDown(
            DriverUtils.get_current_driver(), action_chains, ActionChains.orig_key_down, value, on_element).do_handle()

        ActionChains.orig_key_up = ActionChains.key_up
        ActionChains.key_up = lambda action_chains, value, on_element=None: ActionChainsKeyUp(
            DriverUtils.get_current_driver(), action_chains, ActionChains.orig_key_up, value, on_element).do_handle()

        ActionChains.orig_move_by_offset = ActionChains.move_by_offset
        ActionChains.move_by_offset = lambda action_chains, xoffset, yoffset: ActionChainsMoveOffset(
            DriverUtils.get_current_driver(), action_chains, ActionChains.orig_move_by_offset, xoffset, yoffset).do_handle()

        ActionChains.orig_send_keys = ActionChains.send_keys
        ActionChains.send_keys = lambda action_chains, *keys: ActionChainsSendKeys(
            DriverUtils.get_current_driver(), action_chains, ActionChains.orig_send_keys, *keys).do_handle()

        ActionChains.orig_send_keys_to_element = ActionChains.send_keys_to_element
        ActionChains.send_keys_to_element = lambda action_chains, element, *keys_to_send: ActionChainsSendKeysElement(
            DriverUtils.get_current_driver(), action_chains, ActionChains.orig_send_keys_to_element, element, *keys_to_send).do_handle()

        ActionChains.orig_move_to_element = ActionChains.move_to_element
        ActionChains.move_to_element = lambda action_chains, element: ActionChainsMoveToElement(
            DriverUtils.get_current_driver(), action_chains, ActionChains.orig_move_to_element, element).do_handle()

        ActionChains.orig_move_to_element_with_offset = ActionChains.move_to_element_with_offset
        ActionChains.move_to_element_with_offset = lambda action_chains, element, x_offset, y_offset: ActionChainsMoveToElementOffset(
            DriverUtils.get_current_driver(), action_chains, ActionChains.orig_move_to_element_with_offset, element, x_offset, y_offset).do_handle()


class WebDriverWaitOverrider(object):
    @staticmethod
    def override():
        WebDriverWait.org_until = WebDriverWait.until
        WebDriverWait.until = lambda web_driver_wait, method, message = '': DriverWaitUntil(web_driver_wait, method, message, WebDriverWait.org_until).do_handle()
