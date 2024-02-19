$(document).ready(function () {
  
  jQuery.validator.addMethod("greaterThan",
  function (value, element, params) {
    if (!/Invalid|NaN/.test(new Date(value))) {
      return new Date(value) > new Date($(params).val());
    }
    return isNaN(value) && isNaN($(params).val())
      || (Number(value) > Number($(params).val()));
  }, 'Must be greater than {0}.');

  jQuery.validator.addMethod("lettersonly", function (value, element) {
    return this.optional(element) || /^[a-z\s]+$/i.test(value);
  }, "Only alphabetical characters");

  $("#filterForm").validate({
    rules: {      
      check_out_date:{greaterThan:"#check_in_date"},
      guests: { number: true }
    },
    messages:{
      check_out_date:"Checkout date should be greater than Checkin date"
    }
  })

  $("#changePassword").validate({
    rules: {
      password: {
        minlength: 3
      },
      confirm_password: {
        minlength: 3,
        equalTo: "#password"
      }
    }
  });

  $("#loginForm").validate()

  $("#regForm").validate({
    rules: {
      email: {
        email: true,
        remote: {
          url: "is-email-exist",
          type: "get"
        }
      },
      password: {
        minlength: 3
      },
      confirm_password: {
        minlength: 3,
        equalTo: "#password"
      }
    },
    messages: {
      email: {
        remote: "Email already registered"
      },
      confirm_password: {
        equalTo: "Password and confirm password doesn't match"
      }
    }
  });

})