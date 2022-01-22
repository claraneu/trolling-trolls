
function analyze(data){
  data = data["hatespeechPred"]
  console.log(data)
    let racist, sexist, hatespeech, neutral, negative, positive 
    [racist, sexist, hatespeech, neutral, negative, positive ] = data

  createCanvas()
  createBarChart(racist, sexist, hatespeech, neutral, negative, positive)

}

function createCanvas(){
    var childTag = document.createElement("canvas")
    childTag.setAttribute("id", "chart1")
    //childTag.setAttribute("width", "200")
    //childTag.setAttribute("height", "200")

    var parentTag = document.getElementById("top-left")
    parentTag.appendChild(childTag)


    var childTag = document.createElement("canvas")
    childTag.setAttribute("id", "chart2")
    // childTag.setAttribute("width", "200")
    // childTag.setAttribute("height", "200")

    
    var parentTag = document.getElementById("bottom-left")
    parentTag.appendChild(childTag)

}




function createBarChart(racist, sexist, hatespeech, neutral, negative, positive){

      const labels = ['Racist', 'Sexist', 'Hatespeech', 'Neutral', 'Negative', 'Positive'];
      const data = {
        labels: labels,
        datasets: [{
          label: 'Is this term loaded?',
          backgroundColor: [
            'rgba(133, 128, 200, 0.2)',
            'rgba(229, 33, 87, 0.2)',
            'rgba(133, 128, 200, 0.4)',
            'rgba(229, 33, 87, 0.4)',
            'rgba(133, 128, 200, 0.6)',
            'rgba(229, 33, 87, 0.6)',
            'rgba(133, 128, 200, 0.8)',
            'rgba(229, 33, 87, 0.8)'
          ],
          borderColor: [
            'rgb(133, 128, 200)',
            'rgb(229, 33, 87)',
            'rgb(133, 128, 200)',
            'rgb(229, 33, 87)',
            'rgb(133, 128, 200)',
            'rgb(229, 33, 87)',
            'rgb(133, 128, 200)',
            'rgb(229, 33, 87)'
          ],
          borderWidth: 1,
          data: [racist, sexist, hatespeech, neutral, negative, positive]
        }]
      };

      const config = {
        type: 'pie',
        data: data,
          options: {
            scales: {
              y: {
                beginAtZero: false
              }
          }
       },
      };


     


      const myChart = new Chart(
        document.getElementById('chart1'),
        config)

      const myChart2 = new Chart(
        document.getElementById('chart2'),
        config)

}



//When being used on the back end-
//module.exports = test, htmlCalling