

// function test(){
//     console.log("hi, vis can be called from the index route")
// } 
// function htmlCalling(data){

//     console.log(data)
// }


function analyze(data){
    let numOfUnknown = Number(0)
    let numOfKnown = Number(0)
    for (let i = 0; i < data.length; i ++){
        if (data[i]["user"] == "unknown"){
            numOfUnknown = numOfUnknown +1
        }else {numOfKnown = numOfKnown +1}    
    }
    console.log(racist, sexist, hatespeech, neutral, negative, positive)

  createCanvas()
  createBarChart(racist, sexist, hatespeech, neutral, negative, positive)
}

function createCanvas(){
    var childTag = document.createElement("canvas")
    var parentTag = document.getElementById("dashi")
    parentTag.appendChild(childTag)

}

function createBarChart(racist, sexist, hatespeech, neutral, negative, positive){

      const labels = ['racist', 'sexist', 'hatespeech', 'neutral', 'negative', 'positive'];
      const data = {
        labels: labels,
        datasets: [{
          label: 'My First Dataset',
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(255, 159, 64, 0.2)'
   
          ],
          borderColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 159, 64)'
          ],
          borderWidth: 1,
          data: [barOne, barTwo]
        }]
      };

      const config = {
        type: 'bar',
        data: data,
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        },
      };
      const myChart = new Chart(
        document.getElementsByTagName('canvas'),
        config)
}



//When being used on the back end-
//module.exports = test, htmlCalling