const inputFields = document.querySelectorAll('input')
if (inputFields) {
  inputFields.forEach((input) => {
    if (input.getAttribute('type') !== 'checkbox') {
      input.classList.add('form-control')
    }
  })
}
const topic = document.querySelector('#id_section') 
if (topic) {
  topic.classList.add('form-select')
}
const textarea =  document.querySelector('textarea')
if (textarea) {
  textarea.removeAttribute('required')
}
const labelFields = document.querySelectorAll('label')
if (labelFields) {
  labelFields.forEach((label) => {
    label.classList.add('fw-semibold')
  })
}


const formUpdate = document.querySelector('[form-update]')
if (formUpdate) {
  const btnSend = formUpdate.querySelector('[btn-send]')
  if (btnSend) {
    btnSend.addEventListener('click', () => {
      const confirmSend = confirm('Xác nhận gửi bản nháp đến Tổng biên tập?')
      if (confirmSend) {
        const inputHidden = formUpdate.querySelector('[hidden]')
        inputHidden.value = 'send'
        formUpdate.submit()
      }
    })
  }
  const btnSubmit = formUpdate.querySelector('[btn-turnon]')
  if (btnSubmit) {
    btnSubmit.addEventListener('click', () => {
      const confirmSubmit = confirm('Xác nhận gửi bài viết đến Tổng biên tập?')
      if (confirmSubmit) {
        const inputHidden = formUpdate.querySelector('[hidden]')
        inputHidden.value = 'turnon'
        formUpdate.submit()
      }
    })
  }
}