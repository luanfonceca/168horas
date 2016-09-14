$.validator.addMethod(
  'validCreditCard', 
  function(cardNumber) {
    return Moip.Validator.isValid(cardNumber);
  },
  $.validator.format('Invalid credit card.')
);

$.validator.addMethod(
  'validExpiryDate',
  function(value) {
    var month = $('#id_month').val();
    var year = $('#id_year').val();
    return Moip.Validator.isExpiryDateValid(month, year);
  },
  $.validator.format('Invalid expiry dates.')
);

$.validator.addMethod(
  'validSecurityCode',
  function(cvv) {
    var cardNumber = $('#id_credit_card').val();
    return Moip.Validator.isSecurityCodeValid(cardNumber, cvv);
  },
  $.validator.format('Invalid security code.')
);

$.validator.setDefaults({
  focusInvalid: false,
  errorClass: 'invalid', 
  sucessClass: 'valid', 
  errorElement: 'p',
  ignore: [],
  errorPlacement: function(error, element) {
    $(error).addClass('help-text caption red-text invalid-message');
    $(element).parents('.input-field').append(error);
  }
});

$(document).ready(function() {
  var form = $("#payment_form");

  $(form).submit(function(e) {
    debugger;
    var credit_card = new Moip.CreditCard({
      number: $("#id_credit_card").val(),
      cvc: $("#id_cvv").val(),
      expMonth: $("#id_month").val(),
      expYear: $("#id_year").val(),
      pubKey: $("#id_public_key").val()
    });

    if(credit_card.isValid()){
      $("#id_card_hash").val(credit_card.hash());
      return true;
    }

  });

  $(form).validate({
    rules: {
      credit_card: {
        required: true,
        validCreditCard: true,
      },
      month: {
        required: true,
      },
      year: {
        required: true,
        validExpiryDate: true,
      },
      cvv: {
        required: true,
        validSecurityCode: {
          depends: function(element) {
            var form = $(element).parents('form');
            return $(form).validate().element($('#id_credit_card'));
          }
        }
      },
      holder_name: {
        required: true,
      },
      birth_date: {
        required: true,
      },
      cpf: {
        required: true,
      },
    }
  });

  $(form).find('[name=credit_card]').mask(
    '9999 9999 9999 9999', {
      'placeholder': ' '
    }
  );

  $(form).find('[name=birth_date]').mask(
    '99/99/9999', {
      'placeholder': ' '
    }
  );

  $(form).find('[name=cpf]').mask(
    '999.999.999-99', {
      'placeholder': ' '
    }
  );

  $(form).find('[name=phone]').mask(
    '+55 (99) 9?9999-9999', {
      'placeholder': ' '
    }
  );
});