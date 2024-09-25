const btnAccept = document.querySelector("[btn-accept]");
if (btnAccept) {
  const divAccept = document.querySelector(".div-accept");
  const divPost = document.querySelector(".div-post");
  if (divAccept) {
    btnAccept.addEventListener("click", () => {
      divAccept.classList.remove('d-none')
    });
  }
  if (divPost) {
    btnAccept.addEventListener("click", () => {
      divPost.classList.remove('d-none')
    });
  }
}

const btnRequest = document.querySelector('[btn-request]')
if (btnRequest) {
  const divRequest = document.querySelector('.div-request')
  if (divRequest) {
    btnRequest.addEventListener('click', () => {
      divRequest.classList.remove('d-none')
    })
  }
}

const btnClose = document.querySelector('.fa-circle-xmark')
if (btnClose) {
  const divAccept = document.querySelector(".div-accept");
  if (divAccept) {
    btnClose.addEventListener('click', () => {
      divAccept.classList.add('d-none')
    })
  }
  const divPost = document.querySelector(".div-post");
  if (divPost) {
    btnClose.addEventListener('click', () => {
      divPost.classList.add('d-none')
    })
  }
}

const btnCloseReq = document.querySelector('#close')
if (btnCloseReq) {
  const divRequest = document.querySelector('.div-request')
  if (divRequest) {
    btnCloseReq.addEventListener('click', () => {
      divRequest.classList.add('d-none')
    })
  }
}

const formDelete = document.querySelector("[form-delete]");
if (formDelete) {
  const btnDelete = formDelete.querySelector("[btn-delete]");
  btnDelete.addEventListener("click", () => {
    confirmDelete = confirm("Xác nhận xóa bài viết?");
    if (confirmDelete) {
      formDelete.submit();
    }
  });
}

const formRefuse = document.querySelector("[form-refuse]");
if (formRefuse) {
  const btnRefuse = formRefuse.querySelector("[btn-refuse]");
  btnRefuse.addEventListener("click", () => {
    confirmRefuse = confirm("Xác nhận từ chối bản nháp?");
    if (confirmRefuse) {
      formRefuse.submit();
    }
  });
}

const formAccept = document.querySelector('.form-accept')
if (formAccept) {
  const btnSubmit= formAccept.querySelector('[btn-submit]')
  btnSubmit.addEventListener('click', () => {
    const selectEditor = formAccept.querySelector('.form-select')
    const editRequest = formAccept.querySelector('#id_content')
    const valueEditor = selectEditor.value
    const requestValue = editRequest.value
    if (valueEditor === '') {
      alert('Vui lòng chọn người chỉnh sửa')
      return
    } else if(requestValue === '') {
      alert('Vui lòng điền thông tin cần chỉnh sửa')
      return
    } else {
      const confirmSubmit = confirm('Xác nhận duyệt bài viết?')
      if (confirmSubmit) {
        formAccept.submit()
      }
    }
  })
}

const formPost = document.querySelector(".form-post");
if (formPost) {
  const btnPost= formPost.querySelector('[btn-post]')
  btnPost.addEventListener('click', () => {
    const startTime = formPost.querySelector('#start-time')
    const endTime = formPost.querySelector('#end-time')
    if (startTime.value === '' && endTime.value === '') {
      confirmPost = confirm('Đăng bài viết ở mọi khung giờ?')
      if (confirmPost) {
        formPost.submit()
      }
    } else if (startTime.value === '' || endTime.value === '') {
      alert('Chọn khung giờ đăng')
      return
    } else {
      confirmPost = confirm('Xác nhận đăng bài?')
      if (confirmPost) {
        formPost.submit()
      }
    }
  })
}

const formRequest = document.querySelector('.form-request')
if (formRequest) {
  const btnCmt = formRequest.querySelector('[btn-cmt]')
  btnCmt.addEventListener('click', () => {
    const editRequest = formRequest.querySelector('#id_content')
    const requestValue = editRequest.value
    if (requestValue === '') {
      alert('Vui lòng nhập yêu cầu sửa lại')
      return
    } else {
      formRequest.submit()
    }
  })
}

const labelText = document.querySelector('[for="id_content"]')
if (labelText) {
  labelText.classList.add('fw-semibold')
  labelText.classList.add('text-info')
  document.querySelector('#id_content').classList.add('form-control')
  document.querySelector('#id_content').setAttribute('placeholder', 'Nhập yêu cầu chỉnh sửa')
}