function flashMessages() {
    var Toast = Swal.mixin({
      toast: true,
      position: 'top-end',
      showConfirmButton: false,
      timer: 3000
    });
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          Toast.fire({
              icon: '{{category}}',
              title: '{{message}}'
          })
      {% endfor %}
    {% endif %}
  {% endwith %}
  };