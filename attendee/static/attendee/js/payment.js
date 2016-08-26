$.validator.addMethod(
  'validCreditCard', 
  function(cardNumber) {
    return Moip.Validator.isValid(cardNumber);
  },
  $.validator.format(
    'Invalid credit card.'
  )
);

$.validator.addMethod(
  'validExpiryDate',
  function(value) {
    var month = $('#id_month').val();
    var year = $('#id_year').val();
    return Moip.Validator.isExpiryDateValid(month, year);
  },
  $.validator.format(
    'Invalid expiry dates.'
  )
);

$.validator.addMethod(
  'validSecurityCode',
  function(cvv) {
    var cardNumber = $('#id_credit_card').val();
    return Moip.Validator.isSecurityCodeValid(cardNumber, cvv);
  },
  $.validator.format(
    'Invalid security code.'
  )
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
  $("#payment_form").submit(function(e) {
    e.preventDefault();

    $(this).validate();

    var cc = new Moip.CreditCard({
      number: $(this).find("#id_credit_card").val(),
      cvc: $(this).find("#id_cvv").val(),
      expMonth: $(this).find("#id_month").val(),
      expYear: $(this).find("#id_year").val(),
      pubKey: $(this).find("#id_public_key").val()
    });

    debugger;
    if(cc.isValid()){
      $("#hash").val(cc.hash());
    } else {
      $("#hash").val('');
      alert('Invalid credit card. Verify parameters: number, cvc, expiration Month, expiration Year');
      return false; // Don't submit the form
    }
  });

  $("#payment_form").validate({
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
      name: {
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

  var form = $("#payment_form");
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
    '(99) 9?9999-9999', {
      'placeholder': ' '
    }
  );
});