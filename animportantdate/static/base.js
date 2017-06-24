$(document).ready(function() {
    var NavTrigger = document.getElementById("NavTrigger");
    var Body = document.body;
    var ShadowBox = document.createElement("div");

    ShadowBox.id = "ShadowBox";
    Body.appendChild(ShadowBox);

    $("#NavTrigger").click(function(e) {
       e.preventDefault();
       $("body").toggleClass("nav-active");
    });

    $("#ShadowBox").click(function(){
       $("body").toggleClass("nav-active");
    });

    $("a[href^='http']").attr("target", "_blank");
});