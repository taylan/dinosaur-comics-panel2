var spinnerOpts = {
  lines: 11, // The number of lines to draw
  length: 12, // The length of each line
  width: 9, // The line thickness
  radius: 21, // The radius of the inner circle
  corners: 0.8, // Corner roundness (0..1)
  rotate: 10, // The rotation offset
  direction: 1, // 1: clockwise, -1: counterclockwise
  color: '#ddd', // #rgb or #rrggbb or array of colors
  speed: 0.9, // Rounds per second
  trail: 50, // Afterglow percentage
  shadow: false, // Whether to render a shadow
  hwaccel: true, // Whether to use hardware acceleration
  className: 'spinner', // The CSS class to assign to the spinner
  zIndex: 2e9, // The z-index (defaults to 2000000000)
  top: 'auto', // Top position relative to parent in px
  left: 'auto' // Left position relative to parent in px
};

var spinners = new Array(6);

function doRandomPanel(panel, callback) {
    $("#dc-panel-"+panel).html('');
    spinners[panel-1] = new Spinner(spinnerOpts).spin($("#dc-panel-"+panel)[0]);
    $.get('/a/random-panel/' + panel)
        .done(function(data){
            $('#dc-panel-'+panel).html($.Mustache.render('single-panel-template', data));
        })
        .always(function(){
            spinners[panel-1].stop();
            console.log(typeof callback);
            if(typeof callback == 'function')
                callback();
        });
}

$(document).ready(function(){
    $.Mustache.addFromDom();
});