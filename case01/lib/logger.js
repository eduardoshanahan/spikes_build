var bunyan = require('bunyan');
var path = require('path');

function Logger(name) {
  var logFilePath = path.join('spikesBuild.log');// '/var/log/cvg/models.log'
  var result = bunyan.createLogger(
    {
      name:     name,
      streams: [
        {
          stream: process.stdout,
          level:  'debug'
        }
        ,{
          type:   'rotating-file',
          path:   logFilePath,
          period: '1d',   // daily rotation
          count:  4,        // keep 3 back copies
          level:  'info'
        }
      ],
      serializers: bunyan.stdSerializers
    }
  );
  result.debug('Logs file path is', logFilePath);
  return result;
}

module.exports = Logger;
