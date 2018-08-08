var fancybox_opts = {
    fitToView   : false,
    scroll      : true,
    openEffect  : 'elastic',
    closeEffect : 'elastic',
    prevEffect  : 'none',
    nextEffect  : 'none',
    titleShow   : true,
    type        : 'image'
};

$(function(){

    $("a.open_fancybox").each(function(index, element){
        var anchor = $(element);
        var href = anchor.attr("href");
        if(href){
           $.getJSON(href, callback=function(jsonData){
               anchor.attr("href", "#");
               anchor.attr("data-href", href);
               anchor.attr("data-images", JSON.stringify(jsonData));
               for(var i=0;i<jsonData.length;i++){
                   var obj = jsonData[i];
                   var img = new Image();
                   img.src = obj["href"];
               }
           });
        }
    });

    $("a.open_fancybox").click(function(event){
        var anchor = $(event.currentTarget);
        var jsonImages = JSON.parse(anchor.attr("data-images"));
        if(jsonImages){
            $.fancybox.open(jsonImages, fancybox_opts);
        }
    });

});

