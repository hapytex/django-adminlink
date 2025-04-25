function get_checkboxes(action, pk) {
    document.querySelector(`select[name=action]`).value = action;
    for(const item of document.querySelectorAll('input.action-select[type=checkbox]')) {
      item.checked = false;
    }
    const item = document.querySelector(`input.action-select[type=checkbox][value="${pk}"]`);
    item.checked = true;
    item.form.submit();
}