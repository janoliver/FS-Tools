// -*- coding: utf-8 -*-
$(document).ready(function() {
    
    // make messages according to djangos messages
    $(".messages").hide();
    $(".messages li").each(function() {
        var cl = 'achtung' + $(this).attr('class').replace(/\b[a-z]/g, function(letter) {
            return letter.toUpperCase();
        }); 
        $.achtung({
	    message: $(this).text(), 
	    className: cl,
	    timeout: 5,
	    disableClose: true});

    });

});