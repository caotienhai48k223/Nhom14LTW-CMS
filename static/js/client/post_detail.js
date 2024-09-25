const btnDlt = document.querySelector('[btn-delete-post]')
if (btnDlt) {
  btnDlt.addEventListener('click', () => {
    const confirmDlt = confirm('Chuyển bài viết vào thùng rác?')
    if (confirmDlt) {
      btnDlt.closest('form').submit()
    }
  })
}


const getCookie = (name) => {
  const cookies = document.cookie?.split(';') || []
  const cookie = cookies.find(c => c.trim().startsWith(`${name}=`))
  return cookie ? decodeURIComponent(cookie.trim().substring(name.length + 1)) : null
}

const csrftoken = getCookie('csrftoken')


const buttonEnjoy = document.querySelectorAll('[data-post-id]')
buttonEnjoy.forEach((button) => {
  button.addEventListener('click', (e) => {
    e.preventDefault()
    const postId = button.getAttribute('data-post-id')
    const postUserName = button.getAttribute('data-post-auth')
    const postSlug = button.getAttribute('data-post-slug')
    $.ajax({
      type: 'POST',
      url: `/post/${postUserName}/${postSlug}/`,
      data: {
        enjoy: postId,
        csrfmiddlewaretoken: csrftoken,
      },
      success: (res) => {
        if(res.status === 'added') {
          button.classList.remove('fa-regular')
          button.classList.add('fa-solid')
        } else {
          button.classList.remove('fa-solid')
          button.classList.add('fa-regular')
        }
      }
    })
  })
})
