let map = new google.maps.Map(document.getElementById('map'), {
  center: {lat: 40.8138912, lng: -73.96243270000002},
  zoom: 12
});

let geocoder = new google.maps.Geocoder();


centerMapToZipcode = (zipcode) => {
  geocoder.geocode({address: zipcode}, function(res, status) {
    const lat = res[0].geometry.location.lat()
    const lng = res[0].geometry.location.lng()
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: lat, lng: lng},
      zoom: 12
    });
  });
}

createCommentHTML = c => {
  let comments = $('#comments');

  let card = $('<div class="card"></div>');
  let cardBody = $('<div class="card-body"></div>')
  let cardTitle = $('<h4 class="card-title"></h4>')
  let cardSubtitle = $('<h6 class="card-subtitle"></h6>')
  let cardText = $('<p class="card-text"></p>')

  cardTitle.text(c.comment)
  if (c.sentiment === 1) {
    cardSubtitle.text("Bad")
    cardSubtitle.css({'color': 'red'})
  } else {
    cardSubtitle.text("Good")
    cardSubtitle.css({'color': 'green'})
  }

  cardBody = cardBody.append(cardTitle);
  cardBody = cardBody.append(cardSubtitle);
  cardBody = cardBody.append(cardText);
  card = card.append(cardBody);

  comments.append(card);
}

updateComments = (zipcode) => {
  axios.post('/comments', {zipcode})
    .then(resp => {
      resp.data.map(comment => {
        createCommentHTML(comment);
        addMarkerToMap(comment);
      })
    })
}

getLatLng = (zipcode, cb) => {
  geocoder.geocode({address: zipcode}, function(res, status) {
    console.log(zipcode);
    const lat = res[0].geometry.location.lat()
    const lng = res[0].geometry.location.lng()

    cb({lat, lng});
  }); 
}

addMarkerToMap = c => {
  getLatLng('10027', function(res) {
    const {lat, lng} = res;
    let marker = new google.maps.Marker({
      position: {lat: lat, lng:lng},
      title: "hello"
    })

    let comment = document.createElement("p");
    comment.innerText = c.comment;

    let infoWindow = new google.maps.InfoWindow({
      content: comment
    }) 

    marker.addListener('click', function() {
      infoWindow.open(map, marker);
    })
    marker.setMap(map);
  })
}

updateView = () => {
  const input = document.getElementById('zipcode')
  const zipcode = input.value

  centerMapToZipcode(zipcode);
  updateComments(zipcode);
}