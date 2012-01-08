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

    // click on a lecture or rhp
    $('.vlu, .rhp').click(function(e) {
        e.preventDefault();
        $("." + $(this).attr('href')).toggleClass("tpl");
    });

    // antwortbogen page key functionality
    if($('.bogen').length > 0) {
        
        $(document).keydown(function(key) {
            // select the focused input
            var n = key.which - 48;
            var act = $('.frage.active');
            if(act.find("input[type='radio']").length > 0)
                $('ul li:nth-child(' + n + ')', act).find('input').attr('checked', true);            
            if(act.find("select").length > 0)
                $('select :nth-child(' + n + ')', act).attr('selected', 'selected');

        });

        $('input, textarea, select').focus(function() {
            $('.frage').removeClass('active');
            $(this).parents('.frage').addClass('active');
        });

        $('.frage').click(function() {
            $(this).find('input, textarea, select').focus();
        });

        $("select[name='tutor']").focus();
    }
    
    choiceArray = new Array();
    choiceArray['#ja'] = 'yes';
    choiceArray['#nein'] = 'no';
    choiceArray['#vielleicht'] = 'vllt';

    // click on one of the choices for termine
    $(".terminchoice a").click(function(e) {
        e.preventDefault();

        // add classes to the td
        td = $(this).parent();
        td.addClass('chosen');
        for( var choice in choiceArray)
            td.removeClass(choiceArray[choice]); 
        td.addClass(choiceArray[$(this).attr('href')]);
    });

    // click on save answer
    $(".savebutton").click(function(e) {
        e.preventDefault();
        
        // prepare data array
        data = {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').attr('value')}

        // create array of chosen answers
        $("td.terminchoice").each(function() {
            
            // check if every option has a choice
            if(!$(this).hasClass('chosen')) {
                $.achtung({
	            message: "Bitte zu allen Optionen etwas auswählen!", 
	            className: "error",
	            timeout: 5,
	            disableClose: true});
                return false;
            }
            
            // answer codes: yes: 1, no: -1, perhaps: 0
            if($(this).hasClass('yes'))
                data[$(this).attr('id')] = 1;
            if($(this).hasClass('no'))
                data[$(this).attr('id')] = -1;
            if($(this).hasClass('vllt'))
                data[$(this).attr('id')] = 0;
            
        });
        
        // send vote to server
        $.ajax({
            type: 'POST',
            url: document.location.href, 
            data: data, 
            success: function(resp) {
                console.log(resp);
                if(resp.success) {
                    location.reload();
                }
            }
        });
    });
});