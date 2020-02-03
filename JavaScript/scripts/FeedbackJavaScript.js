var btn = document.getElementById("btn");
//play function

function play (){
    var audio = new Audio('song.mp3');
    audio.play();
};

//epochTime get

const now = Date.now();
var epochTime = now;
//Arrey of the correlation value
var Arrey = [];
Counter =0
  //play function
function play(){
    var audio = new Audio ('song.mp3');
    audio.play();
}
//jQuery

while (epochTime<now+1000) { //should be set to the button class but then the problem of computing...
    $.get('http://192.168.13.100/api/correlations/'+epochTime, function(data){
    let myValue= data.data[354708094967841].crosscorrelations[0].value;  //354708094967841 is one of the devices id 
    document.getElementById("demo").innerHTML +="<br/>"+ myValue ;      
    Arrey.push(myValue);
    console.log(Arrey);
    var sum =0;
    console.log(epochTime);
    if (Counter>=100 && Counter%100==0){ //after 0.1 second and only after each 0.1 second for now : should be set after the problem solved
        for ( i=Counter-100; i<Counter; i++)   
        sum = sum + Arrey[i];
        correlationAverage= sum/100;
        console.log(correlationAverage);  
        document.getElementById("correlationAverage").innerHTML +="<br/>"+ correlationAverage;  
        if (correlationAverage>0.01){ //set threshold
            btn.classList.remove("hide-me"); //if corrlation is high add the button
            //alert("the correlation is high");  // ----> to check the code
            
            
            
        }else{
           btn.classList.add("hide-me"); //if correlation is low remove button
            //alert("the correlation is low"); //-----> to check the code
        } 


        
    }
    
    
    console.log(Counter);
    Counter++;
    console.log(myValue);    //get data from value in async version
     });
     console.log("test");
     epochTime ++;
}



