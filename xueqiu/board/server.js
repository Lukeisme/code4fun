var express = require('express'),
    mongodb = require('mongodb');

var MongoClient = require('mongodb').MongoClient;
var url = 'mongodb://localhost:27017/xueqiu';

docsTotal = [];
docsMonth1 = [];
docsMonth2 = [];
docsMonth3 = [];
docsWeibo  =[];
var getData = function(collect, attr, docname){
    return new Promise(function(resolve, reject){
        MongoClient.connect(url, function(err, db) {
            var cursor = eval('db.collection(collect).find({ "$and" :[{'+attr+':{"$ne":"null"}},{'+attr+':{"$ne":0}}]}).sort({'+attr+':-1})');
            cursor.each(function(err, doc){
                if(doc != null){
                    eval(docname+'.push(doc)');
                }else{
                    db.close();
                    resolve();
                }
                if(err !=null) 
                    reject(err);
            });
        });
    });
}
var getCubesV = function(cb){
    getData('cubesmonth','m1','docsMonth1').then(function(){
        return getData('cubesmonth','m2','docsMonth2');
    },function(err){
        console.log(err);
    }).then(function(){
        return getData('cubesmonth','m3','docsMonth3');
    },function(err){
        console.log(err);
    }).then(function(){
        return getData('cubes','total_gain','docsTotal');
    },function(err){
        console.log(err);
    }).then(function(){
        cb&&cb(docsTotal,docsMonth1,docsMonth2,docsMonth3);
    },function(err){
        console.log(err);
    });
}

var app = express();
app.get('/distribute', function(req, res){
    docsTotal  =[];
    getData('cubes','total_gain','docsTotal').then(function(){
        var upper = docsTotal[0]['total_gain'];
        var lower = Math.floor(docsTotal[0]['total_gain'])-1;
        var num = 0;
        var distri = [];
        for(var i =0 ; i< docsTotal.length; i++){
            if(docsTotal[i]['total_gain']>lower&&docsTotal[i]['total_gain']<=upper){
                num++;
            }else{
                upper = docsTotal[i]['total_gain'];
                lower = Math.floor(docsTotal[i]['total_gain'])-1;
                distri.push({"x":Math.floor(docsTotal[i]['total_gain']),"y":num});
                num = 1;
            }
        }
        res.end(JSON.stringify(distri));
    },function(err){
        console.log(err);
    })
});
app.get('/wrank', function(req, res){
    docsWeibo  =[];
    getData('weibosvalue','trust','docsWeibo').then(function(){
        res.end(JSON.stringify(docsWeibo));
    },function(err){
        console.log(err);
    })
});
app.get('/intersect/:itype?', function(req, res){
    docsTotal=[]
    docsMonth1 = [];
    docsMonth2 = [];
    docsMonth3 = [];
    getCubesV(function(docsTotal, docsMonth1, docsMonth2, docsMonth3){
        var topT = docsTotal.slice(0, 170);
        var top1 = docsMonth1.slice(0, 162);
        var top2 = docsMonth2.slice(0, 165);
        var top3 = docsMonth3.slice(0, 170);
        var common = [];
        if(req.params.itype.toString()=='678'){
            for(var i in top1){
                var topper1 = top1[i];
                for(var j in top2){
                    var topper2 = top2[j];
                    for(var k in top3){
                        var topper3 = top3[k];
                        if(topper1['user_id']==topper2['user_id']&&topper2['user_id']==topper3['user_id']){
                            common.push({'uid': topper1['user_id'],'nickname' :topper1['nickname']});
                        }
                    }
                }
            }
        }
        if(req.params.itype.toString()=='67t'){
            for(var i in top1){
                var topper1 = top1[i];
                for(var j in top2){
                    var topper2 = top2[j];
                    for(var k in topT){
                        var topper3 = topT[k];
                        if(topper1['user_id']==topper2['user_id']&&topper2['user_id']==topper3['user_id']){
                            common.push({'uid': topper1['user_id'],'nickname' :topper1['nickname']});
                        }
                    }
                }
            }
        }
        if(req.params.itype.toString()=='78t'){
            for(var i in topT){
                var topper1 = topT[i];
                for(var j in top2){
                    var topper2 = top2[j];
                    for(var k in top3){
                        var topper3 = top3[k];
                        if(topper1['user_id']==topper2['user_id']&&topper2['user_id']==topper3['user_id']){
                            common.push({'uid': topper1['user_id'],'nickname' :topper1['nickname']});
                        }
                    }
                }
            }
        }
        res.end(JSON.stringify(common));
    });
});
app.get('/raw', function(req, res){
    docsTotal=[]
    docsMonth1 = [];
    docsMonth2 = [];
    docsMonth3 = [];
    getCubesV(function(docsTotal, docsMonth1, docsMonth2, docsMonth3){
        var ranklists ={'6':docsMonth1, '7':docsMonth2, '8':docsMonth3, 'total':docsTotal}
        res.end(JSON.stringify(ranklists));
    });
    
});
app.listen(9000);
