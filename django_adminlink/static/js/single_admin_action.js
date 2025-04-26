/**
 * Selects a single item in a Django admin list and triggers the specified admin action for that item.
 *
 * Retrieves the primary key and action from the provided element's data attributes, updates the action selector, unchecks all other items, checks the targeted item, and submits the form to perform the action on that item only.
 *
 * @param {Element} e - The element containing `data-pk` and `data-action` attributes for the target item and action.
 */
function get_checkboxes(e) {
    const pk = e.getAttribute('data-pk');
    const action = e.getAttribute('data-action');
    const actionSelector = document.querySelector(`select[name=action]`);
    if(actionSelector == null) {
        return;
    }
    for(const acrossInput of document.querySelectorAll('div.actions input.select-across')) {
        acrossInput.value = 0;
    }
    actionSelector.value = action;
    for(const item of document.querySelectorAll('input.action-select[type=checkbox]')) {
      item.checked = false;
    }
    const item = document.querySelector(`input.action-select[type=checkbox][value="${pk}"]`);
    if(item == null) {
        return;
    }
    item.checked = true;
    item.form.submit();
}