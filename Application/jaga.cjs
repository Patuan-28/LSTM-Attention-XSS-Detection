const swal = require("sweetalert2");
const Wdw = window;
const urlWindow = Wdw.location.href; // mengambil URL web yang sedang diakses

var url = "http://127.0.0.1:8000/predict";
const detectXSSInject = () => {
    console.log("URL " + urlWindow);
    console.log("testing " + JSON.stringify({
        input_data: urlWindow  
    }));
    // fetch(url,  {
    //     method: 'POST',
    //     mode : 'no-cors',
    //     headers: {
    //         'Content-Type': 'application/json',
    //         'X-Requested-With': 'XMLHttpRequest',
    //         'Access-Control-Allow-Origin': url,
    //         'Accept': 'application/json'
    //     },
    //     body: JSON.stringify({
    //         input_data: urlWindow
    //     })
    // })
    // .then(response => {
    //     if (response.ok) {
    //         return response.json();
    //     } else {
    //         throw new Error('Network response was not ok.');
    //     }
    // })
    // .then(json => console.log(json))
    // .catch(error => console.error('Error:', error));
    fetch(url, {
        method: "POST",
        mode: "no-cors",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "input_data": urlWindow
        }),
    })
    .then((response) => {
        console.log("testing " +response.text());
        console.log("Response " + response.status + "response 2" + response.statusText);
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        // if (response.status === 200) {
        //     swal.fire({
        //         title: "XSS Detected!",
        //         text: "This website may be vulnerable to XSS attack",
        //         icon: "warning",
        //         confirmButtonText: "OK",
        //     });
        // }else{
        //     swal.fire({
        //         title: "XSS Not Detected!",
        //         text: "This website is safe from XSS attack",
        //         icon: "success",
        //         confirmButtonText: "OK",
        //     });
        // }
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                let json = JSON.parse(xhr.responseText);
                prediction = json.message;
                if(prediction == 'Malicious')
                {
                    swal.fire({
                        title: "Bahaya",
                        html: "Inputan anda dideteksi bersifat XSS Injection <br />",
                        icon: "warning",
                        confirmButtonText: "Tutup",
                        timer: 3000,
                        timerProgressBar: true,
                    });
                }
            } else {
                swal.fire({
                    title: "Aman",
                    html: "Inputan anda tidak dideteksi bersifat XSS Injection <br />",
                    icon: "success",
                    confirmButtonText: "Tutup",
                    timer: 3000,
                    timerProgressBar: true,
                });
            }
        };
    })
    .catch((response) => {
        console.log("Error Reponse "+ response.status + "error response 2" + response.statusText);
    });
};


detectXSSInject();
