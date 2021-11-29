# odoo-pos-inherit
In this repo i inherit the pos module and added QR code to pos receipt

# 1- Create new Odoo Module using command line

```python
$ python odoo-bin scaffold <module name> <where to put it>
```

# 2- Inherit OrderReceipt JS Screen in odoo
1 - Create new js class and put this code that defin a function referenced to

```js
odoo.define('point_of_sale.OrderReceipt', function (require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    function myFunction(text) {
        return text
    }

    class OrderReceipt extends PosComponent {


        constructor() {
            console.log("eslam faisal constructor")
            super(...arguments);
            this._receiptEnv = this.props.order.getOrderReceiptEnv();
        }

        willUpdateProps(nextProps) {
            this._receiptEnv = nextProps.order.getOrderReceiptEnv();
        }

        get receipt() {
            return this.receiptEnv.receipt;
        }

        clientName(receipt) {
            return receipt.client.name
        }

        get orderlines() {
            return this.receiptEnv.orderlines;
        }

        get paymentlines() {
            return this.receiptEnv.paymentlines;
        }

        get isTaxIncluded() {
            return Math.abs(this.receipt.subtotal - this.receipt.total_with_tax) <= 0.000001;
        }

        get receiptEnv() {
            return this._receiptEnv;
        }

        isSimple(line) {
            return (
                line.discount === 0 &&
                line.is_in_unit &&
                line.quantity === 1 &&
                !(
                    line.display_discount_policy == 'without_discount' &&
                    line.price < line.price_lst
                )
            );
        }
    }

    OrderReceipt.template = 'OrderReceipt';

    Registries.Component.add(OrderReceipt);

    return OrderReceipt;
});

```

2- Add new Order Receipt that you created recently to JS directory in your module
![pos inherit](https://user-images.githubusercontent.com/33801510/141646085-0b21c4f7-1ed3-482e-967d-3e3b1dfb7aa0.png)

3- Create a #data.xml file to xpath the new JS file screen and define it in __manifest__.py file and make the module depends on point_of_sale
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>

        <template id="assets" inherit_id="point_of_sale.assets">
            <xpath expr="//script[@src='/point_of_sale/static/src/js/Screens/ReceiptScreen/OrderReceipt.js']"
                   position="replace">
                <script type="text/javascript" src="/pos_inherit/static/src/js/OrderReceipt.js"/>
            </xpath>

        </template>

    </data>
</odoo>

```

# 3- Inherit OrderReceipt XML file
1 - Create new xml file pos_receipt.xml and register it in __manifest__.py but in qweb section 
![post inherit 2](https://user-images.githubusercontent.com/33801510/141647136-5bd0b70c-d6e9-466d-9ca4-53143d61114c.png)

2- inherit pos receipt screen xml by xpath
3 - use t tag for access JS values 
4 - use api.qrserver.com public api to get the QR code with given data
```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">
    <t t-name="OrderReceipt" t-inherit="point_of_sale.OrderReceipt" t-inherit-mode="extension" owl="1">
        <xpath expr="//div[hasclass('pos-receipt-order-data')]" position="after">

            <div id="placehere" style="margin-left:60px;margin-top:16px;margin-right:60px;"></div>

            <script type="text/javascript">
                var qrData = " :اسم المورد "+ " <t t-esc="receipt.company.name"/>";
                qrData += "%0A";
                qrData += "الرقم الضريبي: "+ "<t t-esc="receipt.company.vat"/>";
                qrData += "%0A";
                qrData += ":التاريخ "+ "<t t-esc="receipt.date.localestring"/>";
                qrData += "%0A";
                qrData += "المبلغ الكلي: "+ "<t t-esc="receipt.total_with_tax"/>";

                var clientName = "<t t-if="receipt.client"><t t-esc="receipt.client.name"></t></t>";
                if(clientName !== ""){
                    qrData += "%0A";
                    qrData += "العميل: "+ "<t t-if="receipt.client"><t t-esc="receipt.client.name"></t></t>";
                }

                var clientVat = "<t t-if="receipt.client"><t t-esc="receipt.client.vat"></t></t>";
                if(clientVat !== ""){
                    qrData += "%0A";
                    qrData += "الرقم الضريبي: "+ "<t t-if="receipt.client"><t t-esc="receipt.client.vat"></t></t>";
                }

                var qrCodeElement = document.createElement("img");
                qrCodeElement.setAttribute("src", "images/hydrangeas.jpg");
                qrCodeElement.setAttribute("height", "180");
                qrCodeElement.setAttribute("width", "180");
                qrCodeElement.setAttribute("src", "https://api.qrserver.com/v1/create-qr-code/?data="+qrData);
                document.getElementById("placehere").appendChild(qrCodeElement);
            </script>
        </xpath>

        <xpath expr="//div[hasclass('cashier')]" position="after">
            <div>Served for <t t-if="receipt.client"> <t t-esc="receipt.client.name"></t> </t></div>

        </xpath>
    </t>
</templates>


```

#Finally then create pos order with client
![IMG-20180516-WA0055](https://user-images.githubusercontent.com/33801510/141647226-0480ef07-32ae-48be-92f3-e56a4f071bdc.jpg)

  
