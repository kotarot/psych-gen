<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ compinfo.name }} &mdash; Psych sheets</title>
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
  <link rel="stylesheet" href="http://cdn.datatables.net/1.10.7/css/jquery.dataTables.min.css">
</head>
<body>
  <div class="container">

    <h1>{{ compinfo.name }} &mdash; Psych sheets</h1>

    <p>{{ compinfo.description }}</p>

    <ul class="nav nav-pills">
      {% for event in compdata.events -%}
        <li id="nav-{{ event }}" class="nav-event"><a href="#{{ event }}">{{ event }}</a></li>
      {% endfor %}
    </ul>

    <hr style="margin-top: 0;">

    {% for event in compdata.events -%}
      <div id="table-container-{{ event }}" class="table-container" style="display:none;">
        <h2>{{ attrs.events_name.get(event) }}</h2>
        <table id="table-{{ event }}" class="table table-striped">
          <thead><tr>
            <th>#</th>
            <th>Name</th>
            <th>ID</th>
            <th>Record</th>
            </tr></thead><tbody>
            {% for person in psych.get(event) -%}
              <tr>
                <td>{{ person.rank }}</td>
                <td>{{ person.name }}</td>
                {% if person.haswcaid %}
                  <td data-order="{{ person.id }}"><a href="https://www.worldcubeassociation.org/results/p.php?i={{ person.id }}" target="_blank">{{ person.id }}</a></td>
                {% else %}
                  <td data-order="9999ZZZZ99">&ndash;</td>
                {% endif %}
                <td data-order="{{ person.value }}">{{ person.formatted }}</td>
               </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    {% endfor %}

    <p style="margin-top: 20px;">
      Result data is courtesy of the <a href="https://www.worldcubeassociation.org/" target="_blank">World Cube Association</a>.
      The latest results can be found via the <a href="https://www.worldcubeassociation.org/results/" target="_blank">WCA Results Pages</a>.
      Data was last updated on {{ attrs.date_fetched }}.
    </p>

    <footer class="footer">
      <p>Generated using <a href="https://github.com/kotarot/psych-gen" target="_blank">Psych sheet generator</a>
         by <a href="https://www.worldcubeassociation.org/results/p.php?i=2010TERA01" target="_blank">Kotaro Terada</a>.</p>
    </footer>

  </div><!-- /.container -->

<style>
.nav > li > a {
    padding: 10px 12px;
}
table, thead th {
    border-bottom: 2px solid #DDD !important;
}
footer {
    margin-top: 30px;
    padding-top: 20px;
    color: #777;
    border-top: 1px solid #E5E5E5;
}
</style>

<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
<script src="http://cdn.datatables.net/1.10.7/js/jquery.dataTables.min.js"></script>
<script>
$(document).ready(function() {
    $('li.nav-event:first').addClass('active');
    $('div.table-container:first').show();
});

// Datatables
$(document).ready(function() {
    $('.table').DataTable({'bPaginate': false, 'order': [[0, 'asc']]});
});

// Switch event (when hash changes)
var swevent = function() {
    if (location.hash) {
        var e = location.hash.replace('#', '');

        // Activate tab
        $('li.nav-event').removeClass('active');
        $('li#nav-' + e).addClass('active');

        // Display table
        $('div.table-container').hide();
        $('div#table-container-' + e).show();
    }
};
$(document).ready(function() {
    window.onhashchange = swevent;
    swevent();
});

</script>

</body>
</html>
