const map = L.map('map').setView([45.9432, 24.9668], 6);

L.tileLayer('//{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '© WRC OpenStreetMap'
}).addTo(map);


function onLocationFound(a) {
  let latitudine = document.getElementById("id_latitudine");
  let longitudine = document.getElementById("id_longitudine");

  let marker = new L.marker(a.latlng, { draggable: 'true' }).addTo(map);
  //.bindPopup("You are within " + radius + " meters from this point").openPopup();

  latitudine.value = a.latlng.lat;
  longitudine.value = a.latlng.lng;

  marker.on('dragend', function (event) {
    var marker = event.target;
    var position = marker.getLatLng();

    latitudine.value = position.lat;
    longitudine.value = position.lng;
  });
};

const searchControl = new GeoSearch.GeoSearchControl({
  notFoundMessage: 'Nu am găsit adresa specificată',
  searchLabel: 'Caută adresă',
  provider: new GeoSearch.OpenStreetMapProvider(),
  style: 'bar',
  showMarker: false,
});

function onLocationError(b) {
  let latitudine = document.getElementById("id_latitudine");
  let longitudine = document.getElementById("id_longitudine");

  function onMapClick(e) {
    marker = new L.marker(e.latlng, { draggable: 'true' });

    marker.on('dragend', function (event) {
      var marker = event.target;
      var position = marker.getLatLng();
      marker.setLatLng(new L.LatLng(position.lat, position.lng), { draggable: 'true' });
      map.panTo(new L.LatLng(position.lat, position.lng))
      latitudine.value = position.lat;
      longitudine.value = position.lng;
    });

    map.addLayer(marker);

    latitudine.value = e.latlng.lat;
    longitudine.value = e.latlng.lng;

  };
  const parentLatitudine = latitudine.parentNode;
  const parentLatitudine2 = parentLatitudine.parentNode;
  parentLatitudine.classList.remove("hidden");
  parentLatitudine.previousElementSibling.classList.remove("hidden");
  parentLatitudine2.classList.remove("hidden");

  const parentLongitudine = longitudine.parentNode;
  const parentLongitudine2 = parentLongitudine.parentNode;
  parentLongitudine.classList.remove("hidden");
  parentLongitudine.previousElementSibling.classList.remove("hidden")
  parentLongitudine2.classList.remove("hidden");
  

  map.once('click', onMapClick);
  map.addControl(searchControl);
}

map.on('locationfound', onLocationFound);
map.on('locationerror', onLocationError);

map.locate({ setView: true, maxZoom: 16 });