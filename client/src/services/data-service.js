// import GlobalConfig from './global-config';

let instance = null;
class Service {
    constructor() {
        if (!instance) {
            instance = this;
        }
        this.serverIP = 'http://localhost:5003'
        this.serverUrl = `${this.serverIP}`;

        this.data = {}
        return instance;
    }
}

const DataService = new Service();
export default DataService;
