document.addEventListener('DOMContentLoaded', () => {
  fetchVehicles();

  document.getElementById('search-button').addEventListener('click', () => {
      const query = document.getElementById('search').value;
      fetchVehicles(query);
  });

  document.getElementById('login-button').addEventListener('click', () => {
      document.getElementById('login-modal').style.display = 'flex';
  });

  document.getElementById('signup-button').addEventListener('click', () => {
      document.getElementById('signup-modal').style.display = 'flex';
  });

  document.getElementById('close-login').addEventListener('click', () => {
      document.getElementById('login-modal').style.display = 'none';
  });

  document.getElementById('close-signup').addEventListener('click', () => {
      document.getElementById('signup-modal').style.display = 'none';
  });

  document.getElementById('login-submit').addEventListener('click', login);
  document.getElementById('signup-submit').addEventListener('click', signup);
});

function fetchVehicles(query = '') {
  fetch(`http://localhost:8000/vehicles?query=${query}`)
      .then(response => response.json())
      .then(data => {
          displayVehicles(data);
      });
}

function displayVehicles(vehicles) {
  const vehicleList = document.getElementById('vehicle-list');
  vehicleList.innerHTML = '';
  vehicles.forEach(vehicle => {
      const vehicleDiv = document.createElement('div');
      vehicleDiv.className = 'vehicle';
      vehicleDiv.innerHTML = `
          <img src="static/images/${vehicle.model.toLowerCase()}.jpg" alt="${vehicle.model}">
          <h3>${vehicle.model}</h3>
          <p>Marque: ${vehicle.brand}</p>
          <p>Couleur: ${vehicle.color}</p>
          <p>Vitesse max: ${vehicle.max_speed} km/h</p>
          <p>Km: ${vehicle.mileage}</p>
          <p>Consommation moyenne: ${vehicle.average_consumption} L/100km</p>
      `;
      vehicleList.appendChild(vehicleDiv);
  });
}

function login() {
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;

  fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password })
  })
  .then(response => response.json())
  .then(data => {
      alert(data.message);
      document.getElementById('login-modal').style.display = 'none';
  })
  .catch(error => console.error('Error:', error));
}

function signup() {
  const username = document.getElementById('signup-username').value;
  const password = document.getElementById('signup-password').value;
  const role = document.getElementById('signup-role').value;

  fetch('http://localhost:8000/signup', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password, role })
  })
  .then(response => response.json())
  .then(data => {
      alert('User created successfully');
      document.getElementById('signup-modal').style.display = 'none';
  })
  .catch(error => console.error('Error:', error));
}
