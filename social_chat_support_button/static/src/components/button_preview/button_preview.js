/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { useRecordObserver } from "@web/model/relational_model/utils";

import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { TagsList } from "@web/core/tags_list/tags_list";

import { Record } from "@web/model/record";
import { Field } from "@web/views/fields/field";
import {
    Component,
    useEffect,
    useState,
    useRef,
} from "@odoo/owl";

export class ButtonPreview extends Component {
    static template = "social_chat_support_button.ButtonPreview";
    static components = {
        TagsList,
        Record,
        Field,
    }
    static props = {
        ...standardFieldProps,
    }
    elRef = useRef("czm-chat-support");
    setup() {
        useRecordObserver(this.willUpdateRecord.bind(this));
        this.state = useState({ props: this.props});
        useEffect(() => {
            this.update_button_preview()
        }, ()=>[this.elRef,this.props.record._changes]);
    }

    update_button_preview(){
        $(this.elRef.el).empty()
        $(this.elRef.el).attr({class:""})
        $(this.elRef.el).czmChatSupport(this.props.record.data.json_for_csmChatSupport)
    }
    async willUpdateRecord(record) {
    }
}

export const buttonPreview = {
    component: ButtonPreview,
    supportedTypes: ["char", "text","jsonb"]
};

registry.category("fields").add("button_preview", buttonPreview);
