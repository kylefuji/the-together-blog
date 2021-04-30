const { Client } = require('pg');

const pgclient = new Client({
    host: 'localhost',
    port: '5432',
    user: 'kyle',
    password: 'x9SDV294dvsNkNNLwr9RR1KMASDOL9fwvjsvowO9',
    database: 'thetogetherblog'
});

pgclient.connect();