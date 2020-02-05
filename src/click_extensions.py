import click
from click.exceptions import UsageError
from click._compat import get_text_stderr
from click.utils import echo


def _show_usage_error(self, file=None):
    if file is None:
        file = get_text_stderr()
    color = None
    echo('Error: %s' % self.format_message(), file=file, color=color)
    if self.ctx is not None:
        echo('', file=file)
        color = self.ctx.color
        echo(self.ctx.get_help() + '\n', file=file, color=color)


UsageError.show = _show_usage_error


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
                    raise UsageError("'" + str(self.name) + "' is mutually exclusive with " + str(mutex_opt) + ".",
                                     ctx=ctx)
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
                    raise UsageError("'" + str(self.name) + "' is required if '" + str(req_opt) + "' is specified.",
                                     ctx=ctx)
                else:
                    self.prompt = None
        return super(ClickRequiredIfPresent, self).handle_parse_result(ctx, opts, args)


class ClickCommaSeparatedList(click.ParamType):
    name = "CSV"

    def convert(self, value, param, ctx):
        return value.split(',')


class ClickKeyValue(click.ParamType):
    name = "Key=Value"

    def convert(self, value, param, ctx):
        parts = value.split('=', 1)
        if len(parts) < 2:
            raise UsageError(f"Invalid argument: {value}: must be in Key=Value form.", ctx=ctx)
        return parts[0], parts[1]


class ClickKeyValueCSV(click.ParamType):
    name = "Key=Value[,...]"

    def convert(self, value, param, ctx):
        values = value.split(',')
        pairs = []
        for v in values:
            parts = v.split('=', 1)
            if len(parts) < 2:
                raise UsageError(f"Invalid argument: {v}: must be in Key=Value form.", ctx=ctx)
            pairs.append((parts[0], parts[1]))
        return pairs


class ClickRequires(click.ParamType):
    pass


CSV = ClickCommaSeparatedList()
KeyValue = ClickKeyValue()
KeyValueCSV = ClickKeyValueCSV()
