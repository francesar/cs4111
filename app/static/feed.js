createFeedCommentHTML = c => {
  let comments = $('#comments');

  let card = $('<div class="card"></div>');
  let cardBody = $('<div class="card-body"></div>')
  let cardAuthor = $('<h4 class="card-author"></h4>')
  let cardLocation = $('<h6 class="card-location"></h6>')
  let cardTimestamp = $('<h6 class="card-timestamp"></h6>')
  let cardText = $('<p class="card-text"></p>')
  let cardTopic = $('<h6 class="card-topic"></h6>')

  cardAuthor.text(c.uid)
  cardLocation.text("10027")
  cardTimestamp.text("4/9/2018")
  cardText.text(c.comment)
  cardTopic.text(c.topic_id)

  // if (c.sentiment === 1) {
  //   cardSubtitle.text("Bad")
  //   cardSubtitle.css({'color': 'red'})
  // } else {
  //   cardSubtitle.text("Good")
  //   cardSubtitle.css({'color': 'green'})
  // }
  console.log(c.name)
  console.log("bitch")

  cardBody = cardBody.append(cardAuthor);
  cardBody = cardBody.append(cardLocation);
  cardBody = cardBody.append(cardTimestamp);
  cardBody = cardBody.append(cardText);
  cardBody = cardBody.append(cardTopic);
  card = card.append(cardBody);


  comments.append(card);
}

updateFeedComments = (zipcode) => {
  axios.post('/feedcomments', {zipcode})
    .then(resp => {
        resp.data.map(comment => {
        console.log("blah");
        createFeedCommentHTML(comment);
      })
    })
}

updateFeedView = () => {
  const input = document.getElementById('zipcode')
  const zipcode = input.value
  
  updateFeedComments(zipcode);
}

addComment = () => {
  console.log("new comment")

  axios.post('/newcomment')
  .then(resp => {
      resp.data.map(comment => {
      console.log("posttt");
    })
  })
}