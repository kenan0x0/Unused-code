    # config_data = {'id': client_roles_scope_id,
    #             'name': 'client_roles',
    #             'description':'OpenID Connect scope for add user roles to the access token',
    #             'protocol': 'openid-connect',
    #             'attributes':{
    #                 'include.in.token.scope':'false',
    #                 'display.on.consent.screen':'true',
    #                 'consent.screen.text':'${rolesScopeConsentText}'
    #             },
    #             'protocolMappers':
    #             {
    #                 "id":"c24b0cd6-8341-40cc-96ad-2e8fa36241d5",
    #                 "name":"client roles",
    #                 "protocol":"openid-connect",
    #                 "protocolMapper":"oidc-usermodel-client-role-mapper",
    #                 "consentRequired":False,
    #                 "config":{
    #                     "access.token.claim":"true",
    #                     "id.token.claim":"true",
    #                     "jsonType.label":"String",
    #                     "multivalued":"true",
    #                     "user.attribute":"foo",
    #                     "claim.name":"resource_access.${client_id}.roles"
    #                 }
    #             }
    #             }
