check_iperf()

async function start_iperf() {
  let buttonDirectionChecker
  if (document.getElementById("buttonDirection").checked) {
    buttonDirectionChecker = '&buttonDirection=on'
  } else {
    buttonDirectionChecker = ''
  }
  let response = await fetch("/", {
    method: "post",
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: 'formTrafficValue=' + 
      document.getElementById("formTrafficValue").value +
      '&formTrafficTimer=' + document.getElementById("formTrafficTimer").value +
      buttonDirectionChecker
  })
  if (response.status == 200) {
    json_response = await response.json()
    console.log(json_response);
    check_iperf()
  } else {
    throw new HttpError(response);
  }
}

async function stop_iperf() {
  let response = await fetch("/stop")
  if (response.status == 200) {
    json_response = await response.json()
    console.log(json_response);
    check_iperf()
  } else {
    throw new HttpError(response);
  }
}

async function check_iperf() {
  let response = await fetch("/check")
  if (response.status == 200) {
    json_response = await response.json()
    console.log(json_response);
    if (json_response.answer == '') {
      document.getElementById("startButton").removeAttribute("disabled")
      document.getElementById("stopButton").setAttribute("disabled", "")
    } else {
      document.getElementById("stopButton").removeAttribute("disabled")
      document.getElementById("startButton").setAttribute("disabled", "")
    }
  } else {
    throw new HttpError(response);
  }
}