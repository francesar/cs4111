function toggleCitizenSignUp() {
  $('#citizenLoginForm').modal('show');
}

// $('#submit').on('click', () => {
//   const citizenValues = $('#citizen-info').serializeArray();
//   const homeValue = $('#home-form').serializeArray();
//   const zipcodeValue = $('#zipscore-form').serializeArray();

//   const party = $('#inlineCheckbox1').is(':checked') ? 'Democrat' : 'Republican'

//   let data = {};
  
//   let signUpData = [citizenValues, homeValue, zipcodeValue].map(form => {
//     form.map(pair => {
//       data[pair['name']] = pair['value']
//     })
//   })

//   data['party'] = party;

//   $('#citizenLoginForm').modal('hide');

//   axios.post('/citizenSignUp', data)
//     .catch(err => console.log(err))
// })