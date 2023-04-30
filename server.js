const express = require('express')
const spawn = require("child_process").spawn;
const { networkInterfaces } = require('os');
var path = require('path')
const app = express()

app.use(express.urlencoded({ extended: true }))

app.set('view engine', 'ejs')
app.use(express.static(path.join(__dirname, 'public')));

var queueList = []
var pythonProcessRunning = false 

/*
    Server functions start here
*/

app.get("/", (req, res) => {

    res.render("index")

})

app.post("/", (req, res) => {

    // When the button is clicked, we change the photo on the screen 
    if (req.body.hasOwnProperty("first")) {
        queueList.push("1")
        if (!pythonProcessRunning) {
            manageQueue()
        }
    } else if (req.body.hasOwnProperty("second")) {
        queueList.push("2")
        if (!pythonProcessRunning) {
            manageQueue()
        }
    } else if (req.body.hasOwnProperty("third")) {
        queueList.push("3")
        if (!pythonProcessRunning) {
            manageQueue()
        }
    } else {
        console.log("Issue identifying button types")
    }
    
})

function manageQueue() {

    pythonProcessRunning = true 
    var updateFramePythonProcess

    while (queueList.length > 0) {
    
        if (queueList[0] == "1") {
            updateFramePythonProcess = spawn('python3', ["./updateFrame1.py"])
        } else if (queueList[0] == "2") {
            updateFramePythonProcess = spawn('python3', ["./updateFrame2.py"])
        } else if (queueList[0] == "3") {
            updateFramePythonProcess = spawn('python3', ["./updateFrame3.py"])
        } else {
            console.log("Couldn't identify python process type")
            return 
        }

        updateFramePythonProcess.stdout.on('data', (data) => {
            console.log(data.toString('utf8'))
        });

        updateFramePythonProcess.stderr.on('data', (data) => {
            console.log(data.toString('utf8'))
        });
    
        updateFramePythonProcess.on('exit', function () {
            queueList.shift()
        })
    
    }

    pythonProcessRunning = false 

}

function getIPAddress() {
    
    // Change IP address name depending on Linux or Mac 
    var IPaddress_dev_name = "wlan0"

    // Open webserver to the local network 
    const nets = networkInterfaces();
    const results = Object.create(null);

    for (const name of Object.keys(nets)) { // Grabs local ip address
        for (const net of nets[name]) {
            // Skip over non-IPv4 and internal (i.e. 127.0.0.1) addresses
            // 'IPv4' is in Node <= 17, from 18 it's a number 4 or 6
            const familyV4Value = typeof net.family === 'string' ? 'IPv4' : 4
            if (net.family === familyV4Value && !net.internal) {
                if (!results[name]) {
                    results[name] = [];
                }
                results[name].push(net.address);
            }
        }
    }

    console.log(results)

    return results[IPaddress_dev_name][0]

}

function openPort(port_number) {
    
    var ipaddress = getIPAddress()

    app.listen(`${port_number}`, `${ipaddress}`, () => {

        console.info(`Server started on port ${ipaddress}:3000`); 

    })

}

openPort(3000);