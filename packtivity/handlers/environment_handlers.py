import packtivity.utils as utils
import jq
handlers,environment = utils.handler_decorator()

@environment('docker-encapsulated')
def docker(environment,parameters,state):

    jsonpars = parameters.json()
    for p,v in parameters.leafs():
        p.set(jsonpars, v)

    for i,x in enumerate(environment['par_mounts']):
        script = x.pop('jqscript')
        x['mountcontent'] = jq.jq(script).transform(jsonpars, text_output = True)

    if environment['workdir'] is not None:
        environment['workdir'] = state.contextualize_value(environment['workdir'])
    return environment


@environment('default')
def default(environment,parameters,state):
    return environment
