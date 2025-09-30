/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { TextAreaPopup } from "@point_of_sale/app/utils/input_popups/textarea_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";

patch(PaymentScreen.prototype, {
    // OVERRIDES
    async validateOrder(isForceValidate) {
        const verifyOrderL10nPe = this.verifyOrderL10nPe(isForceValidate)
        if (
            verifyOrderL10nPe &&
            this.pos.isPeruvianCompany() &&
            this.paymentLines.some((line) => line.payment_method.is_card_payment)
        ) {
            let tickets = [];
            // Check if there is a payment line with a ticket
            for (const line of this.paymentLines) {
                if (line.payment_method.is_card_payment) {
                    const { confirmed, payload } = await this.popup.add(TextAreaPopup, {
                        confirmText: _t("Confirm"),
                        cancelText: _t("Cancel"),
                        title: _t("Please register the voucher number of ") + line.payment_method.name,
                    });
                    if (!confirmed) {
                        return;
                    }
                    if (!payload) {
                        this.popup.add(ErrorPopup, {
                            title: _t("Missing voucher number"),
                            body: _t("Please register the voucher number for the payment of ") + line.payment_method.name,
                        });
                        return;
                    }
                    line.ticket = payload.trim();
                    tickets.push(line.ticket);
                }
            }
            this.currentOrder.voucherNumber = tickets.join(",");
        }
        if (verifyOrderL10nPe) {
            await super.validateOrder(...arguments);
        }
    },
    // shouldDownloadInvoice() {
    //     debugger;
    //     return this.pos.isPeruvianCompany()
    //         ? false
    //         : super.shouldDownloadInvoice();
    // },
});