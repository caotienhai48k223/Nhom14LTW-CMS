const formActionMulti = document.querySelector('[form-action-multi]')
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

  const selectInput = formActionMulti.querySelector('select')
  const selectTime = formActionMulti.querySelector('[select-time]')
  selectInput.addEventListener('change', () => {
    const valueSelect = selectInput.value
    if (valueSelect === 'post') {
      selectTime.classList.remove('d-none')
    } else {
      if (!selectTime.classList.contains('d-none')) {
        selectTime.classList.add('d-none')
      }
    }
  })

  const buttonConfirm = formActionMulti.querySelector('[btn-confirm]')
  buttonConfirm.addEventListener('click', () => {
    const valueSelect = selectInput.value
    if (valueSelect === '') {
      alert('Vui lòng chọn hành động')
    } else if (valueSelect === 'post') {
      const selectStartTime = formActionMulti.querySelector('#start_time')
      const selectEndTime = formActionMulti.querySelector('#end_time')
      const inputsChecked = document.querySelectorAll('[checkbox]:checked')
      if (inputsChecked.length > 0) {
        if (selectStartTime.value === '' && selectEndTime.value === '') {
          confirmNoTime = confirm('Đăng ở tất cả khung giờ trong ngày ?')
          if (confirmNoTime) {
            const confirmAction = confirm('Xác nhận hành động?')
            if (confirmAction) {
              ids = []
              inputsChecked.forEach((input) => {
                const id = input.value
                ids.push(id)
              })
              const inputSubmit = formActionMulti.querySelector('[ids]')
              inputSubmit.value = ids.join(', ');
              formActionMulti.submit()
            }
          }
        } else if (selectStartTime.value === '' || selectEndTime.value === '') {
          alert('Vui lòng chọn giờ đăng tải')
          return
        } else {
          const confirmAction = confirm('Xác nhận hành động?')
          if (confirmAction) {
            ids = []
            inputsChecked.forEach((input) => {
              const id = input.value
              ids.push(id)
            })
            const inputSubmit = formActionMulti.querySelector('[ids]')
            inputSubmit.value = ids.join(', ');
            formActionMulti.submit()
          }
        }
      } else {
        alert('Vui lòng chọn bài đăng')
        return
      }
    } else {
      const selectStartTime = formActionMulti.querySelector('#start_time')
      const selectEndTime = formActionMulti.querySelector('#end_time')
      selectStartTime.name = ''
      selectStartTime.value = ''
      selectEndTime.name = ''
      selectEndTime.value = ''
      const inputsChecked = document.querySelectorAll('[checkbox]:checked')
      if (inputsChecked.length > 0) {
        const confirmAction = confirm('Xác nhận hành động?')
        if (confirmAction) {
          ids = []
          inputsChecked.forEach((input) => {
            const id = input.value
            ids.push(id)
          })
          const inputSubmit = formActionMulti.querySelector('[ids]')
          inputSubmit.value = ids.join(', ');
          formActionMulti.submit()
        }
      } else {
        alert('Vui lòng chọn bài đăng')
        return
      }
    }
  })
}