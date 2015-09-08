var swig = require('swig'),
    express = require('express'),
    mongodb = require('mongodb');

var MongoClient = require('mongodb').MongoClient;
var url = 'mongodb://localhost:27017/xueqiu';

var getCubesV = function(cb){
    docsTotal = [];
    docsMonth = [];
    MongoClient.connect(url, function(err, db) {
        var cursor = db.collection('cubes').find().sort({'annualized_gain_rate':-1}).limit(50);
        cursor.each(function(err, doc){
            if(doc != null){
                docsTotal.push(doc)
            }else{
                db.close();
                MongoClient.connect(url, function(err, db) {
                    var cursorM = db.collection('cubes').find().sort({'monthly_gain':-1}).limit(50);
                    cursorM.each(function(err, docM){
                        if(docM != null){
                            docsMonth.push(docM)
                        }else{
                            db.close();
                            cb&&cb(docsTotal,docsMonth);
                        }
                    });
                });
            }
        });
    });
}


var app = express();
app.get('/', function(req, res){
    getCubesV(function(docsTotal, docsMonth){
        var tmpl = swig.compileFile(__dirname + '/template.html'),
            renderedHtml = tmpl({
                cubesVTotal: docsTotal,
                cubesVMonth: docsMonth,
                title: '股票数据'
            });
     
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(renderedHtml);
    })
    
});
app.listen(9000);
