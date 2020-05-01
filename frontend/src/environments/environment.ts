/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'udacity-coffee-auth', // the auth0 domain prefix
    audience: 'coffee', // the audience set for the auth0 app
    clientId: 'XlVkAS3bY50iQIUNhqs5B3vTMr18NVLf', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8100', // the base url of the running ionic application. 
  }
};
