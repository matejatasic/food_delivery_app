const mapButtons = document.querySelectorAll(".map-button");
const map = L.map('map').setView([51.505, -0.09], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

mapButtons.forEach(button => {
    button.addEventListener("click", (e) => {
        const orderId = e.target.getAttribute("data-id");
        const latitude = parseFloat(e.target.getAttribute("data-latitude"));
        const longitude = parseFloat(e.target.getAttribute("data-longitude"));
        const customer_coordinates = [latitude, longitude];
        const restaurant_coordinates_json = document.getElementById(`restaurant_coordinates_${orderId}`).textContent;
        console.log(restaurant_coordinates_json)
        const restaurant_coordinates = JSON.parse(restaurant_coordinates_json);

        L.marker(customer_coordinates).addTo(map);

        restaurant_coordinates.forEach(coordinates => {
            L.polyline([coordinates, customer_coordinates]).addTo(map);
            L.marker(coordinates).addTo(map);
        });
    })
});

$('#map-modal').on('shown.bs.modal', function(){
    setTimeout(function() {
        map.invalidateSize();
    }, 10);
});