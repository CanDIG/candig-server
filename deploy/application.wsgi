import ga4gh.server.frontend.core as core

coreFront = core.coreInstance
coreFront.setup()
application = coreFront.getApp()
application.run(host="127.0.0.1", port=8000)
