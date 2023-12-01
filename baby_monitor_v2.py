<html>
<head>
<style>
    
    h1 {text-align: center}
    
    p {
        text-align: center;
        border-style: outset;
        border-width: 5px;
        border-color: black;
        border-radius: 10px;
        width: 1920px;
        margin-left: 300px;
    }
    
    body {
        background-image: url('https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwallpaperaccess.com%2Ffull%2F340554.png&f=1&nofb=1&ipt=4666bea54fdad35e973f639bad15415b10864756249bf1f5675b2bd18cbbd1ec&ipo=images');
        background-repeat: no-repeat;
        background-attachment: fixed;  
        background-size: cover;
    }
    
    .container{
        width: 100%;
        height: 90vh;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }
    
    .container h2 {
        position: absolute;
        top: 5%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: #fff;
        font-size: 45px;
        font-weight: 600;
        letter-spacing: 2px;
        background-color: rgba(0,0,0,0.5);
    }
    
    
</style>
    <title> CSU CS370 Term Project Fall 2023: Baby Monitor </title>
</head>

<body>
<h1> CS370 Term Project Fall 2023: Baby Monitor </h1>
    <div class="container">
        <p>
            <img src="stream.mjpg" width="1920" height="1080"/>
            <h2 id="current-time"> 12:00:00 </h2>
        </p>
        <button id="recordButton"> Record video </button>
    </div>
<script>
    let time = document.getElementById("current-time");
    setInterval(() => {
    
        let d = new Date();
        time.innerHTML = d.toLocaleTimeString();
        
        }, 1000);

    let button = document.getElementById("recordButton")
    button.addEventListener("click", async function() {
        let stream = await navigator.mediaDevices.getDisplayMedia({
            video: true
        })
        const mime = MediaRecorder.isTypeSupported("video/webm; codecs=vp9")
            ? "video/webm; codecs=vp9"
            : "video/webm"
        let recorder = new MediaRecorder(stream, {
            mimeType: mime
        })

        let chunks = []
        recorder.addEventListener("dataavailable", function(e) {
            chunks.push(e.data)
        })
        recorder.addEventListener("stop", function() {
            let blob = new Blob(chunks, {
                type: chunks[0].type
            })

            let x = document.createElement("a")
            x.href = URL.createObjectURL(blob)
            x.download = "BabyMonitor_Footage.webm"
            x.click()
        })
        recorder.start()
    });

</script>
</body>
</html>
