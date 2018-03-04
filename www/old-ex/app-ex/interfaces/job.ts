export class Job {
    id: string;
    public data: Object;
    public loaded = false;

    constructor(id = '') {
        this.id = id;
    }

    public load(data: Object): void {
        this.data = data;
        this.loaded = true;
    }

    public unload(): void {
        this.loaded = false;
        this.data = null;
    }

    public getData(): Object {
        return this.data;
    }
}
