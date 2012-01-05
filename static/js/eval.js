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
});