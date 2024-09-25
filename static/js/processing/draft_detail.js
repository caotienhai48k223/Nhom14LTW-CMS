const formDelete = document.querySelector("[form-delete]");
if (formDelete) {
  const btnDelete = formDelete.querySelector("[btn-delete]");
  btnDelete.addEventListener("click", () => {
    confirmDelete = confirm("Xác nhận xóa bản nháp?");
    if (confirmDelete) {
      formDelete.submit();
    }
  });
}

const formSend = document.querySelector('[form-send]')
if (formSend) {
  const buttonSend = formSend.querySelector('[btn-send]')
  buttonSend.addEventListener('click', () => {
    const confirmSend = confirm('Xác nhận gửi bản nháp đến Tổng biên tập?')
    if (confirmSend) {
      formSend.submit()
    }
  })
}
