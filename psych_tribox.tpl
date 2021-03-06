<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ compinfo.name }} &mdash; Psych sheet</title>
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
  <link rel="stylesheet" href="http://cdn.datatables.net/1.10.7/css/jquery.dataTables.min.css">
  <link rel="shortcut icon" href="/favicon.ico">
  <link rel="apple-touch-icon-precomposed" href="/apple-touch-icon-precomposed.png">
</head>
<body style="font-family: 'ヒラギノ角ゴ Pro W3','Hiragino Kaku Gothic Pro','メイリオ',Meiryo,'ＭＳ Ｐゴシック',arial,verdana,sans-serif;">
  <div class="container" style="padding-right: 5px; padding-left: 5px;">

    <img src="http://tribox.com/wp-content/uploads/2015/03/cropped-tribox_dot_com_logo4.png" width="640" height="50" alt="tribox" style="margin-top: 10px; max-width: 100%; height: auto;">

    <nav class="navbar navbar-inverse" style="min-height: 0;">
      <div class="container-fluid">
        <div class="navbar-header">
          <a class="navbar-tribox" href="http://tribox.com/open/"><b>tribox Open</b></a>
          <a class="navbar-tribox" href="http://tribox.com/">ホーム</a>
          <a class="navbar-tribox" href="https://store.tribox.com/">ストア</a>
          <a class="navbar-tribox" href="https://contest.tribox.com/">コンテスト</a>
        </div>
      </div>
    </nav>

    <h1>{{ compinfo.name }} &mdash; Psych sheet</h1>

    <p>{{ compinfo.description }}</p>

    <div class="alert" role="alert" style="border-color: #DDD; color: #333; background-color: #FFF;">
      Psych sheet (サイクシート) とは、大会にエントリしている選手の各種目ごとの公式自己ベスト記録ランキングです。
      このページは、<a href="https://www.worldcubeassociation.org/results/misc/export.html" target="_blank">WCA Results terms of use</a>
      にもとづいて作成されています。<br>
      ※左端の数字はランキングを表しています（エントリナンバーではありません）。
    </div>

    <ul id="nav-events" class="nav nav-pills">
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
            <th class="col-desktop">Name</th>
            <th class="col-desktop">Country</th>
            <th class="col-desktop">WCA ID</th>
            <th class="col-mobile">Name</th>
            <th class="col-record">Record</th>
            </tr></thead><tbody>
            {% for person in psych.get(event) -%}
              <tr>
                <td>{{ person.rank }}</td>
                <td class="col-desktop">{{ person.name }}</td>
                <td class="col-desktop">
                  <img src="flags/flags-iso/shiny/24/{{ person.countryiso2 }}.png" width="24" height="24" alt="{{ person.country }}">
                  {{ person.country }}
                </td>
                {% if person.haswcaid %}
                  <td class="col-desktop" data-order="{{ person.id }}">
                    <a href="https://www.worldcubeassociation.org/results/p.php?i={{ person.id }}" target="_blank">{{ person.id }}</a>
                  </td>
                  <td class="col-mobile" data-order="{{ person.name }}">
                    <img src="flags/flags-iso/shiny/16/{{ person.countryiso2 }}.png" width="16" height="16" alt="{{ person.country }}">
                      <a href="https://www.worldcubeassociation.org/results/p.php?i={{ person.id }}" target="_blank">{{ person.name }}</a>
                  </td>
                {% else %}
                  <td class="col-desktop" data-order="9999ZZZZ99">&ndash;</td>
                  <td class="col-mobile" data-order="{{ person.name }}">
                    <img src="flags/flags-iso/shiny/16/{{ person.countryiso2 }}.png" width="16" height="16" alt="{{ person.country }}">
                    {{ person.name }}</a>
                  </td>
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
.navbar-tribox {
    float: left;
    font-size: 14px;
    padding-top: 10px;
    padding-bottom: 10px;
    padding-right: 15px;
    padding-left: 15px;
    line-height: 15px;
    color: #FFF;
}
.navbar-tribox:hover {
    color: #FFF;
    text-decoration: none;
}
#nav-events > li > a {
    padding: 10px 12px;
}
table, thead th {
    border-bottom: 2px solid #DDD !important;
}
th, td {
    padding: 8px !important;
}
@media (max-width: 768px) {
    .col-desktop { display: none !important; }
    .col-mobile  { display: table-cell !important; }
    h1 { font-size: 30px; }
    h2 { font-size: 20px; }
    th, td { letter-spacing: -1px; }
}
@media (min-width: 768px) {
    .col-desktop { display: table-cell !important; }
    .col-mobile  { display: none !important; }
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
    $('.table').DataTable({
        'bPaginate': false, 'order': [[5, 'asc']],
        'columnDefs': [{'orderable': false, 'targets': 0}]
    });
});

// Switch event (when hash changes)
var current_event = '333';
var swevent = function() {
    if (location.hash) {
        current_event = location.hash.replace('#', '');

        // Activate tab
        $('li.nav-event').removeClass('active');
        $('li#nav-' + current_event).addClass('active');

        // Display table
        $('div.table-container').hide();
        $('div#table-container-' + current_event).show();
    }
};
$(document).ready(function() {
    window.onhashchange = swevent;
    swevent();
});

</script>

</body>
</html>
