const formActionMulti = document.querySelector("[form-action-multi]");
if (formActionMulti) {
  const checkAll = document.querySelector("[checkbox-all]");
  const checkBox = document.querySelectorAll("[checkbox]");
  checkAll.addEventListener("click", () => {
    if (checkAll.checked) {
      checkBox.forEach((check) => {
        check.checked = true;
      });
    } else {
      checkBox.forEach((check) => {
        check.checked = false;
      });
    }
  });

  checkBox.forEach((check) => {
    check.addEventListener("click", () => {
      const countChecked = document.querySelectorAll("[checkbox]:checked").length;
      if (countChecked == checkBox.length) {
        checkAll.checked = true;
      } else {
        checkAll.checked = false;
      }
    });
  });

  const buttonConfirm = formActionMulti.querySelector("[btn-confirm]");
  buttonConfirm.addEventListener("click", () => {
    const inputSelect = formActionMulti.querySelector('select')
    const selectValue = inputSelect.value
    if (selectValue === '') {
      alert('Vui lòng chọn hành động')
      return
    } else {
      const inputsChecked = document.querySelectorAll("[checkbox]:checked");
      if (inputsChecked.length > 0) {
        const confirmAction = confirm("Xác nhận hành động?");
        if (confirmAction) {
          ids = [];
          inputsChecked.forEach((input) => {
            const id = input.value;
            ids.push(id);
          });
          const inputSubmit = formActionMulti.querySelector("[ids]");
          inputSubmit.value = ids.join(", ");
          formActionMulti.submit();
        } else {
          return;
        }
      } else {
        alert("Vui lòng chọn bản nháp");
        return;
      }
    }
  });
}
