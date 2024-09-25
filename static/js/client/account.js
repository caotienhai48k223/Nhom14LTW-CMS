const buttonUpdate = document.querySelector('[btn-update-group]')
if (buttonUpdate) {
  const formUpdate = document.querySelector('[form-update-group]')
  buttonUpdate.addEventListener('click', () => {
    formUpdate.classList.toggle('d-none')
  })
  formUpdate.querySelector('.helptext').remove()
  formUpdate.querySelector('label').classList.add('fw-semibold')
}

