
initialize = ->
   options = 
      center: new google.maps.LatLng(43.81211, -91.22695),
      zoom: 15,
      mapTypeId: google.maps.MapTypeId.ROADMAP
      
   ###
   Check if the user's browser supports geolocation and if so, zoom in on their location
   ###
   if navigator.geolocation
      navigator.geolocation.getCurrentPosition(
       (position) -> 
          options['center'] = new google.maps.LatLng(position.coords.latitude, position.coords.longitude)
          options['zoom'] = 17
          showInitialMap options,
       ->
          showInitialMap options)
          
   showInitialMap = (options) ->
      map = new google.maps.Map(document.getElementById("map_canvas"), options)
      datePickerDiv = document.createElement('div')
      datePickerDiv.index = 1
      map.controls[google.maps.ControlPosition.RIGHT_TOP].push(datePickerDiv)

      $.ajax(
         url: encodeURI('get_incident_reports?date=7/4/2012')
         success: (data) -> 
            for incident in data
               do (incident) ->
                  marker = new google.maps.Marker
                     position: new google.maps.LatLng(parseFloat(incident.lat), parseFloat(incident.long))
                     title: incident.description + ', ' + incident.address + ' ' + incident.time
                  marker.setMap(map)
                    
         error: ->
            alert('Error retrieving logs for the selected date.')
       )
       
       datePickerDiv.setAttribute('id', 'datePickerDiv')
       today = new Date()
       $(datePickerDiv).datepicker({minDate: new Date(2012, 0, 1), maxDate: new Date(today.getFullYear(), today.getMonth(), today.getDate() - 1) })

$(document).ready(initialize)