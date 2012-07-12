// Generated by CoffeeScript 1.3.1
(function() {
  var initialize;

  initialize = function() {
    var options, showInitialMap;
    options = {
      center: new google.maps.LatLng(43.81211, -91.22695),
      zoom: 15,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    /*
       Check if the user's browser supports geolocation and if so, zoom in on their location
    */

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        options['center'] = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
        options['zoom'] = 17;
        return showInitialMap(options);
      }, function() {
        return showInitialMap(options);
      });
    }
    return showInitialMap = function(options) {
      var map;
      map = new google.maps.Map(document.getElementById("map_canvas"), options);
      return $.ajax({
        url: encodeURI('get_incident_reports?date=7/4/2012'),
        success: function(data) {
          var incident, _i, _len, _results;
          _results = [];
          for (_i = 0, _len = data.length; _i < _len; _i++) {
            incident = data[_i];
            _results.push((function(incident) {
              var marker;
              marker = new google.maps.Marker({
                position: new google.maps.LatLng(parseFloat(incident.lat), parseFloat(incident.long)),
                title: incident.description + ', ' + incident.address + ' ' + incident.time
              });
              return marker.setMap(map);
            })(incident));
          }
          return _results;
        },
        error: function() {
          return alert('Error retrieving logs for the selected date.');
        }
      });
    };
  };

  $(document).ready(initialize);

}).call(this);