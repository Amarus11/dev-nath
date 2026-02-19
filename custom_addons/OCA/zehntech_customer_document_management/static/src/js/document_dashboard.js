// odoo.define('customer_document.validation', function (require) {
//     "use strict";

//     var FormController = require('web.FormController');
//     var core = require('web.core');

//     FormController.include({
//         _onSave: function (event) {
//             var self = this;
//             var $emailField = this.$el.find('input[name="email"]');
//             var email = $emailField.val();
//             var emailRegex = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;

//             if (!email.match(emailRegex)) {
//                 event.preventDefault();
//                 this.displayNotification({
//                     type: 'warning',
//                     title: 'Invalid Email',
//                     message: 'Please enter a valid email before saving.',
//                 });
//                 $emailField.focus();
//                 return false;
//             }

//             return this._super.apply(this, arguments);
//         }
//     });

//     core.action_registry.add('customer_document.validation', FormController);
// });



// odoo.define('customer_document.expiry_date_validation', function (require) {
//     "use strict";
    
//     var core = require('web.core');
//     var FieldDate = require('web.basic_fields').FieldDate;

//     var _t = core._t;

//     var ExpiryDateField = FieldDate.extend({
//         events: _.extend({}, FieldDate.prototype.events, {
//             'change input': '_onChangeDate',
//         }),

//         _onChangeDate: function (ev) {
//             var inputValue = this.$input.val();
//             var selectedDate = new Date(inputValue);
//             var today = new Date();
//             today.setHours(0, 0, 0, 0); // Reset time to midnight

//             if (selectedDate < today) {
//                 alert(_t("Expiry date cannot be in the past. Please select a valid date."));
//                 this.$input.val(''); // Clear the invalid input
//             }
//         }
//     });

//     // core.form_widget_registry.add('expiry_date', ExpiryDateField);
//     var fieldRegistry = require('web.field_registry');
//     fieldRegistry.add('expiry_date', ExpiryDateField);

// });










