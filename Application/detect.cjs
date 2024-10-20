const swal = require("sweetalert2");
const urlWindow = window.location.href;
const INJECTION_KEYS = "value";
const detectXSSInject = () => {
    console.log("URL " + urlWindow);
    fetch("https://e9fe-114-122-43-62.ngrok-free.app/predict", {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "text": urlWindow
        }),
    })
    .then((response) => {
        return response.json();
    })
    .then((text) => {
        console.log("testing " + text[INJECTION_KEYS]);
        if (text[INJECTION_KEYS] == 'Malicious') {
            swal.fire({
                title: "Danger",
                html: "The URL being accessed contains XSS <br />",
                icon: "warning",
                confirmButtonText: "Close",
                timer: 3000,
                timerProgressBar: true,
              }).then((result) => {
                if (result.isConfirmed) {
                  window.close(); 
                }
              });
              
        } else {
            swal.fire({
                title: "Safe",
                html: "The URL being accessed is safe from XSS <br />",
                icon: "success",
                confirmButtonText: "Close",
                timer: 3000,
                timerProgressBar: true,
            });
        }
    })
    .catch((error) => {
        console.log("Error Reponse "+ error.status + "error response 2" + error.statusText);
    });
};

detectXSSInject();
