import {DjangoService} from '@/services/django';
import {Provide} from 'vue-property-decorator';
import {Vue, Component} from 'vue-property-decorator';
import {Multiselect} from 'vue-multiselect';


@Component({
    components: {Multiselect},
})
export default class LinkAllComponent extends Vue {
    private djangoService = new DjangoService();

    @Provide() instance: LinkInstance | null = null;
    @Provide() linkUrl: string = '';
    @Provide() instancesSelectable: Array<LinkInstance> = [];
    @Provide() linkTypes: Array<LinkType> = [];
    @Provide() linkType: LinkType = this.djangoService.getDefaultLinkType();

    async mounted() {
        await this.fetchLinkTypes();
        this.stopMultiselectFromBeingOpenedOnLoad();
        await this.initForm();
    }

    async selectLinkType(linkType: LinkType) {
        this.linkUrl = '';
        this.instancesSelectable = await this.djangoService.fetchInstancesSelectable(linkType);
        const isCanSelectDefaultInstance = Boolean(this.instancesSelectable[0]);
        if (isCanSelectDefaultInstance) {
            this.instance = this.instancesSelectable[0];
        }
        this.djangoService.save(this.linkTypes, linkType, this.instance, this.linkUrl);
    }

    async linkInstanceChanged(linkInstance: LinkInstance) {
        this.djangoService.save(this.linkTypes, this.linkType, linkInstance, this.linkUrl)
    }

    async linkUrlChanged(linkUrl) {
        this.djangoService.save(this.linkTypes, this.linkType, this.instance, linkUrl)
    }

    instanceLabel(instance: LinkInstance): string {
        if (instance.url && instance.type.isShowUrl) {
            return `${instance.label} (${instance.url})`
        } else {
            return instance.label
        }
    }

    getFileUrl(): string {
        if (this.instance) {
            if (this.instance.url.match(/\.(jpeg|jpg|gif|png)$/) != null) {
                return this.instance.url;
            } else {
                return '';
            }
        } else {
            return '';
        }
    }

    private async fetchLinkTypes() {
        this.linkTypes = await this.djangoService.getLinkTypes();
    }

    private async initForm() {
        this.linkType = this.linkTypes[0];
        await this.djangoService.initDataFromDjango(this);
    }

    private stopMultiselectFromBeingOpenedOnLoad() {
        if (document.activeElement) {
            (document.activeElement as any).blur();
        }
    }
}


export interface LinkType {
    name: string
    verboseName: string
    isGenericForeignKey: boolean
    isShowUrl: boolean
    contentTypePk?: number
    urlPrefix?: string
    placeholder?: string
}


export interface LinkInstance {
    type: LinkType
    instancePk?: number
    label: string
    url: string | null
}
