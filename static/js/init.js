$(document).ready(function () {

      console.log('Paul Wasilewicz 1007938')

      obj = {};
  
      $("#convertBut").click(function(){
        console.log("IN HERE")
        input = $('#selectField').val();
        console.log(input)
        obj.cur = input;
        
        
        $.ajax({
          type:"POST",
          data: JSON.stringify(obj),
          contentType:"application/json",
          dataType:"json",
          url:"/coinBaseSearch",
          async:false,
                  
          success: function(data){
            if(data.error == 'success'){
              if($('#sellPrice').is(':checked')){
                $("#responseTextSell").html("Sell Price of 1 "+data.base+" is "+data.sellAns+" in "+data.currency)
                $("#responseText").html("");
              }
              if($('#spotPrice').is(':checked')){
                $("#responseTextSpot").html("Spot price of 1 "+data.base+" is "+data.spotAns+" in "+data.currency)
                $("#responseText").html("");
              }
              if($('#buyPrice').is(':checked')){
                $("#responseTextBuy").html("Buy price of 1 "+data.base+" is "+data.buyAns+" in "+data.currency)
                $("#responseText").html("");
              }
            }
            else if(data.error='invalid'){
              $("#responseText").html("Error could not find Crypto Currency");
              $("#responseTextSell").html("");
              $("#responseTextSpot").html("");
              $("#responseTextBuy").html("");
            }
          },
          fail: function(error){
            alert(error);
          }
        });
      });

    $("#amountBut").click(function(){
      input = $('#toDisplay').val();
      obj.amount = input

      $.ajax({
        type:"POST",
        data: JSON.stringify(obj),
        contentType:"application/json",
        dataType:"json",
        url:"/coinMarketCap",
        async:false,
                
        success: function(data){
            $("#coinTable tbody tr").remove()
            name = ''
            symbol = ''
            tag = ''
            maxSup = ''
            cirSup = ''
            totSup = ''
            rank = ''
            marCap = ''
            for(i=0;i<data.data.length;i++){
              //console.log(data.data[i].name)
              name = data.data[i].name
              symbol = data.data[i].symbol
              tag = data.data[i].tags[0]
              if(tag == undefined){
                tag = 'None'
              }
              maxSup = data.data[i].max_supply
              if(maxSup == null){
                maxSup = 'None'
              }
              cirSup = data.data[i].circulating_supply
              totSup = data.data[i].total_supply
              rank = data.data[i].cmc_rank
              marCap = data.data[i].quote.USD.market_cap
              $('#coinTable').append('<tr><td>'+name+'</td><td>'+symbol+'</td><td>'+rank+'</td><td>'+maxSup+'</td><td>'+cirSup+'</td><td>'+totSup+'</td><td>'+tag+'</td><td>'+marCap+'</td></tr>')
            }
        },
        fail: function(error){
          alert(error);
        }
      });
    });
    });
    