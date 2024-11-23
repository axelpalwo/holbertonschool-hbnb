let place_data = [];

const checkAuthentication = () => {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
      loginLink.style.display = 'block';
  } else {
      loginLink.style.display = 'none';
      // Fetch places data if the user is authenticated
      fetchPlaces(token);
  }
}
const getCookie = (name) => {
  const cookies = document.cookie.split('; ');
    for (let cookie of cookies) {
        const [key, value] = cookie.split('=');
        if (key === name) {
            return value;
        }
    }
    return null;
}
const fetchPlaces = async (token) => {
  let optsget = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  }
  fetch('http://localhost:5000/api/v1/places/', optsget)
  .then(response => {
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    return response.json(); 
  })
  .then(data => {
    console.log('Datos recibidos:', data);
    place_data = data;
    displayPlaces(data, 'all');
  })
  .catch(error => {
    console.error('Error en la solicitud:', error);
  });
}
const displayPlaces = (data, price) => {
  const PLACE_LIST = document.getElementById('places-list');
  let htmlContentToAppend = '';

  if (PLACE_LIST) {
    data.forEach(place => {
      if (price === 'all' || parseInt(price) >= place.price) {
        htmlContentToAppend += `
          <div class="place-box">
            <h2 class="place-title">${place.title}</h2>
            <p class="place-price">price per night: $${place.price}</p>
            <button class="details-button" id="${place.id}">View Details</button>
          </div>
        `;
      }
    });

    // Actualizar el contenido del DOM
    PLACE_LIST.innerHTML = htmlContentToAppend;
  }
};
document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();
  const LOGIN_BTN = document.getElementById("login-btn");
  const PRICE_FILTER = document.getElementById("price-filter");

  if (LOGIN_BTN) {
    LOGIN_BTN.addEventListener('click', (e) => {
      e.preventDefault()
      const EMAIL = document.getElementById("email").value;
      const PASSWORD = document.getElementById("password").value;

      if (EMAIL.length >= 10 && PASSWORD.length >= 5) {
        let postopts = {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email: EMAIL, password: PASSWORD })
        }
        fetch('http://localhost:5000/api/v1/auth/login', postopts)
          .then(async response => {
            if (response.ok) {
              const data = await response.json();
              document.cookie = `token=${data.access_token}; path=/`;
              window.location.href = 'index.html';
          } else {
              alert('Login failed: ' + response.statusText);
          }
        });
      } else {
        alert('Empty fields left.');
      }
    })
  }

  if (PRICE_FILTER){
    PRICE_FILTER.innerHTML += `
    <option value="10">10</option>
    <option value="50">50</option>
    <option value="100">100</option>
    <option value="all" selected>All</option>
    `
    PRICE_FILTER.addEventListener('change', (event) => {
      let price = PRICE_FILTER.value;
      displayPlaces(place_data, price);
    })
  }
});