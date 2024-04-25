$(function(){
  $('a#hideUserFlds').click(function(e){
    e.preventDefault();
    //$.cookie('hideUserFlds', 1);
    
    // устанавливаем куку hideUserFlds в 1 для всего домена mydomain.com срок истечения куки 10 дней от времени установки
    //$.cookie('hideUserFlds', 1, { expires: 10, path: '/', domain: 'mydomain.com'});
    if ($.cookie('hideUserFlds') == 1)
    {
      $.cookie('hideUserFlds', 0, { expires: 100});
      $('#usrFlds').show();
    }
    else
    {
      $.cookie('hideUserFlds', 1, { expires: 100});
      $('#usrFlds').hide();
    }
  });
  
  $('a.toggleInput').click(function(e){
    e.preventDefault();
    $(this).toggle();
    $(this).next('input').toggle();
  });
  
  
  
})

$(function(){
  $('a#hideRules').click(function(e){
    e.preventDefault();
    //$.cookie('hideUserFlds', 1);
    
    // устанавливаем куку hideUserFlds в 1 для всего домена mydomain.com срок истечения куки 10 дней от времени установки
    //$.cookie('hideUserFlds', 1, { expires: 10, path: '/', domain: 'mydomain.com'});
    if ($.cookie('hideRules') == 1)
    {
      $.cookie('hideRules', 0, { expires: 100});
      $('.rules').show();
    }
    else
    {
      $.cookie('hideRules', 1, { expires: 100});
      $('.rules').hide();
    }
  });
  
  $('a.toggleInput').click(function(e){
    e.preventDefault();
    $(this).toggle();
    $(this).next('input').toggle();
  });
  
})