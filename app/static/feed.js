createFeedCommentHTML = c => {
  let comments = $('#comments');

  let card = $('<div class="card"></div>');
  let cardBody = $('<div class="card-body"></div>')
  let cardAuthor = $('<h4 class="card-author"></h4>')
  let cardLocation = $('<h6 class="card-location"></h6>')
  let cardTimestamp = $('<h6 class="card-timestamp"></h6>')
  let cardText = $('<p class="card-text"></p>')
  let cardTopic = $('<h6 class="card-topic"></h6>')
  let cardVotes = $('<h6 class="card-location"></h6>')
  let cardSentiment = $('<h6 class="card-location"></h6>')

  cardAuthor.text(c.username)
  cardLocation.text(c.zipcode)
  cardTimestamp.text(c.date_posted)
  cardText.text(" \"" + c.comment + "\" ")
  cardTopic.text("Topic: " + c.topic_name)

  if (c.sentiment === 1) {
    cardSentiment.text("Bad")
    cardSentiment.css({'color': 'red'})
  } else {
    cardSentiment.text("Good")
    cardSentiment.css({'color': 'green'})
  }

  if (c.vote_count > 0) {
    cardVotes.text(c.vote_count + " upvotes")
    cardVotes.css({'color': 'green'})
  } else if (c.vote_count > 0) {
    cardVotes.text(c.vote_count + " downvotes")
    cardVotes.css({'color': 'red'})
  } else {
    cardVotes.text(c.vote_count + " votes")
  }
  console.log(c.name)

  cardBody = cardBody.append(cardAuthor);
  cardBody = cardBody.append(cardLocation);
  cardBody = cardBody.append(cardTimestamp);
  cardBody = cardBody.append(cardText);
  cardBody = cardBody.append(cardTopic);
  cardBody = cardBody.append(cardVotes);

  card = card.append(cardBody);


  comments.append(card);
}

updateFeedComments = (zipcode) => {
  console.log("update feed comments " + zipcode)

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
  console.log("update feed view " + zipcode)

  updateFeedComments(zipcode);
}

// addComment = () => {
//   console.log("new comment")

//   axios.post('/newcomment')
  // .then(resp => {
  //     resp.data.map(comment => {
  //     console.log("posttt");
  //   })
  // })
// }