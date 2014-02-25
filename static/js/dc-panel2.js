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

if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

var spinners = new Array(6);

function doRandomPanel(panel, comic_id, callback) {
    $("#dc-panel-"+panel).html('');
    spinners[panel-1] = new Spinner(spinnerOpts).spin($("#dc-panel-"+panel)[0]);
    $.get('/a/random-panel/{0}/comic/{1}'.format(panel, comic_id))
        .done(function(data){
            $('#dc-panel-'+panel).html($.Mustache.render('single-panel-template', data));
        })
        .always(function(){
            spinners[panel-1].stop();
            if(typeof callback == 'function')
                callback();
        });
}

var afterLinkCopyCallback = function(client, args) {
    $("#zclip-addon").addClass('copied');
    setTimeout(function(){
        $("#zclip-addon").removeClass('copied');
    }, 500);
};

var afterPanelLoadCallback = function(){
    $('#random-panel-button').attr('disabled', false);
    var zcClient = new ZeroClipboard(document.getElementById("copy-button"));
    zcClient.on('complete', afterLinkCopyCallback);
    $('#share-panel-url').focus(function(){
        $(this).select();
    }).mouseup(function (e) {e.preventDefault(); });
};

$(document).ready(function(){
    $.Mustache.addFromDom();
    ZeroClipboard.config( { moviePath: '/static/js/ZeroClipboard.swf' } );
});