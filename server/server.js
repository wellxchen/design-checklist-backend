var http = require("http"), fs = require("fs");

var methods = Object.create(null);

http.createServer(function(request, response) {
  function respond(code, body, type) {

    if (!type) type = "text/plain";

    response.writeHead(code, {"Content-Type": type, 
    						  "Access-Control-Allow-Origin" : "http://localhost:3000",
    						  "Access-Control-Allow-Methods": "GET,OPTIONS"});
    if (body && body.pipe)
      body.pipe(response);
    else
      response.end(body);
  }
  if (request.method in methods)
    methods[request.method](urlToPath(request.url),
                            respond, request);
  else
    respond(405, "Method " + request.method +
            " not allowed.");
}).listen(8000);

function urlToPath(url) {
  var path = require("url").parse(url).pathname;
  return "." + decodeURIComponent(path);
}

methods.GET = function(request, respond) {
  fs.stat(request, function(error, stats) {
    if (error && error.code == "ENOENT") {
      var PythonShell = require('python-shell');
      var pyshell = new PythonShell('server.py');
      pyshell.send(JSON.stringify(request));
      pyshell.on('message', function(message) {
        if (message === 'error') {
          respond(404, 'error');
        }
        else {
          respond(200, message); //json 
        }
      });
      pyshell.end(function(err) {
        if (err) {
          throw err;
        }
      });
    }
     
    else if (error)
      respond(500, error.toString());
    else if (stats.isDirectory())
      fs.readdir(path, function(error, files) {
        if (error)
          respond(500, error.toString());
        else
          respond(200, path);
      });
    else
      respond(200, fs.createReadStream(path),
              require("mime").lookup(path));
  });
};

methods.OPTIONS = function(request, respond) {
	 respond(200);
};

/*methods.DELETE = function(path, respond) {
  fs.stat(path, function(error, stats) {
    if (error && error.code == "ENOENT")
      respond(204);
    else if (error)
      respond(500, error.toString());
    else if (stats.isDirectory())
      fs.rmdir(path, respondErrorOrNothing(respond));
    else
      fs.unlink(path, respondErrorOrNothing(respond));
  });
};

function respondErrorOrNothing(respond) {
  return function(error) {
    if (error)
      respond(500, error.toString());
    else
      respond(204);
  };
}

methods.PUT = function(path, respond, request) {
  var outStream = fs.createWriteStream(path);
  outStream.on("error", function(error) {
    respond(500, error.toString());
  });
  outStream.on("finish", function() {
    respond(204);
  });
  request.pipe(outStream);
};*/



