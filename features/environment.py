def after_scenario(context, scenario):
    if 'freezer' in context:
        context.freezer.stop()
