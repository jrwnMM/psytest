const registerForm = document.getElementById('registerForm')
//const deptDataBox = document.getElementById('dept-data-box')
const deptDataBox = document.getElementById('departmentID')
const deptInput = document.getElementById('dept')
const progDataBox = document.getElementById('prog-data-box')
const progInput = document.getElementById('prog')
const yearDataBox = document.getElementById('year-data-box')
const yearInput = document.getElementById('year')
const btnBox = document.getElementById('btn-box')
const alertBox = document.getElementById('alert-box')
const yearText = document.getElementById('year-text')
const progText = document.getElementById('prog-text')
const deptText = document.getElementById('dept-text')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

$.ajax({
    type: 'GET',
    url: "/dept-json/",
    success: function(response){
        console.log(response.data)
        const deptData = response.data
        deptData.map(item=>{
//            const option = document.createElement('div')
//            option.textContent = item.name
//            option.setAttribute('class', 'item')
//            option.setAttribute('data-value', item.name)
//            deptDataBox.appendChild(option)
            const option = document.createElement('option')
            option.textContent = item.name
            option.setAttribute('value', item.name)
            deptDataBox.appendChild(option)
        })
    },
    error: function(error){
        console.log(error)
    }
})
//
//deptInput.addEventListener('change', e=>{
//    console.log(e.target.value)
//    const selectedDept = e.target.value
//
//    alertBox.innerHTML=""
//    progDataBox.innerHTML = ""
//    progText.textContent = "Choose a program"
//    progText.classList.add("default")
//
//progInput.addEventListener('change', e=>{
//    console.log(e.target.value)
//    const selectedProg = e.target.value
//
//    alertBox.innerHTML=""
//    yearDataBox.innerHTML = ""
//    yearText.textContent = "Choose grade/year Level"
//    yearText.classList.add("default")
//
//    $.ajax({
//        type: 'GET',
//        url: `prog-json/${selectedDept}/`,
//        success: function(response){
//            console.log(response.data)
//            const progData = response.data
//            progData.map(item=>{
//                const option = document.createElement('div')
//                option.textContent = item.name
//                option.setAttribute('class', 'item')
//                option.setAttribute('data-value', item.name)
//                progDataBox.appendChild(option)
//            })
//
//            progInput.addEventListener('change', e=>{
//                btnBox.classList.remove('not-visible')
//            })
//        },
//        error: function(error){
//            console.log(error)
//        }
//    })
//})
//
//    $.ajax({
//        type: 'GET',
//        url: `year-json/${selectedProg}/`,
//        success: function(response){
//            console.log(response.data)
//            const yearData = response.data
//            yearData.map(item=>{
//                const option = document.createElement('div')
//                option.textContent = item.name
//                option.setAttribute('class', 'item')
//                option.setAttribute('data-value', item.name)
//                yearDataBox.appendChild(option)
//            })
//
//            yearInput.addEventListener('change', e=>{
//                btnBox.classList.remove('not-visible')
//            })
//        },
//        error: function(error){
//            console.log(error)
//        }
//    })
//})
//
//registerForm.addEventListener('submit', e=>{
//    e.preventDefault()
//    console.log('submitted')
//
//    $.ajax({
//        type: 'POST',
//        url: '/create/',
//        data: {
//            'csrfmiddlewaretoken': csrf[0].value,
//            'dept': deptText.textContent,
//            'prog': progText.textContent,
//            'year': yearText.textContent,
//        },
//        success: function(response){
//            console.log(response)
//            alertBox.innerHTML = `<div class="ui positive message">
//                                    <div class="header">
//                                    Success
//                                    </div>
//                                    <p>Your profile has been registered</p>
//                                </div>`
//        },
//        error: function(error){
//            console.log(error)
//            alertBox.innerHTML = `<div class="ui negative message">
//                                    <div class="header">
//                                    Oops!
//                                    </div>
//                                    <p>Something went wrong</p>
//                                </div>`
//        }
//    })
//})
