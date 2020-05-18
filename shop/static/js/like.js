{% block domready %}
  $('a.like').click(function(e){
    e.preventDefault();
    $.post('{% url "likes:product_like" %}',
      {
        id: $(this).data('id'),
        action: $(this).data('action')
      },
      function(data){
        if (data['status'] == 'ok')
        {
          var previous_action = $('a.like').data('action');

          // toggle data-action
          $('a.like').data('action', previous_action == 'like' ? 'unlike' : 'like');
          // toggle link text
          $('a.like').text(previous_action == 'like' ? 'Unlike' : 'Like');

          // update total likes
          var previous_likes = parseInt($('span.count .total').text());
          $('span.count .total').text(previous_action == 'like' ? previous_likes + 1 : previous_likes - 1);
        }
      }
    );
  });
{% endblock %}

$('button.like').click(function(e){
  e.preventDefault();
  var product_like = event.target;
  $.post('{% url "likes:product_like" %}',
      {
      id: $(product_like).data('id'),
      action: $(product_like).data('action')
      },
      function(data){
          if (data['status'] == 'ok')
          {
              var previous_action = $(product_like).data('action');
              var pr_id = $(product_like).data('id');

              $(product_like).data('action', previous_action == 'like' ? 'unlike' : 'like');
              $(product_like).text(previous_action == 'like' ? 'Unlike' : 'Like');
              
              var previous_likes = parseInt($('span.' + pr_id).text());
              $('span.' + pr_id).text(previous_action == 'like' ? previous_likes + 1 : previous_likes - 1);
      
          }
      });
  });