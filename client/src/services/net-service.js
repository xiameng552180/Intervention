import axios from 'axios';
// import GlobalConfig from './global-config';

const devApiUrl = 'http://localhost:5003'; // for local testing

const GET_REQUEST = 'get';
const POST_REQUEST = 'post';

function request(url, params, type, callback) {
    let func;
    if (type === GET_REQUEST) {
        func = axios.get;
    } else if (type === POST_REQUEST) {
        func = axios.post;
    }

    func(url, params).then((response) => {
        if (response.status === 200) {
            callback(response);
        } else {
            console.error(response);
        }
    })
    .catch((error) => {
        console.error(error);
    });
}




function loadData(callback){
    const url = `${devApiUrl}/loadData`;
    const params = {};
    request(url, params, GET_REQUEST, callback);
}

export default {
    loadData,
};

