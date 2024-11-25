let place_data = [];
let review_data;
const checkAuthentication = () => {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    loginLink.style.display = 'block';
    window.href = 'index.html';
  } else {
    loginLink.style.display = 'none';
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
      place_data = data;
      displayPlaces(data, 'all');
    })
    .catch(error => {
      console.error('Error en la solicitud:', error);
    });
}
const setSSid = (id) => {
  sessionStorage.setItem('place_id', id)
  window.location.href = './place.html';
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
            <button onclick="setSSid('${place.id}')" class="details-button" id="${place.id}">View Details</button>
          </div>
        `;
      }
    });

    // Actualizar el contenido del DOM
    PLACE_LIST.innerHTML = htmlContentToAppend;
  }
};
const fill_prices_filter = (price_filter) => {
  price_filter.innerHTML += `
    <option value="10">10</option>
    <option value="50">50</option>
    <option value="100">100</option>
    <option value="all" selected>All</option>
    `
  price_filter.addEventListener('change', (event) => {
    let price = price_filter.value;
    displayPlaces(place_data, price);
  })
}
const LoginFunct = (logbtn) => {
  logbtn.addEventListener('click', (e) => {
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
const getPlaceData = () => {
  const token = getCookie('token');
  const id = sessionStorage.getItem('place_id');
  let optsget = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  }
  // GET PLACE INFO
  fetch(`http://localhost:5000/api/v1/places/${id}`, optsget)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      place_data = data;
      show_place(place_data);
    })
    .catch(error => {
      console.error('Error en la solicitud:', error);
    });
  // GET REVIEWS
  fetch(`http://localhost:5000/api/v1/places/${id}/reviews`, optsget)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      review_data = data;
      show_review(review_data);
    })
    .catch(error => {
      console.error('Error en la solicitud:', error);
    });
}
const show_review = async (review_info) => {
  const token = getCookie('token');
  let optsget = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  }
  let userlist;
  // Get user name by ID
  await fetch(`http://localhost:5000/api/v1/users/`, optsget)
    .then(async response => {
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      return await response.json();
    })
    .then(data => {
      userlist = data;
    })
    .catch(error => {
      console.error('Error en la solicitud:', error);
    });
  const REVIEW_DETAILS = document.getElementById('reviews');
  let htmlreviewscontent = '';
  let userinfo;
  if (review_info != []) {
    for (review of review_info) {
      for (user of userlist){
        if (user.id == review.user_id){
          userinfo = user;
          break;
        }
      }
      htmlreviewscontent += `
      <div class="review-box">
        <strong>${userinfo.first_name} ${userinfo.last_name}</strong>
        <p>${review.text}</p>
        <div>
          <p>Rating</p>
          <p>${review.rating}</p>
        </div>
      </div>
      `
    }
  }
  REVIEW_DETAILS.innerHTML = htmlreviewscontent;
}
const show_place = (place_info) => {
  const PLACE_TITLE = document.getElementById('place-title');
  PLACE_TITLE.innerHTML = place_info.title
  const PLACE_DETAILS = document.getElementById('place-details');
  let amenities = ''
  for (amenity of place_info.amenities) {
    amenities += `${amenity.name} `
  }
  let htmlContentToAppend = `
  <div class="place-box">
    <p><strong>Host:</strong> ${place_info.owner.first_name} ${place_info.owner.last_name}</p>
    <p><strong>Price per night:</strong> $${place_info.price} usd</p>
    <p><strong>Description:</strong> ${place_info.description}</p>
    <p><strong>Amenities:</strong> ${amenities != '' ? amenities : 'None'}</p>
  </div>
  `
  PLACE_DETAILS.innerHTML = htmlContentToAppend;
}
document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();
  const LOGIN_BTN = document.getElementById("login-btn");
  const PRICE_FILTER = document.getElementById("price-filter");

  // If Login Button exists, an event will occur to submit form
  if (LOGIN_BTN) {
    LoginFunct(LOGIN_BTN);
  }
  // If you're at Index, you will see the price filter
  if (PRICE_FILTER) {
    fill_prices_filter(PRICE_FILTER);
  }
  if (window.location.pathname.endsWith('place.html')) {
    getPlaceData();
  }
});
