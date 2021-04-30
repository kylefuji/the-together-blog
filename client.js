const { Client } = require('pg');

const pgclient = new Client({
    host: process.env.POSTGRES_HOST,
    port: process.env.POSTGRES_PORT,
    user: 'kyle',
    password: 'x9SDV294dvsNkNNLwr9RR1KMASDOL9fwvjsvowO9',
    database: 'thetogetherblog'
});

pgclient.connect();