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
                : match;
        });
    };
}

var spinners = new Array(6);
function startSpinner(panel) {
    $("#dc-panel-" + panel).html('');
    spinners[panel - 1] = new Spinner(spinnerOpts).spin($("#dc-panel-" + panel)[0]);
}

function stopSpinner(panel) {
    spinners[panel - 1].stop();
}

function renderPanel(p, template, data) {
    $('#dc-panel-' + p)
        .html($.Mustache.render(template, data))
        .data('comic', data.comic_id)
        .data('panel', p);
}

function getLockedPanels() {
    var panels = {};
    $('.comic-panel.locked').each(function(i, p) {
        panels[$(p).data('panel')] = $(p).data('comic');
    });
    return panels;
}

function doRandomPanel(panel, comic_id, callback) {
    startSpinner(panel)
    $.get('/a/random-panel/{0}/comic/{1}'.format(panel, comic_id))
        .done(function(data) {
            renderPanel(panel, 'single-panel-template', data)
        })
        .always(function() {
            stopSpinner(panel)
            if (typeof callback == 'function')
                callback();
        });
}

function doRandomComic(panels) {
    $('#random-comic-button').attr('disabled', true);
    $('#dc-panel-footer, #share-section').hide();
    $("#comic-container .comic-panel").each(function(i) {
        startSpinner(i + 1);
    });

    $.post('/a/random-comic', {p: JSON.stringify(panels)})
        .done(function(data) {
            $.each(data.panels, function(i, p) {
                renderPanel(p.panel, 'comic-panel-template', p);
            });
            $('#share-section').html($.Mustache.render('panel-share-section-template', data));
        })
        .always(function() {
            $("#comic-container .comic-panel").each(function(i) {
                stopSpinner(i + 1);
            });
            $('#dc-panel-footer, #share-section').show();
            $('#random-comic-button').attr('disabled', false);
            setUpZeroClipboard();
        });
}

var afterLinkCopyCallback = function(client, args) {
    $("#zclip-addon").addClass('copied');
    setTimeout(function() {
        $("#zclip-addon").removeClass('copied');
    }, 500);
};

function setUpZeroClipboard() {
    var zcClient = new ZeroClipboard(document.getElementById("copy-button"));
    zcClient.on('complete', afterLinkCopyCallback);
    $('#share-url').focus(function() {
        $(this).select();
    }).mouseup(function(e) {
            e.preventDefault();
        });
}

var afterPanelLoadCallback = function() {
    $('#random-panel-button').attr('disabled', false);
    setUpZeroClipboard();
};

$(document).ready(function() {
    $.Mustache.addFromDom();
    ZeroClipboard.config({ moviePath: '/static/js/ZeroClipboard.swf' });

    $(document).on('click', '.comic-panel-lock', function(e) {
        e.preventDefault();
        $(this).parent('.comic-panel').toggleClass('locked');
    });

    $('#comic-container').hover(function(e) {
        $('.comic-panel-lock').fadeIn();
    }, function(e) {
        $('.comic-panel-lock').fadeOut();
    });
});
