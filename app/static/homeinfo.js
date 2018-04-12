changezip = () => {
  const input = document.getElementById('changezip');
  const newZip = input.value;

  let zipcodeField = document.getElementById('zipcode');
  let priceField = document.getElementById('price');
  let scoreField = document.getElementById('score');

  axios.post('/zipinfo', {zipcode: newZip})
    .then(resp => {
      const {price, score} = resp.data;
      zipcodeField.innerText = `For Zipcode: ${newZip}`;
      priceField.innerText = `Avg Home price: ${price}`;
      scoreField.innerText = `Avg Score: ${score}`;
    })
}