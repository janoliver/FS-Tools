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

    // Aktionen
    /*if($('.t tbody tr td.buttons').length > 0) {
        td = $('.t tbody tr td.buttons');
        links = td.find('a');
        links.hide();
        aktionen_link = $('<a href="#" class="button">Aktionen</a>');
        link_list = $('<ul class="aktionenliste"></ul>').hide();
        links.each(function() {
            li = $('<li></li>').append($(this).show());
            link_list.append(li);
        });
        td.append(link_list);
        td.prepend(aktionen_link);

        // show effect
        aktionen_link.hover(function() {
            $(this).hide();
            link_list.show();
        });

        link_list.mouseleave(function() {
            $(this).hide();
            aktionen_link.show();
        })
    }*/
    
    // antwortbogen page key functionality
    if($('.bogen').length > 0) {
        
        $(document).keydown(function(key) {
            
            // select the focused input
            var n = key.which - 48;
            
            var act = $('.frage.active');
            if(n < 10 && n > 0 && !act.hasClass('textfrage')) {
                key.preventDefault();
                if(act.find("input[type='radio']").length > 0)
                    $('ul li:nth-child(' + n + ')', act).find('input').attr('checked', true);            
                if(act.find("select").length > 0)
                    $('select :nth-child(' + n + ')', act).attr('selected', 'selected');
                
                act.nextAll('.frage:first').find('input, textarea, select').focus();
            }

            if(key.which == 9) {
                key.preventDefault();
                act.nextAll('.frage:first').find('input, textarea, select').focus();
            }
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

        td = $(this).parent();
        clicked_choice = choiceArray[$(this).attr('href')];
        
        // remove the choice if the same was selected
        if(td.hasClass('chosen') && td.hasClass(clicked_choice)) {
            td.removeClass('chosen');
            td.removeClass(clicked_choice);
        } else {
            
            // add classes to the td
            td.addClass('chosen');
            for( var choice in choiceArray)
                td.removeClass(choiceArray[choice]); 
            td.addClass(clicked_choice);
        }
    });

    // click on save answer
    $(".savebutton").click(function(e) {
        e.preventDefault();
        
        // prepare data array
        data = {'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').attr('value')}

        // find options
        var must_check = $("input[name='must_check_number']").attr('value') == 'True';
        var wahlanzahl = parseInt($("input[name='wahlanzahl']").attr('value'));
        var counter = 0;
        // create array of chosen answers
        $("td.terminchoice").each(function() {
            
            // check if every option has a choice
            if(!$(this).hasClass('chosen') && must_check && wahlanzahl == 0) {
                $.achtung({
	            message: "Bitte zu allen Optionen etwas auswählen!", 
	            className: "error",
	            timeout: 5,
	            disableClose: true});
                return false;
            }

            if($(this).hasClass('chosen')) {
                // answer codes: yes: 1, no: -1, perhaps: 0
                if($(this).hasClass('yes'))
                    data[$(this).attr('id')] = 1;
                if($(this).hasClass('no'))
                    data[$(this).attr('id')] = -1;
                if($(this).hasClass('vllt'))
                    data[$(this).attr('id')] = 0;

                counter++;
            }
        });
        
        // check if every option has a choice
        if(must_check && wahlanzahl > counter) {
            $.achtung({
	        message: "Bitte zu "+ wahlanzahl +" Optionen etwas auswählen!", 
	        className: "error",
	        timeout: 5,
	        disableClose: true});
            return false;
        }

        // check if every option has a choice
        if(wahlanzahl != 0 && counter > wahlanzahl) {
            $.achtung({
	        message: "Du darfst nur  "+ wahlanzahl +" mal abstimmen!", 
	        className: "error",
	        timeout: 5,
	        disableClose: true});
            return false;
        }
        
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