import LinkAllComponent from '@/link-all';
import {LinkInstance} from '@/link-all';
import {LinkType} from '@/link-all';
import {AxiosResponse} from 'axios';
const axios = require('axios').default;


export class DjangoService {
    private typePkInput: HTMLInputElement = document.querySelector('#id_link_content_type');
    private instancePkInput: HTMLInputElement = document.querySelector('#id_link_instance_pk');
    private urlInput: HTMLInputElement = document.querySelector('#id_link_url');
    private labelInput: HTMLInputElement = document.querySelector('#id_link_label');
    private linkTypeInput: HTMLSelectElement = document.querySelector('#id_link_type');

    private urlLinkType: LinkType = {name: 'url', verboseName: 'URL', isGenericForeignKey: false, placeholder: 'https://example.com', isShowUrl: false};

    getDefaultLinkType(): LinkType {
        return this.urlLinkType;
    }

    async initDataFromDjango(component: LinkAllComponent){
        if (this.typePkInput.value) {
            const linkType = component.linkTypes.find(type => type.contentTypePk === Number(this.typePkInput.value));
            if (linkType) {
                component.linkType = linkType;
                component.instancesSelectable = await this.fetchInstancesSelectable(linkType);
            }
        }

        if (this.instancePkInput.value) {
            component.instance = component.instancesSelectable.find(
                instance => instance.instancePk === Number(this.instancePkInput.value)
            );
        }

        if (this.urlInput.value) {
            component.linkUrl = this.urlInput.value;
        }

        const linkTypeMatched = component.linkTypes.find(type => type.name === this.linkTypeInput.value);
        if (linkTypeMatched) {
            component.linkType = linkTypeMatched;
        }
    }

    save(linkTypes: Array<LinkType>, linkType: LinkType, instance: LinkInstance, linkUrl: string) {
        if (linkType.urlPrefix && !linkUrl.startsWith(linkType.urlPrefix)) {
            this.urlInput.value = linkType.urlPrefix + linkUrl;
        } else {
            this.urlInput.value = linkUrl;
        }

        if (linkType.isGenericForeignKey && instance) {
            this.urlInput.value = '';
            this.typePkInput.value = String(linkType.contentTypePk);
            this.instancePkInput.value = String(instance.instancePk);
            this.labelInput.value = instance.label;
        } else {
            this.typePkInput.value = '';
            this.instancePkInput.value = '';
            this.labelInput.value = '';
        }

        const linkTypesNative = linkTypes.filter(type => !type.isGenericForeignKey)
        if (linkTypesNative.includes(linkType)) {
            this.linkTypeInput.value = linkType.name;
        } else {
            this.linkTypeInput.value = 'generic_foreign_key';
        }
    }

    async fetchInstancesSelectable(linkType: LinkType): Promise<Array<LinkInstance>> {
        let instancesSelectable: Array<LinkInstance> = [];
        if (linkType.isGenericForeignKey) {
            const response: AxiosResponse = await axios.get(`/link-types/${linkType.contentTypePk}/`);
            instancesSelectable = response.data.map(instanceRaw => {return {
                type: linkType,
                instancePk: instanceRaw.pk,
                label: instanceRaw.label,
                url: instanceRaw.url,
            }});
        }
        return instancesSelectable;
    }

    async getLinkTypes(): Promise<Array<LinkType>> {
        const response: AxiosResponse = await axios.get('/link-types/');
        const linkFkTypes: Array<LinkType> = response.data.map(type => { return {
            name: `${type.app_label}.${type.model_name}`,
            verboseName: type.verbose_name,
            isGenericForeignKey: true,
            contentTypePk: type.content_type_pk,
            isShowUrl: type.is_show_url_in_select,
        }})
        const linkTypesDefault = [this.urlLinkType]
        const linkTypesLast: Array<LinkType> = [
            {
                name: 'email',
                verboseName: 'Email',
                isGenericForeignKey: false,
                urlPrefix: 'mailto:',
                placeholder: 'hello@example.com',
                isShowUrl: false,
            },
            {
                name: 'phone',
                verboseName: 'Phone',
                isGenericForeignKey: false,
                urlPrefix: 'tel:',
                placeholder: '+44 7911 123456',
                isShowUrl: false,
            },
            {
                name: 'anchor',
                verboseName: 'Anchor',
                isGenericForeignKey: false,
                urlPrefix: '#',
                placeholder: 'anchor-example',
                isShowUrl: false,
            },
        ];
        return linkTypesDefault.concat(linkFkTypes).concat(linkTypesLast);
    }
}
