const url = window.location.href

const testBox = docuemt.getElementById('quiz-box')
let data

$.ajax({
    type: 'GET',
    url: `${url}data`,
    success: function(response){
        console.log(response)
        data = response.data
        data.array.forEach(element => {
            for (const [question, answers] of Object.entries(element)){
                testBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${question}</b>
                    </div>
                `
            }
        });
    },
    error: function(error){
        console.log(error)
    }
})