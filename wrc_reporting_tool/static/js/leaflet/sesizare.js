let sesizari = JSON.parse(document.getElementById('sesizari-json').textContent)
let map = L.map('map').setView([51.505, -0.09], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const markers = [];
let overlayMaps = {};
let asteptareFeatureGroup = L.featureGroup().addTo(map);
let preluatFeatureGroup = L.featureGroup().addTo(map);
let rezolvatFeatureGroup = L.featureGroup().addTo(map);
let nesolutionatFeatureGroup = L.featureGroup().addTo(map);
let excludereFeatureGroup = L.featureGroup().addTo(map);
let relocareFeatureGroup = L.featureGroup().addTo(map);
let reabilitareFeatureGroup = L.featureGroup().addTo(map);
for (let sesizare of sesizari) {

    markers.push([sesizare.latitudine, sesizare.longitudine])

    switch (sesizare.status__categorie) {

        case null:
            switch (sesizare.status) {
                case 1:
                    let marker = L.marker.svgMarker([sesizare.latitudine, sesizare.longitudine], { iconOptions: { color: "rgb(231, 70, 148)", fillOpacity: 0.6 } }).addTo(asteptareFeatureGroup);
                    overlayMaps[`<div class="h-3 w-3 inline-block mr-2 ${sesizare.status__culoare}"></div>În așteptare`] = asteptareFeatureGroup;
                    break;

                case 2:
                    L.marker.svgMarker([sesizare.latitudine, sesizare.longitudine], { iconOptions: { color: "rgb(227, 160, 8)", fillOpacity: 0.6 } }).addTo(preluatFeatureGroup);
                    overlayMaps[`<div class="h-3 w-3 inline-block mr-2 ${sesizare.status__culoare}"></div>Preluat`] = preluatFeatureGroup;
                    break;
            }
            break;

        case 1:
            L.marker.svgMarker([sesizare.latitudine, sesizare.longitudine], { iconOptions: { color: "rgb(4, 108, 78)", fillOpacity: 0.6 } }).addTo(rezolvatFeatureGroup);
            overlayMaps[`<div class="h-3 w-3 inline-block mr-2 ${sesizare.status__culoare}"></div>Rezolvat`] = rezolvatFeatureGroup;
            break;

        case 2:
            L.marker.svgMarker([sesizare.latitudine, sesizare.longitudine], { iconOptions: { color: "rgb(200, 30, 30)", fillOpacity: 0.6 } }).addTo(nesolutionatFeatureGroup);
            overlayMaps[`<div class="h-3 w-3 inline-block mr-2 ${sesizare.status__culoare}"></div>Nesoluționat`] = nesolutionatFeatureGroup;
            break;

        case 3:
            L.marker.svgMarker([sesizare.latitudine, sesizare.longitudine], { iconOptions: { color: "rgb(117, 26, 61)", fillOpacity: 0.6 } }).addTo(excludereFeatureGroup);
            overlayMaps[`<div class="h-3 w-3 inline-block mr-2 ${sesizare.status__culoare}"></div>Excludere`] = excludereFeatureGroup;
            break;

        case 4:
            L.marker.svgMarker([sesizare.latitudine, sesizare.longitudine], { iconOptions: { color: "rgb(104, 117, 245)", fillOpacity: 0.6 } }).addTo(relocareFeatureGroup);
            overlayMaps[`<div class="h-3 w-3 inline-block mr-2 ${sesizare.status__culoare}"></div>Relocare`] = relocareFeatureGroup;
            break;

        case 5:
            L.marker.svgMarker([sesizare.latitudine, sesizare.longitudine], { iconOptions: { color: "rgb(26, 86, 219)", fillOpacity: 0.6 } }).addTo(reabilitareFeatureGroup);
            overlayMaps[`<div class="h-3 w-3 inline-block mr-2 ${sesizare.status__culoare}"></div>Centru reabilitare`] = reabilitareFeatureGroup;
            break;
    };
};

let controls = L.control.layers(null, overlayMaps, { collapsed: false }).addTo(map);

var bounds = new L.LatLngBounds(markers);
map.fitBounds(bounds, { padding: [20, 20] });

map.on('layeradd layerremove', function () {
    // Create new empty bounds
    var bounds = new L.LatLngBounds();
    // Iterate the map's layers
    map.eachLayer(function (layer) {
        // Check if layer is a featuregroup
        if (layer instanceof L.FeatureGroup) {
            // Extend bounds with group's bounds
            bounds.extend(layer.getBounds());
        }
    });
    // Check if bounds are valid (could be empty)
    if (bounds.isValid()) {
        // Valid, fit bounds
        map.fitBounds(bounds, { padding: [20, 20] });
    } else {
        // Invalid, fit world
        map.fitWorld();
    }
});