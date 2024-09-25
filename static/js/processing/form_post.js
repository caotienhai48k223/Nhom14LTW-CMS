const inputFields = document.querySelectorAll('input')
if (inputFields) {
  inputFields.forEach((input) => {
    if (input.getAttribute('type') !== 'checkbox') {
      input.classList.add('form-control')
    }
  })
}

const section = document.querySelector('#id_topic')
if (section) {
  section.classList.add('form-select')
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
