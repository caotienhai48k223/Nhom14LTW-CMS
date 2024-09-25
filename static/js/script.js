const showAlert = document.querySelector("[show-alert]")
if (showAlert) {
  const time = parseInt(showAlert.getAttribute("date-time"))
  const closeAlert = showAlert.querySelector(".close-alert")
  setTimeout (() => {
    showAlert.classList.add("alert-hidden")
  }, time)
  closeAlert.addEventListener('click', () => {
    showAlert.classList.add("alert-hidden")
  })
}