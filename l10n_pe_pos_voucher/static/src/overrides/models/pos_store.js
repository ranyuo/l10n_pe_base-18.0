/** @odoo-module */

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import { pick } from "@web/core/utils/objects";
import { formatDateTime } from "@web/core/l10n/dates";

patch(PosStore.prototype, {
    isPeruvianCompany() {
        return this.company.country?.code == "PE";
    },
    // @Override
    // doNotAllowRefundAndSales() {
    //     return this.isPeruvianCompany() || super.doNotAllowRefundAndSales(...arguments);
    // },
});

patch(Order.prototype, {
    // @Override
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        if (this.pos.isPeruvianCompany()) {
            json["voucherNumber"] = this.voucherNumber;
        }
        return json;
    },
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.voucherNumber = json.voucher_number || false;
    },
    export_for_printing() {
        return {
            ...super.export_for_printing(...arguments),
            voucherNumber: this.voucherNumber,
        };
    },
    wait_for_push_order() {
        var result = super.wait_for_push_order(...arguments);
        result = Boolean(result || this.pos.isPeruvianCompany());
        return result;
    },
});