import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

PAGE="""\
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
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

# 4 fps = 6 Mbps
#24 fps = 18 Mbps
with picamera.PiCamera(resolution='1280x720', framerate=30) as camera:
    camera.rotation = 0
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 2500)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()

