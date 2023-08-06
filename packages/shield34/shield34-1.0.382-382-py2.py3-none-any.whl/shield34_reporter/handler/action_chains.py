from selenium.common.exceptions import StaleElementReferenceException

from shield34_reporter.handler import SeleniumMethodHandler
from shield34_reporter.model.csv_rows.actions.action_click_and_hold_csv_row import ActionClickAndHoldCsvRow, \
    ActionClickAndHoldElementCsvRow
from shield34_reporter.model.csv_rows.actions.action_click_csv_row import ActionClickCsvRow, ActionClickElementCsvRow
from shield34_reporter.model.csv_rows.actions.action_context_click_csv_row import ActionContextClickCsvRow, \
    ActionContextClickElementCsvRow
from shield34_reporter.model.csv_rows.actions.action_double_click_csv_row import ActionDoubleClickCsvRow, \
    ActionDoubleClickElementCsvRow
from shield34_reporter.model.csv_rows.actions.action_drag_and_drop_element_by_offset import \
    ActionDragAndDropElementByOffset
from shield34_reporter.model.csv_rows.actions.action_drag_and_drop_element_to_element_csv_row import \
    ActionDragAndDropElementToElementCsvRow
from shield34_reporter.model.csv_rows.actions.action_key_down_csv_row import ActionKeyDownCsvRow, \
    ActionKeyDownElementCsvRow
from shield34_reporter.model.csv_rows.actions.action_key_up_csv_row import ActionKeyUpElementCsvRow, ActionKeyUpCsvRow
from shield34_reporter.model.csv_rows.actions.action_move_by_offset_csv_row import ActionMoveByOffsetCsvRow
from shield34_reporter.model.csv_rows.actions.action_move_to_element_csv_row import ActionMoveToElementCsvRow
from shield34_reporter.model.csv_rows.actions.action_move_to_element_with_offset_csv_row import \
    ActionMoveToElementWithOffsetCsvRow
from shield34_reporter.model.csv_rows.actions.action_send_keys_csv_row import ActionSendKeysCsvRow, \
    ActionSendKeysWithElementCsvRow
from shield34_reporter.model.enums.action_name import ActionName


class ActionChainsClick(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, click_method, on_element=None):
        if on_element is None:
            super(ActionChainsClick, self).__init__(ActionName.ACTION_CLICK,
                                                    ActionClickCsvRow(driver))
        else:
            super(ActionChainsClick, self).__init__(ActionName.ACTION_CLICK_ELEMENT,
                                                    ActionClickElementCsvRow(driver, on_element))
        self.click = click_method
        self.driver = driver
        self.on_element = on_element
        self.action_chains = action_chains_obj

    def do_orig_action(self):
        self.click(self.action_chains, self.on_element)
        self._set_return_value(self.action_chains)
        return True


class ActionChainsClickAndHold(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, click_method, on_element=None):
        if on_element is None:
            super(ActionChainsClickAndHold, self).__init__(ActionName.ACTION_CLICK_AND_HOLD,
                                                           ActionClickAndHoldCsvRow(driver))
        else:
            super(ActionChainsClickAndHold, self).__init__(ActionName.ACTION_WEB_ELEMENT_CLICK_AND_HOLD,
                                                           ActionClickAndHoldElementCsvRow(driver, on_element))
        self.click_and_hold = click_method
        self.driver = driver
        self.on_element = on_element
        self.action_chains = action_chains_obj

    def do_orig_action(self):
        self.click_and_hold(self.action_chains, self.on_element)
        self._set_return_value(self.action_chains)
        return True


class ActionChainsContextClick(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, click_method, on_element=None):
        if on_element is None:
            super(ActionChainsContextClick, self).__init__(ActionName.ACTION_CONTEXT_CLICK, ActionContextClickCsvRow(driver))
        else:
            super(ActionChainsContextClick, self).__init__(ActionName.ACTION_WEB_ELEMENT_CONTEXT_CLICK,
                                                           ActionContextClickElementCsvRow(driver, on_element))
        self.context_click = click_method
        self.driver = driver
        self.on_element = on_element
        self.action_chains = action_chains_obj

    def do_orig_action(self):
        self.context_click(self.action_chains, self.on_element)
        self._set_return_value(self.action_chains)
        return True


class ActionChainsDoubleClick(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, click_method, on_element=None):
        if on_element is None:
            super(ActionChainsDoubleClick, self).__init__(ActionName.ACTION_DOUBLE_CLICK, ActionDoubleClickCsvRow(driver))
        else:
            super(ActionChainsDoubleClick, self).__init__(ActionName.ACTION_WEB_ELEMENT_DOUBLE_CLICK, ActionDoubleClickElementCsvRow(driver, on_element))
        self.double_click = click_method
        self.driver = driver
        self.on_element = on_element
        self.action_chains = action_chains_obj

    def do_orig_action(self):
        self.double_click(self.action_chains, self.on_element)
        self._set_return_value(self.action_chains)
        return True


class ActionChainsDragDropOffset(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, drag_method, source, xoffset, yoffset):

        super(ActionChainsDragDropOffset, self).__init__(ActionName.ACTION_DRAG_AND_DROP_ELEMENT_BY_OFFSET,
                                                ActionDragAndDropElementByOffset(driver, source, xoffset, yoffset))
        self.drag_and_drop_by_offset = drag_method
        self.driver = driver
        self.action_chains = action_chains_obj
        self.source = source
        self.xoffset = xoffset
        self.yoffset = yoffset

    def do_orig_action(self):
        self.drag_and_drop_by_offset(self.action_chains, self.source, self.xoffset, self.yoffset)
        self._set_return_value(self.action_chains)
        return True


class ActionChainsDragDrop(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, drag_method, source, target):
        super(ActionChainsDragDrop, self).__init__(ActionName.ACTION_DRAG_AND_DROP_ELEMENT_TO_ELEMENT,
                                                   ActionDragAndDropElementToElementCsvRow(driver, source, target))
        self.drag_and_drop = drag_method
        self.driver = driver
        self.action_chains = action_chains_obj
        self.source = source
        self.target = target

    def do_orig_action(self):
        self.drag_and_drop(self.action_chains, self.source, self.target)
        self._set_return_value(self.action_chains)
        return True


class ActionChainsKeyDown(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, key_down_method, value, on_element=None):
        if on_element is None:
            super(ActionChainsKeyDown, self).__init__(ActionName.ACTION_KEY_DOWN, ActionKeyDownCsvRow(driver, value))
        else:
            super(ActionChainsKeyDown, self).__init__(ActionName.ACTION_KEY_DOWN_ELEMENT,
                                                      ActionKeyDownElementCsvRow(driver, on_element, value))
        self.key_down = key_down_method
        self.driver = driver
        self.value = value
        self.on_element = on_element
        self.action_chains = action_chains_obj

    def do_orig_action(self):
        self.key_down(self.action_chains, self.value, self.on_element)
        self._set_return_value(self.action_chains)
        return True


class ActionChainsKeyUp(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, key_up_method, value, on_element=None):
        if on_element is None:
            super(ActionChainsKeyUp, self).__init__(ActionName.ACTION_KEY_UP, ActionKeyUpCsvRow(driver, value))
        else:
            super(ActionChainsKeyUp, self).__init__(ActionName.ACTION_KEY_UP_ELEMENT,
                                                      ActionKeyUpElementCsvRow(driver, on_element, value))
        self.key_up = key_up_method
        self.driver = driver
        self.value = value
        self.on_element = on_element
        self.action_chains = action_chains_obj

    def do_orig_action(self):
        self.key_up(self.action_chains, self.value, self.on_element)
        self._set_return_value(self.action_chains)
        return True


class ActionChainsMoveOffset(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, move_by_offset_method, xoffset, yoffset):
        super(ActionChainsMoveOffset, self).__init__(ActionName.ACTION_MOVE_BY_OFFSET, ActionMoveByOffsetCsvRow(driver, xoffset, yoffset))

        self.move_by_offset = move_by_offset_method
        self.driver = driver
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.action_chains = action_chains_obj

    def do_orig_action(self):
        self.move_by_offset(self.action_chains, self.xoffset, self.yoffset)
        self._set_return_value(self.action_chains)
        return True


class ActionChainsSendKeys(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, send_keys_method, *keys):
        super(ActionChainsSendKeys, self).__init__(ActionName.ACTION_SEND_KEYS, ActionSendKeysCsvRow(driver, *keys))

        self.send_keys = send_keys_method
        self.driver = driver
        self.keys = keys
        self.action_chains = action_chains_obj

    def do_orig_action(self):
        self.send_keys(self.action_chains, *self.keys)
        self._set_return_value(self.action_chains)
        return True


class ActionChainsSendKeysElement(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, send_keys_method, element, *keys):
        super(ActionChainsSendKeysElement, self).__init__(ActionName.ACTION_SEND_KEYS_ELEMENT,
                                                          ActionSendKeysWithElementCsvRow(driver, element, *keys))
        self.send_keys_to_element = send_keys_method
        self.driver = driver
        self.element = element
        self.keys = keys
        self.action_chains = action_chains_obj

    def do_orig_action(self):
        self.send_keys_to_element(self.action_chains, self.element, *self.keys)
        self._set_return_value(self.action_chains)
        return True


class ActionChainsMoveToElement(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, orig_method, element):
        super(ActionChainsMoveToElement, self).__init__(ActionName.ACTION_MOVE_TO_ELEMENT,
                                                        ActionMoveToElementCsvRow(driver, element))
        self.move_to_element = orig_method
        self.driver = driver
        self.element = element
        self.action_chains = action_chains_obj

    def do_orig_action(self):
        self.move_to_element(self.action_chains, self.element)
        self._set_return_value(self.action_chains)
        return True


class ActionChainsMoveToElementOffset(SeleniumMethodHandler):
    def __init__(self, driver, action_chains_obj, orig_method, element, xoffset, yoffset):
        super(ActionChainsMoveToElementOffset, self).__init__(ActionName.ACTION_MOVE_TO_ELEMENT_WITH_OFFSET,
                                                              ActionMoveToElementWithOffsetCsvRow(driver, element, xoffset, yoffset))
        self.move_to_element_with_offset = orig_method
        self.driver = driver
        self.element = element
        self.x_offset = xoffset
        self.y_offset = yoffset
        self.action_chains = action_chains_obj

    def do_orig_action(self):
        self.move_to_element_with_offset(self.action_chains, self.element, self.x_offset, self.y_offset)
        self._set_return_value(self.action_chains)
        return True