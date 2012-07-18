
initialize = ->
   
   kEarliestDateWithData = new Date(2012, 0, 1)
   kCenterOfLaCrosse = new google.maps.LatLng(43.81211, -91.22695)
   kDefaultZoomLevel = 15
   kZoomLevelWithLocation = 16
   
   ### array of markers on the map ###
   fMarkers = []
   fMap = null
   fSelectedDate = null
   
   ###
   Set up the map and the calendar to allow the user
   to select different dates.
   ###
   setupMapControls = ->
      options = 
       center:      kCenterOfLaCrosse,
       zoom:        kDefaultZoomLevel,
       mapTypeId:   google.maps.MapTypeId.ROADMAP
      fMap = new google.maps.Map(document.getElementById("map_canvas"), options)
      datePickerDiv = document.createElement('div')
      datePickerDiv.setAttribute('id', 'datePickerDiv')
      fMap.controls[google.maps.ControlPosition.RIGHT_TOP].push(datePickerDiv)
      
      today = new Date()
      $(datePickerDiv).datepicker(
       minDate: kEarliestDateWithData,
       maxDate: new Date(today.getFullYear(), today.getMonth(), today.getDate() - 1))
      
      fSelectedDate = $(datePickerDiv).datepicker('getDate')
      
      google.maps.event.addDomListener(datePickerDiv, 'click', ->
         newDate = $(datePickerDiv).datepicker('getDate')
         if newDate.getTime() != fSelectedDate.getTime()
            marker.setMap(null) for marker in fMarkers
            fMarkers = []
            fSelectedDate = newDate      
            updateMap())
      
   ###
   Check if the user's browser supports geolocation and if so, update map options to center
   on the location and zoom in a little bit.
   ###
   getUserLocation = ->
      if navigator.geolocation
         navigator.geolocation.getCurrentPosition(
            (position) -> 
               fMap.setZoom kZoomLevelWithLocation
               fMap.setCenter new google.maps.LatLng(position.coords.latitude, position.coords.longitude))
   
   updateMap = ->
      $.ajax(
         url: encodeURI('get_incident_reports?date=' + (fSelectedDate.getMonth() + 1) + '/' + fSelectedDate.getDate() + '/' + fSelectedDate.getFullYear())
         success: (data) -> 
            for incident in data
               do (incident) ->
                  marker = new google.maps.Marker
                     position: new google.maps.LatLng(parseFloat(incident.lat), parseFloat(incident.long))
                     title: incident.description + ', ' + incident.address + ' ' + incident.time
                  marker.setMap(fMap)
                  fMarkers.push(marker)
                  google.maps.event.addListener(marker, 'click', ->
                     infoWindow = new google.maps.InfoWindow()
                     infoWindow.setContent(marker.title)
                     infoWindow.open(fMap, marker)
                     return false;)
                    
         error: ->
            alert('Error retrieving logs for the selected date.')
       )
      
      authorizeUser = ->
         password = prompt("Enter password")
         if password != null and password != ""
            $.ajax(
             url: 'authorize_user?password=' + password
             success: (data) -> 
               if "true" == data
                  setupMapControls()
                  getUserLocation()
                  updateMap()
               else
                  authorizeUser()
             error: ->
                authorizeUser())

      authorizeUser()      

$(document).ready(initialize)