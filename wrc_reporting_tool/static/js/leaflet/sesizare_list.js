let sesizare = JSON.parse(document.getElementById('sesizare').textContent)
    let map = L.map('map').setView([sesizare[0].latitudine, sesizare[0].longitudine], 13);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    switch (sesizare[0].status__culoare) {
      case 'bg-pink-500': L.marker.svgMarker([sesizare[0].latitudine, sesizare[0].longitudine], { iconOptions: { color: "rgb(231, 70, 148)", fillOpacity: 0.6 }}).addTo(map);
      break;

      case 'bg-yellow-400': L.marker.svgMarker([sesizare[0].latitudine, sesizare[0].longitudine], { iconOptions: { color: "rgb(227, 160, 8)", fillOpacity: 0.6 }}).addTo(map);
      break;

      case 'bg-green-700': L.marker.svgMarker([sesizare[0].latitudine, sesizare[0].longitudine], { iconOptions: { color: "rgb(4, 108, 78)", fillOpacity: 0.6 }}).addTo(map);
      break;

      case 'bg-red-700': L.marker.svgMarker([sesizare[0].latitudine, sesizare[0].longitudine], { iconOptions: { color: "rgb(200, 30, 30)", fillOpacity: 0.6 }}).addTo(map);
      break;

      case 'bg-pink-900': L.marker.svgMarker([sesizare[0].latitudine, sesizare[0].longitudine], { iconOptions: { color: "rgb(117, 26, 61)", fillOpacity: 0.6 }}).addTo(map);
      break;

      case 'bg-indigo-500': L.marker.svgMarker([sesizare[0].latitudine, sesizare[0].longitudine], { iconOptions: { color: "rgb(104, 117, 245)", fillOpacity: 0.6 }}).addTo(map);
      break;

      case 'bg-blue-700': L.marker.svgMarker([sesizare[0].latitudine, sesizare[0].longitudine], { iconOptions: { color: "rgb(26, 86, 219)", fillOpacity: 0.6 }}).addTo(map);
      break;
    }
