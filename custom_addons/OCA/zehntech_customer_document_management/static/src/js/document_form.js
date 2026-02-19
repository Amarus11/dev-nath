// odoo.define('zehntech_customer_document_management.document_form', function (require) {
//     "use strict";
//     var FormController = require('web.FormController');
//     var Dialog = require('web.Dialog');

//     FormController.include({
//         saveRecord: function () {
//             var self = this;
//             var res = this._super.apply(this, arguments);
            
//             // Check if we're in the document form (replace 'ir.attachment' if using a custom model)
//             if (this.modelName === 'ir.attachment' || this.modelName === 'res.partner.document') {
//                 res.then(function () {
//                     Dialog.alert(self, "Your document has been created successfully!", {
//                         title: "Success",
//                     });
//                 });
//             }
//             return res;
//         },
//     });
// });
// odoo.define('customer_document.fix_m2m_binary', function (require) {
//     "use strict";

//     var fieldRegistry = require('web.field_registry');
//     var Many2ManyBinaryField = require('web.relational_fields').FieldMany2ManyBinary;

//     var FixedMany2ManyBinaryField = Many2ManyBinaryField.extend({
//         getExtension: function (fileName) {
//             if (!fileName) {
//                 console.error("File name is undefined, cannot get extension.");
//                 return "";  // Return an empty string instead of causing an error
//             }
//             return fileName.replace(/^.*\./, '');  // Extract file extension
//         }
//     });

//     fieldRegistry.add('many2many_binary', FixedMany2ManyBinaryField);
// });
