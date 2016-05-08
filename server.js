var connect = require('connect');
var serveStatic = require('serve-static');
connect().use(serveStatic("demo")).listen(8085, function(){
    console.log('Server running on 8085...');
});