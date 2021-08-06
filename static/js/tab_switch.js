function show(total,active){
    for(var i=1;i<total+1;i++){
        $("#tab"+i).removeClass("tab-title-active");
        $("#content"+i).hide();
    }
    $("#tab"+active).addClass("tab-title-active");
    $("#content"+active).show();
}