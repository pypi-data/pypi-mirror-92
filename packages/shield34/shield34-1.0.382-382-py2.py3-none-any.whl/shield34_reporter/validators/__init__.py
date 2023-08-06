from shield34_reporter.dynamic_locator.element_dynamic_locator import ElementDynamicLocator


def validate_current_find_element_worked_in_previous_runs(by, value):
    current_find_element_descriptor = ElementDynamicLocator.get_current_find_element_dynamic_locator_descriptor()
    element_locator = by + ": " + value
    if current_find_element_descriptor is not None:
        if element_locator == current_find_element_descriptor['locator']:
            if current_find_element_descriptor['xpath_with_id'] != '' \
                    or current_find_element_descriptor['xpath_with_index'] != '' or len(
                current_find_element_descriptor['attributes']) != 0:
                return True
    return False