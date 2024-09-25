const inputFields = document.querySelectorAll('input')
inputFields.forEach((input) => {
  if (input.getAttribute('type') !== 'checkbox') {
    input.classList.add('form-control')
  }
})
const gender = document.querySelector('#id_gender')
if (gender) {
  gender.classList.add('form-select')
}
const labelFields = document.querySelectorAll('label')
labelFields.forEach((label) => {
  label.classList.add('fw-semibold')
})

const group = document.querySelector('#id_groups')
if (group) {
  group.classList.add('form-select')
}
