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

clearPrevComments = _ => {
  let comments = $('#comments');
  comments.html('');
}

createCommentHTML = c => {
  let comments = $('#comments');

  let card = $('<div class="card"></div>');
  let cardBody = $('<div class="card-body"></div>')
  let cardTitle = $('<h4 class="card-title"></h4>')
  let cardSubtitle = $('<h6 class="card-subtitle"></h6>')
  let cardSubtitleVotes = $('<h6 class="card-subtitle"></h6>')
  let cardText = $('<p class="card-text"></p>')

  cardTitle.text(c.topic_name)
  if (c.sentiment === 1) {
    cardSubtitle.text("Bad")
    cardSubtitle.css({'color': 'red'})
  } else {
    cardSubtitle.text("Good")
    cardSubtitle.css({'color': 'green'})
  }

  cardText.text(c.comment);
  cardSubtitleVotes.text(c.vote_count);

  cardBody = cardBody.append(cardTitle);
  cardBody = cardBody.append(cardSubtitle);
  cardBody = cardBody.append(cardSubtitleVotes);
  cardBody = cardBody.append(cardText);
  card = card.append(cardBody);

  comments.append(card);
}

updateComments = (zipcode) => {
  axios.post('/comments', {zipcode})
    .then(resp => {
      resp.data.map(comment => {
        console.log(comment);
        createCommentHTML(comment);
        addMarkerToMap(comment);
      })
    })
}

getLatLng = (zipcode, cb) => {
  geocoder.geocode({address: zipcode}, function(res, status) {
    const lat = res[0].geometry.location.lat()
    const lng = res[0].geometry.location.lng()

    cb({lat, lng});
  }); 
}

addMarkerToMap = c => {
  getLatLng(c.zipcode, function(res) {
    const {lat, lng} = res;
    let marker = new google.maps.Marker({
      position: {lat: lat, lng:lng},
      title: "hello"
    })

    let info = document.createElement("div")

    let comment = document.createElement("p");
    comment.innerText = c.comment;

    let username = document.createElement("a");
    const redirect_url = `/u/${c.uid}`
    username.innerText = c.username
    username.href = redirect_url

    info.append(comment);
    info.append(username);

    console.log(info);

    let infoWindow = new google.maps.InfoWindow({
      content: info
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

  clearPrevComments();
  centerMapToZipcode(zipcode);
  updateComments(zipcode);
}