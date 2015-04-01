const PORT = 80;
const ADDRESS = '0.0.0.0';

var http = require('http');

var server = http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('Hello World\n');
});

server.listen(PORT, ADDRESS, function () {
    console.log('Server running at http://%s:%d/', ADDRESS, PORT);
    console.lot('Press CTRL+C to exit');

    // Check if we are running as root
    // if (process.getgid() === 0) {
    //   process.setgid('nobody');
    //   process.setuid('nobody');
    // }
});

process.on('SIGTERM', function () {
  if (server === undefined) return;
  server.close(function () {
    // Disconnect from cluster master
    process.disconnect && process.disconnect();
  });
});
