import click


class ClickMutex(click.Option):
    def __init__(self, *args, **kwargs):
        self.exclusive_with:list = kwargs.pop("exclusive_with")

        assert self.exclusive_with, "'exclusive_with' parameter required"
        super(ClickMutex, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        current_opt:bool = self.name in opts
        for mutex_opt in self.exclusive_with:
            if mutex_opt in opts:
                if current_opt:
                    raise click.UsageError("Illegal usage: '" + str(self.name) +
                                           "' is mutually exclusive with " + str(mutex_opt) + ".")
                else:
                    self.prompt = None
        return super(ClickMutex, self).handle_parse_result(ctx, opts, args)


class ClickRequiredIfPresent(click.Option):
    def __init__(self, *args, **kwargs):
        self.required_if:list = kwargs.pop("required_if")

        assert self.required_if, "'required_if' parameter required"
        super(ClickRequiredIfPresent, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        current_opt:bool = self.name in opts
        for req_opt in self.required_if:
            if req_opt in opts:
                if not current_opt:
                    raise click.UsageError("'" + str(self.name) + "' is required if '" +
                                           str(req_opt) + "' is specified.")
                else:
                    self.prompt = None
        return super(ClickRequiredIfPresent, self).handle_parse_result(ctx, opts, args)


class ClickRequireExactlyOneOf(click.Option):
    def __init__(self, *args, **kwargs):
        self.require_group:list = kwargs.pop("require_group")

        assert self.require_group, "'require_group' parameter required"
        super(ClickRequireExactlyOneOf, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        print(ctx)
        print(opts)
        print(args)
        count = 0
        for req_opt in self.require_group:
            if req_opt in opts:
                count += 1
                if count > 1:
                    raise click.UsageError("Exactly one of these must be specified: " + ', '.join(self.require_group))

        return super(ClickRequireExactlyOneOf, self).handle_parse_result(ctx, opts, args)


class ClickCommaSeparatedList(click.ParamType):
    name = "CSV"

    def convert(self, value, param, ctx):
        return value.split(',')


CSV = ClickCommaSeparatedList()
